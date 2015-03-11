/**

 *  Authors: Kruthika Rathinavel
 *  Version: 1.2.1
 *  Email: kruthika@vt.edu
 *  Created: "2014-10-13 18:45:40"
 *  Updated: "2015-02-13 15:06:41"


 * Copyright © 2014 by Virginia Polytechnic Institute and State University
 * All rights reserved

 * Virginia Polytechnic Institute and State University (Virginia Tech) owns the copyright for the BEMOSS software and its
 * associated documentation ("Software") and retains rights to grant research rights under patents related to
 * the BEMOSS software to other academic institutions or non-profit research institutions.
 * You should carefully read the following terms and conditions before using this software.
 * Your use of this Software indicates your acceptance of this license agreement and all terms and conditions.

 * You are hereby licensed to use the Software for Non-Commercial Purpose only.  Non-Commercial Purpose means the
 * use of the Software solely for research.  Non-Commercial Purpose excludes, without limitation, any use of
 * the Software, as part of, or in any way in connection with a product or service which is sold, offered for sale,
 * licensed, leased, loaned, or rented.  Permission to use, copy, modify, and distribute this compilation
 * for Non-Commercial Purpose to other academic institutions or non-profit research institutions is hereby granted
 * without fee, subject to the following terms of this license.

 * Commercial Use: If you desire to use the software for profit-making or commercial purposes,
 * you agree to negotiate in good faith a license with Virginia Tech prior to such profit-making or commercial use.
 * Virginia Tech shall have no obligation to grant such license to you, and may grant exclusive or non-exclusive
 * licenses to others. You may contact the following by email to discuss commercial use:: vtippatents@vtip.org

 * Limitation of Liability: IN NO EVENT WILL VIRGINIA TECH, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR REDISTRIBUTE
 * THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR
 * CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO
 * LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE
 * OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF VIRGINIA TECH OR OTHER PARTY HAS BEEN ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGES.

 * For full terms and conditions, please visit https://bitbucket.org/bemoss/bemoss_os.

 * Address all correspondence regarding this license to Virginia Tech's electronic mail address:: vtippatents@vtip.org

**/


/**
 * @author kruthika
 */
var _values_on_submit_plugload = {};

$( "#sp_on" ).click(function() {
	if ($("#sp_on").css('background-color') == "green") {
		//$(this).css('background-color','rgba(0, 0, 0, 0.40)');
	} else {
		$(this).css('background-color','green');
		$("#sp_off").css('background-color','rgba(222, 222, 222, 0.55)');
		status = 'ON';
	}
});

$( "#sp_off" ).click(function() {
	if ($("#sp_off").css('background-color') == "green") {
		//$(this).css('background-color','rgba(0, 0, 0, 0.40)');
	} else {
		$(this).css('background-color','green');
		$("#sp_on").css('background-color','rgba(222, 222, 222, 0.55)');
		status = 'OFF';
	}
});

//if (device_type_id != '3WSP') {
    //var setHeight = $("#power_con").height();
    //$("#statss").height(setHeight + 'px');
    //$(".btn-group").css('margin-top','40px').css('margin-bottom', '-10px');
//}

