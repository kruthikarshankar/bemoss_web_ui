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


import os
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from alerts.views import get_notifications
from dashboard.models import Building_Zone, DeviceMetadata
from thermostat.models import Thermostat
from lighting.models import Lighting
from smartplug.models import Plugload
import json
from helper import config_helper

from ZMQHelper.zmq_pub import ZMQ_PUB as zmqPub
import settings
from _utils import defaults as __


kwargs = {'subscribe_address': 'ipc:///tmp/volttron-lite-agent-subscribe',
                    'publish_address': 'ipc:///tmp/volttron-lite-agent-publish'}
             
zmq_pub = zmqPub(**kwargs)

device_id = ''
disabled_values_thermostat = {"everyday": {
            'monday_heat': [],
            'monday_cool': [],
            'tuesday_heat': [],
            'tuesday_cool': [],
            'wednesday_heat': [],
            'wednesday_cool': [],
            'thursday_heat': [],
            'thursday_cool': [],
            'friday_heat': [],
            'friday_cool': [],
            'saturday_heat': [],
            'saturday_cool': [],
            'sunday_heat': [],
            'sunday_cool': []},
        "weekdayweekend": {
            'weekday_heat': [],
            'weekday_cool': [],
            'weekend_heat': [],
            'weekend_cool': []},
        "holiday": {
            'holiday_heat': [],
            'holiday_cool': [],
        }}

disabled_values_lighting = {"everyday": {
            'monday': [],
            'tuesday': [],
            'wednesday': [],
            'thursday': [],
            'friday': [],
            'saturday': [],
            'sunday': []},
        "weekdayweekend": {
            'weekday': [],
            'weekend': []},
        "holiday": {
            'holiday': []}}

disabled_values_plugload = {"everyday": {
            'monday': [],
            'tuesday': [],
            'wednesday': [],
            'thursday': [],
            'friday': [],
            'saturday': [],
            'sunday': []},
        "weekdayweekend": {
            'weekday': [],
            'weekend': []},
        "holiday": {
            'holiday': []}}


