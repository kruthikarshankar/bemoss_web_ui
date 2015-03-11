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
 * Created by kruthika on 10/15/14.
 */


$( document ).ready(function() {
    $.csrftoken();

    $('.dropdown-menu li').click(function (event) {
        event.preventDefault();
        var $target = $(event.currentTarget);
        $target.closest('.btn-group')
            .find('[data-bind="label"]').text($target.text())
            .end()
            .children('.dropdown-toggle').dropdown('toggle');

        return false;
    });

    //$('.display').on('click', "a[id^='zonemanager-']" , function() {
    $("a[id^='zonemanager-']").click(function(e) {
        e.preventDefault();// prevent the default anchor functionality
        var this_id = this.id.split("-");
        var user_id = this_id[1];
        $("#ca_panel-" + user_id).show();
    });

    $("a[id^='admin-']").click(function(e) {
        e.preventDefault();// prevent the default anchor functionality
        var this_id = this.id.split("-");
        var user_id = this_id[1];
        $("#ca_panel-" + user_id).hide();
    });

    $("a[id^='tenant-']").click(function(e) {
        e.preventDefault();// prevent the default anchor functionality
        var this_id = this.id.split("-");
        var user_id = this_id[1];
        $("#ca_panel-" + user_id).hide();
    });

    $("#approve_users").click(function(e) {
        e.preventDefault();
        var values = [];
        var approve = false;
        $("#newusrs_tbl").find('tr').each(function (rowIndex, r) {
            approve = false;
            var cols = [];
            $(this).find("input[id^='approve_']").each(function () {
                if ($(this).is(':checked')){
                   var usr_id = this.id;
                   usr_id = usr_id.split("_");
                   cols.push(usr_id[1]);
                   cols.push("true");
                   approve = true;
                }
            });
            if (approve) {
                $(this).find("span[id^='role-']").each(function () {
                    cols.push($(this).text());
                });
                $(this).find("span[id^='zone-']").each(function () {
                    cols.push($(this).text());
                });
            }
            if (cols.length!=0) {
                values.push(cols);
            }
            console.log(values);

        });
           values = {
               "data": values
           };
        var jsonText = JSON.stringify(values);

            console.log(jsonText);
            $.ajax({
			  url : '/approve_users/',
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
                  setTimeout(function(){
                         window.location.reload();
                }, 3000);
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


     $("#modify_roles").click(function(e) {
        e.preventDefault();
        var values = [];
        var modify = false;
        $("#allusrs_tbl").find('tr').each(function (rowIndex, r) {
            var cols = [];
            $(this).find("input[id^='modify_']").each(function () {
                if ($(this).is(':checked')){
                   var usr_id = this.id;
                   usr_id = usr_id.split("_");
                   cols.push(usr_id[1]);
                   modify = true;
                }
            });
            if (modify) {
                $(this).find("span[id^='role-']").each(function () {
                    cols.push($(this).text());
                });
                $(this).find("span[id^='zone-']").each(function () {
                    cols.push($(this).text());
                });

                if (cols.length!=0) {
                    values.push(cols);
                }
                console.log(values);

                 values = {
                       "data": values
                   };
                var jsonText = JSON.stringify(values);

                    console.log(jsonText);
                    $.ajax({
                      url : '/modify_user_permissions/',
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
                          setTimeout(function(){
                                 window.location.reload();
                        }, 3000);
                      },
                      error: function(data) {
                          $('.bottom-right').notify({
                                message: { text: 'The changes could not be updated at the moment. Try again later.' },
                                type: 'blackgloss',
                              fadeOut: { enabled: true, delay: 5000 }
                            }).show();
                      }
                     });

                }

        });

    });

    $(".delete_user").click(function(e) {
        e.preventDefault();
        var values = [];
        var user_id = this.id;
        user_id = user_id.split("_");
        user_id = user_id[1];

        values = {
           "id": user_id
        };
        var jsonText = JSON.stringify(values);

            console.log(jsonText);
            $.ajax({
			  url : '/delete_user/',
			  type: 'POST',
			  data: jsonText,
			  contentType: "application/json; charset=utf-8",
			  dataType: 'json',
			  success : function(data) {
				//window.location.reload(true);
			  	$('.bottom-right').notify({
			  	    message: { text: 'The user was removed from BEMOSS.' },
			  	    type: 'blackgloss',
                    fadeOut: { enabled: true, delay: 5000 }
			  	  }).show();
                  setTimeout(function(){
                         window.location.reload();
                }, 3000);
			  },
			  error: function(data) {
				  $('.bottom-right').notify({
				  	    message: { text: 'The user could not be removed at the moment. Try again later.' },
				  	    type: 'blackgloss',
                      fadeOut: { enabled: true, delay: 5000 }
				  	}).show();
			  }
			 });

    });


});
