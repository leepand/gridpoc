/**
 * project: hjs_cms
 * author: s0nnet
 */


/*选择下拉框*/
$(function(){
    $(".select").each(function(){
        var s = $(this);
        var z = parseInt(s.css("z-index"));
        var dt = $(this).children("dt");
        var dd = $(this).children("dd");
        var _show = function(){
            dd.slideDown(200);
            dt.addClass("cur");
            s.css("z-index",z+1);
        };
        var _hide = function(){
            dd.slideUp(200);
            dt.removeClass("cur");
            s.css("z-index",z);
        };

        dt.click(function(){
            dd.is(":hidden")?_show():_hide();
        });

        dd.find("a").click(function(){
            dt.html($(this).html());
            _hide();
        });

        $("body").click(function(i){
            !$(i.target).parents(".select").first().is(s) ? _hide():"";
        });
    });
});


        $(document).ready(function () {
            $('#loading-example-btn').click(function () {
                btn = $(this);
                simpleLoad(btn, true)
                // Ajax example
                //                $.ajax().always(function () {
                //                    simpleLoad($(this), false)
                //                });
                simpleLoad(btn, false)
            });
        });
        function simpleLoad(btn, state) {
            if (state) {
                btn.children().addClass('fa-spin');
                btn.contents().last().replaceWith(" Loading");
            } else {
                setTimeout(function () {
                    btn.children().removeClass('fa-spin');
                    btn.contents().last().replaceWith(" Refresh");
                }, 2000);
            }
        }