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

# Create your views here.
import datetime
import json
import os
import urllib2
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import tablib
from dashboard.models import DeviceMetadata
from lighting.models import Lighting
import settings
from smartplug.models import Plugload
from thermostat.models import Thermostat
from os.path import expanduser
#from gi.repository import GLib

#downloads_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)
from tsvisual.views import get_uuid_for_data_point

downloads_dir = expanduser('~') + '/Downloads'


@login_required(login_url='/login/')
def export_to_spreadsheet(request):
    headers = ('Device Type', 'Device Status')
    data = []
    data = tablib.Dataset(*data, headers=headers)
    #nw = NetworkStatus.objects.all()
    nw = [[1406349525000.0, 74.0], [1406349581000.0, 74.0], [1406349641000.0, 74.0], [1406349701000.0, 74.0], [1406349762000.0, 74.0], [1406349822000.0, 74.0], [1406349882000.0, 74.0], [1406349942000.0, 74.0], [1406350002000.0, 74.0], [1406350065000.0, 74.0], [1406350122000.0, 74.0], [1406350181000.0, 74.0], [1406350240000.0, 74.0], [1406350302000.0, 74.5], [1406350363000.0, 74.5], [1406350422000.0, 74.5], [1406350481000.0, 74.5], [1406350543000.0, 74.5], [1406350602000.0, 74.5], [1406350662000.0, 74.5], [1406350721000.0, 74.5], [1406350782000.0, 74.5], [1406350843000.0, 74.5], [1406350902000.0, 74.5], [1406350961000.0, 74.5], [1406351024000.0, 74.5], [1406351083000.0, 74.5], [1406351141000.0, 74.5], [1406351202000.0, 74.5], [1406351263000.0, 74.5], [1406351321000.0, 74.5], [1406351384000.0, 74.5], [1406351441000.0, 74.5], [1406351502000.0, 76.0], [1406351561000.0, 76.0], [1406351621000.0, 76.0], [1406351682000.0, 76.0], [1406351742000.0, 76.0], [1406351802000.0, 76.0], [1406351862000.0, 76.0], [1406351922000.0, 76.0], [1406351982000.0, 76.0], [1406352041000.0, 76.0], [1406352102000.0, 76.0], [1406352161000.0, 76.0], [1406352222000.0, 76.0], [1406352282000.0, 76.0], [1406352342000.0, 76.0], [1406352402000.0, 76.0], [1406352461000.0, 76.0], [1406352522000.0, 76.0], [1406352582000.0, 76.0], [1406352642000.0, 76.0], [1406352702000.0, 76.0], [1406352761000.0, 76.0], [1406352822000.0, 76.0], [1406352882000.0, 76.0], [1406352942000.0, 76.0], [1406353001000.0, 76.0], [1406353063000.0, 76.0], [1406353122000.0, 76.0], [1406353182000.0, 76.0], [1406353241000.0, 76.0], [1406353302000.0, 76.0], [1406353362000.0, 76.0], [1406353422000.0, 76.0], [1406353481000.0, 76.0], [1406353541000.0, 76.0], [1406353601000.0, 76.0], [1406353662000.0, 76.0], [1406353722000.0, 76.0], [1406353786000.0, 76.0], [1406353841000.0, 76.0], [1406353901000.0, 76.0], [1406353962000.0, 76.0], [1406354024000.0, 76.0], [1406354081000.0, 76.0], [1406354141000.0, 76.0], [1406354202000.0, 76.0], [1406354263000.0, 76.0], [1406354322000.0, 76.0], [1406354382000.0, 76.0], [1406354442000.0, 76.0], [1406354503000.0, 76.0], [1406354562000.0, 76.0], [1406354625000.0, 76.0], [1406354681000.0, 76.0], [1406354743000.0, 76.0], [1406354803000.0, 76.0], [1406354861000.0, 76.0], [1406354921000.0, 76.0], [1406354981000.0, 76.0], [1406355042000.0, 76.0], [1406355103000.0, 76.0], [1406355161000.0, 76.0], [1406355223000.0, 76.0], [1406355282000.0, 76.0], [1406355343000.0, 76.0], [1406355402000.0, 76.0], [1406355464000.0, 76.0], [1406355522000.0, 76.0], [1406355582000.0, 76.0], [1406355642000.0, 76.0], [1406355701000.0, 76.0], [1406355763000.0, 76.0], [1406355822000.0, 76.0], [1406355887000.0, 76.0], [1406355942000.0, 76.0], [1406356001000.0, 76.0], [1406356062000.0, 76.0], [1406356122000.0, 76.0], [1406356183000.0, 76.0], [1406356241000.0, 76.0], [1406356302000.0, 76.0], [1406356362000.0, 76.0], [1406356425000.0, 76.0], [1406356481000.0, 76.0], [1406356542000.0, 76.0], [1406356602000.0, 76.0], [1406356664000.0, 76.0], [1406356722000.0, 76.0], [1406356780000.0, 76.0], [1406356842000.0, 76.0], [1406356903000.0, 76.0], [1406356963000.0, 76.0], [1406357022000.0, 76.0], [1406357081000.0, 76.0], [1406357142000.0, 76.0], [1406357202000.0, 76.0], [1406357261000.0, 76.0], [1406357322000.0, 76.0], [1406357383000.0, 76.0], [1406357442000.0, 76.0], [1406357505000.0, 76.0], [1406357561000.0, 76.0], [1406357621000.0, 76.0], [1406357682000.0, 76.0], [1406357742000.0, 76.0], [1406357802000.0, 76.0], [1406357862000.0, 76.0], [1406357921000.0, 76.0], [1406357982000.0, 76.0], [1406358041000.0, 76.0], [1406358101000.0, 76.0], [1406358161000.0, 76.0], [1406358222000.0, 76.0], [1406358283000.0, 76.0], [1406358340000.0, 76.0], [1406358401000.0, 76.0], [1406358462000.0, 76.0], [1406358522000.0, 76.0], [1406358582000.0, 76.0], [1406358643000.0, 76.0], [1406358702000.0, 76.0], [1406358761000.0, 76.0], [1406358824000.0, 76.0], [1406358882000.0, 76.0], [1406358942000.0, 76.0], [1406359002000.0, 76.0], [1406359063000.0, 76.0], [1406359122000.0, 76.0], [1406359182000.0, 76.0], [1406359243000.0, 76.0], [1406359300000.0, 76.0], [1406359363000.0, 76.0], [1406359422000.0, 76.0], [1406359481000.0, 76.0], [1406359542000.0, 76.0], [1406359601000.0, 76.0], [1406359661000.0, 76.0], [1406359722000.0, 76.0], [1406359782000.0, 76.0], [1406359842000.0, 76.0], [1406359901000.0, 76.0], [1406359962000.0, 76.0], [1406360021000.0, 76.0], [1406360081000.0, 76.0], [1406360141000.0, 76.0], [1406360202000.0, 76.0], [1406360261000.0, 76.0], [1406360322000.0, 76.0], [1406360385000.0, 76.0], [1406360443000.0, 76.0], [1406360502000.0, 76.0], [1406360565000.0, 76.0], [1406360623000.0, 76.0], [1406360681000.0, 76.0], [1406360742000.0, 76.0], [1406360801000.0, 76.0], [1406360861000.0, 76.0], [1406360923000.0, 76.0], [1406360981000.0, 76.0], [1406361041000.0, 76.0], [1406361102000.0, 76.0], [1406361161000.0, 76.0], [1406361224000.0, 76.0], [1406361281000.0, 76.0], [1406361342000.0, 76.0], [1406361403000.0, 76.0], [1406361462000.0, 76.0], [1406361521000.0, 76.0], [1406361582000.0, 76.0], [1406361645000.0, 76.0], [1406361702000.0, 76.0], [1406361761000.0, 76.0], [1406361826000.0, 76.0], [1406361883000.0, 76.0], [1406361942000.0, 76.0], [1406362002000.0, 76.0], [1406362061000.0, 76.0], [1406362123000.0, 76.0], [1406362184000.0, 76.0], [1406362246000.0, 76.0], [1406362302000.0, 76.0], [1406362363000.0, 76.0], [1406362423000.0, 76.0], [1406362483000.0, 76.0], [1406362543000.0, 76.0], [1406362602000.0, 76.0], [1406362661000.0, 76.0], [1406362722000.0, 76.0], [1406362782000.0, 76.0], [1406362843000.0, 76.0], [1406362901000.0, 76.0], [1406362962000.0, 76.0], [1406363023000.0, 76.0], [1406363085000.0, 76.0], [1406363141000.0, 76.0], [1406363201000.0, 76.0], [1406363262000.0, 76.0], [1406363323000.0, 76.0], [1406363382000.0, 76.0], [1406363443000.0, 76.0], [1406363503000.0, 76.0], [1406363562000.0, 76.0], [1406363623000.0, 76.0], [1406363682000.0, 76.0], [1406363742000.0, 76.0], [1406363802000.0, 76.0], [1406363861000.0, 76.0], [1406363923000.0, 76.0], [1406363982000.0, 76.0], [1406364044000.0, 76.0], [1406364101000.0, 76.0], [1406364162000.0, 76.0], [1406364225000.0, 76.0], [1406364283000.0, 76.0], [1406364340000.0, 76.0], [1406364403000.0, 76.0], [1406364462000.0, 76.0], [1406364522000.0, 76.0], [1406364582000.0, 76.0], [1406364643000.0, 76.0], [1406364702000.0, 76.0], [1406364761000.0, 76.0], [1406364822000.0, 76.0], [1406364882000.0, 76.0], [1406364943000.0, 76.0], [1406365003000.0, 76.0], [1406365061000.0, 76.0], [1406365123000.0, 76.0], [1406365181000.0, 76.0], [1406365242000.0, 76.0], [1406365302000.0, 76.0], [1406365361000.0, 76.0], [1406365423000.0, 76.0], [1406365482000.0, 76.0], [1406365546000.0, 76.0], [1406365602000.0, 76.0], [1406365662000.0, 76.0], [1406365723000.0, 76.0], [1406365782000.0, 76.0], [1406365842000.0, 76.0], [1406365902000.0, 76.0], [1406365962000.0, 76.0], [1406366023000.0, 76.0], [1406366086000.0, 76.0], [1406366142000.0, 76.0], [1406366202000.0, 76.0], [1406366261000.0, 76.0], [1406366323000.0, 76.0], [1406366382000.0, 76.0], [1406366445000.0, 76.0], [1406366503000.0, 76.0], [1406366562000.0, 76.0], [1406366625000.0, 76.0], [1406366681000.0, 76.0], [1406366741000.0, 76.0], [1406366802000.0, 76.0], [1406366863000.0, 76.0], [1406366921000.0, 76.0], [1406366982000.0, 76.0], [1406367043000.0, 76.0], [1406367101000.0, 76.0], [1406367164000.0, 76.0], [1406367222000.0, 76.0], [1406367283000.0, 76.0], [1406367342000.0, 76.0], [1406367403000.0, 76.0], [1406367461000.0, 76.0], [1406367523000.0, 76.0], [1406367582000.0, 76.0], [1406367640000.0, 76.0], [1406367702000.0, 76.0], [1406367762000.0, 76.0], [1406367822000.0, 76.0], [1406367885000.0, 76.0], [1406367941000.0, 76.0], [1406368002000.0, 76.0], [1406368063000.0, 76.0], [1406368122000.0, 76.0], [1406368182000.0, 76.0], [1406368241000.0, 76.0], [1406368302000.0, 76.0], [1406368362000.0, 76.0], [1406368422000.0, 76.0], [1406368484000.0, 76.0], [1406368542000.0, 76.0], [1406368602000.0, 76.0], [1406368662000.0, 76.0], [1406368722000.0, 76.0], [1406368782000.0, 76.0], [1406368843000.0, 76.0], [1406368902000.0, 76.0], [1406368962000.0, 76.0], [1406369022000.0, 76.0], [1406369082000.0, 76.0], [1406369141000.0, 76.0], [1406369202000.0, 76.0], [1406369262000.0, 76.0], [1406369323000.0, 76.0], [1406369382000.0, 76.0], [1406369442000.0, 76.0], [1406369489000.0, 76.0], [1406369563000.0, 76.0], [1406369625000.0, 76.0], [1406369672000.0, 76.0], [1406369742000.0, 76.0], [1406369802000.0, 76.0], [1406369857000.0, 76.0], [1406369923000.0, 76.0], [1406369979000.0, 76.0], [1406370027000.0, 76.0], [1406370101000.0, 76.0], [1406370155000.0, 76.0], [1406370214000.0, 76.0], [1406370283000.0, 76.0], [1406370342000.0, 76.0], [1406370401000.0, 76.0], [1406370462000.0, 76.0], [1406370525000.0, 76.0], [1406370581000.0, 76.0], [1406370642000.0, 76.0], [1406370702000.0, 76.0], [1406370763000.0, 76.0], [1406370822000.0, 76.0], [1406370882000.0, 76.0], [1406370943000.0, 76.0], [1406371002000.0, 76.0], [1406371062000.0, 76.0], [1406371120000.0, 76.0], [1406371183000.0, 76.0], [1406371242000.0, 76.0], [1406371302000.0, 76.0], [1406371363000.0, 76.0], [1406371422000.0, 76.0], [1406371483000.0, 76.0], [1406371542000.0, 76.0], [1406371603000.0, 76.0], [1406371662000.0, 76.0], [1406371722000.0, 76.0], [1406371782000.0, 76.0], [1406371842000.0, 76.0], [1406371903000.0, 76.0], [1406371962000.0, 76.0], [1406372021000.0, 76.0], [1406372082000.0, 76.0], [1406372142000.0, 76.0], [1406372206000.0, 76.0], [1406372261000.0, 76.0], [1406372321000.0, 76.0], [1406372383000.0, 76.0], [1406372442000.0, 76.0], [1406372504000.0, 76.0], [1406372563000.0, 76.0], [1406372609000.0, 76.0], [1406372684000.0, 76.0], [1406372741000.0, 76.0], [1406372804000.0, 76.0], [1406372863000.0, 76.0], [1406372922000.0, 76.0], [1406372982000.0, 76.0], [1406373041000.0, 76.0], [1406373105000.0, 76.0], [1406373163000.0, 76.0], [1406373222000.0, 76.0], [1406373282000.0, 76.0], [1406373342000.0, 76.0], [1406373401000.0, 76.0], [1406373463000.0, 76.0], [1406373522000.0, 76.0], [1406373583000.0, 76.0], [1406373641000.0, 76.0], [1406373703000.0, 76.0], [1406373761000.0, 76.0], [1406373822000.0, 76.0], [1406373881000.0, 76.0], [1406373942000.0, 76.0], [1406374002000.0, 76.0], [1406374062000.0, 76.0], [1406374121000.0, 76.0], [1406374182000.0, 76.0], [1406374242000.0, 76.0], [1406374308000.0, 76.0], [1406374362000.0, 76.0], [1406374422000.0, 76.0], [1406374482000.0, 76.0], [1406374542000.0, 76.0], [1406374603000.0, 76.0], [1406374662000.0, 76.0], [1406374722000.0, 76.0], [1406374781000.0, 76.0], [1406374843000.0, 76.0], [1406374888000.0, 76.0], [1406374963000.0, 76.0], [1406375022000.0, 76.0], [1406375081000.0, 76.0], [1406375141000.0, 76.0], [1406375201000.0, 76.0], [1406375262000.0, 76.0], [1406375314000.0, 76.0], [1406375382000.0, 76.0], [1406375442000.0, 76.0], [1406375503000.0, 76.0], [1406375563000.0, 76.0], [1406375622000.0, 76.0], [1406375684000.0, 76.0], [1406375743000.0, 76.0], [1406375802000.0, 76.0], [1406375862000.0, 76.0], [1406375924000.0, 76.0], [1406375982000.0, 76.0], [1406376043000.0, 76.0], [1406376102000.0, 76.0], [1406376162000.0, 76.0], [1406376222000.0, 76.0], [1406376283000.0, 76.0], [1406376342000.0, 76.0], [1406376402000.0, 76.0], [1406376461000.0, 76.0], [1406376522000.0, 76.0], [1406376580000.0, 76.0], [1406376636000.0, 76.0], [1406376702000.0, 76.0], [1406376763000.0, 76.0], [1406376821000.0, 76.0], [1406376885000.0, 76.0], [1406376942000.0, 76.0], [1406377003000.0, 76.0], [1406377061000.0, 76.0], [1406377123000.0, 76.0], [1406377182000.0, 76.0], [1406377243000.0, 76.0], [1406377301000.0, 76.0], [1406377360000.0, 76.0], [1406377428000.0, 76.0], [1406377483000.0, 76.0], [1406377542000.0, 76.0], [1406377603000.0, 76.0], [1406377663000.0, 76.0], [1406377722000.0, 76.0], [1406377782000.0, 76.0], [1406377842000.0, 76.0], [1406377902000.0, 76.0], [1406377962000.0, 76.0], [1406378022000.0, 76.0], [1406378082000.0, 76.0], [1406378143000.0, 76.0], [1406378199000.0, 76.0], [1406378264000.0, 76.0], [1406378325000.0, 76.0], [1406378382000.0, 76.0], [1406378442000.0, 76.0], [1406378502000.0, 76.0], [1406378563000.0, 76.0], [1406378621000.0, 76.0], [1406378683000.0, 76.0], [1406378742000.0, 76.0], [1406378802000.0, 76.0], [1406378862000.0, 76.0], [1406378923000.0, 76.0], [1406378985000.0, 76.0], [1406379043000.0, 76.0], [1406379101000.0, 76.0], [1406379163000.0, 76.0], [1406379223000.0, 76.0], [1406379282000.0, 76.0], [1406379342000.0, 76.0], [1406379402000.0, 76.0], [1406379463000.0, 76.0], [1406379521000.0, 76.0], [1406379583000.0, 76.0], [1406379642000.0, 76.0], [1406379702000.0, 76.0], [1406379763000.0, 76.0], [1406379822000.0, 76.0], [1406379884000.0, 76.0], [1406379943000.0, 76.0], [1406380002000.0, 76.0], [1406380061000.0, 76.0], [1406380123000.0, 76.0], [1406380182000.0, 76.0], [1406380242000.0, 76.0], [1406380302000.0, 76.0], [1406380363000.0, 76.0], [1406380422000.0, 76.0], [1406380485000.0, 76.0], [1406380542000.0, 76.0], [1406380602000.0, 76.0], [1406380661000.0, 76.0], [1406380723000.0, 76.0], [1406380782000.0, 76.0], [1406380842000.0, 76.0], [1406380902000.0, 76.0], [1406380963000.0, 76.0], [1406381024000.0, 76.0], [1406381083000.0, 76.0], [1406381143000.0, 76.0], [1406381202000.0, 76.0], [1406381261000.0, 76.0], [1406381326000.0, 76.0], [1406381388000.0, 76.0], [1406381457000.0, 76.0], [1406381501000.0, 76.0], [1406381563000.0, 76.0], [1406381622000.0, 76.0], [1406381682000.0, 76.0], [1406381740000.0, 76.0], [1406381803000.0, 76.0], [1406381863000.0, 76.0], [1406381923000.0, 76.0], [1406381982000.0, 76.0], [1406382043000.0, 76.0], [1406382102000.0, 76.0], [1406382160000.0, 76.0], [1406382223000.0, 76.0], [1406382282000.0, 76.0], [1406382342000.0, 76.0], [1406382402000.0, 76.0], [1406382462000.0, 76.0], [1406382521000.0, 76.0], [1406382582000.0, 76.0], [1406382641000.0, 76.0], [1406382702000.0, 76.0], [1406382762000.0, 76.0], [1406382823000.0, 76.0], [1406382885000.0, 76.0], [1406382942000.0, 76.0], [1406383001000.0, 76.0], [1406383062000.0, 76.0], [1406383123000.0, 76.0], [1406383182000.0, 76.0], [1406383242000.0, 76.0], [1406383302000.0, 76.0], [1406383362000.0, 76.0], [1406383426000.0, 76.0], [1406383482000.0, 76.0], [1406383545000.0, 76.0], [1406383603000.0, 76.0], [1406383663000.0, 76.0], [1406383723000.0, 76.0], [1406383780000.0, 76.0], [1406383843000.0, 76.0], [1406383903000.0, 76.0], [1406383963000.0, 76.0], [1406384022000.0, 76.0], [1406384081000.0, 76.0], [1406384143000.0, 76.0], [1406384203000.0, 76.0], [1406384262000.0, 76.0], [1406384322000.0, 76.0], [1406384382000.0, 76.0], [1406384446000.0, 76.0], [1406384501000.0, 76.0], [1406384562000.0, 76.0], [1406384622000.0, 76.0], [1406384685000.0, 76.0], [1406384743000.0, 76.0], [1406384803000.0, 76.0], [1406384862000.0, 76.0], [1406384922000.0, 76.0], [1406384983000.0, 76.0], [1406385043000.0, 76.0], [1406385102000.0, 76.0], [1406385163000.0, 76.0], [1406385223000.0, 76.0], [1406385281000.0, 76.0], [1406385342000.0, 76.0], [1406385401000.0, 76.0], [1406385462000.0, 76.0], [1406385523000.0, 76.0], [1406385583000.0, 76.0], [1406385642000.0, 76.0], [1406385701000.0, 76.0], [1406385763000.0, 76.0], [1406385823000.0, 76.0], [1406385882000.0, 76.0], [1406385942000.0, 76.0], [1406386002000.0, 76.0], [1406386063000.0, 76.0], [1406386122000.0, 76.0], [1406386183000.0, 76.0], [1406386241000.0, 76.0], [1406386306000.0, 76.0], [1406386363000.0, 76.0], [1406386420000.0, 76.0], [1406386482000.0, 76.0], [1406386543000.0, 76.0], [1406386603000.0, 76.0], [1406386662000.0, 76.0], [1406386722000.0, 76.0], [1406386782000.0, 76.0], [1406386842000.0, 76.0], [1406386903000.0, 76.0], [1406386955000.0, 76.0], [1406387025000.0, 76.0], [1406387082000.0, 76.0], [1406387143000.0, 76.0], [1406387203000.0, 76.0], [1406387262000.0, 76.0], [1406387322000.0, 76.0], [1406387382000.0, 76.0], [1406387443000.0, 76.0], [1406387502000.0, 76.0], [1406387563000.0, 76.0], [1406387623000.0, 76.0], [1406387682000.0, 76.0], [1406387746000.0, 76.0], [1406387805000.0, 76.0], [1406387865000.0, 76.0], [1406387923000.0, 76.0], [1406387982000.0, 76.0], [1406388043000.0, 76.0], [1406388101000.0, 76.0], [1406388163000.0, 76.0], [1406388222000.0, 76.0], [1406388287000.0, 76.0], [1406388343000.0, 76.0], [1406388402000.0, 76.0], [1406388462000.0, 76.0], [1406388523000.0, 76.0], [1406388580000.0, 76.0], [1406388642000.0, 76.0], [1406388705000.0, 76.0], [1406388762000.0, 76.0], [1406388821000.0, 76.0], [1406388882000.0, 76.0], [1406388945000.0, 76.0], [1406389005000.0, 76.0], [1406389062000.0, 76.0], [1406389122000.0, 76.0], [1406389181000.0, 76.0], [1406389241000.0, 76.0], [1406389302000.0, 76.0], [1406389363000.0, 76.0], [1406389421000.0, 76.0], [1406389485000.0, 76.0], [1406389542000.0, 76.0], [1406389605000.0, 76.0], [1406389661000.0, 76.0], [1406389721000.0, 76.0]]
    for nwthis in nw:
        #data.append((nwthis.device_type, nwthis.device_status))
        s = nwthis[0] / 1000.0
        s = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S')
        data.append((s, nwthis[1]))
    response = HttpResponse(data.xls, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = "attachment; filename=export.xls"

    return response


@login_required(login_url='/login/')
def export_smap_data_to_spreadsheet(request, mac):
    headers = ('Time', 'Data Point')
    mac = mac.encode('utf-8')
    device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
    print device_metadata
    device_id = device_metadata[0]['device_id']
    device_type_id = device_metadata[0]['device_model_id']
    device_type = device_metadata[0]['device_type']
    mac_address = device_metadata[0]['mac_address']
    device_type_id = device_type_id.device_model_id
    print device_type_id, device_id

    if device_type_id == '1TH' or device_type_id == '1NST':
        device_smap = export_thermostat_smap_data(request, device_id, headers)

        with open(device_type + '_' + mac + '_smap.xls', 'wb') as f:
            f.write(device_smap.xls)
        response = HttpResponse(device_smap.xls, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=" + device_type + "_" + mac + "_smap.xls"
        return response
    elif device_type_id == '2WL' or device_type_id == '3WSP':
        device_smap = export_plugload_smap_data(request, device_id, headers, device_type_id)
        response = HttpResponse(device_smap.xls, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=" + device_type + "_" + mac + "_smap.xls"
        return response
    elif device_type_id == '2DB' or device_type_id == '2SDB' or device_type_id == '2WSL':
        device_smap = export_lighting_smap_data(request, device_id, headers)
        with open(device_type + '_' + mac + '_smap.xls', 'wb') as f:
            f.write(device_smap.xls)
        response = HttpResponse(device_smap.xls, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=" + device_type + "_" + mac + "_smap.xls"
        return response
    elif device_type_id == '3WP':
        device_smap = export_wattplug_smap_data(request, device_id, headers)
        with open(device_type + '_' + mac + '_smap.xls', 'wb') as f:
            f.write(device_smap.xls)
        response = HttpResponse(device_smap.xls, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=" + device_type + "_" + mac + "_smap.xls"
        return response


def export_wattplug_smap_data(request, device_id, headers):
    device_status = [ob.data_as_json() for ob in Plugload.objects.filter(plugload_id=device_id)]
    device_zone = device_status[0]['zone']['id']
    device_nickname = device_status[0]['nickname']
    zone_nickname = device_status[0]['zone']['zone_nickname']

    device_info = str(device_zone) + '/plugload/' + device_id
    device_info = device_info.encode('ascii', 'ignore')
    device_smap_tag = '/bemoss/' + str(device_zone) + '/plugload/' + device_id

    device_smap_tag = device_smap_tag.encode('ascii', 'ignore')
    status = device_smap_tag + '/status'
    power = device_smap_tag + '/power'
    print status

    _uuid_status = get_uuid_for_data_point(status)
    _uuid_power = get_uuid_for_data_point(power)

    rs_status = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_status)
    rs_power = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_power)

    data = []
    data = tablib.Dataset(*data, headers=headers, title=device_nickname)

    rs_status = append_data_smap(rs_status, tablib.Dataset(*data, headers=headers, title="Status"))
    rs_power = append_data_smap(rs_power, tablib.Dataset(*data, headers=headers, title="Power"))

    device_smap = tablib.Databook((rs_status, rs_power))

    return device_smap


def export_lighting_smap_data(request, device_id, headers):
    device_status = [ob.data_as_json() for ob in Lighting.objects.filter(lighting_id=device_id)]
    device_zone = device_status[0]['zone']['id']
    device_nickname = device_status[0]['nickname']
    zone_nickname = device_status[0]['zone']['zone_nickname']

    device_info = str(device_zone) + '/lighting/' + device_id
    device_info = device_info.encode('ascii', 'ignore')
    device_smap_tag = '/bemoss/' + str(device_zone) + '/lighting/' + device_id
    device_smap_tag = device_smap_tag.encode('ascii', 'ignore')
    status = device_smap_tag + '/status'
    brightness = device_smap_tag + '/brightness'
    print status

    _uuid_status = get_uuid_for_data_point(status)
    _uuid_brightness = get_uuid_for_data_point(brightness)

    rs_status = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_status)
    rs_brightness = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_brightness)

    data = []
    data = tablib.Dataset(*data, headers=headers, title=device_nickname)

    rs_status = append_data_smap(rs_status, tablib.Dataset(*data, headers=headers, title="Status"))
    rs_brightness = append_data_smap(rs_brightness, tablib.Dataset(*data, headers=headers, title="Brightness"))

    device_smap = tablib.Databook((rs_status, rs_brightness))
    return device_smap


def export_plugload_smap_data(request, device_id, headers, device_type_id):
    if device_type_id == '2WL':
        device_status = [ob.data_as_json() for ob in Lighting.objects.filter(lighting_id=device_id)]
        device_zone = device_status[0]['zone']['id']
        device_nickname = device_status[0]['nickname']
        zone_nickname = device_status[0]['zone']['zone_nickname']

        device_info = str(device_zone) + '/lighting/' + device_id
        device_info = device_info.encode('ascii', 'ignore')
        device_smap_tag = '/bemoss/' + str(device_zone) + '/lighting/' + device_id
    else:
        device_status = [ob.data_as_json() for ob in Plugload.objects.filter(plugload_id=device_id)]
        device_zone = device_status[0]['zone']['id']
        device_nickname = device_status[0]['nickname']
        zone_nickname = device_status[0]['zone']['zone_nickname']

        device_info = str(device_zone) + '/plugload/' + device_id
        device_info = device_info.encode('ascii', 'ignore')
        device_smap_tag = '/bemoss/' + str(device_zone) + '/plugload/' + device_id

    device_smap_tag = device_smap_tag.encode('ascii', 'ignore')
    status = device_smap_tag + '/status'
    print status

    _uuid_status = get_uuid_for_data_point(status)
    rs_status = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_status)

    data = []
    data = tablib.Dataset(*data, headers=headers, title=device_nickname)

    rs_status = append_data_smap(rs_status, data)
    return rs_status


