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


from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
import json
import ast
import re
import time
from alerts.views import get_notifications

from ZMQHelper.zmq_pub import ZMQ_PUB
from helper import config_helper
from ZMQHelper import zmq_topics

from .models import DeviceMetadata, Building_Zone, GlobalSetting
from thermostat.models import Thermostat
from smartplug.models import Plugload
from lighting.models import Lighting
from admin.models import NetworkStatus



kwargs = {'subscribe_address': 'ipc:///tmp/volttron-lite-agent-subscribe',
                    'publish_address': 'ipc:///tmp/volttron-lite-agent-publish'}

zmq_pub = ZMQ_PUB(**kwargs)

@login_required(login_url='/login/')
def add_new_zone(request):
    if request.POST:
        _data = request.raw_post_data
        #print _data
        zone_id = ""
        a = re.compile("^[A-Za-z0-9_ ]*[A-Za-z0-9 ][A-Za-z0-9_ ]*$")
        if (a.match(_data)):
            p = Building_Zone.objects.get_or_create(zone_nickname=str(_data))
            zone_id = Building_Zone.objects.get(zone_nickname=str(_data)).zone_id
            global_settings = GlobalSetting(id=zone_id, heat_setpoint=70, cool_setpoint=72, illuminance=67, zone_id=zone_id)
            global_settings.save()
            message = "success"
            if request.is_ajax():
                return HttpResponse(str(zone_id), mimetype='text/plain')
        else:
            message = "invalid"
            if request.is_ajax():
                return HttpResponse("invalid", mimetype='text/plain')
    

@login_required(login_url='/login/')
def save_changes_modal(request):
    if request.POST:
        _data = request.raw_post_data
        #print type(_data)
        a = re.compile("^[A-Za-z0-9_]*[A-Za-z0-9][A-Za-z0-9_]*$")
        _data = ast.literal_eval(_data)
        if a.match(_data['nickname']):
            device_id = _data['id']
            nickname = _data['nickname']
            #device = Device_Info.objects.get(id=device_id)
            device_type_id = _data['device_type']
            if device_type_id == '1TH' or device_type_id == '1NST':
                device = Thermostat.objects.get(thermostat_id=device_id)
                device.nickname = nickname
                device.save()
            elif device_type_id == '2DB' or device_type_id == '2SDB' or device_type_id =='2HUE' or device_type_id =='2WL' or device_type_id == '2WSL':
                device = Lighting.objects.get(lighting_id=device_id)
                device.nickname = nickname
                device.save()
            elif device_type_id == '3WSP' or device_type_id =='3MOD' or device_type_id =='3VTH' or device_type_id =='3DSP' or device_type_id == '3WP':
                device = Plugload.objects.get(plugload_id=device_id)
                device.nickname = nickname
                device.save()

            message = {'status':'success',
                       'device_id':device_id,
                       'nickname':nickname}
            if request.is_ajax():
                return HttpResponse(json.dumps(message), mimetype='application/json')
        else:
            message = "invalid"
            if request.is_ajax():
                return HttpResponse(json.dumps(message), mimetype='application/json')


@login_required(login_url='/login/')
def save_zone_nickname_changes(request):
    context = RequestContext(request)
    if request.POST:
        _data = request.raw_post_data
        a = re.compile("^[A-Za-z0-9_]*[A-Za-z0-9][A-Za-z0-9_]*$")
        _data = ast.literal_eval(_data)
        if a.match(_data['nickname']):
            zone_id = _data['id']
            nickname = _data['nickname']
            zone = Building_Zone.objects.get(zone_id=zone_id)
            zone.zone_nickname = nickname  # change field
            zone.save()
            message = {'status':'success',
                       'zone_id':zone_id,
                       'nickname':nickname}
            if request.is_ajax():
                return HttpResponse(json.dumps(message),mimetype='application/json')
        else:
            message = "invalid"
            if request.is_ajax():
                return HttpResponse(json.dumps(message),mimetype='application/json')


