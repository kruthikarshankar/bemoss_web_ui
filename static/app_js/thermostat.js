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
 * Created by kruthika on 10/19/14.
 */
var _values_on_submit = {};
$(onStart); //short-hand for $(document).ready(onStart);
function onStart($) {

    //if (device_type_id == '1NST') {
    if (override_th == 'True') {
        $("#override_yes").removeClass('btn-default').addClass('btn-success');
        $("#override_no").removeClass('btn-success').addClass('btn-default');
    } else {
        $("#override_no").removeClass('btn-default').addClass('btn-success');
        $("#override_yes").removeClass('btn-success').addClass('btn-default');
    }
    //}

    if (mode == 'HEAT') {
        $("#th_heat").removeClass('btn-default').addClass('btn-success');
        $("#th_cool").removeClass('btn-success').addClass('btn-default');
        $("#th_off").removeClass('btn-success').addClass('btn-default');
        $("#coolplus").prop('disabled', true);
        $("#coolminus").prop('disabled', true);
        $("#heatplus").prop('disabled', false);
        $("#heatminus").prop('disabled', false);
        if (role != 'admin' && uzone != zone) {
           $("#heatplus").prop('disabled', true);
           $("#heatminus").prop('disabled', true);
        }
    } else if (mode == 'COOL') {
        $("#th_cool").removeClass('btn-default').addClass('btn-success');
        $("#th_heat").removeClass('btn-success').addClass('btn-default');
        $("#th_off").removeClass('btn-success').addClass('btn-default');
        $("#heatplus").prop('disabled', true);
        $("#heatminus").prop('disabled', true);
        $("#coolplus").prop('disabled', false);
        $("#coolminus").prop('disabled', false);
        if (role != 'admin' && uzone != zone) {
           $("#coolplus").prop('disabled', true);
            $("#coolminus").prop('disabled', true);
        }
    } else if (mode == 'OFF') {
        $("#th_off").removeClass('btn-default').addClass('btn-success');
        $("#th_heat").removeClass('btn-success').addClass('btn-default');
        $("#th_cool").removeClass('btn-success').addClass('btn-default');
        $("#coolplus").prop('disabled', true);
        $("#coolminus").prop('disabled', true);
        $("#heatplus").prop('disabled', true);
        $("#heatminus").prop('disabled', true);
    }

    if (fan_mode == 'AUTO') {
        $("#fan_auto").removeClass('btn-default').addClass('btn-success');
        $("#fan_on").removeClass('btn-success').addClass('btn-default');
    } else {
        $("#fan_on").removeClass('btn-default').addClass('btn-success');
        $("#fan_auto").removeClass('btn-success').addClass('btn-default');
    }
}

$( document ).ready(function() {
    $.csrftoken();

    var ws = new WebSocket("ws://" + window.location.host + "/socket_thermostat");
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
                     change_tstat_values(_message);
                 } else if ($.type( _data['message'] ) === "object"){
                     change_tstat_values(_data['message']);
                 }

             }
             if (topic[5] == device_id && topic[6] == 'update') {
                 var message_upd = _data['message'];
                 if (message_upd.indexOf('success') > -1) {
                     change_values_on_success_submit(_values_on_submit);
                     $('.bottom-right').notify({
                        message: { text: 'The changes made at '+update_time+" are now updated in the device!"},
                        type: 'blackgloss',

                         fadeOut: { enabled: true, delay: 5000 }
                      }).show();
                 }
             }
         }
     };


