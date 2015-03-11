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

__author__ = "kruthika"

from alerts.views import get_notifications
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from datetime import datetime
from django.http import HttpResponse
from dashboard.models import Building_Zone, DeviceMetadata
from helper import config_helper
from _utils import page_load_utils as _helper
from ZMQHelper.zmq_pub import ZMQ_PUB as zmqPub
from thermostat.models import Thermostat
from lighting.models import Lighting
from smartplug.models import Plugload
import httplib
import os
import time
import json
import urllib2
import logging
import settings

logger = logging.getLogger("views")

kwargs = {'subscribe_address': 'ipc:///tmp/volttron-lite-agent-subscribe',
                    'publish_address': 'ipc:///tmp/volttron-lite-agent-publish'}
             
zmq_pub = zmqPub(**kwargs)


def recursive_get_device_update(update_variable):
    #wifi_3m50_device_initial_update = SessionHelper.get_device_update_message(update_variable)
    wifi_3m50_device_initial_update = config_helper.get_device_update_message(update_variable)
    print wifi_3m50_device_initial_update
    if wifi_3m50_device_initial_update != '{empty_string}':
        vals = wifi_3m50_device_initial_update
        return vals
    else:
        recursive_get_device_update(update_variable)


@login_required(login_url='/login/')
def thermostat(request, mac):
    print 'Thermostat pageload'
    context = RequestContext(request)
    mac = mac.encode('ascii', 'ignore')

    device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
    print device_metadata
    device_type = device_metadata[0]['device_type']
    device_id = device_metadata[0]['device_id']
    device_type_id = device_metadata[0]['device_model_id']
    device_type_id = device_type_id.device_model_id
    print device_type_id

    device_status = [ob.data_as_json() for ob in Thermostat.objects.filter(thermostat_id=device_id)]
    device_zone = device_status[0]['zone']['id']
    device_nickname = device_status[0]['nickname']
    zone_nickname = device_status[0]['zone']['zone_nickname']
    override = device_status[0]['override']

    info_required = "Update thermostat data"
    ieb_topic = '/ui/agent/bemoss/' + str(device_zone) + '/' + device_type + '/' + device_id + '/device_status'
    zmq_pub.requestAgent(ieb_topic, info_required, "text/plain", "UI")

    json_file = open(os.path.join(settings.PROJECT_DIR, 'resources/page_load/page_load.json'), "r+")
    _json_data = json.load(json_file)
    if device_id not in _json_data['thermostat']:
        _json_data['thermostat'][device_id] = {"page_load": "{empty_string}"}

    json_file.seek(0)
    json_file.write(json.dumps(_json_data, indent=4, sort_keys=True))
    json_file.truncate()
    json_file.close()

    time.sleep(3)
    #Using page_load.json
    vals = _helper.get_page_load_data(device_id, device_type, device_type_id)
    print vals

    #Get current weather data from wunderground
    json_file = open(os.path.join(settings.PROJECT_DIR, 'resources/metadata/bemoss_metadata.json'), "r+")
    _json_data = json.load(json_file)
    zipcode = _json_data['building_location_zipcode']
    json_file.close()

    rs = {}
    try:
        rs = urllib2.urlopen("http://api.wunderground.com/api/4fef576e26759640/conditions/q/" + zipcode + ".json")
    except urllib2.HTTPError, e:
        logger.error('HTTPError = ' + str(e.code))
    except urllib2.URLError, e:
        logger.error('URLError = ' + str(e.reason))
    except httplib.HTTPException, e:
        logger.error('HTTPException = ' + str(e.message))
    except Exception:
        import traceback
        logger.error('generic exception: ' + traceback.format_exc())
    print rs
    print zipcode
    if rs == {} :
        location = 'Arlington, VA (Network unavailable - showing default values)    '
        temp_f = '77'
        humidity = '10%'
        precip = '0.0'
        winds = '1.0'
        icon = 'mostlysunny'
        weather = 'Sunny'
    else:
        json_string = rs.read()
        try:
            parsed_json = json.loads(json_string)
            location = parsed_json['current_observation']['display_location']['full']
            temp_f = parsed_json['current_observation']['temp_f']
            humidity = parsed_json['current_observation']['relative_humidity']
            precip = parsed_json['current_observation']['precip_1hr_in']
            winds = parsed_json['current_observation']['wind_mph']
            icon = str(parsed_json['current_observation']['icon'])
            weather = parsed_json['current_observation']['weather']
        except Exception:
            location = 'Arlington, VA (Zipcode Error. Update settings/Contact Admin.)'
            temp_f = '77'
            humidity = '10%'
            precip = '0.0'
            winds = '1.0'
            icon = 'mostlysunny'
            weather = 'Sunny'

        #weather_icon = SessionHelper.get_weather_icon(icon)
    weather_icon = config_helper.get_weather_icon(icon)
    print "icon "+weather_icon

    zones = [ob.as_json() for ob in Building_Zone.objects.all()]
    thermostats_sn = [ob.data_side_nav() for ob in Thermostat.objects.filter(network_status='ONLINE', thermostat_id__bemoss=True)]
    lighting_sn = [ob.data_side_nav() for ob in Lighting.objects.filter(network_status='ONLINE', lighting_id__bemoss=True)]
    plugload_sn = [ob.data_side_nav() for ob in Plugload.objects.filter(network_status='ONLINE', plugload_id__bemoss=True)]
    active_al = get_notifications()
    context.update({'active_al':active_al})
    context.update({
            'zones': zones, 'thermostat_sn': thermostats_sn,
             'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn})

    return render_to_response(
        'thermostat/thermostat.html',
        {'device_id': device_id, 'device_zone': device_zone, 'device_type_id': device_type_id, 'zone_nickname': zone_nickname, 'mac_address': mac,
         'device_nickname': device_nickname, 'device_data': vals, 'location': location, 'temp_f': temp_f, 'humidity': humidity, 'precip': precip,
         'winds': winds, 'override': override, 'weather_icon': weather_icon, 'weather': weather, 'mac': mac},
        context)


def get_zip_code():
    try:
        location_info = urllib2.urlopen('http://ipinfo.io/json').read()
        location_info_json = json.loads(location_info)
        zipcode = location_info_json['postal'].encode('ascii', 'ignore')
        return zipcode
    except urllib2.HTTPError, e:
        logger.error('HTTPError = ' + str(e.code))
    except urllib2.URLError, e:
        logger.error('URLError = ' + str(e.reason))
    except httplib.HTTPException, e:
        logger.error('HTTPException = ' + str(e.message))
    except Exception:
        import traceback
        logger.error('generic exception: ' + traceback.format_exc())


@login_required(login_url='/login/')
def weather(request):
    print os.path.basename(__file__)+"in weather function"
    if request.method == 'GET':
        #Get current weather data from wunderground
        json_file = open(os.path.join(settings.PROJECT_DIR, 'resources/metadata/bemoss_metadata.json'), "r+")
        _json_data = json.load(json_file)
        zipcode = _json_data['building_location_zipcode']
        json_file.close()

        rs = {}
        try:
            rs = urllib2.urlopen("http://api.wunderground.com/api/4fef576e26759640/conditions/q/" + zipcode + ".json")
        except urllib2.HTTPError, e:
            logger.error('HTTPError = ' + str(e.code))
        except urllib2.URLError, e:
            logger.error('URLError = ' + str(e.reason))
        except httplib.HTTPException, e:
            logger.error('HTTPException = ' + str(e.message))
        except Exception:
            import traceback
            logger.error('generic exception: ' + traceback.format_exc())
        print rs
        if rs == {}:
            location = 'Arlington, VA (Network unavailable - showing default values)'
            temp_f = '77'
            humidity = '10%'
            precip = '0.0'
            winds = '1.0'
            icon = 'mostlysunny'
            weather = 'Sunny'
        else:
            json_string = rs.read()
            try:
                parsed_json = json.loads(json_string)
                location = parsed_json['current_observation']['display_location']['full']
                temp_f = parsed_json['current_observation']['temp_f']
                humidity = parsed_json['current_observation']['relative_humidity']
                precip = parsed_json['current_observation']['precip_1hr_in']
                winds = parsed_json['current_observation']['wind_mph']
                icon = str(parsed_json['current_observation']['icon'])
                weather = parsed_json['current_observation']['weather']
            except Exception:
                location = 'Arlington, VA (Zipcode Error. Update settings/Contact Admin.)'
                temp_f = '77'
                humidity = '10%'
                precip = '0.0'
                winds = '1.0'
                icon = 'mostlysunny'
                weather = 'Sunny'

        #weather_icon = SessionHelper.get_weather_icon(icon)
        weather_icon = config_helper.get_weather_icon(icon)
        #weather_icon = "<i class=\"" + weather_icon + "\"></i>"
        print "icon"+weather_icon
        
        jsonresult = {
                          'locat':location,
                          'temp_f':temp_f,
                          'humidity':humidity,
                          'precip':precip,
                          'winds':winds,
                          'icon':weather_icon,
                          'weather':weather
                          }
        print json.dumps(jsonresult)
        if request.is_ajax():
            return HttpResponse(json.dumps(jsonresult), mimetype='application/json')


@login_required(login_url='/login/')
def submit_values(request):
    if request.POST:
        _data = request.raw_post_data
        json_data = json.loads(_data)

        device_info = json_data['device_info']
        print device_info

        json_data.pop('device_info')
        print json_data

        device_id = device_info.split("/")
        device_id = device_id[2]

        override = json_data['override']
        device_obj = Thermostat.objects.get(thermostat_id=device_id)
        device_obj.override = override
        device_obj.save()
        json_data.pop('override')
        print json_data

        update_number = "wifi_3m50_01"

        ieb_topic = '/ui/agent/bemoss/'+device_info+'/update'
        print ieb_topic
        content_type = "application/json"
        fromUI = "UI"
        print "entering in sending message to agent"
        kwargs = {'subscribe_address': 'ipc:///tmp/volttron-lite-agent-subscribe',
                    'publish_address': 'ipc:///tmp/volttron-lite-agent-publish'}
        _zmq_pub = zmqPub(**kwargs)
        print "created instance of the zmqpub class"
        _zmq_pub.sendToAgent(ieb_topic, json_data, content_type, fromUI)
        print json_data
        print "success in sending message to agent"

        a_dict = {'update_number': update_number}
        json_data.update(a_dict)
        print json_data

        if request.is_ajax():
            return HttpResponse(json.dumps(json_data), mimetype='application/json')


@login_required(login_url='/login/')
def get_thermostat_current_status(request):
    print "Getting current status of thermostat"
    if request.method == 'POST':
        data_recv = request.raw_post_data
        data_recv = json.loads(data_recv)
        # same as the thermostat load method
        info_required = "current status"
        wifi_3m50_update_send_topic = '/ui/agent/bemoss/' + data_recv['device_info'] + '/device_status'
        print wifi_3m50_update_send_topic
        zmq_pub.requestAgent(wifi_3m50_update_send_topic, info_required, "text/plain", "UI")

        jsonresult = {'status': 'sent'}

        if request.is_ajax():
            return HttpResponse(json.dumps(jsonresult), mimetype='application/json')