@login_required(login_url='/login/')
def identify_device(request):

    if request.POST:
        _data = request.raw_post_data
        _data = json.loads(_data)
        #print _data
        #print "Identify device"
        device_info = [ob.data_as_json() for ob in DeviceMetadata.objects.filter(device_id=_data['id'])]
        device_id = device_info[0]['device_id']
        if 'zone_id' in _data:
            device_zone = _data['zone_id']
        device_model = device_info[0]['device_model_id']
        device_type_id = device_model.device_model_id

        if device_type_id == '1TH' or device_type_id == '1NST':
            device_zone = Thermostat.objects.get(thermostat_id=device_id).zone_id
            #print device_zone
            device_type = 'thermostat'
        elif device_type_id == '2DB' or device_type_id == '2SDB' or device_type_id =='2HUE' or device_type_id =='2WL' or device_type_id == '2WSL':
            device_zone = Lighting.objects.get(lighting_id=device_id).zone_id
            #print device_zone
            device_type = 'lighting'
        elif device_type_id == '3WSP' or device_type_id =='3MOD' or device_type_id =='3VTH' or device_type_id =='3DSP' or device_type_id == '3WP':
            device_zone = Plugload.objects.get(plugload_id=device_id).zone_id
            #print device_zone
            device_type = 'plugload'

        info_required = "Identify device"
        ieb_topic = '/ui/agent/bemoss/' + str(device_zone) + '/' + device_type + '/' + device_id + '/identify'
        #wifi_3m50_update_send_topic = 'ui/agent/bemoss/zone1/thermostat/' + device_id + '/device_status'
        zmq_pub.requestAgent(ieb_topic, info_required, "text/plain", "UI")
        zmq_topics.reset_update_topic('identify_device_status_' + device_type)
        #print "Reset old device status"

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def identify_status(request):
    if request.POST:
        _data = request.raw_post_data
        device_info = [ob.data_as_json() for ob in DeviceMetadata.objects.filter(device_id=_data)]
        device_type_id = device_info[0]['device_model_id']
        device_type_id = device_type_id.device_model_id
        if device_type_id == '1TH' or device_type_id == '1NST':
            device_type = 'thermostat'
        elif device_type_id == '2DB' or device_type_id == '2SDB' or device_type_id =='2HUE' or device_type_id =='2WL' or device_type_id == '2WSL':
            device_type = 'lighting'
        elif device_type_id == '3WSP' or device_type_id =='3MOD' or device_type_id =='3VTH' or device_type_id =='3DSP' or device_type_id == '3WP':
            device_type = 'plugload'

        #identify_status_message = recursive_get_device_update('identify_device_status_' + device_type)
        identify_status_message = config_helper.get_device_update_message('identify_device_status_' + device_type)

        data_split = identify_status_message.split("/")
        if data_split[0] == _data:
            result = data_split[1]

        json_result = {'status': result}
        zmq_topics.reset_update_topic('identify_device_status_' + device_type)

    if request.is_ajax():
        return HttpResponse(json.dumps(json_result), mimetype='application/json')


def recursive_get_device_update(update_variable):
    #wifi_3m50_device_initial_update = SessionHelper.get_device_update_message(update_variable)
    wifi_3m50_device_initial_update = config_helper.get_device_update_message(update_variable)
    vals = ""
    if wifi_3m50_device_initial_update != '{update_number}/{status}':
        vals = wifi_3m50_device_initial_update
        return vals
    else:
        time.sleep(5)
        recursive_get_device_update(update_variable)


