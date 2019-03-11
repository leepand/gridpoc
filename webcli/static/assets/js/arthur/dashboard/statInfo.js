/**
 * project: arthur
 * author: leepand
 *
 */

function ServHealthReport(myonline_algo_cnt,myall_algo_cnt){
    var $card = $("#ServHealth-card");

    function updateView(cnt1,cnt2) {

        var online_cnt = cnt1;
        var all_cnt = cnt2;
        var message_class, weight_change, advice="";
        var BMI = (all_cnt-online_cnt) / all_cnt;
        /*
        Underweight = <18.5
        Normal weight = 18.5–24.9
        Overweight = 25–29.9
        Obesity = BMI of 30 or greater
        */
        if (BMI > 0.51 & BMI <= 0.8) {
            message_class = "text-danger";
            message = "Danger!";
            //weight_change = Math.ceil(18.5 * (height * height))+ 1;
            advice = 'Please check your service';
        } else if (BMI <= 0.51) {
            message_class = "text-success";
            message = "health.";
        } else if (BMI > 0.8) {
            message_class = "text-danger";
            message = "Over Danger!";
            //weight_change = Math.ceil(24.9 * (height * height)) - 1;
            advice = 'Please check your service';
        } else {
            message_class = "text-danger";
            message = "You're obese!";
            //weight_change = Math.ceil(24.9 * (height * height)) - 1;
            advice = 'Please check your service';
        }

        var content = '<span class="'+message_class+'">' + message + '</span>'
            +'<small>Your Service down ratio is '+BMI.toFixed(1)+'. ' +advice+ '</small>'
        $(".content", $card).html(content);
    }
    updateView(myonline_algo_cnt,myall_algo_cnt);
    
};

/*Dashboard列表*/
function get_dashboard_index(){
    $.ajax({
        type: "GET",
        async: true,
        dataType: "json",
        url: "/api/dashboard/index",
        error: function(){
            console.log("/api/dashboard/index/error");
        },
        success: function(data){
            if(data.code == 101){
                alert(data.message);
            }
            if(data.code == 201){
                if(!data.result){
                    return;
                }
                
                var dt_user = data.result.dt_user;
                console.log('dt_user.user_cnt',dt_user.user_cnt);
                $("#user_cnt").html(dt_user.user_cnt);
                var dt_algo = data.result.dt_algo_ser;
                $("#all_algo_cnt").html(dt_algo.all_algo_cnt);
                $("#online_algo_cnt").html(dt_algo.online_algo_cnt);
                $("#online_today_algo_cnt").html(dt_algo.online_today_algo_cnt);
                $("#offline_today_algo_cnt").html(dt_algo.offline_today_algo_cnt);
                $("#my_algo_cnt").html(dt_algo.my_algo_cnt);
                $("#my_online_algo_cnt").html(dt_algo.my_online_algo_cnt);
                var all_algo_cnt=Number(dt_algo.all_algo_cnt+0.0001);
                var online_algo_ratio = (Math.round(dt_algo.online_algo_cnt / all_algo_cnt * 10000) / 100.00 + "%");
                var online_process_css;
                online_process_css='<span style="width: '+online_algo_ratio+';" class="progress-bar progress-bar-success style-primary">'
                    +'<span class="sr-only">10.00% progress</span>' 
                    +' </span>';
                $("#online_process_css") .html(online_process_css) ;     
                $("#online_algo_ratio").html(online_algo_ratio);
                var my_algo_cnt=Number(dt_algo.my_algo_cnt+0.0001);
                var my_online_algo_ratio = (Math.round(dt_algo.my_online_algo_cnt / my_algo_cnt * 10000) / 100.00 + "%");
                var my_online_process_css;
                my_online_process_css='<span style="width: '+my_online_algo_ratio+';" class="progress-bar progress-bar-success style-primary">'
                    +'<span class="sr-only">10.00% progress</span>' 
                    +' </span>';
                
                $("#my_online_process_css") .html(my_online_process_css) ;     
                $("#my_online_algo_ratio").html(my_online_algo_ratio);
                ServHealthReport(dt_algo.my_online_algo_cnt,my_algo_cnt);
                if(dt_algo.my_priv == 3){
                        priv = "最强王者";
                    }else if(dt_algo.my_priv == 2){
                        priv = "永恒钻石";
                    }else if(dt_algo.my_priv == 1){
                        priv = "倔强青铜";
                    }else{
                        priv = "--";
                    }
                $("#my_priv").html(priv);
            }
        }
    });
}



$(document).ready(function(){
    User.onAuthenticated(function(){
        //console.log('ddddddd');
        get_dashboard_index();
    });
})