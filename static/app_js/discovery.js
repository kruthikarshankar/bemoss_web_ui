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

    $('.dropdown-menu li').click(function(event) {
        event.preventDefault();
      var $target = $( event.currentTarget );
      $target.closest( '.btn-group' )
         .find( '[data-bind="label"]' ).text( $target.text() )
            .end()
         .children( '.dropdown-toggle' ).dropdown( 'toggle' );

      return false;
    });

    $(".identify").click(function (evt) {
        evt.preventDefault();
        var identifier = (this).id;
        identify_id = identifier.split("-");
        identify_id = identify_id[1];
        //alert(identify_id);
        values = {
            "id": identify_id
        };
        var jsonText = JSON.stringify(values);
        $.ajax({
            url: '/identify_device/',
            type: 'POST',
            data: jsonText,
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            success: function (data) {
                if (data.indexOf("success") > -1) {
                    $('#' + identify_id + "-spin").addClass('fa fa-spinner fa-spin').removeClass('icon-search');
                    $("#" + identifier).removeClass('btn-warning').addClass('btn-success disabled');
                    identify_status(identify_id, identifier);
                    $('.bottom-right').notify({
                        message: { text: 'Communicating with the device for identification...' },
                        type: 'blackgloss',
                        fadeOut: { enabled: true, delay: 5000 }
                    }).show();
                }
            },
            error: function (data) {
                $('.bottom-right').notify({
                    message: { text: 'Oh snap! Try again. ' },
                    type: 'blackgloss',
                    fadeOut: { enabled: true, delay: 5000 }
                }).show();
            }
        });
    });

    $("#submit_thermostats").click(function (evt) {
        evt.preventDefault();
        var data = {'thermostats':[]};
        var cols_data = [];
        var col_data_th = [];
        $("#thermostats_tbl").find('tr').each(function (rowIndex, r) {
            var cols = [];
            var device_type;
            $(this).find("span[id^='zone-']").each(function () {
                var device_id = this.id;
                device_id = device_id.split("-");
                cols.push(device_id[1]);
                cols.push($(this).text());
                device_type = device_id[2];
            });
            /*$(this).find("input").each(function () {
                cols.push($(this).val());
            });*/
            $(this).find("input[id^='nick-']").each(function () {
                cols.push($(this).val());
            });
            $(this).find("input[id^='nbd-']").each(function () {
                if ($(this).is(':checked')){
                   cols.push("true");
                } else {
                   cols.push("false");
                }
            });
            if (cols.length!=0) {
                //cols_data.push(cols);
                if (device_type == '1TH' || device_type == '1NST') {
                    //data['thermostats'] = cols_data;
                    col_data_th.push(cols);
                }
            }
            console.log(data);

        });

        data['thermostats'] = col_data_th;

            var values = data;
            var jsonText = JSON.stringify(values);
            console.log(jsonText);
            $.ajax({
			  url : '/change_zones_thermostats/',
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

     $("#submit_plugloads").click(function (evt) {
        evt.preventDefault();
        var data = [];
        $("#plugload_tbl").find('tr').each(function (rowIndex, r) {
            var cols = [];
            $(this).find("span[id^='zone-']").each(function () {
                var device_id = this.id;
                device_id = device_id.split("-");
                cols.push(device_id[1]);
                cols.push($(this).text());
            });
            $(this).find("input[id^='nick-']").each(function () {
                cols.push($(this).val());
            });
            $(this).find("input[id^='nbd-']").each(function () {
                if ($(this).is(':checked')){
                   cols.push("true");
                } else {
                   cols.push("false");
                }
            });
            if (cols.length!=0) {
                data.push(cols);
            }
            console.log(data);

        });
            values = {
                "data":data
            };
            var jsonText = JSON.stringify(values);
            console.log(jsonText);
            $.ajax({
			  url : '/change_zones_plugloads/',
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

    $("#submit_lighting").click(function (evt) {
        evt.preventDefault();
        var data = [];
        $("#lighting_tbl").find('tr').each(function (rowIndex, r) {
            var cols = [];
            $(this).find("span[id^='zone-']").each(function () {
                var device_id = this.id;
                device_id = device_id.split("-");
                cols.push(device_id[1]);
                cols.push($(this).text());
            });
            $(this).find("input[id^='nick-']").each(function () {
                cols.push($(this).val());
            });
            $(this).find("input[id^='nbd-']").each(function () {
                if ($(this).is(':checked')){
                   cols.push("true");
                } else {
                   cols.push("false");
                }
            });
            if (cols.length!=0) {
                data.push(cols);
            }
            console.log(data);

        });
            values = {
                "data":data
            };
            var jsonText = JSON.stringify(values);
            console.log(jsonText);
            $.ajax({
			  url : '/change_zones_lighting/',
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


     $("#modify_thermostats").click(function(e) {
        e.preventDefault();
        var values = {'thermostats':[]};
        var device_type;
        var cols_data = [];
        var col_data_th = [];
        $("#thermostats_tblm").find('tr').each(function (rowIndex, r) {
            var modify = false;
            var cols = [];
            var device_id;
            $(this).find("input[id^='modify_']").each(function () {
                if ($(this).is(':checked')){
                   device_id = this.id;
                   device_id = device_id.split("_");
                   modify = true;
                }
            });
            if (modify) {
                cols.push(device_id[1]);
                $(this).find("input[id^='mnick-']").each(function () {
                    cols.push($(this).val());
                });
                $(this).find("span[id^='mzone-']").each(function () {
                    cols.push($(this).text());
                    var device_id = this.id;
                    device_id = device_id.split("-");

                    device_type = device_id[2];
                });

                if (cols.length!=0) {
                if (device_type == '1TH' || device_type == '1NST') {
                    col_data_th.push(cols);
                }
            }

            }

            });

         values['thermostats'] = col_data_th;

         var jsonText = JSON.stringify(values);

                    console.log(jsonText);
                    $.ajax({
                      url : '/modify_thermostats/',
                      type: 'POST',
                      data: jsonText,
                      contentType: "application/json; charset=utf-8",
                      dataType: 'json',
                      success : function(data) {

                        $('.bottom-right').notify({
                            message: { text: 'Your changes were updated in the system.' },
                            type: 'blackgloss',
                            fadeOut: { enabled: true, delay: 5000 }
                          }).show();
                       //window.location.reload(true);
                           setTimeout(function(){
                         window.location.reload();
                            }, 4000);

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


     $("#modify_lightingloads").click(function(e) {
        e.preventDefault();
        var device_type;
         var values = [];
        $("#lighting_tblm").find('tr').each(function (rowIndex, r) {
            var cols = [];
            var modify=false;
            var device_id = "";
            $(this).find("input[id^='modify_']").each(function () {
                if ($(this).is(':checked')){
                   device_id = this.id;
                   device_id = device_id.split("_");
                   modify = true;
                }
            });
            if (modify) {
                cols.push(device_id[1]);
                $(this).find("input[id^='mnick-']").each(function () {
                    cols.push($(this).val());
                });
                $(this).find("span[id^='mzone-']").each(function () {
                    cols.push($(this).text());
                });

                if (cols.length!=0) {
                    values.push(cols);
                }
                console.log(values);
                var jsonText = JSON.stringify(values);
                    console.log(jsonText);
                }

        });
        var jsonText = JSON.stringify(values);
                    console.log(jsonText);

         $.ajax({
                      url : '/modify_lighting_loads/',
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
                         }, 4000);
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

     $("#modify_plugloads").click(function(e) {
        e.preventDefault();

         var values = [];
        $("#plugload_tblm").find('tr').each(function (rowIndex, r) {
            var cols = [];
            var modify = false;
            var device_id="";
            $(this).find("input[id^='modify_']").each(function () {
                if ($(this).is(':checked')){
                   device_id = this.id;
                   device_id = device_id.split("_");
                   modify = true;
                }
            });
            if (modify) {
                cols.push(device_id[1]);
                $(this).find("input[id^='mnick-']").each(function () {
                    cols.push($(this).val());
                });
                $(this).find("span[id^='mzone-']").each(function () {
                    cols.push($(this).text());
                });

                if (cols.length!=0) {
                    values.push(cols);
                }
                console.log(values);


                }

        });

          var jsonText = JSON.stringify(values);

                    console.log(jsonText);
                    $.ajax({
                      url : '/modify_plugloads/',
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
                        }, 4000);
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