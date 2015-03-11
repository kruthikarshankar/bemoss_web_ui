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
    var nick_re = /^[A-Za-z0-9]{6,10}$/;

    $(function ($) {

        $("#add_new_zone_submit").click(function (evt) {
            evt.preventDefault();
            values = $("#add_new_zone").val();
            if (!nick_re.test(values)) {
                document.getElementById("newzoneerror").innerHTML = "Nickname can only contain letters and numbers. Please try again.";
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
                            $("#accordion2").append('<div class="panel" id="sortable_' + data + '"><div class="panel-heading"><p> <a href="#collapse_' + data + '" data-toggle="collapse" class="accordion-toggle collapsed" id="' + data + '_nick_dp">' + values.charAt(0).toUpperCase() + values.slice(1) + '</a>&nbsp;&nbsp;&nbsp;<i id="' + data + '_znedit" class="icon-pencil" data-backdrop="false" data-target="#' + data + '_znmodal" data-toggle="modal"></i></p> </div><div style="display: none;" aria-hidden="true" aria-labelledby="myModalLabel" role="dialog" tabindex="-1" class="modal fade" id="' + data + '_znmodal"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button aria-hidden="true" data-dismiss="modal" class="close" type="button">x</button><h4 id="myModalLabel" class="modal-title">Edit Zone Information</h4></div><div class="modal-body"><table class="table table-condensed"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td>Zone Nickname</td><td id="' + data + '_znick">' + values.charAt(0).toUpperCase() + values.slice(1) + '</td><td><a href="javascript:;" class="znickname_edit" ><i class="icon-small icon-edit" id="' + data + '_znick_edit"></i></a></td><script>$( "#' + data + '_znick_edit" ).click(function() {var newtest = document.getElementById(this.id.replace("_edit",""));newtest.innerHTML = \'<input type="text" id="' + data + '_znickname" placeholder="' + values + '"></input>\'});</script></tr></tbody></table></div><div class="modal-footer"><button data-dismiss="modal" class="btn btn-default" type="button">Close</button><button class="btn btn-primary save_changes_zn" id="#savechanges-' + data + '" type="button">Save changes</button><script>$( ".save_changes_zn" ).click(function(evt) {evt.preventDefault();var save_this = new Common();save_this.Save_Zone_Changes(this.id);});</script></div></div><!-- /.modal-content --></div><!-- /.modal-dialog --></div><div style="height: 0px;" class="panel-collapse collapse" id="collapse_' + data + '"><ul class="panel-body connectedSortable" id="panelbody_' + data + '"><script>$(".panel-body").droppable().sortable({dropOnEmpty: true,connectWith: ".connectedSortable"}).disableSelection();</script></ul></div></div>');
                            $('.bottom-right').notify({
                                message: { text: 'A new zone was added.' },
                                type: 'blackgloss',
                                fadeOut: { enabled: true, delay: 5000 }
                            }).show();

                            $(".panel").mousemove(function (e) {
                                if (e.which == 1) {
                                    if ($(".panel-collapse").hasClass("collapse")) {
                                        $(".panel-collapse").removeClass("collapse");
                                        $(".panel-collapse").addClass("in");
                                        $(".panel-body").show();
                                    }

                                } else {

                                    $(".panel-body").mouseenter(function (e) {
                                        if (e.which == 1) {
                                            $(".panel-body").show();
                                            //$(".panel-body").css("background","rgba(17, 19, 4, 0.35)");
                                        }
                                    });
                                }
                            });

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
                            //$('#zoned_device_listing').load(' #zoned_device_listing'/*, function(){$(this).children().unwrap()}*/);
                            //$('#zoned_device_listing').html(data);
                            req_value_modal = data.zone_id + "_znick";
                            req_val_stats = data.zone_id + "_nick_dp";
                            modal_zone_nickname = data.zone_id + "_ztdnick";
                            var newtest = document.getElementById(req_value_modal);
                            document.getElementById(req_val_stats).innerHTML = znickname.charAt(0).toUpperCase() + znickname.slice(1);
                            if (document.getElementById(modal_zone_nickname) != null)
                                document.getElementById(modal_zone_nickname).innerHTML = znickname.charAt(0).toUpperCase() + znickname.slice(1);
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


    });
});