def export_thermostat_smap_data(request, device_id, headers):
    device_status = [ob.data_as_json() for ob in Thermostat.objects.filter(thermostat_id=device_id)]
    print device_status
    device_zone = device_status[0]['zone']['id']
    device_nickname = device_status[0]['nickname']
    zone_nickname = device_status[0]['zone']['zone_nickname']

    device_info = str(device_zone) + '/thermostat/' + device_id
    device_info = device_info.encode('ascii', 'ignore')
    device_smap_tag = '/bemoss/' + str(device_zone) + '/thermostat/' + device_id
    device_smap_tag = device_smap_tag.encode('ascii', 'ignore')
    temperature = device_smap_tag + '/temperature'
    heat_setpoint = device_smap_tag + '/heat_setpoint'
    cool_setpoint = device_smap_tag + '/cool_setpoint'
    print temperature

    _uuid_temperature = get_uuid_for_data_point(temperature)
    _uuid_heat_setpoint = get_uuid_for_data_point(heat_setpoint)
    _uuid_cool_setpoint = get_uuid_for_data_point(cool_setpoint)

    rs_temperature = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_temperature)
    rs_heat_setpoint = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_heat_setpoint)
    rs_cool_setpoint = get_data_from_smap("http://localhost/backend/api/data/uuid/" + _uuid_cool_setpoint)

    data = []
    data = tablib.Dataset(*data, headers=headers, title=device_nickname)

    rs_temperature = append_data_smap(rs_temperature, tablib.Dataset(*data, headers=headers, title="Temperature"))
    rs_heat_setpoint = append_data_smap(rs_heat_setpoint, tablib.Dataset(*data, headers=headers, title="Heat Setpoint"))
    rs_cool_setpoint = append_data_smap(rs_cool_setpoint, tablib.Dataset(*data, headers=headers, title="Cool Setpoint"))

    device_smap = tablib.Databook((rs_temperature, rs_heat_setpoint, rs_cool_setpoint))

    return device_smap


