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

    $('#Custom').click(function(e) {
        e.preventDefault();// prevent the default anchor functionality
        //$("#drop_custom_alert").removeAttr('disabled');
        //$("#drop_custom_alert_comparator").removeAttr('disabled');
        //if ( $('#alert').text() == 'Custom') {
            $("#ca_panel").css("display", "block");
            $("#ca_panel_comparator").css("display", "block");
            $("#ca_panel_val").css("display", "block");
        //}

    });

    $('#Custom').click(function(e) {
        e.preventDefault();// prevent the default anchor functionality
        $("#drop_custom_alert").removeAttr('disabled');
        $("#drop_custom_alert_comparator").removeAttr('disabled');
    });



    //Dropdown value append
    $('.alert_select li').click(function(event) {
      event.preventDefault();
      var $target = $( event.currentTarget );
      $target.closest( '.btn-group' )
         .find( '[data-bind="label"]' ).text( $target.text() )
            .end()
         .children( '.dropdown-toggle' ).dropdown( 'toggle' );

      return false;
    });

    $('#drop_alert').click(function(event) {
        $("#drop_alert").removeClass('btn-danger').addClass('btn-default');
    });

    $('#drop_pr').click(function (event) {
        $("#drop_pr").removeClass('btn-danger');
        $("#drop_pr").addClass('btn-default');
    });

    //Checkbox value append
    $('.bemoss_checkbox').click(function(event) {
        if (undefined == $(this).attr("checked"))
            $(this).attr("checked","checked");
        else if ($(this).attr("checked") == "checked")
            $(this).removeAttr("checked");
        /*if (this.id == "Email" && $(this).attr("checked")) {
            $("#email").removeAttr('disabled');
            if ($("#Text").attr("checked")) {
                if (('#phone').is(':disabled')) {
                    $("#phone").removeAttr('disabled');
                }
            }
        } else {
            $("#email").attr("disabled","disabled");
            if ($("#Text").attr("checked")) {
                if (('#phone').is(':disabled')) {
                    $("#phone").removeAttr('disabled');
                }
            }
        }
        if (this.id == "Text" && $(this).attr("checked")) {
            $("#phone").removeAttr('disabled');
            if ($("#Email").attr("checked")) {
                if (('#email').is(':disabled')) {
                    $("#email").removeAttr('disabled');
                }
            }
        } else {
            $("#phone").attr("disabled","disabled");
            if ($("#Email").attr("checked")) {
                if (('#email').is(':disabled')) {
                    $("#email").removeAttr('disabled');
                }
            }
        }
        if (this.id == "BemossNotification" && $(this).attr("checked")) {
            if ($("#Email").attr("checked")) {
                if (('#email').is(':disabled')) {
                    $("#email").removeAttr('disabled');
                }
            }
            if ($("#Text").attr("checked")) {
                if (('#phone').is(':disabled')) {
                    $("#phone").removeAttr('disabled');
                }
            }
        }*/
    });

    //Create alert ajax call
    $('#create_alert').click(function(event) {
        event.preventDefault();
        var _alert = $('#alert').text();
        var custom_alert = "-";
        var custom_alert_comparator =  "-";
        var value = "0";
        if (_alert == 'Custom') {
            custom_alert = $("#custom_alert").text();
            custom_alert_comparator =  $("#custom_alert_comparator").text();
            value = $('#alert_val').val();
        }


        var priority = $('#pr_lvl').text();
        var n_type = [];
        $('.bemoss_checkbox').each(function () {
            if ($(this).attr("checked") == "checked") {
                n_type.push(this.id.split("_").join(" "));
            }
        });
        var email = $('#email').val();
        if (undefined!=email) {
            email = email.split(",");
        } else {
            email = "";
        }
        var phone = $('#phone').val();
        if (undefined!=phone) {
            phone = phone.split(",");
        } else {
            phone = "";
        }
        console.log(n_type);
        var values = {
            "alert":_alert,
            "custom_alert": custom_alert,
            "custom_alert_comparator": custom_alert_comparator,
            "value":value,
            "priority":priority,
            "email":email,
            "phone":phone,
            "n_type":n_type
        };
        console.log(values);
        var jsonText = JSON.stringify(values);
        console.log(jsonText);
        $.ajax({
		  url : '/create_alert/',
		  type: 'POST',
		  data: jsonText,
		  dataType: 'json',
		  success : function(data) {
			//window.location.reload(true);
		  	$('.bottom-right').notify({
		  	    message: { text: 'The new alert was created' },
		  	    type: 'blackgloss',
                fadeOut: { enabled: true, delay: 5000 }
		  	  }).show();
              setTimeout(function(){
                         window.location.reload();
                }, 3000);
		  },
		  error: function(data) {
              if (_alert == "Choose an Alert" || priority == "Priority Level") {
                  if (_alert == "Choose an Alert" && priority != "Priority Level") {
                    $("#drop_alert").removeClass('btn-default');
                    $("#drop_alert").addClass('btn-danger');
                  } else if (_alert != "Choose an Alert" && priority == "Priority Level") {
                    $("#drop_pr").removeClass('btn-default');
                    $("#drop_pr").addClass('btn-danger');
                  } else {
                    $("#drop_alert").removeClass('btn-default');
                    $("#drop_alert").addClass('btn-danger');
                    $("#drop_pr").removeClass('btn-default');
                    $("#drop_pr").addClass('btn-danger');
                  }

                  $('.bottom-right').notify({
                      message: { text: 'Select your choices from the dropdown appropriately. Please try again.' },
                      type: 'blackgloss',
                      fadeOut: { enabled: true, delay: 5000 }
                  }).show();
              } else {
                  $('.bottom-right').notify({
					  	    message: { text: 'Oh snap! Try submitting again. ' },
					  	    type: 'blackgloss',
                      fadeOut: { enabled: true, delay: 5000 }
				  }).show();
              }
		  }
		 });

    });


    $(".delete_alert").click(function(event) {
        event.preventDefault();
        var reg_al_id = this.id.split('_');
        reg_al_id = reg_al_id[1];
        $.ajax({
            url: '/del_alert/',
            type: 'POST',
            data: reg_al_id,
            success: function (data) {
                //window.location.reload(true);
                //alert("success");
                $('.bottom-right').notify({
                    message: { text: 'The alert was deleted successfully.' },
                    type: 'blackgloss',
                    fadeOut: { enabled: true, delay: 5000 }
                }).show();
                setTimeout(function(){
                         window.location.reload();
                }, 3000);
            },
            error: function (data) {
                $('.bottom-right').notify({
                    message: { text: 'The alert could not deleted at the moment. Please try again later.' },
                    type: 'blackgloss',
                    fadeOut: { enabled: true, delay: 5000 }
                }).show();
            }
        });
    });

});