function change_values_on_success_submit(data) {
    if (data.thermostat_mode == 'OFF') {
        $("#th_off").removeClass('btn-default').addClass('btn-success');
        $("#th_heat").removeClass('btn-success').addClass('btn-default');
        $("#th_cool").removeClass('btn-success').addClass('btn-default');
        $("#coolplus").prop('disabled', true);
        $("#coolminus").prop('disabled', true);
        $("#heatplus").prop('disabled', true);
        $("#heatminus").prop('disabled', true);
    } else if (data.thermostat_mode == 'HEAT') {
        $("#th_heat").removeClass('btn-default').addClass('btn-success');
        $("#th_off").removeClass('btn-success').addClass('btn-default');
        $("#th_cool").removeClass('btn-success').addClass('btn-default');
        $("#coolplus").prop('disabled', true);
        $("#coolminus").prop('disabled', true);
        $("#heatplus").prop('disabled', false);
        $("#heatminus").prop('disabled', false);
        if (role != 'admin' && uzone != zone) {
           $("#heatplus").prop('disabled', true);
           $("#heatminus").prop('disabled', true);
        }
    } else if (data.thermostat_mode == 'COOL') {
        $("#th_cool").removeClass('btn-default').addClass('btn-success');
        $("#th_off").removeClass('btn-success').addClass('btn-default');
        $("#th_heat").removeClass('btn-success').addClass('btn-default');
        $("#coolplus").prop('disabled', false);
        $("#coolminus").prop('disabled', false);
        $("#heatplus").prop('disabled', true);
        $("#heatminus").prop('disabled', true);
        if (role != 'admin' && uzone != zone) {
           $("#coolplus").prop('disabled', true);
            $("#coolminus").prop('disabled', true);
        }

    }
    if (data.fan_mode == 'ON') {
        $("#fan_on").removeClass('btn-default').addClass('btn-success');
        $("#fan_auto").removeClass('btn-success').addClass('btn-default');
    } else if (data.fan_mode == 'AUTO') {
        $("#fan_auto").removeClass('btn-default').addClass('btn-success');
        $("#fan_on").removeClass('btn-success').addClass('btn-default');
    }

    if ((data.override).toString().toLowerCase() == 'true') {
        $("#override_yes").removeClass('btn-default').addClass('btn-success');
        $('#override_no').removeClass('btn-success').addClass('btn-default');
    } else {
        $("#override_no").removeClass('btn-default').addClass('btn-success');
        $('#override_yes').removeClass('btn-success').addClass('btn-default');
    }

    if (device_type_id == '1NST') {
        $(".progress-bar").css("width", (data.battery).toString() + "%");
        $(".sr-only").text((data.battery).toString() + " %");
        $("#battery_lvl").text((data.battery).toString() + " %");
    }
}


