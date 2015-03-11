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

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render_to_response
from _utils import page_load_utils as _helper
from ZMQHelper.zmq_pub import ZMQ_PUB as zmqPub
from alerts.views import get_notifications
from dashboard.models import Building_Zone, DeviceMetadata


from helper import config_helper

import json
from lighting.models import Lighting
from smartplug.models import Plugload
from thermostat.models import Thermostat
import settings
import time
import os


def recursive_get_device_update(update_variable):
    #wifi_3m50_device_initial_update = SessionHelper.get_device_update_message(update_variable)
    wifi_3m50_device_initial_update = config_helper.get_device_update_message(update_variable)
    print wifi_3m50_device_initial_update
    vals = ""
    if wifi_3m50_device_initial_update != '{empty_string}':
        vals = wifi_3m50_device_initial_update
        return vals
    else:
        recursive_get_device_update(update_variable)


#Functionality for lighting page load
@login_required(login_url='/login/')
def lighting(request, mac):
    print 'inside lighting view method'
    context = RequestContext(request)
    username = request.session.get('user')
    print username
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
    
    mac = mac.encode('ascii', 'ignore')

    device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
    print device_metadata
    device_id = device_metadata[0]['device_id']
    controller_type = device_metadata[0]['device_model_id']
    controller_type = controller_type.device_model_id

    device_status = [ob.data_as_json() for ob in Lighting.objects.filter(lighting_id=device_id)]
    device_zone = device_status[0]['zone']['id']
    device_nickname = device_status[0]['nickname']
    zone_nickname = device_status[0]['zone']['zone_nickname']

    kwargs = {'subscribe_address': 'ipc:///tmp/volttron-lite-agent-subscribe',
                    'publish_address': 'ipc:///tmp/volttron-lite-agent-publish'}
    _zmq_pub = zmqPub(**kwargs)
 
    print "created instance of the zmqpub class"
    info_required = "Update Hue data"
    wifi_3m50_update_send_topic = '/ui/agent/bemoss/' + str(device_zone) + '/lighting/' + device_id + '/device_status'
    _zmq_pub.requestAgent(wifi_3m50_update_send_topic, info_required, "text/plain", "UI")

    json_file = open(os.path.join(settings.PROJECT_DIR, 'resources/page_load/page_load.json'), "r+")
    _json_data = json.load(json_file)
    if device_id not in _json_data['lighting']:
        _json_data['lighting'][device_id] = {"page_load": "{empty_string}"}

    json_file.seek(0)
    json_file.write(json.dumps(_json_data, indent=4, sort_keys=True))
    json_file.truncate()
    json_file.close()

    time.sleep(3)

    _data = _helper.get_page_load_data(device_id, 'lighting', controller_type)

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
        'lighting/lighting.html',
        {'type': controller_type, 'device_data': _data, 'device_id': device_id, 'device_zone': device_zone,
         'device_type': controller_type, 'mac_address': mac, 'zone_nickname': zone_nickname,
         'device_nickname': device_nickname, 'zones': zones, 'thermostat_sn': thermostats_sn,
         'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn}, context)


#Update lighting controller status
@login_required(login_url='/login/')
def update_device_light(request):
    print 'inside lighting update device method'
    if request.POST:
        _data = request.raw_post_data
        _data = json.loads(_data)
        device_info = _data['device_info']
        if 'color' in str(_data):
            lt_color = _data['color']
            if 'a(' in str(lt_color):
                lt_color = '(0,0,0)'
            lt_color = eval(lt_color)
            _data['color'] = lt_color

        _data.pop('device_info')
        content_type = "application/json"
        fromUI = "UI"
        kwargs = {'subscribe_address': 'ipc:///tmp/volttron-lite-agent-subscribe',
                        'publish_address': 'ipc:///tmp/volttron-lite-agent-publish'}
        _zmq_pub = zmqPub(**kwargs)
        lighting_update_send_topic = '/ui/agent/bemoss/'+device_info+'/update'
        _zmq_pub.sendToAgent(lighting_update_send_topic, _data, content_type, fromUI)

    if request.is_ajax():
            return HttpResponse(json.dumps(_data), mimetype='application/json')


@login_required(login_url='/login/')
def get_lighting_current_status(request):
    print "Getting current status of thermostat"
    if request.method == 'POST':
        data_recv = request.raw_post_data
        data_recv = json.loads(data_recv)
        # same as the thermostat load method
        info_required = "current status"
        lighting_update_send_topic = '/ui/agent/bemoss/' + data_recv['device_info'] + '/device_status'
        #wifi_3m50_update_send_topic = "/ui/zone1/wifithermo3m50/qaz3m50/device_status"
        kwargs = {'subscribe_address': 'ipc:///tmp/volttron-lite-agent-subscribe',
                        'publish_address': 'ipc:///tmp/volttron-lite-agent-publish'}
        _zmq_pub = zmqPub(**kwargs)
        _zmq_pub.requestAgent(lighting_update_send_topic, info_required, "text/plain", "UI")
        json_result = {'status': 'sent'}

        if request.is_ajax():
            return HttpResponse(json.dumps(json_result), mimetype='application/json')