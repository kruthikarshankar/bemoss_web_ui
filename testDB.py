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

__author__ = 'kruthika'

from django.core.management import setup_environ
import settings
import datetime

setup_environ(settings)

from dashboard.models import DeviceMetadata, DeviceModel, Building_Zone
from thermostat.models import Thermostat
from lighting.models import Lighting
from smartplug.models import Plugload
from admin.models import NetworkStatus

print "Adding database records for device_info table."

zone_999 = Building_Zone.objects.get(zone_id=999)

#Thermostat device_model objects
device_model_nest = DeviceModel.objects.get(device_model_id='1NST')
device_model_radio_th = DeviceModel.objects.get(device_model_id='1TH')


#Thermostats
device_info_th1 = DeviceMetadata(device_id="Thermostat1", device_type="thermostat", vendor_name="Google",
                                 device_model="Nest", device_model_id=device_model_nest, mac_address="ASDKJH1310",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_th1.save()

device_info_th2 = DeviceMetadata(device_id="Thermostat2", device_type="thermostat", vendor_name="Radio",
                                 device_model="CT30", device_model_id=device_model_radio_th, mac_address="ASASJH1310",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_th2.save()


#Lighting Controllers' Device Models
device_model_db = DeviceModel.objects.get(device_model_id='2DB')
device_model_sdb = DeviceModel.objects.get(device_model_id='2SDB')
device_model_hue = DeviceModel.objects.get(device_model_id='2HUE')
device_model_wl = DeviceModel.objects.get(device_model_id='2WL')
device_model_wsl = DeviceModel.objects.get(device_model_id='2WSL')

#Lighting Controllers
device_info_lt1 = DeviceMetadata(device_id="Lighting1", device_type="lighting", vendor_name="Dimmable Ballast",
                                 device_model="Dimmable ballast", device_model_id=device_model_db,
                                 mac_address="AASKJH1310", min_range=20, max_range=95, identifiable=True,
                                 communication="Wifi", date_added=datetime.datetime.now(), bemoss=True)
device_info_lt1.save()

device_info_lt2 = DeviceMetadata(device_id="Lighting2", device_type="lighting", vendor_name="StepDim",
                                 device_model="StepDim Ballast", device_model_id=device_model_sdb,
                                 mac_address="LKASJH1310", min_range=20, max_range=95, identifiable=True,
                                 communication="Wifi", date_added=datetime.datetime.now(), bemoss=True)
device_info_lt2.save()

device_info_lt3 = DeviceMetadata(device_id="Lighting3", device_type="lighting", vendor_name="Philips",
                                 device_model="Philips Hue", device_model_id=device_model_hue, mac_address="DFASDH1310",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_lt3.save()

device_info_lt4 = DeviceMetadata(device_id="Lighting4", device_type="lighting", vendor_name="Belkin",
                                 device_model="Wemo", device_model_id=device_model_wl, mac_address="DFADL918A0",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_lt4.save()

device_info_lt5 = DeviceMetadata(device_id="Lighting5", device_type="lighting", vendor_name="Wattstopper",
                                 device_model="Wattstopper", device_model_id=device_model_wsl, mac_address="LKADL918A0",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_lt5.save()


#Plugload Device Model Objects
device_model_wsp = DeviceModel.objects.get(device_model_id='3WSP')
device_model_wp = DeviceModel.objects.get(device_model_id='3WP')
device_model_dsp = DeviceModel.objects.get(device_model_id='3DSP')

#Plugload controllers
device_info_pl1 = DeviceMetadata(device_id="Plugload1", device_type="plugload", vendor_name="Belkin",
                                 device_model="Wemo SPlug", device_model_id=device_model_wsp, mac_address="DZASDH1310",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_pl1.save()

device_info_pl2 = DeviceMetadata(device_id="Plugload2", device_type="plugload", vendor_name="Wattstopper",
                                 device_model="Wastt Splug", device_model_id=device_model_wp, mac_address="IKHJL918A0",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_pl2.save()

device_info_pl3 = DeviceMetadata(device_id="Plugload3", device_type="plugload", vendor_name="Digi",
                                 device_model="Digi SPlug", device_model_id=device_model_dsp, mac_address="THADL918A0",
                                 min_range=20, max_range=95, identifiable=True, communication="Wifi",
                                 date_added=datetime.datetime.now(), bemoss=True)
device_info_pl3.save()


print "Devices added to device_info table"
#-----------------------------------------------------------------------------------------------------------------------

#Adding thermostat status to thermostat tables.
thermostat1 = Thermostat(thermostat_id=device_info_th1, temperature=70, thermostat_mode="HEAT", fan_mode="AUTO",
                         heat_setpoint=75, cool_setpoint=65.5, thermostat_state="HEAT", fan_state="AUTO",
                         ip_address='34.23.12.76', zone_id=zone_999.zone_id, nickname="Thermostat1", network_status='ONLINE',
                         last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
thermostat1.save()

thermostat2 = Thermostat(thermostat_id=device_info_th2, temperature=70, thermostat_mode="HEAT", fan_mode="AUTO",
                         heat_setpoint=75, cool_setpoint=65.5, thermostat_state="HEAT", fan_state="AUTO",
                         ip_address='34.73.12.76', zone_id=zone_999.zone_id, nickname="Thermostat2", network_status='ONLINE',
                         last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
thermostat2.save()

print "Thermostats added to thermostat table"
#-----------------------------------------------------------------------------------------------------------------------

#Adding Lighting Controllers
lighting1 = Lighting(lighting_id=device_info_lt1, status='ON', brightness=34, color=(45,23,56), multiple_on_off='101',
                     ip_address='34.54.23.64', nickname="Lighting1", zone_id=zone_999.zone_id, network_status='ONLINE',
                     last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
lighting1.save()

lighting2 = Lighting(lighting_id=device_info_lt2, status='ON', brightness=94, color=(45,29,56), multiple_on_off='111',
                     ip_address='76.54.73.64', nickname="Lighting2", zone_id=zone_999.zone_id, network_status='ONLINE',
                     last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
lighting2.save()

lighting3 = Lighting(lighting_id=device_info_lt3, status='ON', brightness=54, color=(45,23,56), multiple_on_off='101',
                     ip_address='34.54.233.64', nickname="Lighting3", zone_id=zone_999.zone_id, network_status='ONLINE',
                     last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
lighting3.save()

lighting4 = Lighting(lighting_id=device_info_lt4, status='ON', brightness=84, color=(85,29,56), multiple_on_off='111',
                     ip_address='76.54.71.64', nickname="Lighting4", zone_id=zone_999.zone_id, network_status='ONLINE',
                     last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
lighting4.save()

print "Lighting controllers added to Lighting table"
#-----------------------------------------------------------------------------------------------------------------------

#Adding Plugload Controllers
plugload1 = Plugload(plugload_id=device_info_pl1, status='ON', power=3, energy=5, ip_address='34.98.23.64',
                     nickname="Plugload1", zone_id=zone_999.zone_id, network_status='ONLINE',
                     last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
plugload1.save()

plugload2 = Plugload(plugload_id=device_info_pl2, status='ON', power=3, energy=5, ip_address='34.89.23.64',
                     nickname="Plugload2", zone_id=zone_999.zone_id, network_status='ONLINE',
                     last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
plugload2.save()

plugload3 = Plugload(plugload_id=device_info_pl3, status='ON', power=3, energy=5, ip_address='9.89.23.64',
                     nickname="Plugload3", zone_id=zone_999.zone_id, network_status='ONLINE',
                     last_scanned_time=datetime.datetime.now(), last_offline_time=datetime.datetime.now())
plugload3.save()

print "Plugload controllers added to plugload table"
#-----------------------------------------------------------------------------------------------------------------------

#Network Status table.
nw1 = NetworkStatus(node_name="Beaglebone", node_type="EmdSys", node_model="Black", node_status="ONLINE", building_name="bemoss",
                    associated_zone=zone_999, ip_address='12.65.34.97', mac_address='234adjkhf', date_added=datetime.datetime.now(), communication="MQTCP")
nw1.save()

nw2 = NetworkStatus(node_name="Pandaboard", node_type="EmdSys", node_model="Bigg",  mac_address='234adjkhf',node_status="ONLINE", building_name="bemoss",
                    associated_zone=zone_999, ip_address='12.65.34.77', date_added=datetime.datetime.now(), communication="MQTCP")
nw2.save()

nw3 = NetworkStatus(node_name="BananaPi", node_type="EmdSys", node_model="China",  mac_address='234adjkhf',node_status="ONLINE", building_name="bemoss",
                    associated_zone=zone_999, ip_address='12.12.34.87', date_added=datetime.datetime.now(), communication="MQTCP")
nw3.save()

