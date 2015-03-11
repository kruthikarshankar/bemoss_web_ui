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
 * Created by kruthika on 8/29/14.
 */


$(document).ready(function(){
    $.csrftoken();


	  //Plot options
	  var options = {
			    legend: {
			      show: true,
			      labels:["Status"]
			    },
			    cursor: {
			           show: true,
			           zoom: true
			    },
			    seriesDefaults: {
                    show: true,
			      showMarker:false,
			      pointLabels: {show:false},
			      rendererOption:{smooth: true}
			    },
			    axesDefaults: {
			      labelRenderer: $.jqplot.CanvasAxisLabelRenderer
			    },
			    axes: {
			      xaxis: {
			        label: "Time",
			        renderer: $.jqplot.DateAxisRenderer,
			        tickOptions:{formatString:'%I:%M:%S %p'},
			        numberTicks: 10,
		            min : _status[0][0],
		            max: _status[_status.length-1][0]
			      },
			      yaxis: {
			        min:0,
			        max:1,
			        label: "Status (0=OFF, 1=ON)"
			      }
			    }
	  };



	  //Initialize plot for lighting
      var data_points = [_status];
	  var plot1 = $.jqplot('chart100', data_points ,options);
      $("#status").attr('checked','checked');

      temp = {
            seriesStyles: {
                seriesColors: ['red', 'orange', 'yellow', 'green', 'blue', 'indigo'],
                highlightColors: ['lightpink', 'lightsalmon', 'lightyellow', 'lightgreen', 'lightblue', 'mediumslateblue']
            },
            grid: {
                //backgroundColor: 'rgb(211, 233, 195)'
            },
            axesStyles: {
               borderWidth: 0,
               label: {
                   fontFamily: 'Sans',
                   textColor: 'white',
                   fontSize: '9pt'
               }
            }
        };


        plot1.themeEngine.newTheme('uma', temp);
        plot1.activateTheme('uma');

        var timeOut;

        function update_plot(_data) {
              _status = _data.status;
              var new_data = [];

              $.each($('input:checked'), function(index, value){
                   //new_data.push(outdoor_temp);
                   if (this.id == 'status') {
                       new_data.push(_status);
                   }
                   options.legend.labels.push(this.value);
                   options.axes.xaxis.min = _status[0][0];
                   options.axes.xaxis.max = _status[_status.length-1][0];
              });

              if (plot1) {
                  plot1.destroy();
              }

              //var plot2 = $('#chart100').jqplot(new_data, options);
              var plot2 = $.jqplot('chart100', new_data ,options);
              plot2.themeEngine.newTheme('uma', temp);
              plot2.activateTheme('uma');

              console.log('nowww');
              $("#auto_update").attr('disabled','disabled');
              $("#stop_auto_update").removeAttr('disabled');
        }


        function do_update() {
            var values = {
		        "device_info": device_info
		    };
	        var jsonText = JSON.stringify(values);
            console.log(jsonText);
			//setTimeout(function() {
				$.ajax({
				  url : '/pl_smap_update/',
				  //url : 'http://38.68.237.143/backend/api/data/uuid/97699b93-9d6d-5e31-b4ef-7ac78fdc985a',
				  type: 'POST',
                  data: jsonText,
                  dataType: 'json',
				  //dataType: 'jsonp',
				  success : function(data) {
					//update_status = $.parseJSON(data.status);
					  console.log ("testing");
					  console.log (data);
                      update_plot(data);
    			  	  //stopTimer('setTimeOut_chartUpdate');
				  },
				  error: function(data) {

                      clearTimeout(timeOut);
                      $('.bottom-right').notify({
					  	    message: { text: 'Communication Error. Try again later!'},
					  	    type: 'blackgloss',
                          fadeOut: { enabled: true, delay: 5000 }
					  	  }).show();
				  }
				 });
                timeOut = setTimeout(do_update, 30000);
			//},5000);
	}

    	  //Auto update the chart
	  $('#auto_update').click( function(evt){
          evt.preventDefault();
	      do_update();
	   });

      $('#stop_auto_update').click(function(){
          clearTimeout(timeOut);
          $('#stop_auto_update').attr('disabled', 'disabled');
          $('#auto_update').removeAttr('disabled');
      });

        $('#stack_chart').click( function(evt){
            evt.preventDefault();
	        stackCharts();
	   });

	  function stackCharts(){
        if (timeOut) {
          clearTimeout(timeOut);
          $('#stop_auto_update').attr('disabled', 'disabled');
          $('#auto_update').removeAttr('disabled');
        }
        options.legend.labels = [];
        var new_data = [];
        $.each($('input:checked'), function(index, value){
           //new_data.push(outdoor_temp);
           if (this.id == 'status') {
               new_data.push(_status);
           }
           options.legend.labels.push(this.value);
           options.axes.xaxis.min = _status[0][0];
           options.axes.xaxis.max = _status[_status.length-1][0];
        });
          //plot1.legend.labels.push("Humidity");
          //plot1.data.push(humidity);
          if (plot1) {
              plot1.destroy();
          }

          //var plot2 = $('#chart100').jqplot(new_data, options);
          var plot2 = $.jqplot('chart100', new_data ,options);
          plot2.themeEngine.newTheme('uma', temp);
          plot2.activateTheme('uma');
      }

    /* $("#print_chart").click( function(evt){
         evt.preventDefault();
         var canvas = $(".jqplot-base-canvas");
         var context = canvas[0].getContext("2d");

        // First drawing commands
        context.fillStyle = "rgba(0, 0, 255, .5)";
        context.fillRect(0, 0, canvas[0].width, canvas[0].height);
        var dataUrl    = canvas[0].toDataURL();

        window.open(dataUrl, "toDataURL() image", "width=200, height=500");
     });*/

$("#print_chart").click( function(evt){
         evt.preventDefault();
         var canvas = $(".jqplot-base-canvas");
        var printCanvas = $('.jqplot-base-canvas');
    printCanvas.attr("width", 957);
    printCanvas.attr("height", 350);
    var printCanvasContext = printCanvas.get(0).getContext('2d');
    window.print();
     });



/*
    (function($) {
	$.fn.CanvasHack = function() {
		var canvases = this.find('canvas').filter(function() {
			return $(this).css('position') == 'absolute';
		});

		canvases.wrap(function() {
			var canvas = $(this);
			var div = $('<div />').css({
				position: 'absolute',
				top: canvas.css('top'),
				left: canvas.css('left')
			});
			canvas.css({
				top: '0',
				left: '0'
			});
			return div;
		});

		return this;
	};
    })(jQuery);

    $('body').CanvasHack();


    if (!$.jqplot.use_excanvas) {
         $('div.jqplot-target').each(function () {
            var outerDiv = $(document.createElement('div'));
            var header = $(document.createElement('div'));
            var div = $(document.createElement('div'));

            outerDiv.append(header);
            outerDiv.append(div);

            outerDiv.addClass('jqplot-image-container');
            header.addClass('jqplot-image-container-header');
            div.addClass('jqplot-image-container-content');

            header.html('Right Click to Save Image As...');

            var close = $(document.createElement('a'));
            close.addClass('jqplot-image-container-close');
            close.html('Close');
            close.attr('href', '#');
            close.click(function () {
               $(this).parents('div.jqplot-image-container').hide(500);
               return false;
            })
            header.append(close);

            $(this).after(outerDiv);
            outerDiv.hide();

            outerDiv = header = div = close = null;

            if (!$.jqplot._noToImageButton) {
               var btn = $(document.createElement('button'));
               btn.text('View Plot Image');
               btn.addClass('jqplot-image-button');
               btn.on('click', { chart: $(this) }, function (evt) {
                  var imgelem = evt.data.chart.jqplotToImageElem();
                  var div = $(this).nextAll('div.jqplot-image-container').first();
                  div.children('div.jqplot-image-container-content').empty();
                  div.children('div.jqplot-image-container-content').append(imgelem);
                  div.show(500);
                  div = null;
               });

               $(this).after(btn);
               btn.after('<br />');
               btn = null;
            }
         });
      }

       $(function() {

      $.fn.jqplotToImage =
      function(x_offset, y_offset) {
        if ($(this).width() == 0 || $(this).height() == 0) {
          return null;
        }
        var newCanvas = document.createElement("canvas");
        newCanvas.width = $(this).outerWidth() + Number(x_offset);
        newCanvas.height = $(this).outerHeight() + Number(y_offset);

        if (!newCanvas.getContext) return null;

        var newContext = newCanvas.getContext("2d");
        newContext.textAlign = 'left';
        newContext.textBaseline = 'top';

        function _jqpToImage(el, x_offset, y_offset) {
          var tagname = el.tagName.toLowerCase();
          var p = $(el).position();
          var css = getComputedStyle(el);
          var left = x_offset + p.left + parseInt(css.marginLeft) + parseInt(css.borderLeftWidth) + parseInt(css.paddingLeft);
          var top = y_offset + p.top + parseInt(css.marginTop) + parseInt(css.borderTopWidth)+ parseInt(css.paddingTop);

          if ((tagname == 'div' || tagname == 'span') && !$(el).hasClass('jqplot-highlighter-tooltip')) {
            $(el).children().each(function() {
              _jqpToImage(this, left, top);
            });
            var text = $(el).childText();

            if (text) {
              var metrics = newContext.measureText(text);
              newContext.font = $(el).getComputedFontStyle();
              newContext.fillText(text, left, top);
              // For debugging.
              //newContext.strokeRect(left, top, $(el).width(), $(el).height());
            }
          }
          else if (tagname == 'canvas') {
            newContext.drawImage(el, left, top);
          }
        }
        $(this).children().each(function() {
          _jqpToImage(this, x_offset, y_offset);
        });
        return newCanvas;
      };

      $.fn.css2 = jQuery.fn.css;
      $.fn.css = function() {
        if (arguments.length) return jQuery.fn.css2.apply(this, arguments);
        return window.getComputedStyle(this[0]);
      };

      // Returns font style as abbreviation for "font" property.
      $.fn.getComputedFontStyle = function() {
        var css = this.css();
        var attr = ['font-style', 'font-weight', 'font-size', 'font-family'];
        var style = [];

        for (var i=0 ; i < attr.length; ++i) {
          attr = String(css[attr[i]]);

          if (attr && attr != 'normal') {
            style.push(attr);
          }
        }
        return style.join(' ');
      };

      $.fn.childText =
        function() {
          return $(this).contents().filter(function() {
            return this.nodeType == 3;  // Node.TEXT_NODE not defined in I7
          }).text();
        };

    }); */

});