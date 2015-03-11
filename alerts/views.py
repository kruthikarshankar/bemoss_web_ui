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


#All classes for alerts and notifications page handling
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from dashboard.models import Building_Zone
from alerts.models import ActiveAlert, EventTrigger, Priority, NotificationChannel, Notification, \
    NotificationChannelAddress, DeviceType
from accounts.models import UserFullName
from thermostat.models import Thermostat
from lighting.models import Lighting
from smartplug.models import Plugload

import json
import datetime


@login_required(login_url='/login/')
def alerts(request):
    print 'inside alerts view method'
    context = RequestContext(request)

    zones = [ob.as_json() for ob in Building_Zone.objects.all()]
    thermostats_sn = [ob.data_side_nav() for ob in Thermostat.objects.filter(network_status='ONLINE', thermostat_id__bemoss=True)]
    lighting_sn = [ob.data_side_nav() for ob in Lighting.objects.filter(network_status='ONLINE', lighting_id__bemoss=True)]
    plugload_sn = [ob.data_side_nav() for ob in Plugload.objects.filter(network_status='ONLINE', plugload_id__bemoss=True)]


    context.update({
            'zones': zones, 'thermostat_sn': thermostats_sn,
             'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn
            })

    if request.user.get_profile().group.name.lower() == 'admin':

        usr = UserFullName.objects.filter(username=request.user)[0]
        _registered_alerts = [ob.as_json() for ob in ActiveAlert.objects.all()]
        _alerts = [ob.as_json() for ob in EventTrigger.objects.all()]
        _alert_pr = [ob.as_json() for ob in Priority.objects.all()]
        _n_type = [ob.as_json() for ob in NotificationChannel.objects.all()]
        active_al = get_notifications()

        return render_to_response(
            'admin/alarms.html',
            {'registered_alerts': _registered_alerts, 'alerts': _alerts, 'priority': _alert_pr, 'n_type': _n_type,
             'thermostat_sn': thermostats_sn, 'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn,
             'user_full_name': usr,
             'active_al': active_al},
            context)
    else:
        return HttpResponseRedirect('/home/')


@login_required(login_url='/login/')
def create_alert(request):
    print 'inside create alert method'
    if request.POST:
        _data = request.raw_post_data
        #print _data
        _data = json.loads(_data)
        #print _data

        _alert = EventTrigger.objects.get(event_trigger_desc=_data['alert'])
        #print _alert

        _priority = Priority.objects.get(priority_level=_data['priority'])
        #print _priority

        _device_type = DeviceType.objects.get(id=_alert.device_type_id)
        #print _device_type

        ra = ActiveAlert(event_trigger=_alert, device_type=_device_type, trigger_parameter=_data['custom_alert'],
                         comparator=_data['custom_alert_comparator'], threshold=_data['value'],
                         priority_id=_priority.id, user_id=1, created_on=datetime.datetime.now())
        ra.save()

        for ntype in _data['n_type']:
            n_id = NotificationChannel.objects.get(notification_channel=ntype)
            #print n_id
            if ntype == "Email":
                emails = _data['email']
                for every_email in emails:
                    if every_email != "":
                        NotificationChannelAddress.objects.create(notification_channel=n_id, active_alert=ra,
                                                                  notify_address=every_email.strip())
            if ntype == "Text":
                phone_numbers = _data['phone']
                for every_ph_number in phone_numbers:
                    if every_ph_number != "":
                        NotificationChannelAddress.objects.create(notification_channel=n_id, active_alert=ra,
                                                                  notify_address=every_ph_number.strip())

            if ntype == "BemossNotification":
                NotificationChannelAddress.objects.create(notification_channel=n_id, active_alert=ra,
                                                                  notify_address="Bemoss")

            #ra.notification_channel.add(n_id[0]['id'])

    if request.is_ajax():
            return HttpResponse(json.dumps(_data), mimetype='application/json')

@login_required(login_url='/login/')
def delete_alert(request):
    print "Inside delete alert method"
    if request.POST:
        _data = request.raw_post_data
        #print type(_data)

        ActiveAlert.objects.filter(id=int(_data)).delete()

    if request.is_ajax():
        return HttpResponse(json.dumps)


def get_notifications():
    print "Fetching active notifications from the database"
    active_alerts = [ob.as_json() for ob in Notification.objects.all().order_by('dt_triggered')[:5]]
    #print active_alerts
    return active_alerts


def notifications(request):
    print "Notifications page load"
    context = RequestContext(request)

    zones = [ob.as_json() for ob in Building_Zone.objects.all()]
    thermostats_sn = [ob.data_side_nav() for ob in Thermostat.objects.filter(network_status='ONLINE', thermostat_id__bemoss=True)]
    lighting_sn = [ob.data_side_nav() for ob in Lighting.objects.filter(network_status='ONLINE', lighting_id__bemoss=True)]
    plugload_sn = [ob.data_side_nav() for ob in Plugload.objects.filter(network_status='ONLINE', plugload_id__bemoss=True)]


    active_al = get_notifications()

    context.update({"active_al": active_al})
    context.update({
            'zones': zones, 'thermostat_sn': thermostats_sn,
             'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn
            })

    if request.user.get_profile().group.name.lower() == 'admin':
        usr = UserFullName.objects.filter(username=request.user)[0]
        _registered_alerts = [ob.as_json() for ob in ActiveAlert.objects.all()]
        _alerts = [ob.as_json() for ob in EventTrigger.objects.all()]
        _alert_pr = [ob.as_json() for ob in Priority.objects.all()]
        _n_type = [ob.as_json() for ob in NotificationChannel.objects.all()]
        active_al = get_notifications()

        return render_to_response(
            'admin/notifications.html',
            {'registered_alerts': _registered_alerts, 'alerts': _alerts, 'priority': _alert_pr, 'n_type': _n_type,
             'thermostat_sn': thermostats_sn, 'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn, 'zones': zones, 'user_full_name': usr,
             'active_al': active_al},
            context)
    else:
        return HttpResponseRedirect('/home/')