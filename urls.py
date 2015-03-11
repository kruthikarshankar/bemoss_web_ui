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

from django.conf.urls.defaults import patterns, include, url
from django.utils.functional import curry
from django.views.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bemoss_web_ui.views.home', name='home'),
    # url(r'^bemoss_web_ui/', include('bemoss_web_ui.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #register user
    (r'^register/$', 'accounts.views.register'),
    #login
    (r'^login/$', 'accounts.views.login_user'),
    #user manager
    (r'^usr_mngr/$', 'accounts.views.user_manager'),
    #approve users
    (r'^approve_users/$', 'accounts.views.approve_users'),
    #modify user permissions
    (r'^modify_user_permissions/$', 'accounts.views.modify_user_permissions'),
    #delete user
    (r'^delete_user/$', 'accounts.views.delete_user'),
    #redirect to login page or home page
    (r'^$', 'dashboard.views.bemoss_home'),
    #logout
    #(r'^logout/$', 'accounts.views.logout_user'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login'}),
    #url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login'}, name='logout'),
    #(r'^logout_bemoss/$', 'accounts.views.logout_user'),
    #wifithermostat3m50
    #(r'^wifi3m50/$', 'wifithermostat_3m50.views.wifithermo3m50'),
    (r'^tstat/(?P<mac>[a-zA-Z0-9]+)/$', 'thermostat.views.thermostat'),
    #wifithermostat3m50-submitdata
    #(r'^submitdata/$', 'wifithermostat_3m50.views.submitvalues'),
    #(r'^submitdata3m50/$', 'wifithermostat_3m50.views.submitvalues'),
    (r'^submitdata3m50/$', 'thermostat.views.submit_values'),
    #wifithermostatct30
    #(r'^wifict30/$', 'wifithermostat_ct30.views.wifithermoct30'),
    #plugload
    (r'^plug/(?P<mac>[a-zA-Z0-9]+)/$', 'smartplug.views.smartplug'),
    #philips hue
    (r'^hue/$', 'lighting.views.philipshue'),
    #lighting controller
    #(r'^light/$', 'lighting.views.lightingg'),
    (r'^light/(?P<mac>[a-zA-Z0-9]+)/$', 'lighting.views.lighting'),
    #lighting controller update device 
    (r'^update_light/$', 'lighting.views.update_device_light'),
    #lighting controller update device 
    (r'^update_light_device_status/$', 'lighting.views.update_device_agent_status'),
    #get light status realtime
    (r'^lt_stat/$', 'lighting.views.get_lighting_current_status'),
    #set schedule form
    #(r'^schedule/$', 'wifithermostat_3m50.views.setschedule'),
    (r'^schedule/$', 'schedule.views.thermostat_schedule'),
    #thermostat_scheduling
    (r'^th_schedule/(?P<mac>[a-zA-Z0-9]+)/$', 'schedule.views.thermostat_schedule'),
    #lighting_scheduling
    (r'^lt_schedule/(?P<mac>[a-zA-Z0-9]+)/$', 'schedule.views.lighting_schedule'),
    #plugload_scheduling
    (r'^pl_schedule/(?P<mac>[a-zA-Z0-9]+)/$', 'schedule.views.plugload_schedule'),
    #update thermostat schedule
    #(r'^submit_schedule/$', 'wifithermostat_3m50.views.update_thermostat_schedule'),
    (r'^submit_schedule/$', 'schedule.views.update_thermostat_schedule'),
    #update schedule 
    #(r'^update_schedule/$', 'wifithermostat_3m50.views.update_schedule_status_to_browser'),
    (r'^update_schedule/$', 'schedule.views.update_schedule_status_to_browser'),
    #periodic update of thermostat
    #(r'^thstat/$', 'wifithermostat_3m50.views.get_thermostat_current_status'),
    (r'^thstat/$', 'thermostat.views.get_thermostat_current_status'),
    #wunderground
    (r'^weather/$', 'thermostat.views.weather'),
    #device_update
    #(r'^update_3m50/$', 'wifithermostat_3m50.views.deviceupdatemessagetobrowser'),
    (r'^update_3m50/$', 'thermostat.views.deviceupdatemessagetobrowser'),
    #dashboard
    (r'^dashboard/$', 'dashboard.views.dashboard'),
    #dashboard
    (r'^identify_device/$', 'dashboard.views.identify_device'),
    #identify_device_status
    (r'^identify_status/$', 'dashboard.views.identify_status'),
    #dashboard - add new zone
    (r'^add_new_zone/$', 'dashboard.views.add_new_zone'),
    #dashboard - add new zone
    (r'^save_view_edit_changes_dashboard/$', 'dashboard.views.save_changes_modal'),
    #dashboard - change nickname
    (r'^save_zone_nickname_change/$', 'dashboard.views.save_zone_nickname_changes'),
    #smap plot - thermostat
    #(r'^historicdata/$', 'wifithermostat_3m50.views.smap_plot_thermostat'),
    (r'^th_statistics/(?P<mac>[a-zA-Z0-9]+)$', 'tsvisual.views.smap_plot_thermostat'),
    # smap plot - lighting
    #(r'^historicdata/$', 'wifithermostat_3m50.views.smap_plot_thermostat'),
    (r'^lt_statistics/(?P<mac>[a-zA-Z0-9]+)$', 'tsvisual.views.smap_plot_lighting'),
    # smap plot - thermostat
    #(r'^historicdata/$', 'wifithermostat_3m50.views.smap_plot_thermostat'),
    (r'^pl_statistics/(?P<mac>[a-zA-Z0-9]+)$', 'tsvisual.views.smap_plot_plugload'),
    #wattstopper plugload smap plot
    (r'^wtpl_statistics/(?P<mac>[a-zA-Z0-9]+)$', 'tsvisual.views.smap_plot_wattstopper_plugload'),
    #auto update smap
    (r'^th_smap_update/$', 'tsvisual.views.auto_update_smap_thermostat'),
    (r'^lt_smap_update/$', 'tsvisual.views.auto_update_smap_lighting'),
    (r'^pl_smap_update/$', 'tsvisual.views.auto_update_smap_plugload'),
    (r'^wtpl_smap_update/$', 'tsvisual.views.auto_update_smap_wattstopper_plugload'),
    #update_plugload
    (r'^update_plugload/$', 'smartplug.views.submit_changes'),
    #update_plugload_status
    (r'^update_plugload_status/$', 'smartplug.views.update_device_agent_status'),
    #get plugload current status
    (r'^plugload_stat/$', 'smartplug.views.get_plugload_current_status'),
    #alerts and notifications home
    (r'^alerts/$', 'alerts.views.alerts'),
    #create new alert
    (r'^create_alert/$', 'alerts.views.create_alert'),
    #delete alert
    (r'^del_alert/$', 'alerts.views.delete_alert'),
    #register new user - registration page
    (r'^register_new_user/$', 'accounts.views.register_new_user'),
    #submit_active_schedule
    (r'^submit_active_schedule/$', 'schedule.views.activate_schedule'),
    (r'^dstat/$', 'admin.views.device_status'),
    #network status
    (r'^nwstat/$', 'admin.views.network_status'),
    #notifications
    (r'^ntfns/$', 'alerts.views.notifications'),
    #discovery
    (r'^discover/$', 'dashboard.views.discover'),
    (r'^ndiscover/$', 'dashboard.views.discover_nodes'),
    #change_zone_thermostat
    (r'^change_zones_thermostats/$', 'dashboard.views.change_zones_thermostats'),
    #change_zone_plugload
    (r'^change_zones_plugloads/$', 'dashboard.views.change_zones_plugloads'),
    #change_zone_lighting
    (r'^change_zones_lighting/$', 'dashboard.views.change_zones_lighting_loads'),
    #modify thermostats
    (r'^modify_thermostats/$', 'dashboard.views.modify_thermostats'),
    #modify plugloads
    (r'^modify_plugloads/$', 'dashboard.views.modify_plugloads'),
    #modify lighting
    (r'^modify_lighting_loads/$', 'dashboard.views.modify_lighting_loads'),
    #change_zones_lite
    (r'^change_zones_lite/$', 'dashboard.views.change_zones_lite'),
    #home page (new dashboard)
    (r'^home/$', 'dashboard.views.bemoss_home'),
    #change global settings
    (r'^change_global_settings/$', 'dashboard.views.change_global_settings'),
    #dashboard_devices_in_zone
    (r'^devices/(?P<zone_dev>[a-zA-Z0-9_]+)$', 'dashboard.views.zone_device_listing'),
    (r'^all_devices/(?P<zone_dev>[a-zA-Z0-9_]+)$', 'dashboard.views.zone_device_all_listing'),
    #bemoss_settings
    (r'^bemoss_settings/', 'admin.views.bemoss_settings'),
    # delete holiday
    (r'^delete_holiday/', 'admin.views.delete_holiday'),
    # add holiday
    (r'^add_holiday/', 'admin.views.add_holiday'),
    #bemoss location (weather requirement)
    (r'^b_location_modify/', 'admin.views.update_bemoss_location'),
    #export to excel
    (r'^export_excel/', 'reports.views.export_to_spreadsheet'),
    #export thermostat data
    (r'^export_thd/', 'reports.views.export_thermostat_to_spreadsheet'),
    (r'^export_ltd/', 'reports.views.export_lighting_to_spreadsheet'),
    (r'^export_pld/', 'reports.views.export_plugload_to_spreadsheet'),
    (r'^export_alld/', 'reports.views.export_all_device_information'),
    # /report_thschd/-{{ device_id }}
    (r'^report_thschd/(?P<mac>[a-zA-Z0-9]+)$', 'reports.views.export_schedule_thermostats_daily'),
    (r'^report_thschh/(?P<mac>[a-zA-Z0-9]+)$', 'reports.views.export_schedule_thermostats_holiday'),
    (r'^report_ltschd/(?P<mac>[a-zA-Z0-9]+)$', 'reports.views.export_schedule_lighting_daily'),
    (r'^report_ltschh/(?P<mac>[a-zA-Z0-9]+)$', 'reports.views.export_schedule_lighting_holiday'),
    (r'^report_plschd/(?P<mac>[a-zA-Z0-9]+)$', 'reports.views.export_schedule_plugload_daily'),
    (r'^report_plschh/(?P<mac>[a-zA-Z0-9]+)$', 'reports.views.export_schedule_plugload_holiday'),
    (r'^export/(?P<mac>[a-zA-Z0-9]+)$', 'reports.views.export_smap_data_to_spreadsheet'),
)

#handler404 = 'error.views.error404'    
#handler500 = 'error.views.error500'
handler500 = 'error.views.handler500'
handler404 = 'error.views.handler404'