$( document ).ready(function() {
	$.csrftoken();

    if (device_type_id != '3WSP') {
        var gauge_target = document.getElementById("chart_9");
        var gauge = new Gauge(gauge_target);
    }

    var ws = new WebSocket("ws://" + window.location.host + "/socket_plugload");

     ws.onopen = function () {
         ws.send("WS opened from html page");
     };

     ws.onmessage = function (event) {
         var _data = event.data;
         _data = $.parseJSON(_data);
         var topic = _data['topic'];
         // ["", "ui", "web", "thermostat", "999", "Wifithermostat1", "device_status", "response"]
         if (topic) {
             topic = topic.split('/');
             console.log(topic);
             if (topic[5] == device_id && topic[6] == 'device_status') {
                 if ($.type( _data['message'] ) === "string"){
                     var _message = $.parseJSON(_data['message']);
                     change_plugload_values(_message);
                 } else if ($.type( _data['message'] ) === "object"){
                     change_plugload_values(_data['message']);
                 }

             }
             if (topic[5] == device_id && topic[6] == 'update') {
                 var message_upd = _data['message'];
                 if (message_upd.indexOf('success') > -1) {
                     change_plugload_values_on_success(_values_on_submit_plugload);
                     $('.bottom-right').notify({
                        message: { text: 'The changes made at '+update_time+" are now updated in the device!"},
                        type: 'blackgloss',
                         fadeOut: { enabled: true, delay: 5000 }
                      }).show();
                 }
             }
         }
     };

    (function get_plugload_data(){
	values = {
		    "device_info": device_info
		    };
	var jsonText = JSON.stringify(values);
	setTimeout(function()
	{
		$.ajax({
		  url : '/plugload_stat/',
		  type: 'POST',
		  data: jsonText,
		  dataType: 'json',
		  success : function(data) {
		  	//change_tstat_values(data);
		  	get_plugload_data();
		  },
		  error: function(data) {
			get_plugload_data();
		  }
		 });
	},60000);
	})();

    /*var options = {
        grid: {
                //background: 'rgba(0, 0, 0, 0.25)'
                background: 'transparent'

            },
        seriesDefaults: {
            renderer: $.jqplot.MeterGaugeRenderer,
            rendererOptions: {
                //diameter:'400',
                background:'transparent',
                ringColor:'rgba(222, 255, 222, 0.55)',
                ringWidth: '4',
                //label: 'Power(W)',
                //intervalOuterRadius: '140',
                ticks: [0, 250, 500, 750, 1000],
                tickColor: 'rgba(245, 245, 255, 1)'
                //intervals:[400,700,1000],
                //intervalColors:['#66cc66', '#E7E658', '#cc6666']
                //intervalColors:['rgba(102, 204, 102, 0.52)', 'rgba(231, 230, 88, 0.52)', 'rgba(204, 102, 102, 0.52)']
            }
        }
    };*/

            var popts = {
                lines: 12, // The number of lines to draw
                angle: 0.0, // The length of each line
                lineWidth: 0.2, // The line thickness2
                pointer: {
                    length: 0.8, // The radius of the inner circle
                    strokeWidth: 0.03, // The rotation offset
                    color: '#00000' // Fill color
                },
                limitMax: 'true',   // If true, the pointer will not go past the end of the gauge
                colorStart: '#6FADCF',   // Colors
                colorStop: '#8FC0DA',    // just experiment with them
                strokeColor: '#E0E0E0',   // to see which ones work best for you
                generateGradient: true,
                percentColors: [
                    [0, "#a9d70b" ],
                    [500, "#f9c802"],
                    [1000, "#ff0000"]
                ],
                //animationSpeed: 30,
                fontSize: 20
            };


    if (device_type_id != '3WSP') {
        if (power != "") {
            //var power_val = [power];
            //var power_meter = $.jqplot('chart9', [power_val], options);
            $("#power_val").text(power);
            var power_val = parseInt(power);
            gauge.setTextField(document.getElementById("9-textfield"));
            gauge.setOptions(popts);
            gauge.maxValue = 1000;
            gauge.set(power_val);

        } else {
            //var power_val = [0];
            //var power_meter = $.jqplot('chart9', [power_val], options);
        }
    }

    function change_plugload_values_on_success(data) {
		if (data.status == 'ON') {
			$("#sp_on").css('background-color','green');
			$("#sp_off").css('background-color','rgba(222, 222, 222, 0.55)');
		} else {
			$("#sp_off").css('background-color','green');
			$("#sp_on").css('background-color','rgba(222, 222, 222, 0.55)');
		}
	}

	function change_plugload_values(data) {
		if (data.status == 'ON') {
			$("#sp_on").css('background-color','green');
			$("#sp_off").css('background-color','rgba(222, 222, 222, 0.55)');
		} else {
			$("#sp_off").css('background-color','green');
			$("#sp_on").css('background-color','rgba(222, 222, 222, 0.55)');			
		}
        if (device_type_id != '3WSP') {
            if (data.power) {
                $("#power_val").text(data.power);
                /*if (power_meter) {
                    power_meter.destroy();
                }
                power_val = [data.power];
                power_meter = $.jqplot('chart9', [power_val], options);*/
                gauge.set(parseInt(data.power));

            }
        }
	}

	$( "#confirm_change" ).click(function(evt) {
		evt.preventDefault();
		update_time = new Date();
		update_time = update_time.toLocaleTimeString();
		var status;
		if ($("#sp_off").css('background-color') == "green" || $("#sp_off").css('background-color') == "rgb(0, 128, 0)")
			status = 'OFF';
		else if ($("#sp_on").css('background-color') == "green" || $("#sp_on").css('background-color') == "rgb(0, 128, 0)")
			status = 'ON';
		
		//if (status != device_status) {
			values = {
					"status":status,
					"device_info":device_info
			};
		//}
		_values_on_submit_plugload = values;
        submit_plugload_data(values)
	});

    function submit_plugload_data(values) {
        var jsonText = JSON.stringify(values);
	    console.log(jsonText);
		$.ajax({
			  url : '/update_plugload/',
			  type: 'POST',
			  data: jsonText,
			  dataType: 'json',
			  success : function(data) {
			  	/*$('.bottom-right').notify({
			  	    message: { text: 'Your changes will be updated shortly' },
			  	    type: 'blackgloss'
			  	  }).show();*/
			  },
			  error: function(data) {
                  submit_plugload_data(values);
				  $('.bottom-right').notify({
				  	    message: { text: 'Something went wrong when submitting the thermostat data. Please try again.' },
				  	    type: 'blackgloss',
                      fadeOut: { enabled: true, delay: 5000 }
				  	}).show();
			  }
			 });
    }

});