@login_required(login_url='/login/')
def discover_nodes(request):
    #print 'inside dashboard - node discovery page method'
    context = RequestContext(request)

    username = request.user
    #print username

    if request.user.get_profile().group.name.lower() == 'admin':
        zones = [ob.as_json() for ob in Building_Zone.objects.all()]
        thermostats_sn = [ob.data_side_nav() for ob in Thermostat.objects.filter(network_status='ONLINE',
                                                                                 thermostat_id__bemoss=True)]
        lighting_sn = [ob.data_side_nav() for ob in Lighting.objects.filter(network_status='ONLINE',
                                                                            lighting_id__bemoss=True)]
        plugload_sn = [ob.data_side_nav() for ob in Plugload.objects.filter(network_status='ONLINE',
                                                                            plugload_id__bemoss=True)]
        active_al = get_notifications()
        context.update({'active_al':active_al})
        context.update({
            'zones': zones, 'thermostat_sn': thermostats_sn,
             'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn
        })

        return render_to_response(
            'dashboard/node_discovery.html',
            {}, context)
    else:
        return HttpResponseRedirect('/home/')


@login_required(login_url='/login/')
def discover(request):
    #print 'inside dashboard - device discovery page method'
    context = RequestContext(request)

    username = request.user
    #print username

    zones = [ob.as_json() for ob in Building_Zone.objects.all()]
    thermostats_sn = [ob.data_side_nav() for ob in Thermostat.objects.filter(network_status='ONLINE',
                                                                             thermostat_id__bemoss=True)]
    lighting_sn = [ob.data_side_nav() for ob in Lighting.objects.filter(network_status='ONLINE',
                                                                        lighting_id__bemoss=True)]
    plugload_sn = [ob.data_side_nav() for ob in Plugload.objects.filter(network_status='ONLINE',
                                                                        plugload_id__bemoss=True)]

    if request.user.get_profile().group.name.lower() == 'admin':
        thermostats = [ob.data_dashboard() for ob in Thermostat.objects.filter(network_status='ONLINE', thermostat_id__bemoss=True)]
        plugloads = [ob.data_dashboard() for ob in Plugload.objects.filter(network_status='ONLINE', plugload_id__bemoss=True)]
        lighting_loads = [ob.data_dashboard() for ob in Lighting.objects.filter(network_status='ONLINE', lighting_id__bemoss=True)]
        context.update({
            'zones': zones, 'thermostat_sn': thermostats_sn,
             'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn
        })
        active_al = get_notifications()
        context.update({'active_al':active_al})
        return render_to_response(
            'dashboard/discovery.html',
            {'thermostats': thermostats, 'plugloads':plugloads, 'lighting_loads':lighting_loads}, context)
    else:
        return HttpResponseRedirect('/home/')


