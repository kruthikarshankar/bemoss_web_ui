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




$( document ).ready(function() {
    $.csrftoken();

    //var nick_re = /^[A-Za-z0-9_ ]*[A-Za-z0-9 ][A-Za-z0-9_ ]{5,10}$/;
    var nick_re = /^[A-Za-z0-9 ]{6,10}$/;

    $('body').on('click',"button[id^='hplus-']", function (e) {
        // Stop acting like a button
        e.preventDefault();
        // Get its current value
        var zone_id = this.id;
        zone_id = zone_id.split("-");
        zone_id = zone_id[1];
        var currentVal = parseFloat($("#heat_sp-"+zone_id).text());
        // If is not undefined
        if (!isNaN(currentVal) && currentVal < 95) {
            // Increment
            $("#heat_sp-"+zone_id).text(currentVal + 1);
        } else {
            // Otherwise put a 0 there
            $("#heat_sp-"+zone_id).text(95);
        }
    });

// This button will decrement the heat value till 0
    $('body').on('click',"button[id^='hminus-']", function (e) {
        // Stop acting like a button
        e.preventDefault();
        // Get its current value
        var zone_id = this.id;
        zone_id = zone_id.split("-");
        zone_id = zone_id[1];
        var currentVal = parseFloat($("#heat_sp-"+zone_id).text());
        // If it isn't undefined or its greater than 0
        if (!isNaN(currentVal) && currentVal > 35) {
            // Decrement one
            $("#heat_sp-"+zone_id).text(currentVal - 1);
        } else {
            // Otherwise put a 0 there
            $("#heat_sp-"+zone_id).text(35);
        }
    });

    $('body').on('click',"button[id^='cplus-']", function (e) {
        // Stop acting like a button
        e.preventDefault();
        // Get its current value
        var zone_id = this.id;
        zone_id = zone_id.split("-");
        zone_id = zone_id[1];
        var currentVal = parseFloat($("#cool_sp-"+zone_id).text());
        // If is not undefined
        if (!isNaN(currentVal) && currentVal < 95) {
            // Increment
            $("#cool_sp-"+zone_id).text(currentVal + 1);
        } else {
            // Otherwise put a 0 there
            $("#cool_sp-"+zone_id).text(95);
        }
    });

// This button will decrement the heat value till 0
    $('body').on('click',"button[id^='cminus-']", function (e) {
        // Stop acting like a button
        e.preventDefault();
        // Get its current value
        var zone_id = this.id;
        zone_id = zone_id.split("-");
        zone_id = zone_id[1];
        var currentVal = parseFloat($("#cool_sp-"+zone_id).text());
        // If it isn't undefined or its greater than 0
        if (!isNaN(currentVal) && currentVal > 35) {
            // Decrement one
           $("#cool_sp-"+zone_id).text(currentVal - 1);
        } else {
            // Otherwise put a 0 there
           $("#cool_sp-"+zone_id).text(35);
        }
    });

    $("#add_new_zone_submit").click(function (evt) {
            evt.preventDefault();
            values = $("#add_new_zone").val();
            if (!nick_re.test(values)) {
                document.getElementById("newzoneerror").innerHTML = "Nickname can only contain letters and numbers and a space. Please try again.";
                document.getElementById(values).value = "";
            } else {
                $.ajax({
                    url: '/add_new_zone/',
                    type: 'POST',
                    data: values,
                    success: function (data) {
                        if (data == "invalid") {
                            document.getElementById("newzoneerror").innerHTML = "Your nickname was not accepted by BEMOSS. Please try again.";
                        } else {
                            location.reload();
                            $('.bottom-right').notify({
                                message: { text: 'A new zone was added.' },
                                type: 'blackgloss',
                                fadeOut: { enabled: true, delay: 5000 }
                            }).show();
                        }
                    },
                    error: function (data) {
                        $('.bottom-right').notify({
                            message: { text: 'Oh snap! Try submitting again. ' },
                            type: 'blackgloss',
                            fadeOut: { enabled: true, delay: 5000 }
                        }).show();
                    }
                });
            }
        });

    $(".save_changes_zn").click(function (evt) {
        evt.preventDefault();
        values = this.id.split('-');
        zone_id = values[1];
        values = values[1] + "_znickname";
        var value_er = values;
        znickname = $("#" + values).val();
        var error_id = "zonenickname_" + zone_id;
        if (!nick_re.test(znickname)) {
            document.getElementById(error_id).innerHTML = "Nickname error. Please try again.";
            document.getElementById(values).value = "";
        } else {
            values = {
                "id": zone_id,
                "nickname": znickname
            };
            var jsonText = JSON.stringify(values);
            $.ajax({
                url: '/save_zone_nickname_change/',
                type: 'POST',
                data: jsonText,
                contentType: "application/json; charset=utf-8",
                dataType: 'json',
                success: function (data) {
                    if (data == "invalid") {
                        document.getElementById(error_id).innerHTML = "Nickname error. Please try again.";
                        document.getElementById(value_er).value = "";
                    } else {
                        req_value_modal = data.zone_id + "_znick";
                        var newtest = document.getElementById(req_value_modal);
                        newtest.innerHTML = znickname.charAt(0).toUpperCase() + znickname.slice(1);
                        $('.bottom-right').notify({
                            message: { text: 'Heads up! The zone nickname change was successful.' },
                            type: 'blackgloss',
                            fadeOut: { enabled: true, delay: 5000 }
                        }).show();
                    }

                },
                error: function (data) {
                    $('.bottom-right').notify({
                        message: { text: 'Oh snap! Try submitting again. ' },
                        type: 'blackgloss',
                        fadeOut: { enabled: true, delay: 5000 }
                    }).show();
                }
            });
        }
    });

    $('body').on('click',"button[id^='gs-']", function (e) {
        e.preventDefault();
        var zone_id = this.id;
        zone_id = zone_id.split("-");
        zone_id = zone_id[1];
        var heat_setpoint = "heat_sp-" + zone_id;
        var cool_setpoint = "cool_sp-" + zone_id;
        var illumination = "illumination-" +  zone_id;
        heat_setpoint = $("#"+heat_setpoint).text();
        cool_setpoint = $("#"+cool_setpoint).text();
        illumination = $("#"+illumination).text();

        var values = {
            "zone_id": zone_id,
            "heat_setpoint": heat_setpoint,
            "cool_setpoint": cool_setpoint,
            "illumination": illumination
        };
        var jsonText = JSON.stringify(values);
        console.log(jsonText);
        $.ajax({
			  url : '/change_global_settings/',
			  type: 'POST',
			  data: jsonText,
			  contentType: "application/json; charset=utf-8",
			  dataType: 'json',
			  success : function(data) {
				//window.location.reload(true);
			  	$('.bottom-right').notify({
			  	    message: { text: 'Your changes were updated in the system.' },
			  	    type: 'blackgloss',
                    fadeOut: { enabled: true, delay: 5000 }
			  	  }).show();
			  },
			  error: function(data) {
				  $('.bottom-right').notify({
				  	    message: { text: 'The changes could not be updated at the moment. Try again later.' },
				  	    type: 'blackgloss',
                      fadeOut: { enabled: true, delay: 5000 }
				  	}).show();
			  }
			 });

    });

});
