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


#Database models for alerts and notifications
from django.db import models
from django.contrib.auth.models import User


class DeviceType(models.Model):
    device_type = models.CharField(max_length=30) #system, thermostat, plugload, lighting

    class Meta:
        db_table = "device_type"

    def __unicode__(self):
        return str(self.as_json())

    def as_json(self):
        return dict(
            id=self.id,
            alarm_type=self.device_type.encode('utf-8').title())


class EventTrigger(models.Model):
    device_type = models.ForeignKey(DeviceType) #system, thermostat, plugload, lighting
    event_trigger_desc = models.CharField(max_length=50) #temperature exceeds, humidity exceeds, low battery etc.

    class Meta:
        db_table = "event_trigger"

    def __unicode__(self):
        return str(self.id)

    def as_json(self):
        device_type = DeviceType.as_json(self.device_type)
        return dict(
            id=self.id,
            alarm_type=device_type['alarm_type'].encode('utf-8'),
            alarm_desc=self.event_trigger_desc.encode('utf-8'))


class NotificationChannel(models.Model):
    notification_channel = models.CharField(max_length=50)

    class Meta:
        db_table = "notification_channel"

    def __str__(self):
        return self.notification_channel

    def __unicode__(self):
        return str(self.notification_channel)

    def as_json(self):
        return dict(
            id=self.id,
            notification_channel=self.notification_channel.encode('utf-8'))


class Priority(models.Model):
    priority_level = models.CharField(max_length=10)

    class Meta:
        db_table = "priority"

    def __unicode__(self):
        return str(self.as_json())

    def as_json(self):
        return dict(
            id=self.id,
            priority=self.priority_level.encode('utf-8').title())


class ActiveAlert(models.Model):
    device_type = models.ForeignKey(DeviceType)
    event_trigger = models.ForeignKey(EventTrigger)
    trigger_parameter = models.CharField(max_length=40)
    comparator = models.CharField(max_length=20)
    threshold = models.CharField(max_length=5)
    notification_channel = models.ManyToManyField(NotificationChannel, through="NotificationChannelAddress")
    priority = models.ForeignKey(Priority)
    user = models.ForeignKey(User)
    created_on = models.DateTimeField()

    class Meta:
        db_table = "active_alert"

    def __unicode__(self):
        return str(self.id)

    def as_json(self):
        alarm_type = DeviceType.as_json(self.device_type)
        alarm = EventTrigger.as_json(self.event_trigger)
        notification = self.notification_channel.all()
        #notification = NotificationType.as_json(self.notification_type)
        notify_address = [ob.as_json() for ob in NotificationChannelAddress.objects.filter(active_alert_id=self.id)]
        print notify_address
        user = User.objects.get(id=1)
        priority = Priority.as_json(self.priority)

        return dict(
            id=self.id,
            alarm=alarm,
            alarm_type=alarm_type,
            trigger_parameter=self.trigger_parameter.encode('utf-8').title(),
            comparator=self.comparator,
            value=self.threshold,
            notification=notification,
            notify_address=notify_address,
            priority=priority,
            created_on=self.created_on,
            created_by=user)


class NotificationChannelAddress(models.Model):
    notification_channel = models.ForeignKey(NotificationChannel)
    active_alert = models.ForeignKey(ActiveAlert)
    notify_address = models.CharField(max_length=50)

    def __unicode__(self):
        return str(self.notify_address)

    def as_json(self):
        return dict(
            channel=self.notification_channel.notification_channel,
            address=self.notify_address
        )


class Notification(models.Model):
    active_alert = models.ForeignKey(ActiveAlert)
    alert_notification_status = models.BooleanField() #TRUE OR FALSE - if notification was sent successfully then TRUE else FALSE
    dt_triggered = models.DateTimeField()

    class Meta:
        db_table = "notification"

    def __unicode__(self):
        return str(self.as_json())

    def as_json(self):
        ra = ActiveAlert.as_json(self.active_alert)

        return dict(
            id=self.id,
            reg_alert=ra,
            alert_status=self.alert_notification_status,
            active_dt=self.dt_triggered)