@login_required(login_url='/login/')
def thermostat_schedule(request, mac):
    print 'Inside Set Schedule method in Schedule app'
    context = RequestContext(request)
    username = request.user
    if request.user.get_profile().group.name.lower() == 'admin':
        print username
        print type(mac)
        mac = mac.encode('ascii', 'ignore')
        print type(mac)

        device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
        print device_metadata
        device_id = device_metadata[0]['device_id']
        device_type_id = device_metadata[0]['device_model_id']
        device_type_id = device_type_id.device_model_id

        device_status = [ob.data_as_json() for ob in Thermostat.objects.filter(thermostat_id=device_id)]
        device_zone = device_status[0]['zone']['id']
        device_nickname = device_status[0]['nickname']
        zone_nickname = device_status[0]['zone']['zone_nickname']
        #Send message to OS to launch application
        app_launcher_topic = '/ui/appLauncher/thermostat_scheduler/' + device_id + '/launch'
        token = {"auth_token": "bemoss"}
        zmq_pub.requestAgent(app_launcher_topic, json.dumps(token), "application/json", "UI")

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

        _data = {}
        active_schedule = []
        disabled_range = __.DISABLED_VALUES_THERMOSTAT

        #Check if schedule file for this device exists
        _file_name = os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/thermostat/' + device_id
                                  + '_schedule.json')
        if os.path.isfile(_file_name):
            json_file = open(_file_name, 'r+')
            _json_data = json.load(json_file)
            if device_id in _json_data['thermostat']:
                print 'device id present'
                _data = _json_data['thermostat'][device_id]['schedulers']

                active_schedule = _json_data['thermostat'][device_id]['active']
                active_schedule = [str(x) for x in active_schedule]
                disabled_range = get_disabled_date_ranges_thermostat(_data)
                #disabled_range = get_disabled_date_ranges(_data, disabled_values_plugload)
                _data = json.dumps(_data)
                _data = json.loads(_data, object_hook=_decode_dict)
            json_file.close()
        else:
            #json_file = open(_file_name, 'w+')
            _json_data = {"thermostat": {
                device_id: {
                    "active": ['everyday', 'holiday'],
                    "inactive": [],
                    "schedulers": __.THERMOSTAT_DEFAULT_SCHEDULE
                }}}

            with open(_file_name, 'w') as _new_file:
                json.dump(_json_data, _new_file, sort_keys=True, indent=4, ensure_ascii=False)
            _new_file.close()
            if type(_json_data) is dict:
                _data = _json_data['thermostat'][device_id]['schedulers']
            else:
                _json_data = json.loads(_json_data)
                _data = _json_data['thermostat'][device_id]['schedulers']
            active_schedule = ['everyday', 'holiday']
            disabled_range = get_disabled_date_ranges_thermostat(_data)

        return render_to_response(
            'schedule/th_sch.html',
            {'device_id': device_id, 'device_zone': device_zone, 'zone_nickname': zone_nickname, 'mac_address': mac,
             'device_nickname': device_nickname, 'schedule': _data,
             'disabled_ranges': disabled_range, 'active_schedule': active_schedule,  'zones': zones,
             'thermostat_sn': thermostats_sn,
             'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn}, context)
    else:
        return HttpResponseRedirect('/home')


def get_disabled_date_ranges_thermostat(_data):

    disabled_values = __.DISABLED_VALUES_THERMOSTAT
    for sch_type in _data:
        if sch_type == 'holiday':
            for item in _data[sch_type]:
                value = []
                for _item in _data[sch_type][item]:
                    value.append(int(_item['at']))
                disabled_values[sch_type][sch_type + '_' + item] = value
        else:
            for day in _data[sch_type]:
                for item in _data[sch_type][day]:
                    value = []
                    for _item in _data[sch_type][day][item]:
                        value.append(int(_item['at']))
                    disabled_values[sch_type][day + '_' + item] = value
    print disabled_values
    return disabled_values


@login_required(login_url='/login/')
def update_thermostat_schedule(request):
    if request.POST:
        _data = json.loads(request.body)
        print _data
        device_info = _data['device_info']
        device_info = device_info.split('/')
        device_id = device_info[2]
        device_type = device_info[1]
        device_zone = device_info[0]
        schedule_type = ''
        if 'everyday' in str(_data):
            schedule_type = 'everyday'
        elif 'weekdayweekend' in str(_data):
            schedule_type = 'weekdayweekend'
        elif 'holiday' in str(_data):
            schedule_type = 'holiday'
        save_schedule(device_id, device_type, _data['schedule'], schedule_type)

        message_to_agent = {
            "path": os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/' + device_type + '/' + device_id
                              + '_schedule.json'),
            "auth_token": "bemoss"
        }
        ieb_topic = '/ui/app/' + device_type + '_scheduler/' + device_id + '/update'
        print ieb_topic
        zmq_pub.requestAgent(ieb_topic, json.dumps(message_to_agent), "application/json", "UI")

        _data_to_send = {"update_number": "to_be_added"}

        if request.is_ajax():
            return HttpResponse(json.dumps(_data_to_send), mimetype='application/json')


def save_schedule(device_id, device_type, _data, schedule_type):
    #json_file = open(os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/' + device_type + '_schedule.json'), "r+")
    _file_name = os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/' + device_type + '/' + device_id
                              + '_schedule.json')
    json_file = open(_file_name, "r+")
    _json_data = json.load(json_file)
    print _json_data
    if device_id not in _json_data[device_type]:
        _json_data[device_type][device_id] = {'active': [], 'inactive': [], 'schedulers': {}}
    _json_data[device_type][device_id]['schedulers'][schedule_type] = _data[schedule_type]
    print _json_data
    json_file.seek(0)
    json_file.write(json.dumps(_json_data, indent=4, sort_keys=True))
    json_file.truncate()
    json_file.close()
    pass


def activate_schedule(request):
    if request.POST:
        _data = json.loads(request.body)
        device_info = _data['device_info']
        device_info = device_info.split('/')
        device_type = device_info[1]
        device_id = device_info[2]
        #json_file = open(os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/' + device_type + '_schedule.json'), "r+")
        _file_name = os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/' + device_type + '/' + device_id
                              + '_schedule.json')
        json_file = open(_file_name, "r+")
        _json_data = json.load(json_file)
        _json_data[device_type][device_id]['active'] = _data['active']
        _json_data[device_type][device_id]['inactive'] = _data['inactive']
        json_file.seek(0)
        json_file.write(json.dumps(_json_data, indent=4, sort_keys=True))
        json_file.truncate()
        json_file.close()

        message_to_agent = {
            "path": _file_name,
            "auth_token": "bemoss"
        }
        ieb_topic = '/ui/app/' + device_type + '_scheduler/' + device_id + '/update'
        print ieb_topic
        zmq_pub.requestAgent(ieb_topic, json.dumps(message_to_agent), "application/json", "UI")

        _data_to_send = {"status": "success"}

        if request.is_ajax():
            return HttpResponse(json.dumps(_data_to_send), mimetype='application/json')

