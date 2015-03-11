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


from django.contrib.auth.models import User
from admin.models import NetworkStatus

__author__ = 'kruthika'

from django import template
from thermostat.models import Thermostat
from lighting.models import Lighting
from smartplug.models import Plugload

register = template.Library()


@register.filter
def device_count(zone_id):
    th_count = Thermostat.objects.filter(network_status='ONLINE', zone_id=zone_id, thermostat_id__bemoss=True).count()
    pl_count = Plugload.objects.filter(network_status='ONLINE', zone_id=zone_id, plugload_id__bemoss=True).count()
    lt_count = Lighting.objects.filter(network_status='ONLINE', zone_id=zone_id, lighting_id__bemoss=True).count()
    lengthh = th_count + pl_count + lt_count
    return lengthh


@register.filter
def dev_emsys_count(zone_id):
    th_count = Thermostat.objects.filter(network_status='ONLINE', zone_id=zone_id, thermostat_id__bemoss=True).count()
    pl_count = Plugload.objects.filter(network_status='ONLINE', zone_id=zone_id, plugload_id__bemoss=True).count()
    lt_count = Lighting.objects.filter(network_status='ONLINE', zone_id=zone_id, lighting_id__bemoss=True).count()
    lengthh = th_count +  pl_count + lt_count
    return lengthh


@register.filter
def dev_emsys_ct_all(zone_id):
    '''
    th_count = Thermostat.objects.filter(network_status='ONLINE', thermostat_id__bemoss=True).count()
    pl_count = Plugload.objects.filter(network_status='ONLINE', plugload_id__bemoss=True).count()
    lt_count = Lighting.objects.filter(network_status='ONLINE', lighting_id__bemoss=True).count()
    lengthh = th_count + pl_count + lt_count
    '''
    lengthh = all_dev_ct(000) + embsys_count(000)
    return lengthh


@register.filter
def all_dev_ct(what):
    th_count = Thermostat.objects.filter(network_status='ONLINE', thermostat_id__bemoss=True).count()
    lt_count = Lighting.objects.filter(network_status='ONLINE', lighting_id__bemoss=True).count()
    pl_count = Plugload.objects.filter(network_status='ONLINE', plugload_id__bemoss=True).count()
    count = th_count + lt_count + pl_count
    return count

@register.filter
def embsys_count(zone_id):
    bemoss_lite = NetworkStatus.objects.filter(node_status='ONLINE').count()
    return bemoss_lite


@register.filter
def all_count(zone_id):
    th_count = Thermostat.objects.filter(network_status='ONLINE', zone_id=zone_id, thermostat_id__bemoss=True).count()
    lt_count = Lighting.objects.filter(network_status='ONLINE', zone_id=zone_id, lighting_id__bemoss=True).count()
    pl_count = Plugload.objects.filter(network_status='ONLINE', zone_id=zone_id, plugload_id__bemoss=True).count()
    count = th_count + lt_count + pl_count
    return count


@register.filter
def hvac_count(zone_id):
    th_count = Thermostat.objects.filter(network_status='ONLINE', zone_id=zone_id, thermostat_id__bemoss=True).count()
    count = th_count
    return count


@register.filter
def d_ct(_d_type):
    if _d_type == 'hvac':
        th_count = Thermostat.objects.filter(network_status='ONLINE', zone_id=999, thermostat_id__bemoss=True).count()
        count = th_count
        return count
    elif _d_type == 'light':
        lt_count = Lighting.objects.filter(network_status='ONLINE', zone_id=999, lighting_id__bemoss=True).count()
        return lt_count
    elif _d_type == 'plug':
        pl_count = Plugload.objects.filter(network_status='ONLINE',zone_id=999, plugload_id__bemoss=True).count()
        return pl_count


@register.filter
def md_ct(_d_type):
    if _d_type == 'hvac':
        th_count = Thermostat.objects.filter(network_status='ONLINE', thermostat_id__bemoss=True).count()
        count = th_count
        return count
    elif _d_type == 'light':
        lt_count = Lighting.objects.filter(network_status='ONLINE', lighting_id__bemoss=True).count()
        return lt_count
    elif _d_type == 'plug':
        pl_count = Plugload.objects.filter(network_status='ONLINE', plugload_id__bemoss=True).count()
        return pl_count

@register.filter
def lt_count(zone_id):
    lt_count = Lighting.objects.filter(network_status='ONLINE', zone_id=zone_id, lighting_id__bemoss=True).count()
    return lt_count


@register.filter
def pl_count(zone_id):
    pl_count = Plugload.objects.filter(network_status='ONLINE', zone_id=zone_id, plugload_id__bemoss=True).count()
    return pl_count


@register.filter
def new_users(users):
    nusers = User.objects.filter(is_active=False).count()
    return nusers