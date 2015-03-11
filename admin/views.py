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
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from datetime import datetime
from alerts.views import get_notifications
from dashboard.models import Building_Zone
import settings
from thermostat.models import Thermostat
from lighting.models import Lighting
from smartplug.models import Plugload
from .models import NetworkStatus
from ZMQHelper.zmq_pub import ZMQ_PUB
from schedule.models import Holiday

kwargs = {'subscribe_address': 'ipc:///tmp/volttron-lite-agent-subscribe',
                    'publish_address': 'ipc:///tmp/volttron-lite-agent-publish'}

zmq_pub = ZMQ_PUB(**kwargs)

@login_required(login_url='/login/')
def device_status(request):
    print 'Device status page load'
    context = RequestContext(request)
    #username = request.session.get('user')
    if request.session.get('last_visit'):
    # The session has a value for the last visit
        last_visit_time = request.session.get('last_visit')

        visits = request.session.get('visits', 0)

        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
    else:
        # The get returns None, and the session does not have a value for the last visit.
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1

    if request.user.get_profile().group.name.lower() == 'admin':
        thermostats = [ob.device_status() for ob in Thermostat.objects.all()]
        print thermostats
        plugloads = [ob.device_status() for ob in Plugload.objects.all()]
        print plugloads
        lighting = [ob.device_status() for ob in Lighting.objects.all()]

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

        return render_to_response(
            'admin/device_status.html',
            {'thermostats': thermostats, 'plugloads': plugloads, 'lighting': lighting,
             'zones': zones, 'thermostat_sn': thermostats_sn,
             'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn},
            context)
    else:
        return HttpResponseRedirect('/home/')


@login_required(login_url='/login/')
def network_status(request):
    print 'Network status page load'
    context = RequestContext(request)
    #username = request.session.get('user')
    if request.session.get('last_visit'):
    # The session has a value for the last visit
        last_visit_time = request.session.get('last_visit')

        visits = request.session.get('visits', 0)

        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
    else:
        # The get returns None, and the session does not have a value for the last visit.
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1

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
        nw_status = [ob.network_status() for ob in NetworkStatus.objects.all()]

        return render_to_response(
            'admin/network_status.html',
            {'nw_status': nw_status, 'zones': zones, 'thermostat_sn': thermostats_sn,
             'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn},
            context)
    else:
        return HttpResponseRedirect('/home/')


def bemoss_settings(request):
    print 'BEMOSS Settings page load'
    context = RequestContext(request)
    #username = request.session.get('user')
    if request.session.get('last_visit'):
    # The session has a value for the last visit
        last_visit_time = request.session.get('last_visit')

        visits = request.session.get('visits', 0)

        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
    else:
        # The get returns None, and the session does not have a value for the last visit.
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1

    holidays = [ob.as_json() for ob in Holiday.objects.all()]
    print holidays

    json_file = open(os.path.join(settings.PROJECT_DIR, 'resources/metadata/bemoss_metadata.json'), "r+")
    _json_data = json.load(json_file)
    b_location = _json_data['building_location_zipcode']
    json_file.close()

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
        return render_to_response(
            'admin/bemoss_settings.html',
            {'holidays': holidays, 'zones': zones, 'thermostat_sn': thermostats_sn,
             'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn, 'b_location': b_location},
            context)
    else:
        return HttpResponseRedirect('/home/')


@login_required(login_url='/login/')
def delete_holiday(request):
    if request.POST:
        _data = request.body
        _data = json.loads(_data)

        if _data['id']:
            h_id = int(_data['id'])
            Holiday.objects.filter(holiday_id=h_id).delete()

        info_required = "Holiday removed"
        ieb_topic = '/ui/agent/bemoss/holiday/' + str(h_id) + '/remove'
        zmq_pub.requestAgent(ieb_topic, info_required, "text/plain", "UI")

        json_text = {"status": "success"}

    if request.is_ajax():
        return HttpResponse(json.dumps(json_text), mimetype='application/json')


@login_required(login_url='/login/')
def add_holiday(request):

    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        print _data

        _date = _data['date']
        if _date:
            _date = _date.split("T")
            _date = _date[0]
            _date = _date.split("-")
            year = int(_date[0])
            month = int(_date[1])
            day = int(_date[2])
            h_date = datetime(year, month, day).date()
            print _date
            new_holiday = Holiday(date=h_date, description=_data['desc'])
            new_holiday.save()

        new_h = Holiday.objects.get(date=h_date)

        info_required = "Holiday added"
        ieb_topic = '/ui/agent/bemoss/holiday/' + str(new_h.holiday_id) + '/added'
        zmq_pub.requestAgent(ieb_topic, info_required, "text/plain", "UI")

    json_text = {"status": "success"}

    if request.is_ajax():
        return HttpResponse(json.dumps(json_text), mimetype='application/json')


@login_required(login_url='/login/')
def update_bemoss_location(request):
    if request.POST:
        _data = request.body
        _data = json.loads(_data)

        b_location = _data['b_loc']

        json_file = open(os.path.join(settings.PROJECT_DIR, 'resources/metadata/bemoss_metadata.json'), "r+")
        _json_data = json.load(json_file)
        _json_data['building_location_zipcode'] = b_location

        json_file.seek(0)
        json_file.write(json.dumps(_json_data, indent=4, sort_keys=True))
        json_file.truncate()
        json_file.close()

    json_text = {"status": "success"}

    if request.is_ajax():
        return HttpResponse(json.dumps(json_text), mimetype='application/json')