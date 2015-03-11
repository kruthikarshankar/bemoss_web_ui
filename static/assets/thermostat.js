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
 * 3/20/2014 - Functions to dynamically activate buttons in thermostat.html page
 */

var _values_on_submit = {};

//Modify color of thermostat mode  when clicked
$( "#shortcutcool" ).click(function() {
	//alert( "Handler for .click() called." );
	if ($("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.498039)" || $("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.5)") {
		//$(this).css('background-color','rgba(0, 0, 0, 0.40)');
	} else {
		$(this).css('background-color','rgba(0, 128, 0, 0.50)');
		tmode = 'COOL';
		$('#shortcuthsp').css('background-color',"rgba(255,255,255,0.4)");
		//$('#heatvalue').html('-');
		$('#heatminus').attr('disabled', "disabled");
		$('#heatplus').attr('disabled', "disabled");
		$('#shortcutcsp').css('background-color',"rgba(0,0,0,0.4)");
		//$('#coolvalue').html('60');
		//t_cool = 60;
		$('#coolminus').removeAttr('disabled');
		$('#coolplus').removeAttr('disabled');
	}
	if ($("#shortcutheat").css('background-color') == "rgba(0, 128, 0, 0.498039)" || $("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.5)") {
		$("#shortcutheat").css('background-color','rgba(0, 0, 0, 0.40)');
	} 
	/*if ($("#shortcutauto").css('background-color') == "rgba(0, 128, 0, 0.498039)" || $("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.5)") {
		$("#shortcutauto").css('background-color','rgba(0, 0, 0, 0.40)');
	} */
	if ($("#shortcutoff").css('background-color') == "rgba(0, 128, 0, 0.498039)" || $("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.5)") {
		$("#shortcutoff").css('background-color','rgba(0, 0, 0, 0.40)');
	} 
});

$( "#shortcutheat" ).click(function() {
	//alert( "Handler for .click() called." );
	if ($("#shortcutheat").css('background-color') == "rgba(0, 128, 0, 0.498039)" || $("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.5)") {
		//$(this).css('background-color','rgba(0, 0, 0, 0.40)');
	} else {
		$(this).css('background-color','rgba(0, 128, 0, 0.50)');
		tmode = 'HEAT';
		$('#shortcutcsp').css('background-color',"rgba(255,255,255,0.4)");
		//$('#coolvalue').html('-');
		$('#coolminus').attr('disabled', "disabled");
		$('#coolplus').attr('disabled', "disabled");
		$('#shortcuthsp').css('background-color',"rgba(0,0,0,0.4)");
		//$('#heatvalue').html('70');
		//t_heat = 70;
		$('#heatminus').removeAttr('disabled');
		$('#heatplus').removeAttr('disabled');
	}
	if ($("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.498039)" || $("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.5)") {
		$("#shortcutcool").css('background-color','rgba(0, 0, 0, 0.40)');
	} 
	/*if ($("#shortcutauto").css('background-color') == "rgba(0, 128, 0, 0.498039)" || $("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.5)") {
		$("#shortcutauto").css('background-color','rgba(0, 0, 0, 0.40)');
	} */
	if ($("#shortcutoff").css('background-color') == "rgba(0, 128, 0, 0.498039)" || $("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.5)") {
		$("#shortcutoff").css('background-color','rgba(0, 0, 0, 0.40)');
	} 
});

$( "#shortcutoff" ).click(function() {
	//alert( "Handler for .click() called." );
	if ($("#shortcutoff").css('background-color') == "rgba(0, 128, 0, 0.498039)" || $("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.5)") {
		//$(this).css('background-color','rgba(0, 0, 0, 0.40)');
	} else {
		$(this).css('background-color','rgba(0, 128, 0, 0.50)');
		tmode = 'OFF';
		$('#shortcutcsp').css('background-color',"rgba(255,255,255,0.4)");
		//$('#coolvalue').html('-');
		$('#coolminus').attr('disabled', "disabled");
		$('#coolplus').attr('disabled', "disabled");
		$('#shortcuthsp').css('background-color',"rgba(255,255,255,0.4)");
		//$('#heatvalue').html('-');
		$('#heatminus').attr('disabled', "disabled");
		$('#heatplus').attr('disabled', "disabled");
		//alert(tmode);
	}
	if ($("#shortcutheat").css('background-color') == "rgba(0, 128, 0, 0.498039)" || $("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.5)") {
		$("#shortcutheat").css('background-color','rgba(0, 0, 0, 0.40)');
	} 
	/*if ($("#shortcutauto").css('background-color') == "rgba(0, 128, 0, 0.498039)" || $("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.5)") {
		$("#shortcutauto").css('background-color','rgba(0, 0, 0, 0.40)');
	} */
	if ($("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.498039)" || $("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.5)") {
		$("#shortcutcool").css('background-color','rgba(0, 0, 0, 0.40)');
	} 
});


$( "#fanauto" ).click(function() {
	//alert( "Handler for .click() called." );
	if ($("#fanauto").css('background-color') == "rgba(0, 128, 0, 0.498039)" || $("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.5)") {
		//$(this).css('background-color','rgba(0, 0, 0, 0.40)');
	} else {
		$(this).css('background-color','rgba(0, 128, 0, 0.50)');
		fmode = 'AUTO';
		//alert(fmode);
	}
	/*if ($("#fancirculate").css('background-color') == "rgba(0, 128, 0, 0.498039)" || $("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.5)") {
		$("#fancirculate").css('background-color','rgba(0, 0, 0, 0.40)');
	} */
	if ($("#fanoff").css('background-color') == "rgba(0, 128, 0, 0.498039)") {
		$("#fanoff").css('background-color','rgba(0, 0, 0, 0.40)');
	} 
});

$( "#fanoff" ).click(function() {
	//alert( "Handler for .click() called." );
	if ($("#fanoff").css('background-color') == "rgba(0, 128, 0, 0.498039)" || $("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.5)") {
		//$(this).css('background-color','rgba(0, 0, 0, 0.40)');
	} else {
		$(this).css('background-color','rgba(0, 128, 0, 0.50)');
		fmode = 'ON';
		//alert(fmode);
	}
	/*if ($("#fancirculate").css('background-color') == "rgba(0, 128, 0, 0.498039)" || $("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.5)") {
		$("#fancirculate").css('background-color','rgba(0, 0, 0, 0.40)');
	} */
	if ($("#fanauto").css('background-color') == "rgba(0, 128, 0, 0.498039)" || $("#shortcutcool").css('background-color') == "rgba(0, 128, 0, 0.5)") {
		$("#fanauto").css('background-color','rgba(0, 0, 0, 0.40)');
	} 
});

//Change heat and cool set points with range check ( 0 to 120 F)

$('#heatplus').click(function(e){
        // Stop acting like a button
        e.preventDefault();
        // Get its current value
        var currentVal = parseFloat($("#heatvalue").text());
        // If is not undefined
        if (!isNaN(currentVal) && currentVal < 95) {
            // Increment
            $('#heatvalue').text(currentVal + 1);
            t_heat = t_heat + 1.0;
        } else {
            // Otherwise put a 0 there
            $('#heatvalue').text(95);
            t_heat = 95.0;
        }
    });

// This button will decrement the heat value till 0
$("#heatminus").click(function(e) {
        // Stop acting like a button
        e.preventDefault();
        // Get its current value
        var currentVal = parseFloat($("#heatvalue").text());
        // If it isn't undefined or its greater than 0
        if (!isNaN(currentVal) && currentVal > 35) {
            // Decrement one
            $('#heatvalue').text(currentVal - 1);
            t_heat = t_heat - 1.0;
        } else {
            // Otherwise put a 0 there
            $('#heatvalue').text(35);
            t_heat = 35;
        }
    });

$('#coolplus').click(function(e){
        // Stop acting like a button
        e.preventDefault();
        // Get its current value
        var currentVal = parseFloat($("#coolvalue").text());
        // If is not undefined
        if (!isNaN(currentVal) && currentVal < 95) {
            // Increment
            $('#coolvalue').text(currentVal + 1);
            t_cool = t_cool + 1.0;
        } else {
            // Otherwise put a 0 there
            $('#coolvalue').text(95);
            t_cool = 95;

        }
    });

// This button will decrement the heat value till 0
$("#coolminus").click(function(e) {
        // Stop acting like a button
        e.preventDefault();
        // Get its current value
        var currentVal = parseFloat($("#coolvalue").text());
        // If it isn't undefined or its greater than 0
        if (!isNaN(currentVal) && currentVal > 35) {
            // Decrement one
            $('#coolvalue').text(currentVal - 1);
            t_cool = t_cool - 1.0;
        } else {
            // Otherwise put a 0 there
            $('#coolvalue').text(35);
            t_cool = 35;
        }
    });

//End change heat and cool set points

var wifi3m50_update = 'update';
var update_time;
function changeValues(data) {
		$("#locateion").text(data.locat);
    	$("#humidity").text(data.humidity);
		$("#precip").text(data.precip+" in.");
		$("#winds").text(data.winds +" mph");
		$("#iconandtemp").html("<i class=\""+data.icon +"\"></i>"+" " +data.temp_f+" F");
		$("#weather").text(data.weather);
}


$( document ).ready(function() {
$.csrftoken();

 var ws = new WebSocket("ws://localhost:8081/socket_thermostat");
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
                        type: 'blackgloss'
                      }).show();
                 }
             }
         }
     };


function change_values_on_success_submit(data) {
    if (data.thermostat_mode === 'OFF') {
        $("#shortcutoff").css('background-color', 'rgba(0, 128, 0, 0.50)');
        $("#shortcutheat").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcutcool").css('background-color', 'rgba(0, 0, 0, 0.40)');
        //$("#shortcutauto").css('background-color', 'rgba(0, 0, 0, 0.40)');
    } else if (data.thermostat_mode === 'HEAT') {
        $("#shortcutoff").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcutheat").css('background-color', 'rgba(0, 128, 0, 0.50)');
        $("#shortcutcool").css('background-color', 'rgba(0, 0, 0, 0.40)');
        //$("#shortcutauto").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcutcsp").css('background-color', 'rgba(255, 255, 255, 0.4)');
        $("#coolplus").attr('disabled', 'disabled');
        $("#coolminus").attr('disabled', 'disabled');
        $("#shortcuthsp").css('background-color', 'rgba(0,0,0, 0.4)');
        $("#heatplus").removeAttr('disabled', 'disabled');
        $("#heatminus").removeAttr('disabled', 'disabled');
        $("#heatvalue").text(data.heat_setpoint);
    } else if (data.thermostat_mode === 'COOL') {
        $("#shortcutoff").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcutcool").css('background-color', 'rgba(0, 128, 0, 0.50)');
        $("#shortcutheat").css('background-color', 'rgba(0, 0, 0, 0.40)');
        //$("#shortcutauto").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcuthsp").css('background-color', 'rgba(255, 255, 255, 0.4)');
        $("#heatplus").attr('disabled', 'disabled');
        $("#heatminus").attr('disabled', 'disabled');
        $("#shortcutcsp").css('background-color', 'rgba(0,0,0, 0.4)');
        $("#coolplus").removeAttr('disabled', 'disabled');
        $("#coolminus").removeAttr('disabled', 'disabled');
        $("#coolvalue").text(data.cool_setpoint);
    } /*else if (data.thermostat_mode === 'AUTO') {
        $("#shortcutoff").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcutauto").css('background-color', 'rgba(0, 128, 0, 0.50)');
        $("#shortcutheat").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcutcool").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcuthsp").css('background-color', 'rgba(255, 255, 255, 0.4)');
        $("#heatplus").attr('disabled', 'disabled');
        $("#heatminus").attr('disabled', 'disabled');
        $("#shortcutcsp").css('background-color', 'rgba(255, 255, 255, 0.4)');
        $("#coolplus").attr('disabled', 'disabled');
        $("#coolminus").attr('disabled', 'disabled');
    } */

    if (data.fan_mode === 'ON') {
        $("#fanoff").css('background-color', 'rgba(0, 128, 0, 0.50)');
        //$("#fancirculate").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#fanauto").css('background-color', 'rgba(0, 0, 0, 0.40)');
    //} else if (data.fan_mode === 'CIRCULATE') {
        //$("#fanoff").css('background-color', 'rgba(0, 0, 0, 0.40)');
        //$("#fancirculate").css('background-color', 'rgba(0, 128, 0, 0.50)');
        //$("#fanauto").css('background-color', 'rgba(0, 0, 0, 0.40)');
    } else if (data.fan_mode === 'AUTO') {
        //$("#fancirculate").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#fanoff").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#fanauto").css('background-color', 'rgba(0, 128, 0, 0.50)');
    }
}


function change_tstat_values(data) {
	$('#indoortemp').html(data.temperature+"&deg;F");
    if (data.thermostat_mode === 'OFF') {
        $("#shortcutoff").css('background-color', 'rgba(0, 128, 0, 0.50)');
        $("#shortcutheat").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcutcool").css('background-color', 'rgba(0, 0, 0, 0.40)');
        //$("#shortcutauto").css('background-color', 'rgba(0, 0, 0, 0.40)');
    } else if (data.thermostat_mode === 'HEAT') {
        $("#shortcutoff").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcutheat").css('background-color', 'rgba(0, 128, 0, 0.50)');
        $("#shortcutcool").css('background-color', 'rgba(0, 0, 0, 0.40)');
        //$("#shortcutauto").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcutcsp").css('background-color', 'rgba(255, 255, 255, 0.4)');
        $("#coolplus").attr('disabled', 'disabled');
        $("#coolminus").attr('disabled', 'disabled');
        $("#coolvalue").text(data.cool_setpoint);
        $("#shortcuthsp").css('background-color', 'rgba(0,0,0, 0.4)');
        $("#heatplus").removeAttr('disabled', 'disabled');
        $("#heatminus").removeAttr('disabled', 'disabled');
        $("#heatvalue").text(data.heat_setpoint);
    } else if (data.thermostat_mode === 'COOL') {
        $("#shortcutoff").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcutcool").css('background-color', 'rgba(0, 128, 0, 0.50)');
        $("#shortcutheat").css('background-color', 'rgba(0, 0, 0, 0.40)');
        //$("#shortcutauto").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcuthsp").css('background-color', 'rgba(255, 255, 255, 0.4)');
        $("#heatplus").attr('disabled', 'disabled');
        $("#heatminus").attr('disabled', 'disabled');
        $("#heatvalue").text(data.heat_setpoint);
        $("#shortcutcsp").css('background-color', 'rgba(0,0,0, 0.4)');
        $("#coolplus").removeAttr('disabled', 'disabled');
        $("#coolminus").removeAttr('disabled', 'disabled');
        $("#coolvalue").text(data.cool_setpoint);
    } /*else if (data.thermostat_mode === 'AUTO') {
        $("#shortcutoff").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcutauto").css('background-color', 'rgba(0, 128, 0, 0.50)');
        $("#shortcutheat").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcutcool").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcuthsp").css('background-color', 'rgba(255, 255, 255, 0.4)');
        $("#heatplus").attr('disabled', 'disabled');
        $("#heatminus").attr('disabled', 'disabled');
        $("#heatvalue").text(data.heat_setpoint);
        $("#shortcutcsp").css('background-color', 'rgba(255, 255, 255, 0.4)');
        $("#coolplus").attr('disabled', 'disabled');
        $("#coolminus").attr('disabled', 'disabled');
        $("#coolvalue").text(data.cool_setpoint);
    } else {
        $("#shortcutoff").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcutauto").css('background-color', 'rgba(0, 128, 0, 0.50)');
        $("#shortcutheat").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcutcool").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#shortcuthsp").css('background-color', 'rgba(255, 255, 255, 0.4)');
        $("#heatplus").attr('disabled', 'disabled');
        $("#heatminus").attr('disabled', 'disabled');
        $("#heatvalue").text(data.heat_setpoint);
        $("#shortcutcsp").css('background-color', 'rgba(255, 255, 255, 0.4)');
        $("#coolplus").attr('disabled', 'disabled');
        $("#coolminus").attr('disabled', 'disabled');
        $("#coolvalue").text(data.cool_setpoint);
    } */
    if (data.fan_mode === 'ON') {
        $("#fanoff").css('background-color', 'rgba(0, 128, 0, 0.50)');
        //$("#fancirculate").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#fanauto").css('background-color', 'rgba(0, 0, 0, 0.40)');
    //} else if (data.fan_mode === 'CIRCULATE') {
        //$("#fanoff").css('background-color', 'rgba(0, 0, 0, 0.40)');
        //$("#fancirculate").css('background-color', 'rgba(0, 128, 0, 0.50)');
        //$("#fanauto").css('background-color', 'rgba(0, 0, 0, 0.40)');
    } else if (data.fan_mode === 'AUTO') {
        //$("#fancirculate").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#fanoff").css('background-color', 'rgba(0, 0, 0, 0.40)');
        $("#fanauto").css('background-color', 'rgba(0, 128, 0, 0.50)');
    }
	
	$("#heatvalue").innerHTML = data.heat_setpoint;
	$("#coolvalue").innerHTML = data.cool_setpoint;

}

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

	if (tmode == 'HEAT') {
		var values = {
			    "thermostat_mode": tmode,
			    "fan_mode": fmode,
			    "heat_setpoint": t_heat,
			    "device_info":device_info
			    //"hold": hold
			    };
	} else if (tmode == 'COOL') {
		var values = {
			    "thermostat_mode": tmode,
			    "fan_mode": fmode,
			    "cool_setpoint": t_cool,
			    "device_info":device_info
			    //"hold": hold
			    };
	} else {
		var values = {
			    "thermostat_mode": tmode,
			    "fan_mode": fmode,
			    "device_info":device_info
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
                        type: 'blackgloss'
                    }).show();
              }
		 });
    }


});