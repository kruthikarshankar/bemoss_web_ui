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

setup_environ(settings)

from alerts.models import Priority, NotificationChannel, EventTrigger, DeviceType
from dashboard.models import DeviceModel, Building_Zone
from django.contrib.auth.models import Group, Permission, User
from dashboard.models import GlobalSetting
from schedule.models import Holiday
from accounts.models import UserProfile
import datetime

DEVICE_TYPE_CHOICES = (
    ('1TH', 'thermostat'),
    ('1NST', 'Nest'),
    ('2DB', 'dimmable ballast'),
    ('2HUE', 'philips hue'),
    ('2SDB', 'step dim ballast'),
    ('2WL', 'wemo light switch'),
    ('2WSL', 'wattstopper lighting'),
    ('3WSP', 'wemo smart plug'),
    ('3MOD', 'modlet smart plug'),
    ('3WP', 'wattstopper plugload'),
    ('3VTH', 'vt load controller'),
    ('3DSP', 'digi smart plug'))

thermostat = DeviceModel(device_model_id='1TH', device_model_name='Thermostat')
thermostat.save()

nest = DeviceModel(device_model_id='1NST', device_model_name='Nest')
nest.save()

dimmable_ballast = DeviceModel(device_model_id='2DB', device_model_name='Dimmable Ballast')
dimmable_ballast.save()

step_dim_ballast = DeviceModel(device_model_id='2SDB', device_model_name='Step Dim Ballast')
step_dim_ballast.save()

hue = DeviceModel(device_model_id='2HUE', device_model_name='Philips Hue')
hue.save()

wemo_light_switch = DeviceModel(device_model_id='2WL', device_model_name='Wemo Light Switch')
wemo_light_switch.save()

wattstopper_lighting = DeviceModel(device_model_id='2WSL', device_model_name='Wattstopper Lighting Product')
wattstopper_lighting.save()

wemo_smart_plug = DeviceModel(device_model_id='3WSP', device_model_name='Wemo Smart Plug')
wemo_smart_plug.save()

modlet_smart_plug = DeviceModel(device_model_id='3MOD', device_model_name='Modlet Smart Plug')
modlet_smart_plug.save()

wattstopper_plugload = DeviceModel(device_model_id='3WP', device_model_name='Wattstopper Plugload')
wattstopper_plugload.save()

vt_load_controller = DeviceModel(device_model_id='3VTH', device_model_name='VT Load Controller')
vt_load_controller.save()

digi_smart_plug = DeviceModel(device_model_id='3DSP', device_model_name='Digi Smart Plug')
digi_smart_plug.save()

print "device_model table updated with device model information."

zone_999 = Building_Zone(zone_id=999, zone_nickname="BEMOSS Core")
zone_999.save()
#Adding global settings

gz999 = GlobalSetting(id=999,heat_setpoint=70, cool_setpoint=72, illuminance=67, zone_id=999)
gz999.save()


#User groups

tenant = Group(id=1, name="Tenant")
tenant.save()

zonemgr = Group(id=2, name="Zone Manager")
zonemgr.save()

admin = Group(id=3, name="Admin")
admin.save()

#Add admin to user profile
admin = User.objects.get(username='admin')
admin.first_name = "Admin"
admin.save()
#user_id = admin.id
#uprof = UserProfile(user_id=1)
#uprof.save()
adminprof = admin.get_profile()
adminprof.group = Group.objects.get(name='Admin')
adminprof.save()

#Holidays

newyear = Holiday(holiday_id=1, date=datetime.datetime(2014,01,01),description="New Year")
newyear.save()

mlk = Holiday(holiday_id=2, date=datetime.datetime(2014,01,20),description="MLK Holiday")
mlk.save()

#Alerts and Notifications

#Priority
low_p = Priority(id=1, priority_level='Low')
low_p.save()

med_p = Priority(id=2, priority_level='Warning')
med_p.save()

high_p = Priority(id=3, priority_level='Critical')
high_p.save()

#NotificationChannel
emailN = NotificationChannel(id=1, notification_channel='Email')
emailN.save()

textN = NotificationChannel(id=2, notification_channel='Text')
textN.save()

#bN = NotificationChannel(id=3, notification_channel='BemossNotification')
#bN.save()

#Device Type
dt1 = DeviceType(id=1, device_type='Thermostat')
dt1.save()

dt2 = DeviceType(id=2, device_type='Plugload')
dt2.save()

dt3 = DeviceType(id=3, device_type='Lighting')
dt3.save()

dt8 = DeviceType(id=8, device_type='Custom')
dt8.save()

dt9 = DeviceType(id=9, device_type='Platform')
dt9.save()

#Event Trigger
et1 = EventTrigger(id=1, device_type_id=9, event_trigger_desc="Any Load Controller Offline")
et1.save()

et2 = EventTrigger(id=2, device_type_id=9, event_trigger_desc="Any BEMOSS Node Offline")
et2.save()

et3 = EventTrigger(id=1, device_type_id=1, event_trigger_desc="Unauthorized Changes To Thermostat Mode/SetPoint")
et3.save()

et4 = EventTrigger(id=4, device_type_id=1, event_trigger_desc="Custom")
et4.save()




