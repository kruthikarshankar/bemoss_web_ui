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
from django.contrib.auth.models import User, Group
from dashboard.models import Building_Zone
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserFullName(User):
    class Meta:
        proxy = True

    def __unicode__(self):
        return self.get_full_name()


class UserId(User):
    class Meta:
        proxy = True

    def __unicode__(self):
        return self.id

'''
Carrier	Email to SMS Gateway
*****************************************************************


Alltel	                        [10-digit phone number]@message.alltel.com
                Example: 1234567890@message.alltel.com

AT&T (formerly Cingular)        [10-digit phone number]@txt.att.net
                                [10-digit phone number]@mms.att.net (MMS)
                                [10-digit phone number]@cingularme.com
                Example: 1234567890@txt.att.net

Boost Mobile	                [10-digit phone number]@myboostmobile.com
                Example: 1234567890@myboostmobile.com

Nextel (now Sprint Nextel)	[10-digit telephone number]@messaging.nextel.com
                Example: 1234567890@messaging.nextel.com

Sprint PCS (now Sprint Nextel)	[10-digit phone number]@messaging.sprintpcs.com
                                [10-digit phone number]@pm.sprint.com (MMS)
                Example: 1234567890@messaging.sprintpcs.com

T-Mobile	                [10-digit phone number]@tmomail.net
                Example: 1234567890@tmomail.net

US Cellular	                [10-digit phone number]email.uscc.net (SMS)
                                [10-digit phone number]@mms.uscc.net (MMS)
                Example: 1234567890@email.uscc.net

Verizon	                        [10-digit phone number]@vtext.com
                                [10-digit phone number]@vzwpix.com (MMS)
                Example: 1234567890@vtext.com

Virgin Mobile USA	        [10-digit phone number]@vmobl.com
                Example: 1234567890@vmobl.com

*****************************************************************
'''

'''
class PhoneCarrier(models.Model):

    CARRIER_CHOICES = (
        ('alt', 'AllTel'),
        ('att', 'AT&T'),
        ('bst', 'Boost'),
        ('nxtl', 'NexTel'),
        ('spt', 'Sprint'),
        ('tmbl', 'T-Mobile'),
        ('usc', 'US Cellular'),
        ('vrzn', 'Verizon'),
        ('vmu', 'Virgin Mobile USA'))

    id = models.CharField(primary_key=True, max_length=4) #, choices=CARRIER_CHOICES)
    carrier = models.CharField(max_length=30)
    address_text = models.CharField(max_length=40)

    def __unicode__(self):
        return self.id

    def as_json(self):
        return dict(
            id=self.id.encode('utf-8'),
            carrier=self.carrier.encode('utf-8'),
            address=self.address_text.encode('utf-8'))
'''


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    contact_phone = models.BigIntegerField(max_length=10, null=True, blank=True)
    group = models.ForeignKey(Group, null=True, blank=True)
    zone = models.ForeignKey(Building_Zone, null=True, blank=True)

    def __unicode__(self):
        return self.user_id

    def as_json(self):
        return dict(
            id=self.user_id,
            user=self.user,
            contact_phone=self.contact_phone,
            group=self.group,
            zone=self.zone)


class UserRegistrationRequests(models.Model):
    user = models.ForeignKey(User, unique=True)
    request_date = models.DateTimeField()

    class Meta:
        db_table = "user_registration_request"

    def __unicode__(self):
        return self.id

    def as_json(self):
        return dict(
            id=self.id,
            user=self.user,
            request_date=self.request_date
        )


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)