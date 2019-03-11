$(function(){
    //参数设置，若用默认值可以省略以下面代
    toastr.options = {
"closeButton": false, //是否显示关闭按钮
"debug": false, //是否使用debug模式
"showDuration": "300",//显示的动画时间
"hideDuration": "1000",//消失的动画时间
"timeOut": "5000", //展现时间
"extendedTimeOut": "1000",//加长展示时间
"showEasing": "swing",//显示时的动画缓冲方式
"hideEasing": "linear",//消失时的动画缓冲方式
"showMethod": "fadeIn",//显示时的动画方式
"hideMethod": "fadeOut" //消失时的动画方式
};
});
$(".show-signup-form, .show-signin-form").click(function(){
    $("#signin-card").fadeToggle(0);
    $("#signup-card").fadeToggle(0);
});
            
$('#signup-birth-date').datepicker({
    maxDate : 'now',
    startDate : new Date('1900-08-08'),
    endDate : new Date(),
    autoclose: true,
    todayHighlight: true});

function login(email, password) {
    
    User.login(email, password, {
        success: function(){
            //toastr.success("login success!")
            location.href="index.html";
        },
        error: function(res) {
            //toastr.error(res);
            LoginInfo(res);
        }
    });
}
function shakeModal(){
    $('#loginModal .modal-dialog').addClass('shake');
             $('.error').addClass('alert alert-danger').html("Invalid username/password combination");
             $('input[type="password"]').val('');
             setTimeout( function(){ 
                $('#loginModal .modal-dialog').removeClass('shake'); 
    }, 1000 ); 
}

$("#login-form").submit(function(e){
    e.preventDefault();
    var username = $("#login-email").val();
    var password = $("#login-password").val();
    //console.log('ddddd',username);
    var that = this;
    //var myform=$('#newArticleForm'); 
    //shakeModal();
    if(username=="undefined"){
        //console.log('ddddd',username);
        return false;
    }else{
        login(username, password);
    }  
});

        $("#signup-card form").submit(function(e){
                e.preventDefault();
                var data = {
                    "first_name": $("#signup-firstname").val(),
                    "last_name": $("#signup-lastname").val(),
                    "email": $("#signup-email").val(),
                    "username": $("#signup-email").val(),
                    "password": $("#signup-password").val(),
                    "userprofile": {
                        "gender": $("input[name='signup-gender']:checked").val(),
                        "birth_date": $("#signup-birth-date").data('datepicker').getFormattedDate('yyyy-mm-dd'),
                        "height": $("#signup-height").val(),
                    }
                };
                $("#signup-error-message").hide()
                User.register(data, {
                    success: function(res){
                        Weights.insertWeight(moment().format('YYYY-MM-DD'), $("#signup-weight").val(), {
                            success: function(){
                                login(data.email, data.password);
                            },
                            error: function() {
                                login(data.email, data.password);
                            }
                        })
                    },
                    error: function(res){
                        var errors = JSON.parse(res.responseText);
                        $("#signup-error-message").show()
                        for(var i in errors) {
                            $("#signup-error-message span").html(i + ": " + errors[i]);
                            break;
                        }
                        console.log(res)
                    }
                })
            });



function showRegisterForm(){
    $('.loginBox').fadeOut('fast',function(){
        $('.registerBox').fadeIn('fast');
        $('.login-footer').fadeOut('fast',function(){
            $('.register-footer').fadeIn('fast');
        });
        $('.modal-title').html('Register with');
    }); 
    $('.error').removeClass('alert alert-danger').html('');
       
}
function showLoginForm(){
    $('#loginModal .registerBox').fadeOut('fast',function(){
        $('.loginBox').fadeIn('fast');
        $('.register-footer').fadeOut('fast',function(){
            $('.login-footer').fadeIn('fast');    
        });
        
        $('.modal-title').html('Login with');
    });       
     $('.error').removeClass('alert alert-danger').html(''); 
}

function openLoginModal(){
    showLoginForm();
    setTimeout(function(){
        $('#loginModal').modal('show');    
    }, 230);
    
}
function openRegisterModal(){
    showRegisterForm();
    setTimeout(function(){
        $('#loginModal').modal('show');    
    }, 230);
    
}

$(document).ready(function(){
     openLoginModal();

});