@login_required(login_url='/login/')
def change_zones_thermostats(request):
    #print "Inside change zones for hvac controllers"
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        for thermostat in _data['thermostats']:
            if thermostat[1] != "Assign a New Zone":
                zone = Building_Zone.objects.get(zone_nickname__iexact=thermostat[1])
                th_instance = Thermostat.objects.get(thermostat_id=thermostat[0])
                #/ui/networkagent/device_id/old_zone_id/new_zone_id/change
                if zone.zone_id != th_instance.zone_id:
                    zone_update_send_topic = '/ui/networkagent/' + str(thermostat[0]) + '/' + str(th_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")

                th_instance.zone = zone  # change field
                th_instance.nickname = thermostat[2]
                if thermostat[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(thermostat[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    d_info = DeviceMetadata.objects.get(device_id=thermostat[0])
                    d_info.bemoss = False
                    d_info.save()
                    #th_instance.network_status = 'NBD'
                th_instance.save()
            else:
                zone = Building_Zone.objects.get(zone_id=999)
                th_instance = Thermostat.objects.get(thermostat_id=thermostat[0])
                th_instance.zone = zone  # change field
                th_instance.nickname = thermostat[2]
                if thermostat[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(thermostat[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    d_info = DeviceMetadata.objects.get(device_id=thermostat[0])
                    d_info.bemoss = False
                    d_info.save()
                    #th_instance.network_status = 'NBD'
                th_instance.save()

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def change_zones_plugloads(request):
    #print "Inside change zones for plugloads"
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        for plugload in _data['data']:
            if plugload[1] != "Assign a New Zone":
                zone = Building_Zone.objects.get(zone_nickname__iexact=plugload[1])
                pl_instance = Plugload.objects.get(plugload_id=plugload[0])
                if zone.zone_id != pl_instance.zone_id:
                    zone_update_send_topic = '/ui/networkagent/' + str(plugload[0]) + '/' + str(pl_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                pl_instance.zone = zone  # change field
                pl_instance.nickname = plugload[2]
                if plugload[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(plugload[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #pl_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=plugload[0])
                    d_info.bemoss = False
                    d_info.save()
                pl_instance.save()
            else:
                zone = Building_Zone.objects.get(zone_id=999)
                pl_instance = Plugload.objects.get(plugload_id=plugload[0])
                pl_instance.zone = zone  # change field
                pl_instance.nickname = plugload[2]
                if plugload[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(plugload[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #pl_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=plugload[0])
                    d_info.bemoss = False
                    d_info.save()
                pl_instance.save()

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def change_zones_lighting_loads(request):
    #print "Inside change zones for lighting loads"
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        for lt_load in _data['data']:
            if lt_load[1] != "Assign a New Zone":
                zone = Building_Zone.objects.get(zone_nickname__iexact=lt_load[1])
                lt_instance = Lighting.objects.get(lighting_id=lt_load[0])
                if zone.zone_id != lt_instance.zone_id:
                    zone_update_send_topic = '/ui/networkagent/' + str(lt_load[0]) + '/' + str(lt_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                lt_instance.zone = zone  # change field
                lt_instance.nickname = lt_load[2]
                if lt_load[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(lt_load[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #lt_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=lt_load[0])
                    d_info.bemoss = False
                    d_info.save()
                lt_instance.save()
            else:
                zone = Building_Zone.objects.get(zone_id=999)
                lt_instance = Lighting.objects.get(lighting_id=lt_load[0])
                lt_instance.zone = zone  # change field
                lt_instance.nickname = lt_load[2]
                if lt_load[3] == 'true':
                    zone_update_send_topic = '/ui/discoveryagent/' + str(lt_load[0]) + '/nbd'
                    zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
                    #lt_instance.network_status = 'NBD'
                    d_info = DeviceMetadata.objects.get(device_id=lt_load[0])
                    d_info.bemoss = False
                    d_info.save()
                lt_instance.save()

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def change_zones_lite(request):
    #print "Inside change zones for bemoss lite"
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        for lite in _data['data']:
            if lite[1] != "Associate with Zone":
                zone = Building_Zone.objects.get(zone_nickname__iexact=lite[1])
                lite_instance = NetworkStatus.objects.get(node_id=lite[0])
                lite_instance.associated_zone = zone  # change field
                lite_instance.save()

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def bemoss_home(request):
    context = RequestContext(request)
    username = request.user

    zones = [ob.as_json() for ob in Building_Zone.objects.all()]
    thermostats_sn = [ob.data_side_nav() for ob in Thermostat.objects.filter(network_status='ONLINE',
                                                                             thermostat_id__bemoss=True)]
    lighting_sn = [ob.data_side_nav() for ob in Lighting.objects.filter(network_status='ONLINE',
                                                                        lighting_id__bemoss=True)]
    plugload_sn = [ob.data_side_nav() for ob in Plugload.objects.filter(network_status='ONLINE',
                                                                        plugload_id__bemoss=True)]
    device_count ={
                    "devices": {
                    }
                    }

    all_zones = Building_Zone.objects.all()
    for zone in all_zones:
        th_count = Thermostat.objects.filter(network_status='ONLINE', zone_id=zone.zone_id,
                                             thermostat_id__bemoss=True).count()
        t_count = th_count

        pl_count = Plugload.objects.filter(network_status='ONLINE', zone_id=zone.zone_id, plugload_id__bemoss=True).count()
        lt_count = Lighting.objects.filter(network_status='ONLINE', zone_id=zone.zone_id, lighting_id__bemoss=True).count()


        device_count['devices'][zone.zone_id] = {'th': 0, 'pl': 0, 'lt': 0}
        device_count['devices'][zone.zone_id]['th'] = t_count
        device_count['devices'][zone.zone_id]['pl'] = pl_count
        device_count['devices'][zone.zone_id]['lt'] = lt_count

    zones_p = [ob.data_dashboard() for ob in Building_Zone.objects.all().order_by('zone_nickname')]

    for zone in zones_p:
        z_id = zone['id']
        zone['t_count'] = device_count['devices'][z_id]['th']
        zone['pl_count'] = device_count['devices'][z_id]['pl']
        zone['lt_count'] = device_count['devices'][z_id]['lt']

    active_al = get_notifications()
    context.update({'active_al':active_al})
    context.update({
            'zones': zones, 'thermostat_sn': thermostats_sn,
             'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn
    })

    return render_to_response(
        'dashboard/dashboard.html',
        {'zones_p': zones_p}, context)


@login_required(login_url='/login/')
def change_global_settings(request):
    #context = RequestContext(request)
    #username = request.user

    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        zone_id = _data['zone_id']
        zone = Building_Zone.objects.get(zone_id=zone_id)
        gsettings = GlobalSetting.objects.get(zone_id=zone)
        gsettings.heat_setpoint = _data['heat_setpoint']
        gsettings.cool_setpoint = _data['cool_setpoint']
        gsettings.illuminance = _data['illumination']
        gsettings.save()

        if request.is_ajax():
            return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def zone_device_listing(request, zone_dev):
    context = RequestContext(request)
    username = request.user

    zone_dev = zone_dev.encode('ascii', 'ignore')
    zone_info = zone_dev.split("_")
    zone_id = zone_info[0]
    device_type = zone_info[1]

    #Side navigation bar
    zones = [ob.as_json() for ob in Building_Zone.objects.all()]
    thermostats_sn = [ob.data_side_nav() for ob in Thermostat.objects.filter(network_status='ONLINE',
                                                                             thermostat_id__bemoss=True)]
    lighting_sn = [ob.data_side_nav() for ob in Lighting.objects.filter(network_status='ONLINE',
                                                                        lighting_id__bemoss=True)]
    plugload_sn = [ob.data_side_nav() for ob in Plugload.objects.filter(network_status='ONLINE',
                                                                        plugload_id__bemoss=True)]

    context.update({
        'zones': zones, 'thermostat_sn': thermostats_sn,
         'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn
    })

    #For the page
    if device_type == 'th':
        thermostats = [ob.data_as_json() for ob in Thermostat.objects.filter(zone_id=zone_id, thermostat_id__bemoss=True)]
        if len(thermostats) != 0:
            zone_nickname = thermostats[0]['zone']['zone_nickname']
        #print thermostats

        active_al = get_notifications()
        context.update({'active_al':active_al})
        return render_to_response(
            'dashboard/thermostats.html',
            {'thermostats': thermostats, 'zone_id': zone_id, 'zone_nickname': zone_nickname,
             'zones': zones, 'thermostat_sn': thermostats_sn, 'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn}, context)

    elif device_type == 'lt':
        lighting = [ob.data_as_json() for ob in Lighting.objects.filter(zone_id=zone_id, lighting_id__bemoss=True)]
        zone_nickname = lighting[0]['zone']['zone_nickname']
        #print lighting

        return render_to_response(
            'dashboard/lighting_loads.html',
            {'lighting_loads': lighting, 'zone_id': zone_id, 'zone_nickname': zone_nickname,
             'zones': zones, 'thermostat_sn': thermostats_sn, 'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn}, context)

    elif device_type == 'pl':
        plugloads = [ob.data_as_json() for ob in Plugload.objects.filter(zone_id=zone_id, plugload_id__bemoss=True)]
        zone_nickname = plugloads[0]['zone']['zone_nickname']
        #print plugloads

        return render_to_response(
            'dashboard/plugloads.html',
            {'plugloads': plugloads, 'zone_id': zone_id, 'zone_nickname': zone_nickname,
             'zones': zones, 'thermostat_sn': thermostats_sn, 'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn
             }, context)


@login_required(login_url='/login/')
def zone_device_all_listing(request, zone_dev):
    context = RequestContext(request)
    username = request.user

    zone_id = zone_dev.encode('ascii', 'ignore')

    #Side navigation bar
    zones = [ob.as_json() for ob in Building_Zone.objects.all()]
    thermostats_sn = [ob.data_side_nav() for ob in Thermostat.objects.filter(network_status='ONLINE',
                                                                             thermostat_id__bemoss=True)]
    lighting_sn = [ob.data_side_nav() for ob in Lighting.objects.filter(network_status='ONLINE',
                                                                        lighting_id__bemoss=True)]
    plugload_sn = [ob.data_side_nav() for ob in Plugload.objects.filter(network_status='ONLINE',
                                                                        plugload_id__bemoss=True)]

    active_al = get_notifications()
    context.update({'active_al':active_al})
    context.update({
        'zones': zones, 'thermostat_sn': thermostats_sn,
         'lighting_sn': lighting_sn, 'plugload_sn': plugload_sn
    })

    #For the page

    thermostats = [ob.data_as_json() for ob in Thermostat.objects.filter(zone_id=zone_id, thermostat_id__bemoss=True)]
    if len(thermostats) != 0:
        zone_nickname = thermostats[0]['zone']['zone_nickname']
    #print thermostats

    lighting = [ob.data_as_json() for ob in Lighting.objects.filter(zone_id=zone_id, lighting_id__bemoss=True)]
    if len(lighting) != 0:
        zone_nickname = lighting[0]['zone']['zone_nickname']
    #print lighting

    plugloads = [ob.data_as_json() for ob in Plugload.objects.filter(zone_id=zone_id, plugload_id__bemoss=True)]
    if len(plugloads) != 0:
        zone_nickname = plugloads[0]['zone']['zone_nickname']
    #print plugloads

    return render_to_response(
        'dashboard/zone_devices_all.html',
        {'thermostats': thermostats, 'lighting_loads': lighting,
         'plugloads': plugloads, 'zone_id': zone_id, 'zone_nickname': zone_nickname
         }, context)

@login_required(login_url='/login/')
def modify_thermostats(request):
    #print "Inside modify hvac controllers"
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        for thermostat in _data['thermostats']:
            zone = Building_Zone.objects.get(zone_nickname__iexact=thermostat[2])
            th_instance = Thermostat.objects.get(thermostat_id=thermostat[0])
            if zone.zone_id != th_instance.zone_id:
                zone_update_send_topic = '/ui/networkagent/' + str(thermostat[0]) + '/' + str(th_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
            th_instance.zone = zone  # change field
            th_instance.nickname = thermostat[1]
            th_instance.save()

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def modify_plugloads(request):
    #print "Inside modify plugloads"
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        for plugload in _data:
            zone = Building_Zone.objects.get(zone_nickname__iexact=plugload[2])
            pl_instance = Plugload.objects.get(plugload_id=plugload[0])
            if zone.zone_id != pl_instance.zone_id:
                zone_update_send_topic = '/ui/networkagent/' + str(plugload[0]) + '/' + str(pl_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
            pl_instance.zone = zone  # change field
            pl_instance.nickname = plugload[1]
            pl_instance.save()

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')


@login_required(login_url='/login/')
def modify_lighting_loads(request):
    #print "Inside modify lighting loads"
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        #print _data

        for lt_load in _data:
            zone = Building_Zone.objects.get(zone_nickname__iexact=lt_load[2])
            lt_instance = Lighting.objects.get(lighting_id=lt_load[0])
            if zone.zone_id != lt_instance.zone_id:
                zone_update_send_topic = '/ui/networkagent/' + str(lt_load[0]) + '/' + str(lt_instance.zone_id) + '/' + str(zone.zone_id) + '/change'
                zmq_pub.requestAgent(zone_update_send_topic, '{"auth_token": "bemoss"}', "text/plain", "UI")
            lt_instance.zone = zone  # change field
            lt_instance.nickname = lt_load[1]
            lt_instance.save()

    if request.is_ajax():
        return HttpResponse(json.dumps("success"), mimetype='application/json')













