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



import json
from zmq.eventloop import ioloop

ioloop.install()
from zmq.eventloop.zmqstream import ZMQStream
import zmq

from tornado import websocket
from tornado import web
from tornado import ioloop
from helper import messages as _
from tornado.options import options, define
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import os


ctx = zmq.Context()


define('port', type=int, default=8080)
define('host', type=str, default="localhost")


def main():
    #settings = {
        #"static_path": os.path.join(os.path.dirname(__file__), "static"),
        #}
    #parse_command_line()
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_tornado'
    wsgi_app = tornado.wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())
    tornado_app = tornado.web.Application(
        [
            (r"/socket_thermostat", ThermostatEventHandler),
            (r"/socket_plugload", PlugLoadEventHandler),
            (r"/socket_lighting", LightingEventHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': os.path.expanduser("~") +
                                                                      "/workspace/bemoss_web_ui/static"}),
            ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ])
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)
    print _.SERVER_STARTUP.format(options.host, options.port)
    tornado.ioloop.IOLoop.instance().start()


class WebHandler(web.RequestHandler):
    def get(self):
        pass
        #self.render("/home/kruthika/workspace/bemoss_web_ui/template.html", title="My new title")


class MainHandler(websocket.WebSocketHandler):
    _first = True

    @property
    def ref(self):
        return id(self)

    def initialize(self):
        print 'Initializing tornado websocket'
        self.push_socket = ctx.socket(zmq.PUSH)
        self.sub_socket = ctx.socket(zmq.SUB)

        self.push_socket.connect("ipc:///tmp/volttron-lite-agent-publish")
        self.sub_socket.connect("ipc:///tmp/volttron-lite-agent-subscribe")
        self.zmq_subscribe()

        self.zmq_stream = ZMQStream(self.sub_socket)
        self.zmq_stream.on_recv(self.zmq_msg_recv)

    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        self.write_message("WebSocket opened from server")

    def on_message(self, message):
        if self._first:
            msg = {'message': message, 'id':self.ref, 'action':'connect'}
            print 'in if part - tornado server'
            #print msg

            self._first = False

        else:
            msg = {'message': message, 'id':self.ref, 'action':'message'}
            print 'in else part - tornado server'
            print msg

        self.write_message(msg)
        #self.push_socket.send_pyobj(msg)

    def on_close(self):
        self.write_message("WebSocket closed")
        msg = {'message': '', 'id': id(self), 'action': 'close'}
        self.write_message(msg)
        #self.push_socket.send_pyobj(msg)
        #self.zmq_stream.close()
        #self.sub_socket.close()
        #self.push_socket.close()

    def zmq_msg_recv(self, data):
        #self.write_message(data)
        print data
        zmessage = {'topic': '', 'headers': {}, 'message': ''}
        for item in data:
            if '/ui/web' in item:
                zmessage['topic'] = item
            elif 'Date' in str(item):
                mesg = json.loads(item)
                zmessage['headers'] = mesg
            else:
                if '[' in item:
                    item = eval(item)
                    print type(item)
                    item = item[0]
                    if item[0] == '{':
                        item = json.loads(item)
                    zmessage['message'] = item
                else:
                    zmessage['message'] = item

        '''for zmessage in data:
            #zmessage = pickle.loads(zmessage)
            print type(zmessage)
            print zmessage
            # _id, _msg = zmessage['id'], zmessage['message']

            #if _id != self.ref:
                #continue'''

        self.write_message(zmessage)

    def zmq_subscribe(self):
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, "")


class ThermostatEventHandler(MainHandler):

    def zmq_subscribe(self):
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, '/ui/web/thermostat/')


class PlugLoadEventHandler(MainHandler):

    def zmq_subscribe(self):
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, '/ui/web/plugload/')


class LightingEventHandler(MainHandler):

    def zmq_subscribe(self):
        self.sub_socket.setsockopt(zmq.SUBSCRIBE, '/ui/web/lighting/')


application = web.Application([
    (r"/", WebHandler),
    (r"/socket_thermostat", ThermostatEventHandler),
    (r"/socket_plugload", PlugLoadEventHandler),
    (r"/socket_lighting", LightingEventHandler),
])


if __name__ == "__main__":
    tornado.options.parse_command_line()
    main()
    #application.listen(8081)
    #ioloop.IOLoop.instance().start()
