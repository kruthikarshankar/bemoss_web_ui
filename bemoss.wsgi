import os
import sys
sys.path = ['/home/kruthika/workspace']+sys.path
sys.path.insert(3, '/home/kruthika/workspace/bemoss_web_ui/volttron/')
sys.path.insert(2, '/home/kruthika/workspace/bemoss_web_ui/clock')
#print sys.path
os.environ['DJANGO_SETTINGS_MODULE']='bemoss_web_ui.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

