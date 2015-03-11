# -*- coding: utf-8 -*-
# Authors: Kruthika Rathinavel
# Version: 1.2.1
# Email: kruthika@vt.edu
# Created: "2014-10-13 18:45:40"
# Updated: "2015-02-13 15:06:41"


# Copyright © 2014 by Virginia Polytechnic Institute and State University
# All rights reserved
#
# Virginia Polytechnic Institute and State University (Virginia Tech) owns the copyright for the BEMOSS software and its
# associated documentation ("Software") and retains rights to grant research rights under patents related to
# the BEMOSS software to other academic institutions or non-profit research institutions.
# You should carefully read the following terms and conditions before using this software.
# Your use of this Software indicates your acceptance of this license agreement and all terms and conditions.
#
# You are hereby licensed to use the Software for Non-Commercial Purpose only.  Non-Commercial Purpose means the
# use of the Software solely for research.  Non-Commercial Purpose excludes, without limitation, any use of
# the Software, as part of, or in any way in connection with a product or service which is sold, offered for sale,
# licensed, leased, loaned, or rented.  Permission to use, copy, modify, and distribute this compilation
# for Non-Commercial Purpose to other academic institutions or non-profit research institutions is hereby granted
# without fee, subject to the following terms of this license.
#
# Commercial Use: If you desire to use the software for profit-making or commercial purposes,
# you agree to negotiate in good faith a license with Virginia Tech prior to such profit-making or commercial use.
# Virginia Tech shall have no obligation to grant such license to you, and may grant exclusive or non-exclusive
# licenses to others. You may contact the following by email to discuss commercial use:: vtippatents@vtip.org
#
# Limitation of Liability: IN NO EVENT WILL VIRGINIA TECH, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR REDISTRIBUTE
# THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR
# CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO
# LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE
# OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF VIRGINIA TECH OR OTHER PARTY HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGES.
#
# For full terms and conditions, please visit https://bitbucket.org/bemoss/bemoss_os.
#
# Address all correspondence regarding this license to Virginia Tech's electronic mail address: vtippatents@vtip.org


import json
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from alerts.views import get_notifications
from dashboard.models import Building_Zone
from lighting.models import Lighting


import logging
import helper.messages as _
from smartplug.models import Plugload
from thermostat.models import Thermostat

logger = logging.getLogger("views")


def login_user(request):
    print "inside login_user() method"
    #Obtain the context for the user's request.
    context = RequestContext(request)

    if request.method == 'POST':     
            # Gather the username and password provided by the user.
            # This information is obtained from the login form.
            username = request.POST['username']
            password = request.POST['password']
    
            # Use Django's machinery to attempt to see if the username/password
            # combination is valid - a User object is returned if it is.
            user = authenticate(username=username, password=password)
    
            # If we have a User object, the details are correct.
            # If None (Python's way of representing the absence of a value), no user
            # with matching credentials was found.
            if user is not None:
                # Is the account active? It could have been disabled.
                if user.is_active:
                    # If the account is valid and active, we can log the user in.
                    # We'll send the user back to the homepage.
                    login(request, user)
                    request.session['zipcode'] = '22204'
                    logger.info("Login of user : %s", user.username)
                    redirect_to = str(request.META.get('HTTP_REFERER', '/'))
                    if redirect_to.__contains__('next='):
                        redirect_to = str(redirect_to).split('=')
                        redirect_to = redirect_to[1]
                        #return HttpResponseRedirect('/dashboard/')
                        return HttpResponseRedirect(redirect_to)
                    else:
                        return HttpResponseRedirect('/home/')
                else:
                    # An inactive account was used - no logging in!
                    messages.error(request, _.INACTIVE_USER)
                    return HttpResponseRedirect('/login/')

            else:
                # Bad login details were provided. So we can't log the user in.
                print "Invalid login details: {0}, {1}".format(username, password)
                messages.error(request, _.INCORRECT_USER_PASSWORD)
                #return HttpResponse("Invalid login details supplied.")
                return HttpResponseRedirect('/login/')
                #render_to_response('login/login.html', {}, context)

    else:
        print request
        #user = authenticate(username=username, password=password)
        if request.user.is_authenticated():
            return HttpResponseRedirect('/home/')
        else:
        # The request is not a HTTP POST, so display the login form.
        # This scenario would most likely be a HTTP GET.
            return render_to_response('accounts/login.html', {}, context)
    

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required(login_url='/login/')
def logout_user(request):
    print "i am in"
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/login/')