@login_required(login_url='/login/')
def update_schedule_status_to_browser(request):
    print "device_schedule_update_message_to_browser"
    if request.method == 'POST':
        _data = request.raw_post_data
        device_info = _data
        device_info = device_info.split('/')
        device_type = device_info[1]
        device_id = device_info[2]
        topic = 'schedule_update_status'
        thermostat_update_schedule_status = config_helper.get_update_message(topic)
        print type(thermostat_update_schedule_status)
        data_split = str(thermostat_update_schedule_status).split("/")
        if data_split[0] == device_id:
            result = data_split[1]
        else:
            result = 'failure'
        json_result = {'status': result}
        #zmq_topics.reset_update_topic()
        print json.dumps(json_result)
        if request.is_ajax():
            return HttpResponse(json.dumps(json_result), mimetype='application/json')


@login_required(login_url='/login/')
def plugload_schedule(request, mac):
    print 'Inside Set Schedule method in Schedule app'
    context = RequestContext(request)
    username = request.user
    if request.user.get_profile().group.name.lower() == 'admin':
        print username
        print type(mac)
        mac = mac.encode('ascii', 'ignore')
        print type(mac)

        device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
        print device_metadata
        device_id = device_metadata[0]['device_id']
        device_type_id = device_metadata[0]['device_model_id']
        device_type_id = device_type_id.device_model_id

        if device_type_id == '2WL':
            device_status = [ob.data_as_json() for ob in Lighting.objects.filter(lighting_id=device_id)]
            device_zone = device_status[0]['zone']['id']
            device_nickname = device_status[0]['nickname']
            zone_nickname = device_status[0]['zone']['zone_nickname']
        else:
            device_status = [ob.data_as_json() for ob in Plugload.objects.filter(plugload_id=device_id)]
            device_zone = device_status[0]['zone']['id']
            device_nickname = device_status[0]['nickname']
            zone_nickname = device_status[0]['zone']['zone_nickname']


        # Send message to OS to launch application
        app_launcher_topic = '/ui/appLauncher/plugload_scheduler/' + device_id + '/launch'
        token = {"auth_token": "bemoss"}
        zmq_pub.requestAgent(app_launcher_topic, json.dumps(token), "application/json", "UI")

        _data = {}
        active_schedule = []
        disabled_range = __.DISABLED_VALUES_PLUGLOAD

        if device_type_id == '2WL':
            #Check if schedule file for this device exists
            _file_name = os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/lighting/' + device_id
                                      + '_schedule.json')
            if os.path.isfile(_file_name):
                json_file = open(_file_name, 'r+')
                _json_data = json.load(json_file)
                if device_id in _json_data['lighting']:
                    print 'device id present'
                    _data = _json_data['lighting'][device_id]['schedulers']

                    active_schedule = _json_data['lighting'][device_id]['active']
                    active_schedule = [str(x) for x in active_schedule]
                    disabled_range = get_disabled_date_ranges(_data, __.DISABLED_VALUES_LIGHTING)
                    _data = json.dumps(_data)
                    _data = json.loads(_data, object_hook=_decode_dict)
                json_file.close()
            else:
                #json_file = open(_file_name, 'w+')
                _json_data = {"lighting": {
                    device_id: {
                        "active": ['everyday', 'holiday'],
                        "inactive": [],
                        "schedulers": __.LIGHTING_DEFAULT_SCHEDULE_2WL
                    }}}

                with open(_file_name, 'w') as _new_file:
                    json.dump(_json_data, _new_file, sort_keys=True, indent=4, ensure_ascii=False)
                _new_file.close()
                if type(_json_data) is dict:
                    _data = _json_data['lighting'][device_id]['schedulers']
                else:
                    _json_data = json.loads(_json_data)
                    _data = _json_data['lighting'][device_id]['schedulers']
                active_schedule = ['everyday', 'holiday']
                disabled_range = get_disabled_date_ranges(_data, __.DISABLED_VALUES_LIGHTING)
        else:
            _file_name = os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/plugload/' + device_id
                                      + '_schedule.json')
            if os.path.isfile(_file_name):
                json_file = open(_file_name, 'r+')
                _json_data = json.load(json_file)
                if device_id in _json_data['plugload']:
                    print 'device id present'
                    _data = _json_data['plugload'][device_id]['schedulers']

                    active_schedule = _json_data['plugload'][device_id]['active']
                    active_schedule = [str(x) for x in active_schedule]
                    disabled_range = get_disabled_date_ranges(_data, __.DISABLED_VALUES_PLUGLOAD)
                    _data = json.dumps(_data)
                    _data = json.loads(_data, object_hook=_decode_dict)
                json_file.close()
            else:
                #json_file = open(_file_name, 'w+')
                _json_data = {"plugload": {
                    device_id: {
                        "active": ['everyday', 'holiday'],
                        "inactive": [],
                        "schedulers": __.PLUGLOAD_DEFAULT_SCHEDULE
                    }}}

                with open(_file_name, 'w') as _new_file:
                    json.dump(_json_data, _new_file, sort_keys=True, indent=4, ensure_ascii=False)
                _new_file.close()
                if type(_json_data) is dict:
                    _data = _json_data['plugload'][device_id]['schedulers']
                else:
                    _json_data = json.loads(_json_data)
                    _data = _json_data['plugload'][device_id]['schedulers']
                active_schedule = ['everyday', 'holiday']
                disabled_range = get_disabled_date_ranges(_data, __.DISABLED_VALUES_PLUGLOAD)

        '''
        if device_type_id =='2WL':
            json_file = open(os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/lighting_schedule.json'), "r+")
            _json_data = json.load(json_file)

            if device_id in _json_data['lighting']:
                print 'device id present'
                _data = _json_data['lighting'][device_id]['schedulers']

                active_schedule = _json_data['lighting'][device_id]['active']
                active_schedule = [str(x) for x in active_schedule]
                disabled_range = get_disabled_date_ranges(_data, disabled_values_lighting)
                _data = json.dumps(_data)
                _data = json.loads(_data, object_hook=_decode_dict)
            else:
                _data = {}
                active_schedule = []
                disabled_range = disabled_values_lighting
        else:
            json_file = open(os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/plugload_schedule.json'), "r+")
            _json_data = json.load(json_file)

            if device_id in _json_data['plugload']:
                print 'device id present'
                _data = _json_data['plugload'][device_id]['schedulers']

                active_schedule = _json_data['plugload'][device_id]['active']
                active_schedule = [str(x) for x in active_schedule]
                disabled_range = get_disabled_date_ranges(_data, disabled_values_plugload)
                _data = json.dumps(_data)
                _data = json.loads(_data, object_hook=_decode_dict)
            else:
                _data = {}
                active_schedule = []
                disabled_range = disabled_values_plugload
        '''

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
            'schedule/pl_sch.html',
            {'device_id': device_id, 'device_zone': device_zone, 'zone_nickname': zone_nickname, 'mac_address': mac,
             'device_nickname': device_nickname, 'schedule': _data,
             'disabled_ranges': disabled_range, 'active_schedule': active_schedule, 'type': device_type_id,
             'device_type_id': device_type_id}, context)
    else:
        return HttpResponseRedirect('/home/')