function change_tstat_values(data) {
	$("#indoor_temp").text(data.temperature);
    if (data.thermostat_mode == 'OFF') {
        $("#th_off").removeClass('btn-default').addClass('btn-success');
        $("#th_heat").removeClass('btn-success').addClass('btn-default');
        $("#th_cool").removeClass('btn-success').addClass('btn-default');
        $("#coolplus").prop('disabled', true);
        $("#coolminus").prop('disabled', true);
        $("#heatplus").prop('disabled', true);
        $("#heatminus").prop('disabled', true);
    } else if (data.thermostat_mode == 'HEAT') {
        $("#th_heat").removeClass('btn-default').addClass('btn-success');
        $("#th_off").removeClass('btn-success').addClass('btn-default');
        $("#th_cool").removeClass('btn-success').addClass('btn-default');
        $("#coolplus").prop('disabled', true);
        $("#coolminus").prop('disabled', true);
        $("#heatplus").prop('disabled', false);
        $("#heatminus").prop('disabled', false);
        if (role != 'admin' && uzone != zone) {
           $("#heatplus").prop('disabled', true);
           $("#heatminus").prop('disabled', true);
        }
    } else if (data.thermostat_mode == 'COOL') {
        $("#th_cool").removeClass('btn-default').addClass('btn-success');
        $("#th_off").removeClass('btn-success').addClass('btn-default');
        $("#th_heat").removeClass('btn-success').addClass('btn-default');
        $("#coolplus").prop('disabled', false);
        $("#coolminus").prop('disabled', false);
        $("#heatplus").prop('disabled', true);
        $("#heatminus").prop('disabled', true);
        if (role != 'admin' && uzone != zone) {
           $("#coolplus").prop('disabled', true);
            $("#coolminus").prop('disabled', true);
        }

    }
    if (data.fan_mode == 'ON') {
        $("#fan_on").removeClass('btn-default').addClass('btn-success');
        $("#fan_auto").removeClass('btn-success').addClass('btn-default');
    } else if (data.fan_mode == 'AUTO') {
        $("#fan_auto").removeClass('btn-default').addClass('btn-success');
        $("#fan_on").removeClass('btn-success').addClass('btn-default');
    }
	$("#heat_setpoint").text(data.heat_setpoint);
    $("#cool_setpoint").text(data.cool_setpoint);

    if ((data.override).toString().toLowerCase() == 'true') {
        $("#override_yes").removeClass('btn-default').addClass('btn-success');
        $('#override_no').removeClass('btn-success').addClass('btn-default');
    } else {
        $("#override_no").removeClass('btn-default').addClass('btn-success');
        $('#override_yes').removeClass('btn-success').addClass('btn-default');
    }

    if (device_type_id == '1NST') {
        $(".progress-bar").css("width", (data.battery).toString() + "%");
        $(".sr-only").text((data.battery).toString() + " %");
        $("#battery_lvl").text((data.battery).toString() + " %");
    }

}

    $("#override_no").click(function(e) {
        e.preventDefault();
            if ($(this).hasClass('btn-success')) {
                $(this).removeClass('btn-success').addClass('btn-default');
                $('#override_yes').removeClass('btn-default').addClass('btn-success');
            } else {
                $(this).removeClass('btn-default').addClass('btn-success');
                $('#override_yes').removeClass('btn-success').addClass('btn-default');
            }
    });

    $("#override_yes").click(function(e) {
        e.preventDefault();
            if ($(this).hasClass('btn-success')) {
                $(this).removeClass('btn-success').addClass('btn-default');
                $('#override_no').removeClass('btn-default').addClass('btn-success');
            } else {
                $(this).removeClass('btn-default').addClass('btn-success');
                $('#override_no').removeClass('btn-success').addClass('btn-default');
            }
    });

    $('#th_heat').click(function (e) {
        e.preventDefault();
        if ($(this).hasClass('btn-default')) {
            $(this).removeClass('btn-default').addClass('btn-success');
            $("#th_cool").removeClass('btn-success').addClass('btn-default');
            $("#th_off").removeClass('btn-success').addClass('btn-default');
            $("#coolplus").prop('disabled', true);
            $("#coolminus").prop('disabled', true);
            $("#heatplus").prop('disabled', false);
            $("#heatminus").prop('disabled', false);
        }
    });

    $('#th_cool').click(function (e) {
        e.preventDefault();
        if ($(this).hasClass('btn-default')) {
            $(this).removeClass('btn-default').addClass('btn-success');
            $("#th_heat").removeClass('btn-success').addClass('btn-default');
            $("#th_off").removeClass('btn-success').addClass('btn-default');
            $("#heatplus").prop('disabled', true);
            $("#heatminus").prop('disabled', true);
            $("#coolplus").prop('disabled', false);
            $("#coolminus").prop('disabled', false);
        }
    });

    $('#th_off').click(function (e) {
        e.preventDefault();
        if ($(this).hasClass('btn-default')) {
            $(this).removeClass('btn-default').addClass('btn-success');
            $("#th_heat").removeClass('btn-success').addClass('btn-default');
            $("#th_cool").removeClass('btn-success').addClass('btn-default');
            $("#coolplus").prop('disabled', true);
            $("#coolminus").prop('disabled', true);
            $("#heatplus").prop('disabled', true);
            $("#heatminus").prop('disabled', true);
        }
    });

    $('#fan_auto').click(function (e) {
        e.preventDefault();
        if ($(this).hasClass('btn-default')) {
            $(this).removeClass('btn-default').addClass('btn-success');
            $("#fan_on").removeClass('btn-success').addClass('btn-default');
        }
    });

    $('#fan_on').click(function (e) {
        e.preventDefault();
        if ($(this).hasClass('btn-default')) {
            $(this).removeClass('btn-default').addClass('btn-success');
            $("#fan_auto").removeClass('btn-success').addClass('btn-default');
        }
    });


    $('#heatplus').click(function (e) {
        e.preventDefault();
        var currentVal = parseInt($("#heat_setpoint").text());
        if (!isNaN(currentVal) && currentVal < 95) {
            $('#heat_setpoint').text(currentVal + 1);
        } else {
            $('#heat_setpoint').text(95);
        }
    });

    $("#heatminus").click(function (e) {
        e.preventDefault();
        var currentVal = parseInt($("#heat_setpoint").text());
        if (!isNaN(currentVal) && currentVal > 35) {
            $('#heat_setpoint').text(currentVal - 1);
        } else {
            $('#heat_setpoint').text(35);
        }
    });

    $('#coolplus').click(function (e) {
        e.preventDefault();
        var currentVal = parseInt($("#cool_setpoint").text());
        if (!isNaN(currentVal) && currentVal < 95) {
            $('#cool_setpoint').text(currentVal + 1);
        } else {
            $('#cool_setpoint').text(95);
        }
    });

    $("#coolminus").click(function (e) {
        e.preventDefault();
        var currentVal = parseInt($("#cool_setpoint").text());
        if (!isNaN(currentVal) && currentVal > 35) {
            $('#cool_setpoint').text(currentVal - 1);
        } else {
            $('#cool_setpoint').text(35);
        }
    });



    (function weatherloop(){
	setTimeout(function()
	{
		$.ajax({
		  url : '/weather/',
		  type: 'GET',
		  //dataType : "json",
		  success : function(data) {
		  	changeValues(data);
		  	weatherloop();
		  },
		  error: function(data) {
		  	weatherloop();
		  }
		  //timeout: 3000
		 });
	},3000000);
	})();


    (function get_thermostat_data(){
	values = {
		    "device_info": device_info
		    };
	var jsonText = JSON.stringify(values);
	setTimeout(function()
	{
		$.ajax({
		  url : '/thstat/',
		  type: 'POST',
		  data: jsonText,
		  dataType: 'json',
		  success : function(data) {
		  	//change_tstat_values(data);
		  	get_thermostat_data();
		  },
		  error: function(data) {
			get_thermostat_data();
		  }
		 });
	},60000);
	})();

$( "#submitthermostatdata" ).click(function(evt) {
	evt.preventDefault();
	update_time = new Date();
	update_time = update_time.toLocaleTimeString();
    var tmode = 'HEAT';
    var fmode = 'AUTO';
    if ($("#th_heat").hasClass('btn-success')) {
        tmode = 'HEAT';
    } else if ($("#th_cool").hasClass('btn-success')) {
        tmode = 'COOL';
    } else {
        tmode = 'OFF';
    }

    if ($("#fan_auto").hasClass('btn-success')) {
        fmode = 'AUTO';
    } else if ($("#fan_on").hasClass('btn-success')) {
        fmode = 'ON';
    }

    if ($("#override_yes").hasClass('btn-success')) {
        override_th = true;
    } else {
        override_th = false;
    }

    var heat_setpoint = $("#heat_setpoint").text();
    var cool_setpoint = $("#cool_setpoint").text();

	if (tmode == 'HEAT') {
		var values = {
			    "thermostat_mode": tmode,
			    "fan_mode": fmode,
			    "heat_setpoint": parseFloat(heat_setpoint),
			    "device_info":device_info,
			    "override": override_th
			    };
	} else if (tmode == 'COOL') {
		var values = {
			    "thermostat_mode": tmode,
			    "fan_mode": fmode,
			    "cool_setpoint": parseFloat(cool_setpoint),
			    "device_info":device_info,
			    "override": override_th
			    };
	} else {
		var values = {
			    "thermostat_mode": tmode,
			    "fan_mode": fmode,
			    "device_info":device_info,
                "override": override_th
			    };
	}
    _values_on_submit = values;
    submit_thermostat_data(values);

});

    function submit_thermostat_data(values) {
        var jsonText = JSON.stringify(values);
        console.log(jsonText);
        $.ajax({
              url : '/submitdata3m50/',
              type: 'POST',
              data: jsonText,
              dataType: 'json',
              success : function(data) {
                wifi3m50_update = data.update_number;
                /*wifi_3m50_data_updated(wifi3m50_update);
                $('.bottom-right').notify({
                    message: { text: 'Your thermostat settings will be updated shortly' },
                    type: 'blackgloss'
                  }).show(); */
              },
              error: function(data) {
                  submit_thermostat_data(values);
                  $('.bottom-right').notify({
                        message: { text: 'Something went wrong when submitting the thermostat data. Please try again.' },
                        type: 'blackgloss',
                      fadeOut: { enabled: true, delay: 5000 }
                    }).show();
              }
		 });
    }

});