def register(request):
    context = RequestContext(request)

    return render_to_response('accounts/register.html', {}, context)


#Function to register new user to the system
#TODO test
def register_new_user(request):
    if request.POST:
        _data = request.body
        print _data
        _data = json.loads(_data)

        user = User.objects.create_user(
            username=_data['username'],
            password=_data['password'],
            email=_data['email'])
        print "created user"
        user.save()
        user.is_active = False
        user.save()
        _user = User.objects.get(username=_data['username'])
        _user.first_name = _data['firstname']
        _user.last_name = _data['lastname']
        _user.save()
        uinfo = user.get_profile()
        uinfo.group = Group.objects.get(id=1) #Add user as tenant by default
        uinfo.contact_phone = _data['phone']
        uinfo.save()
        print "saved user"


        jsonText = {
            "status": _.USER_REGISTRATION_SUCCESS
        }
        #messages.error(request, _.USER_REGISTRATION_SUCCESS)
    return HttpResponse(json.dumps(jsonText), mimetype='text/plain')


@login_required(login_url='/login/')
def user_manager(request):
    context = RequestContext(request)
    zones = [ob.as_json() for ob in Building_Zone.objects.all()]
    thermostats_sn = [ob.data_side_nav() for ob in Thermostat.objects.filter(network_status='ONLINE', thermostat_id__bemoss=True)]
    lighting_sn = [ob.data_side_nav() for ob in Lighting.objects.filter(network_status='ONLINE', lighting_id__bemoss=True)]
    plugload_sn = [ob.data_side_nav() for ob in Plugload.objects.filter(network_status='ONLINE', plugload_id__bemoss=True)]

    active_al = get_notifications()
    context.update({'active_al':active_al})
    context.update({
        'zones': zones, 'thermostat_sn': thermostats_sn,
         'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn
    })

    if request.user.get_profile().group.name.lower() == 'admin':
        _users = User.objects.all()
        groups = Group.objects.all()
        print _users
        return render_to_response('admin/user_manager.html', {"users":_users, 'zones': zones, 'thermostat_sn': thermostats_sn,
             'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn, 'groups': groups}, context)
    else:
        return HttpResponseRedirect('/home/')


@login_required(login_url='/login/')
def approve_users(request):
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        print _data

        for user in _data['data']:
            usr = User.objects.get(id=user[0])
            if user[1] == "true":
                usr.is_active = True
            uprofile = usr.get_profile()
            uprofile.group_id = Group.objects.get(name=user[2])
            if user[3] != "Assign a Zone" and user[2] == "Zone Manager":
                uprofile.zone_id = Building_Zone.objects.get(zone_nickname=user[3])
            uprofile.save()
            usr.save()
            send_mail(_.EMAIL_USER_APPROVED_SUBJECT,
                      _.EMAIL_USER_MESSAGE.format(usr.first_name + ' ' + usr.last_name,
                                                  request.get_host()), _.EMAIL_FROM_ADDRESS,
                      [usr.email], fail_silently=True)

        print "user accounts activated"
        json_text = {
            "status": "success"
        }

    return HttpResponse(json.dumps(json_text), mimetype='text/plain')


@login_required(login_url='/login/')
def modify_user_permissions(request):
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        print _data

        for user in _data['data']:
            usr = User.objects.get(id=user[0])
            uprofile = usr.get_profile()
            uprofile.group_id = Group.objects.get(name=user[1])
            if user[2] != "" and user[1] == "Zone Manager":
                uprofile.zone_id = Building_Zone.objects.get(zone_nickname=user[2])
            uprofile.save()
            usr.save()

        print "user accounts permissions modified"
        json_text = {
            "status": "success"
        }

    return HttpResponse(json.dumps(json_text), mimetype='text/plain')


@login_required(login_url='/login/')
def delete_user(request):
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        print _data

        user_id = _data['id']
        usr = User.objects.get(id=user_id)
        usrprof = usr.get_profile()
        usrprof.delete()
        usr.delete()

        print "user account removed"
        json_text = {
            "status": "success"
        }

    return HttpResponse(json.dumps(json_text), mimetype='text/plain')