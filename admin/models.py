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


from django.db import models

#Table that stores information about the BEMOSS embedded system devices
from dashboard.models import Building_Zone


class NetworkStatus(models.Model):
    node_id = models.AutoField(primary_key=True)
    node_name = models.CharField(max_length=20)
    node_type = models.CharField(max_length=10)
    node_model = models.CharField(max_length=10)
    node_status = models.CharField(max_length=10)
    building_name = models.CharField(max_length=20)
    ip_address = models.IPAddressField()
    mac_address = models.CharField(max_length=50, null=True, blank=True)
    associated_zone = models.ForeignKey(Building_Zone, null=True, blank=True, db_column="associated_zone")
    date_added = models.DateTimeField()
    communication = models.CharField(max_length=10)
    last_scanned_time = models.DateTimeField(null=True, blank=True)
    last_offline_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "node_info"

    def __unicode__(self):
        return self.node_id

    def network_status(self):
        return dict(
            device_id=self.node_id,
            device_name=self.node_name.encode('utf-8').title(),
            device_type=self.node_type.encode('utf-8').title(),
            device_model=self.node_model.encode('utf-8').title(),
            device_status=self.node_status.encode('utf-8').title(),
            associated_zone=self.associated_zone,
            date_added=self.date_added,
            ip_address=self.ip_address,
            last_scanned=self.last_scanned_time,
            last_offline=self.last_offline_time)

    def data_dashboard(self):
        zone_req = Building_Zone.as_json(self.associated_zone)
        return dict(
            device_id=self.node_id,
            device_name=self.node_name.encode('utf-8').title(),
            device_model=self.node_model.encode('utf-8').title(),
            device_type=self.node_type.encode('utf-8').title(),
            mac_address=self.mac_address.encode('utf-8'),
            device_status=self.node_status.encode('utf-8').title(),
            associated_zone=zone_req,
            ip_address=self.ip_address,
            date_added=self.date_added,
            last_scanned=self.last_scanned_time,
            last_offline=self.last_offline_time)