def append_data_smap(_data, data):
    for smap_data in _data:
        s = smap_data[0] / 1000.0
        s = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S')
        data.append((s, smap_data[1]))
    return data


def get_data_from_smap(url):
    rs = urllib2.urlopen(url)

    json_string = rs.read()
    parsed_json = json.loads(json_string)
    parsed_json = parsed_json[0]['Readings']
    return parsed_json


@login_required(login_url='/login/')
def export_thermostat_to_spreadsheet(request):
    _data_th = [ob.device_status() for ob in Thermostat.objects.filter(thermostat_id__bemoss=True)]
    response = get_data([_data_th], "thermostat")
    return response


@login_required(login_url='/login/')
def export_lighting_to_spreadsheet(request):
    _data = [ob.device_status() for ob in Lighting.objects.filter(lighting_id__bemoss=True)]
    response = get_data([_data], "lighting")
    return response

@login_required(login_url='/login/')
def export_plugload_to_spreadsheet(request):
    _data = [ob.device_status() for ob in Plugload.objects.filter(plugload_id__bemoss=True)]
    response = get_data([_data], "plugload")
    return response


def get_data(__data, device_type):
    headers = ('Device Nickname', 'Zone', 'Device Model', 'Device Added On', 'Network Status', 'Last Scanned Time',
               'Last Offline Time')
    data = []
    data = tablib.Dataset(*data, headers=headers, title=device_type)
    for _data in __data:
        for device in _data:
            data.append((device['nickname'], device['zone_nickname'], device['device_model'],
                        str(device['date_added']),
                        device['network_status'],
                        str(device['last_scanned']),
                         str(device['last_offline'])))
    response = HttpResponse(data.xls, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = "attachment; filename=bemoss_" + device_type + ".xls"
    return response


@login_required(login_url='/login/')
def export_all_device_information(request):
    _data_th = [ob.device_status() for ob in Thermostat.objects.filter(thermostat_id__bemoss=True)]
    _data_hvac = data_this([_data_th], "Thermostats")
    _data_lt = [ob.device_status() for ob in Lighting.objects.filter(lighting_id__bemoss=True)]
    _data_lt = data_this([_data_lt], "Lighting Loads")
    _data_pl = [ob.device_status() for ob in Plugload.objects.filter(plugload_id__bemoss=True)]
    _data_pl = data_this([_data_pl], "Plugloads")

    devices = tablib.Databook((_data_hvac, _data_lt, _data_pl))
    #with open(downloads_dir + 'bemoss_devices.xls', 'wb') as f:
    with open('bemoss_devices.xls', 'wb') as f:
        f.write(devices.xls)
    response = HttpResponse(devices.xls, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = "attachment; filename=bemoss_devices.xls"
    return response


def data_this(__data, sheetname):
    headers = ('Device Nickname', 'Zone', 'Device Model', 'Device Added On', 'Network Status', 'Last Scanned Time',
               'Last Offline Time')
    data = []
    data = tablib.Dataset(*data, headers=headers,  title=sheetname)
    for _data in __data:
        for device in _data:
            data.append((device['nickname'], device['zone_nickname'], device['device_model'],
                        str(device['date_added']),
                        device['network_status'],
                        str(device['last_scanned']),
                         str(device['last_offline'])))
    return data


@login_required(login_url='/login/')
def export_schedule_thermostats_holiday(request, mac):
    mac = mac.encode('ascii', 'ignore')
    device = DeviceMetadata.objects.get(mac_address=mac)

    _file_name = os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/thermostat/' + device.device_id
                              + '_schedule.json')
    if os.path.isfile(_file_name):
            json_file = open(_file_name, 'r+')
            _json_data = json.load(json_file)
            if device.device_id in _json_data['thermostat']:
                print 'device id present'
                _data = _json_data['thermostat'][device.device_id]['schedulers']['holiday']
                _data = json.dumps(_data)
                _data = json.loads(_data, object_hook=_decode_dict)
            json_file.close()

    headers = ('Period Name', 'From', 'Mode', 'Setpoint (F)')
    data = []
    data = tablib.Dataset(*data, headers=headers,  title='Holiday')

    if 'heat' in _data:
            heat_data = _data['heat']
            for record in heat_data:
                rec_time = str(int(record['at'])/60) + ':' + str(int(record['at']) % 60)
                data.append((record['nickname'], rec_time, 'Heat', record['setpoint']))
    if 'cool' in _data:
        cool_data = _data['cool']
        for record in cool_data:
            rec_time = str(int(record['at'])/60) + ':' + str(int(record['at']) % 60)
            data.append((record['nickname'], rec_time, 'Cool', record['setpoint']))
    response = HttpResponse(data.xls, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = "attachment; filename=" + device.device_model + "_holiday_sch.xls"
    return response


@login_required(login_url='/login/')
def export_schedule_thermostats_daily(request, mac):
    mac = mac.encode('ascii', 'ignore')
    device = DeviceMetadata.objects.get(mac_address=mac)

    _file_name = os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/thermostat/' + device.device_id
                              + '_schedule.json')
    if os.path.isfile(_file_name):
            json_file = open(_file_name, 'r+')
            _json_data = json.load(json_file)
            if device.device_id in _json_data['thermostat']:
                print 'device id present'
                _data = _json_data['thermostat'][device.device_id]['schedulers']['everyday']
                _data = json.dumps(_data)
                _data = json.loads(_data, object_hook=_decode_dict)
            json_file.close()

    headers = ('Period Name', 'From', 'Mode', 'Setpoint (F)')
    _data_mon = _data_tue = _data_wed = _data_thu = _data_fri = _data_sat = _data_sun = []

    for day in _data:
        data = []
        data = tablib.Dataset(*data, headers=headers,  title=day)
        day_data = _data[day]
        if 'heat' in day_data:
            heat_data = day_data['heat']
            for record in heat_data:
                rec_time = str(int(record['at'])/60) + ':' + str(int(record['at']) % 60)
                data.append((record['nickname'], rec_time, 'Heat', record['setpoint']))
        if 'cool' in day_data:
            cool_data = day_data['cool']
            for record in cool_data:
                rec_time = str(int(record['at'])/60) + ':' + str(int(record['at']) % 60)
                data.append((record['nickname'], rec_time, 'Cool', record['setpoint']))

        if day == 'monday':
            _data_mon = data
        elif day == 'tuesday':
            _data_tue = data
        elif day == 'wednesday':
            _data_wed = data
        elif day == 'thursday':
            _data_thu = data
        elif day == 'friday':
            _data_fri = data
        elif day == 'saturday':
            _data_sat = data
        elif day == 'sunday':
            _data_sun = data

    schedule = tablib.Databook((_data_mon, _data_tue, _data_wed, _data_thu, _data_fri, _data_sat, _data_sun))

    with open(device.device_model + "_daily_sch.xls", 'wb') as f:
        f.write(schedule.xls)
    response = HttpResponse(schedule.xls, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = "attachment; filename=" +device.device_model + "_daily_sch.xls"
    return response


@login_required(login_url='/login/')
def export_schedule_lighting_daily(request, mac):
    mac = mac.encode('ascii', 'ignore')
    device = DeviceMetadata.objects.get(mac_address=mac)

    if device.device_model_id.device_model_id == '2WL':

        _file_name = os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/lighting/' + device.device_id
                                  + '_schedule.json')
        if os.path.isfile(_file_name):
                json_file = open(_file_name, 'r+')
                _json_data = json.load(json_file)
                if device.device_id in _json_data['lighting']:
                    print 'device id present'
                    _data = _json_data['lighting'][device.device_id]['schedulers']['everyday']
                    _data = json.dumps(_data)
                    _data = json.loads(_data, object_hook=_decode_dict)
                json_file.close()

        headers = ('Period Name', 'From', 'Status')
        _data_mon = _data_tue = _data_wed = _data_thu = _data_fri = _data_sat = _data_sun = []

        for day in _data:
            data = []
            data = tablib.Dataset(*data, headers=headers,  title=day)
            day_data = _data[day]
            for record in day_data:
                rec_time = str(int(record['at'])/60) + ':' + str(int(record['at']) % 60)
                data.append((record['nickname'], rec_time, record['status']))

            if day == 'monday':
                _data_mon = data
            elif day == 'tuesday':
                _data_tue = data
            elif day == 'wednesday':
                _data_wed = data
            elif day == 'thursday':
                _data_thu = data
            elif day == 'friday':
                _data_fri = data
            elif day == 'saturday':
                _data_sat = data
            elif day == 'sunday':
                _data_sun = data

        schedule = tablib.Databook((_data_mon, _data_tue, _data_wed, _data_thu, _data_fri, _data_sat, _data_sun))

        with open(device.device_model + "_daily_sch.xls", 'wb') as f:
            f.write(schedule.xls)
        response = HttpResponse(schedule.xls, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=" +device.device_model + "_daily_sch.xls"
        return response

    elif device.device_model_id.device_model_id == '2DB' or \
                    device.device_model_id.device_model_id == '2SDB' or \
                    device.device_model_id.device_model_id == '2WSL':

        _file_name = os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/lighting/' + device.device_id
                                  + '_schedule.json')
        if os.path.isfile(_file_name):
                json_file = open(_file_name, 'r+')
                _json_data = json.load(json_file)
                if device.device_id in _json_data['lighting']:
                    print 'device id present'
                    _data = _json_data['lighting'][device.device_id]['schedulers']['everyday']
                    _data = json.dumps(_data)
                    _data = json.loads(_data, object_hook=_decode_dict)
                json_file.close()

        headers = ('Period Name', 'From', 'Status (ON/OFF)', 'Brightness (%)')
        _data_mon = _data_tue = _data_wed = _data_thu = _data_fri = _data_sat = _data_sun = []

        for day in _data:
            data = []
            data = tablib.Dataset(*data, headers=headers,  title=day)
            day_data = _data[day]
            for record in day_data:
                rec_time = str(int(record['at'])/60) + ':' + str(int(record['at']) % 60)
                data.append((record['nickname'], rec_time, record['status'], record['brightness']))

            if day == 'monday':
                _data_mon = data
            elif day == 'tuesday':
                _data_tue = data
            elif day == 'wednesday':
                _data_wed = data
            elif day == 'thursday':
                _data_thu = data
            elif day == 'friday':
                _data_fri = data
            elif day == 'saturday':
                _data_sat = data
            elif day == 'sunday':
                _data_sun = data

        schedule = tablib.Databook((_data_mon, _data_tue, _data_wed, _data_thu, _data_fri, _data_sat, _data_sun))

        with open(device.device_model + "_daily_sch.xls", 'wb') as f:
            f.write(schedule.xls)
        response = HttpResponse(schedule.xls, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=" +device.device_model + "_daily_sch.xls"
        return response

    elif device.device_model_id.device_model_id == '2HUE':

        _file_name = os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/lighting/' + device.device_id
                                  + '_schedule.json')
        if os.path.isfile(_file_name):
                json_file = open(_file_name, 'r+')
                _json_data = json.load(json_file)
                if device.device_id in _json_data['lighting']:
                    print 'device id present'
                    _data = _json_data['lighting'][device.device_id]['schedulers']['everyday']
                    _data = json.dumps(_data)
                    _data = json.loads(_data, object_hook=_decode_dict)
                json_file.close()

        headers = ('Period Name', 'From', 'Status (ON/OFF)', 'Brightness (%)', 'Color')
        _data_mon = _data_tue = _data_wed = _data_thu = _data_fri = _data_sat = _data_sun = []

        for day in _data:
            data = []
            data = tablib.Dataset(*data, headers=headers,  title=day)
            day_data = _data[day]
            for record in day_data:
                rec_time = str(int(record['at'])/60) + ':' + str(int(record['at']) % 60)
                data.append((record['nickname'], rec_time, record['status'], record['brightness'], record['color']))

            if day == 'monday':
                _data_mon = data
            elif day == 'tuesday':
                _data_tue = data
            elif day == 'wednesday':
                _data_wed = data
            elif day == 'thursday':
                _data_thu = data
            elif day == 'friday':
                _data_fri = data
            elif day == 'saturday':
                _data_sat = data
            elif day == 'sunday':
                _data_sun = data

        schedule = tablib.Databook((_data_mon, _data_tue, _data_wed, _data_thu, _data_fri, _data_sat, _data_sun))

        with open(device.device_model + "_daily_sch.xls", 'wb') as f:
            f.write(schedule.xls)
        response = HttpResponse(schedule.xls, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=" +device.device_model + "_daily_sch.xls"
        return response


@login_required(login_url='/login/')
def export_schedule_lighting_holiday(request, mac):
    mac = mac.encode('ascii', 'ignore')
    device = DeviceMetadata.objects.get(mac_address=mac)

    if device.device_model_id.device_model_id == '2WL':

        _file_name = os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/lighting/' + device.device_id
                                  + '_schedule.json')
        if os.path.isfile(_file_name):
                json_file = open(_file_name, 'r+')
                _json_data = json.load(json_file)
                if device.device_id in _json_data['lighting']:
                    print 'device id present'
                    _data = _json_data['lighting'][device.device_id]['schedulers']['holiday']['holiday']
                    _data = json.dumps(_data)
                    _data = json.loads(_data, object_hook=_decode_dict)
                json_file.close()

        headers = ('Period Name', 'From', 'Status')
        _data_mon = _data_tue = _data_wed = _data_thu = _data_fri = _data_sat = _data_sun = []
        data = []
        data = tablib.Dataset(*data, headers=headers,  title='Holiday')
        for record in _data:
            rec_time = str(int(record['at'])/60) + ':' + str(int(record['at']) % 60)
            data.append((record['nickname'], rec_time, record['status']))

        response = HttpResponse(data.xls, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=" + device.device_model + "_holiday_sch.xls"
        return response

    elif device.device_model_id.device_model_id == '2DB' or \
                    device.device_model_id.device_model_id == '2SDB' or \
                    device.device_model_id.device_model_id == '2WSL':

        _file_name = os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/lighting/' + device.device_id
                                  + '_schedule.json')
        if os.path.isfile(_file_name):
                json_file = open(_file_name, 'r+')
                _json_data = json.load(json_file)
                if device.device_id in _json_data['lighting']:
                    print 'device id present'
                    _data = _json_data['lighting'][device.device_id]['schedulers']['holiday']['holiday']
                    _data = json.dumps(_data)
                    _data = json.loads(_data, object_hook=_decode_dict)
                json_file.close()

        headers = ('Period Name', 'From', 'Status (ON/OFF)', 'Brightness (%)')
        data = []
        data = tablib.Dataset(*data, headers=headers,  title='Holiday')
        for record in _data:
            rec_time = str(int(record['at'])/60) + ':' + str(int(record['at']) % 60)
            data.append((record['nickname'], rec_time, record['status'], record['brightness']))

        response = HttpResponse(data.xls, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=" + device.device_model + "_holiday_sch.xls"
        return response

    elif device.device_model_id.device_model_id == '2HUE':

        _file_name = os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/lighting/' + device.device_id
                                  + '_schedule.json')
        if os.path.isfile(_file_name):
                json_file = open(_file_name, 'r+')
                _json_data = json.load(json_file)
                if device.device_id in _json_data['lighting']:
                    print 'device id present'
                    _data = _json_data['lighting'][device.device_id]['schedulers']['holiday']['holiday']
                    _data = json.dumps(_data)
                    _data = json.loads(_data, object_hook=_decode_dict)
                json_file.close()

        headers = ('Period Name', 'From', 'Status (ON/OFF)', 'Brightness (%)', 'Color')
        data = []
        data = tablib.Dataset(*data, headers=headers,  title='Holiday')
        for record in _data:
            rec_time = str(int(record['at'])/60) + ':' + str(int(record['at']) % 60)
            data.append((record['nickname'], rec_time, record['status'], record['brightness'], record['color']))

        response = HttpResponse(data.xls, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=" + device.device_model + "_holiday_sch.xls"
        return response

@login_required(login_url='/login/')
def export_schedule_plugload_daily(request, mac):
    mac = mac.encode('ascii', 'ignore')
    device = DeviceMetadata.objects.get(mac_address=mac)

    _file_name = os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/plugload/' + device.device_id
                              + '_schedule.json')
    if os.path.isfile(_file_name):
            json_file = open(_file_name, 'r+')
            _json_data = json.load(json_file)
            if device.device_id in _json_data['plugload']:
                print 'device id present'
                _data = _json_data['plugload'][device.device_id]['schedulers']['everyday']
                _data = json.dumps(_data)
                _data = json.loads(_data, object_hook=_decode_dict)
            json_file.close()

    headers = ('Period Name', 'From', 'Status')
    _data_mon = _data_tue = _data_wed = _data_thu = _data_fri = _data_sat = _data_sun = []

    for day in _data:
        data = []
        data = tablib.Dataset(*data, headers=headers,  title=day)
        day_data = _data[day]
        for record in day_data:
            rec_time = str(int(record['at'])/60) + ':' + str(int(record['at']) % 60)
            data.append((record['nickname'], rec_time, record['status']))

        if day == 'monday':
            _data_mon = data
        elif day == 'tuesday':
            _data_tue = data
        elif day == 'wednesday':
            _data_wed = data
        elif day == 'thursday':
            _data_thu = data
        elif day == 'friday':
            _data_fri = data
        elif day == 'saturday':
            _data_sat = data
        elif day == 'sunday':
            _data_sun = data

    schedule = tablib.Databook((_data_mon, _data_tue, _data_wed, _data_thu, _data_fri, _data_sat, _data_sun))

    with open(device.device_model + "_daily_sch.xls", 'wb') as f:
        f.write(schedule.xls)
    response = HttpResponse(schedule.xls, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = "attachment; filename=" +device.device_model + "_daily_sch.xls"
    return response


@login_required(login_url='/login/')
def export_schedule_plugload_holiday(request, mac):
    mac = mac.encode('ascii', 'ignore')
    device = DeviceMetadata.objects.get(mac_address=mac)

    _file_name = os.path.join(settings.PROJECT_DIR, 'resources/scheduler_data/plugload/' + device.device_id
                              + '_schedule.json')
    if os.path.isfile(_file_name):
            json_file = open(_file_name, 'r+')
            _json_data = json.load(json_file)
            if device.device_id in _json_data['plugload']:
                print 'device id present'
                _data = _json_data['plugload'][device.device_id]['schedulers']['holiday']['holiday']
                _data = json.dumps(_data)
                _data = json.loads(_data, object_hook=_decode_dict)
            json_file.close()

    headers = ('Period Name', 'From', 'Status')
    _data_mon = _data_tue = _data_wed = _data_thu = _data_fri = _data_sat = _data_sun = []
    data = []
    data = tablib.Dataset(*data, headers=headers,  title='Holiday')
    for record in _data:
        rec_time = str(int(record['at'])/60) + ':' + str(int(record['at']) % 60)
        data.append((record['nickname'], rec_time, record['status']))

    response = HttpResponse(data.xls, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = "attachment; filename=" + device.device_model + "_holiday_sch.xls"
    return response


def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv


def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv