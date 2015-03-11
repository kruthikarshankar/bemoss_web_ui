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

import sys
import logging
import os

sys.path.append(os.getcwd())

from volttron.lite.agent import utils, matching
from volttron.lite.agent import BaseAgent, PublishMixin
from ZMQHelper import zmq_topics
from _utils import page_load_helper


utils.setup_logging()
_log = logging.getLogger(__name__)


class IEBSubscriber(PublishMixin, BaseAgent):
    
    def __init__(self, config_path, **kwargs):
        super(IEBSubscriber, self).__init__(**kwargs)
        self.config = utils.load_config(config_path)

    def setup(self):
        self._agent_id = self.config['agentid']
        # Always call the base class setup()
        super(IEBSubscriber, self).setup()
        print "IEB SUbscrbier"

    #Thermostat device_status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/thermostat/([0-9a-zA-Z]+)/device_status/response')
    def on_match_device_status_update(self, topic, headers, message, match):
        device_info = topic.split('/')
        device_id = device_info[6]
        device_type = device_info[5]
        page_load_helper.page_load(device_id, device_type, message[0])
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = topic.split('/')
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        self.publish(str(topic_to_tcp), headers, str(message))

    #Thermostat update status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/thermostat/([0-9a-zA-Z]+)/update/response')
    def on_match_status_update(self, topic, headers, message, match):
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = topic.split('/')
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        self.publish(str(topic_to_tcp), headers, str(message))
        if len(str(message)) != 0:
            print(" Thermostat update status is "+str(message).strip('[]').upper())

    #Scheduler App - UI Response Handler
    @matching.match_regex('/app/ui/thermostat_scheduler/([0-9a-zA-Z]+)/update/response')
    def on_match_device_scheduleth_response(self, topic, headers, message, match):
        device_id = topic.split('/')
        device_id = device_id[4]
        zmq_topics.set_schedule_update_status(device_id, message)


    @matching.match_regex('/app/ui/plugload_scheduler/([0-9a-zA-Z]+)/update/response')
    def on_match_device_schedulepl_response(self, topic, headers, message, match):
        device_id = topic.split('/')
        device_id = device_id[4]
        zmq_topics.set_schedule_update_status(device_id, message)


    @matching.match_regex('/app/ui/lighting_scheduler/([0-9a-zA-Z]+)/update/response')
    def on_match_device_schedulelt_response(self, topic, headers, message, match):
        device_id = topic.split('/')
        device_id = device_id[4]
        zmq_topics.set_schedule_update_status(device_id, message)


    #Lighting device_status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/lighting/([0-9a-zA-Z]+)/device_status/response')
    def on_match_hue_page_load(self, topic, headers, message, match):
        device_info = topic.split('/')
        device_id = device_info[6]
        device_type = device_info[5]
        page_load_helper.page_load(device_id, device_type, message[0])
        if message:
            print 'success, thermostat updated'+str(message).strip('[]')
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = device_info
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        self.publish(str(topic_to_tcp), headers, str(message))

    #Lighting update status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/lighting/([0-9a-zA-Z]+)/update/response')
    def on_match_hue_device_update_status(self, topic, headers, message, match):
        if message:
            print 'success, thermostat updated'+str(message).strip('[]')
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = topic.split('/')
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        self.publish(str(topic_to_tcp), headers, str(message))

    #Plugload update status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/plugload/([0-9a-zA-Z]+)/update/response')
    def on_match_status_update_plugload(self, topic, headers, message, match):
        if message:
            print 'success, thermostat updated'+str(message).strip('[]')
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = topic.split('/')
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        self.publish(str(topic_to_tcp), headers, str(message))

    #Plugload device_status response from agent --  handler
    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/plugload/([0-9a-zA-Z]+)/device_status/response')
    def on_match_device_status_update_plugload(self, topic, headers, message, match):
        device_info = topic.split('/')
        device_id = device_info[6]
        device_type = device_info[5]
        page_load_helper.page_load(device_id, device_type, message[0])
        if message:
            print 'success, thermostat updated'+str(message).strip('[]')
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))
        topic = device_info
        topic_to_tcp = '/ui/web/'+topic[5]+'/'+topic[4]+'/'+topic[6]+'/'+topic[7]+'/'+topic[8]
        self.publish(str(topic_to_tcp), headers, str(message))

    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/thermostat/([0-9a-zA-Z]+)/identify/response')
    def on_match_device_identify_thermostat(self, topic, headers, message, match):
        device_id = topic.split('/')
        device_id = device_id[6]
        update_topic = "identify_device_status_thermostat"
        zmq_topics.identify_device_update(device_id, message, update_topic)
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))

    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/lighting/([0-9a-zA-Z]+)/identify/response')
    def on_match_device_identify_lighting(self, topic, headers, message, match):
        device_id = topic.split('/')
        device_id = device_id[6]
        update_topic = "identify_device_status_lighting"
        zmq_topics.identify_device_update(device_id, message, update_topic)
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))

    @matching.match_regex('/agent/ui/bemoss/([0-9]{3})/plugload/([0-9a-zA-Z]+)/identify/response')
    def on_match_device_identify_plugload(self, topic, headers, message, match):
        device_id = topic.split('/')
        device_id = device_id[6]
        update_topic = "identify_device_status_plugload"
        zmq_topics.identify_device_update(device_id, message, update_topic)
        _log.debug("Topic: {topic}, Headers: {headers}, "
                         "Message: {message}".format(
                         topic=topic, headers=headers, message=message))


def main(argv=sys.argv):
    try:
        utils.default_main(IEBSubscriber,
                           description='IEBSubscriber',
                           argv=argv)
    except Exception as e:
        _log.exception('unhandled exception', e)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass

