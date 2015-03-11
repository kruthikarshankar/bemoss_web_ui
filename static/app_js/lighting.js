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
 * 7/14/2014 - Functions to dynamically control lighting.html page
 */

var _values_on_submit_lighting = {};

//Modify status	 when clicked
$( "#light_on" ).click(function() {
	if ($("#light_on").css('background-color') == "green") {
		//$(this).css('background-color','rgba(0, 0, 0, 0.40)');
	} else {
		$(this).css('background-color','green');
		$("#light_off").css('background-color','rgba(222, 222, 222, 0.55)');
		status = 'ON';
        $('#brightness').slider('value', '100');
        $('#brightness').slider('enable');
        $('#brightness_value').val('100%');
	}
});

$( "#light_off" ).click(function() {
	if ($("#light_off").css('background-color') == "green") {
		//$(this).css('background-color','rgba(0, 0, 0, 0.40)');
	} else {
		$(this).css('background-color','green');
		$("#light_on").css('background-color','rgba(222, 222, 222, 0.55)');
		status = 'OFF';
        $('#brightness').slider('value', '0');
        $('#brightness').slider('disable');
        $('#brightness_value').val('0%');
	}
});
$(function() {
    if (_type == '2SDB') {
        $("#brightness").slider({
            value: brightness,
            orientation: "horizontal",
            range: "min",
            animate: true,
            min: 0,
            max: 100,
            step: 50,
            slide: function (event, ui) {
                $("#brightness_value").val(ui.value + "%");
            }
        });
    } else {
        $("#brightness").slider({
            value: brightness,
            orientation: "horizontal",
            range: "min",
            animate: true,
            min: 0,
            max: 100,
            slide: function (event, ui) {
                $("#brightness_value").val(ui.value + "%");
            }
        });
    }

    /*$("#saturation").slider({
        value: saturation,
        orientation: "horizontal",
        range: "min",
        animate: true,
        min: 0,
        max: 100,
        slide: function (event, ui) {
            $("#saturation_value").val(ui.value + "%");
        }
    });*/

    $("#brightness_value").val($("#brightness").slider("value") + "%");
    //$("#saturation_value").val($("#saturation").slider("value") + "%");
    $(".slider").slider("float");


    //$("#saturation").slider('disable');
    //$("#saturation_value").val('');
    if (_type == '2WL') {
        $('#brightness').slider("disable");
        $("#brightness_value").val('');
        $('#dim_container').css('background-color', 'rgba(255, 255, 255, 0.4)');
    }

    /*if (_type == '2HUE') {
        $("#saturation").slider('enable');
        $("#saturation_value").val($("#saturation").slider("value") + "%");
    }*/

    if (_type == '2HUE') {
        $('#color_container').show();
        if (role == 'admin' || zone == uzone) {
            $('.color-box').colpick({
                colorScheme:'dark',
                layout:'rgbhex',
                color:color,
                submit:0,
                onChange:function(hsb,hex,rgb,el) {
                    $(el).css('background-color', 'rgb('+rgb.r+','+rgb.g+','+rgb.b+')');
                }
            })
            .css('background-color', color);
        } else {
            $('#color_container').css('background-color', color);
        }
    } else {
        $('#color_container').css('background-color','rgba(255, 255, 255, 0.4)');
        //$('#saturation_container').css('background-color','rgba(255, 255, 255, 0.4)');
    }

     if (role != 'admin' && uzone != zone) {
         $('#brightness').slider("disable");

    }
});

$( document ).ready(function() {
$.csrftoken();


    console.log("ws://" + window.location.host + "/socket_lighting");
    var ws = new WebSocket("ws://" + window.location.host + "/socket_lighting");
    console.log("websocket connection established");
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
                     change_lighting_values(_message);
                 } else if ($.type( _data['message'] ) === "object"){
                     change_lighting_values(_data['message']);
                 }

             }
             if (topic[5] == device_id && topic[6] == 'update') {
                 var message_upd = _data['message'];
                 if (message_upd.indexOf('success') > -1) {
                     change_lighting_values(_values_on_submit_lighting);
                     $('.bottom-right').notify({
                        message: { text: 'The changes made at '+update_time+" are now updated in the device!"},
                        type: 'blackgloss',

                         fadeOut: { enabled: true, delay: 5000 }
                      }).show();
                 }
             }
         }
     };


    function change_lighting_values(data) {
        if (data.status == 'ON') {
            $("#light_on").css('background-color', 'green');
            $("#light_off").css('background-color', 'rgba(222, 222, 222, 0.55)');
            if (data.brightness) {
                if ($("#brightness").slider("option", "disabled", true) && (role == 'admin' || uzone == zone)) {
                    $('#brightness').slider('enable');
                }
            }
            status = 'ON';
		} else {
			$("#light_off").css('background-color','green');
			$("#light_on").css('background-color','rgba(222, 222, 222, 0.55)');
            status = 'OFF';
            $('#brightness').slider('disable');
		}

        if (data.brightness) {
            $('#brightness').slider({ value: data.brightness });
            $("#brightness_value").val(data.brightness + "%");
        }

        /*if (data.saturation && _type == '2HUE') {
            $('#saturation').slider({ value: data.saturation });
            $("#saturation_value").val(data.saturation + "%");
        }*/

        if (data.color && _type == '2HUE') {
            var _color = data.color;
            _color = _color.toString();
            if (_color.indexOf('rgb') > -1) {}
            else {
                if (_color.indexOf('(') > -1) {
                    _color = 'rgb' + _color;
                } else {
                    _color = 'rgb(' + _color + ')';
                }
            }
            $('.color-box').colpick({ color: _color });
            $('.color-box').css('background-color', _color);
        }
    }


(function get_lighting_data(){
	values = {
		    "device_info": device_info
		    };
	var jsonText = JSON.stringify(values);
	setTimeout(function()
	{
		$.ajax({
		  url : '/lt_stat/',
		  type: 'POST',
		  data: jsonText,
		  dataType: 'json',
		  success : function(data) {
		  	get_lighting_data();
		  },
		  error: function(data) {
			get_lighting_data();
		  }
		 });
	},60000);
	})();


$( "#submit_lighting_data" ).click(function(evt) {
	evt.preventDefault();
	update_time = new Date();
	update_time = update_time.toLocaleTimeString();
	//alert(update_time);
	var status;
	if ($("#light_off").css('background-color') == "green" || $("#light_off").css('background-color') == "rgb(0, 128, 0)")
		status = 'OFF';
	else if ($("#light_on").css('background-color') == "green" || $("#light_on").css('background-color') == "rgb(0, 128, 0)")
		status = 'ON';


    if (_type == '2WL') {
        var values = {
		    "status": status,
		    "device_info":device_info
		    };
    } else if (_type == '2SDB' || _type == '2DB' || _type == '2WSL') {
        var values = {
		    "brightness": parseFloat($( "#brightness_value" ).val().replace("%","")),
		    "status": status,
		    "device_info":device_info
		    };
    } else if (_type == '2HUE') {
        var lt_color = $('.color-box').css('background-color').toString();
        lt_color = lt_color.replace('rgb','');
        if (lt_color.indexOf('a(') > -1) {
            lt_color = '(255,255,255)';
        }
        var values = {
		    "brightness": parseFloat($( "#brightness_value" ).val().replace("%","")),
		    "color": lt_color,
		    "status": status,
		    //"saturation": parseFloat($( "#saturation_value" ).val().replace("%","")),
		    "device_info":device_info
		    };
    }
    _values_on_submit_lighting = values;
    submit_lighting_data(values);

});


function submit_lighting_data(values) {
    var jsonText = JSON.stringify(values);
    console.log(jsonText);
	$.ajax({
		  url : '/update_light/',
		  type: 'POST',
		  data: jsonText,
		  dataType: 'json',
		  success : function(data) {
			//lighting_data_updated();
		  	/*$('.bottom-right').notify({
		  	    message: { text: 'Your settings will be updated shortly' },
		  	    type: 'blackgloss'
		  	  }).show();*/
		  },
		  error: function(data) {
              submit_lighting_data(values);
			  $('.bottom-right').notify({
			  	    message: { text: 'Something went wrong when submitting the data. Please try again.' },
			  	    type: 'blackgloss',
                  fadeOut: { enabled: true, delay: 5000 }
			  	}).show();
		  }
		 });
}

});