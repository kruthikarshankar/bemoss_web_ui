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

    $('.widget-content').on('click', '#add_new_holiday', function(e) {
        e.preventDefault();

        var table =$('#holidays').children()[1];
        console.log(table);
		//var noOfRows = document.getElementById(req_table).rows.length;

        var tr_id = $('#holidays tbody tr:last').attr('id');
        console.log( tr_id);
        tr_id = tr_id.split("_");
        tr_id = tr_id[1];

        if (tr_id == '') {
            tr_id = 0;
        }
        var new_tr_id = parseInt(tr_id) + 1 ;

        var row = table.insertRow();
        row.id = "hd_" + new_tr_id;
		var cell1 = row.insertCell(0);
		var cell2 = row.insertCell(1);
		var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        cell1.className = 'col-sm-4';
        cell2.className = 'col-sm-4';
        cell3.className = 'col-sm-2';
        cell4.className = 'col-sm-2';
        cell4.id = 'addtd_' + new_tr_id;

        cell1.innerHTML = "<div class='col-md-10'> <div class='input-group date' id='date_" + new_tr_id + "'>" + "" +
                    "<input type='text' class='form-control' data-date-format='YYYY/MM/DD'/>" +
                    "<span class='input-group-addon'><i class='icon icon-calendar'></i>" +
                    "</span></div></div>";
		cell2.innerHTML = "<input type='text' placeholder='Holiday Description' id='hd_desc-" + new_tr_id + "'" +
                                        " class='form-control' value=''>";
        cell3.innerHTML = "<button class='btn btn-sm btn-danger delete_td' type='button' id='delete_" + new_tr_id + "'>X</button>";
        cell4.innerHTML = "<button class='btn  btn-success add_td' type='button' id='add_" + new_tr_id + "'>Add</button>";
        $('#date_' + new_tr_id).datetimepicker({
                    icons: {
                        time: "fa fa-clock-o",
                        date: "fa fa-calendar",
                        up: "icon icon-chevron-up",
                        down: "icon icon-chevron-down"
                    },
                    pickTime: false
                });


    });

    $('.widget-content').on('click', "button[id^='delete_']" , function(e) {
        e.preventDefault();

        var tp_id = this.id;
        tp_id = tp_id.split("_");
        var delete_id = tp_id[1];

        var values = {
            "id": delete_id
        };

        var jsonText = JSON.stringify(values);
        $.ajax({
            url: '/delete_holiday/',
            type: 'POST',
            data: jsonText,
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            success: function (data) {
                if (data.status == "success") {
                    $("#hd_" + delete_id).remove();
                    $('.bottom-right').notify({
                        message: { text: 'Holiday removed from BEMOSS.' },
                        type: 'blackgloss',
                        fadeOut: { enabled: true, delay: 5000 }
                    }).show();
                }
            },
            error: function (data) {
                $('.bottom-right').notify({
                    message: { text: 'Holiday could not be removed at the moment. Try again later. ' },
                    type: 'blackgloss',
                    fadeOut: { enabled: true, delay: 5000 }
                }).show();
            }
        });

    });

    $('.widget-content').on('click', "button[id^='add_']" , function(e) {
        e.preventDefault();

        var tp_id = this.id;
        tp_id = tp_id.split("_");
        var add_id = tp_id[1];

        var values = {
            "id": add_id,
            "date": $("#date_" + add_id).data("DateTimePicker").getDate()._d.toJSON(),
            "desc":$("#hd_desc-" + add_id).val()
        };

        var jsonText = JSON.stringify(values);
        $.ajax({
            url: '/add_holiday/',
            type: 'POST',
            data: jsonText,
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            success: function (data) {
                if (data.status == "success") {
                    $("#addtd_" + add_id).html("");
                    $('.bottom-right').notify({
                        message: { text: 'Holiday added to BEMOSS.' },
                        type: 'blackgloss',
                        fadeOut: { enabled: true, delay: 5000 }
                    }).show();
                }
            },
            error: function (data) {
                $('.bottom-right').notify({
                    message: { text: 'Holiday could not be added at the moment. Try again later. ' },
                    type: 'blackgloss',
                    fadeOut: { enabled: true, delay: 5000 }
                }).show();
            }
        });

    });

    $("#bloc_submit").click(function(e) {
        e.preventDefault();
        var pattern=/^[0-9]{5}$/;
        var b_location = $("#b_loc").val();
        if (!pattern.test(b_location)) {
            //$("#b_loc").css("color","red");
            $(".help-block").show();
        } else {
            var values = {
                "b_loc": b_location
            };

            var jsonText = JSON.stringify(values);
            $.ajax({
                url: '/b_location_modify/',
                type: 'POST',
                data: jsonText,
                contentType: "application/json; charset=utf-8",
                dataType: 'json',
                success: function (data) {
                    if (data.status == "success") {
                        //$("#addtd_" + add_id).html("");
                        $('.bottom-right').notify({
                            message: { text: 'Building location updated.' },
                            type: 'blackgloss',
                            fadeOut: { enabled: true, delay: 5000 }
                        }).show();
                    }
                },
                error: function (data) {
                    $('.bottom-right').notify({
                        message: { text: 'Building location could not be updated at the moment. Try again later. ' },
                        type: 'blackgloss',
                        fadeOut: { enabled: true, delay: 5000 }
                    }).show();
                }
            });
        }
    });
});