@login_required(login_url='/login/')
def lighting_schedule(request, mac):
    print 'Inside Set Schedule method in Schedule app'
    context = RequestContext(request)
    username = request.user
    if request.user.get_profile().group.name.lower() == 'admin':
        print username
        print type(mac)
        mac = mac.encode('ascii', 'ignore')
        print type(mac)

        device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
        print device_metadata
        device_id = device_metadata[0]['device_id']
        device_type_id = device_metadata[0]['device_model_id']
        device_type_id = device_type_id.device_model_id
        device_status = [ob.data_as_json() for ob in Lighting.objects.filter(lighting_id=device_id)]
        device_zone = device_status[0]['zone']['id']
        device_nickname = device_status[0]['nickname']
        zone_nickname = device_status[0]['zone']['zone_nickname']

        '''
        device_info = [ob.as_json() for ob in Device_Info.objects.filter(mac_address=mac)]
        print device_info
        device_id = device_info[0]['id']
        device_id = device_id.encode('ascii', 'ignore')
        device_zone = device_info[0]['zone']['id']
        device_nickname = device_info[0]['nickname']
        zone_nickname = device_info[0]['zone']['zone_nickname']
        device_type_id = device_info[0]['device_type_id']
        print device_id
        print device_zone
        '''

        # Send message to OS to launch application
        app_launcher_topic = '/ui/appLauncher/lighting_scheduler/' + device_id + '/launch'
        token = {"auth_token": "bemoss"}
        zmq_pub.requestAgent(app_launcher_topic, json.dumps(token), "application/json", "UI")

        _data = {}
        active_schedule = []
        disabled_range = __.DISABLED_VALUES_LIGHTING

        #Check if schedule file for this device exists
        _file_name = os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/lighting/' + device_id
                                  + '_schedule.json')
        if os.path.isfile(_file_name):
            json_file = open(_file_name, 'r+')
            _json_data = json.load(json_file)
            if device_id in _json_data['lighting']:
                print 'device id present'
                _data = _json_data['lighting'][device_id]['schedulers']

                active_schedule = _json_data['lighting'][device_id]['active']
                active_schedule = [str(x) for x in active_schedule]
                disabled_range = get_disabled_date_ranges(_data, __.DISABLED_VALUES_LIGHTING)
                _data = json.dumps(_data)
                _data = json.loads(_data, object_hook=_decode_dict)
            json_file.close()
        else:
            #json_file = open(_file_name, 'w+')
            if device_type_id == '2SDB' or device_type_id == '2DB' or device_type_id == '2WSL':
                _json_data = {"lighting": {
                device_id: {
                    "active": ['everyday', 'holiday'],
                    "inactive": [],
                    "schedulers": __.LIGHTING_DEFAULT_SCHEDULE_2DB_2SDB
                    }}}
            elif device_type_id == '2HUE':
                _json_data = {"lighting": {
                device_id: {
                    "active": ['everyday', 'holiday'],
                    "inactive": [],
                    "schedulers": __.LIGHTING_DEFAULT_SCHEDULE_2HUE
                    }}}

            with open(_file_name, 'w') as _new_file:
                json.dump(_json_data, _new_file, sort_keys=True, indent=4, ensure_ascii=False)
            _new_file.close()
            if type(_json_data) is dict:
                _data = _json_data['lighting'][device_id]['schedulers']
            else:
                _json_data = json.loads(_json_data)
                _data = _json_data['lighting'][device_id]['schedulers']
            active_schedule = ['everyday', 'holiday']
            disabled_range = get_disabled_date_ranges(_data, __.DISABLED_VALUES_LIGHTING)

        '''
        json_file = open(os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/lighting_schedule.json'), "r+")
        _json_data = json.load(json_file)

        if device_id in _json_data['lighting']:
            print 'device id present'
            _data = _json_data['lighting'][device_id]['schedulers']

            active_schedule = _json_data['lighting'][device_id]['active']
            active_schedule = [str(x) for x in active_schedule]
            disabled_range = get_disabled_date_ranges(_data, disabled_values_lighting)
            _data = json.dumps(_data)
            _data = json.loads(_data, object_hook=_decode_dict)
        else:
            _data = {}
            active_schedule = []
            disabled_range = disabled_values_lighting
        '''

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
            'schedule/lt_sch.html',
            {'device_id': device_id, 'device_zone': device_zone, 'zone_nickname': zone_nickname, 'mac_address': mac,
             'device_nickname': device_nickname, 'schedule': _data,
             'disabled_ranges': disabled_range, 'active_schedule': active_schedule, 'type': device_type_id,
             'zones': zones,
             'thermostat_sn': thermostats_sn,
             'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn}, context)
    else:
        return HttpResponseRedirect('/home/')


def get_disabled_date_ranges(_data, disabled_values_type):
    disabled_values = disabled_values_type
    for sch_type in _data:
        if sch_type == 'holiday':
            for item in _data[sch_type]:
                value = []
                for _item in _data[sch_type][item]:
                    value.append(int(_item['at']))
                disabled_values[sch_type][item] = value
        else:
            for day in _data[sch_type]:
                value = []
                for item in _data[sch_type][day]:
                    value.append(int(item['at']))
                disabled_values[sch_type][day] = value
    print disabled_values
    return disabled_values


def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv


def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv