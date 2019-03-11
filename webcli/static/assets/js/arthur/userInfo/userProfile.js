userinfo={
    
}
function initProfile(){
    console.log('User.email',User.name);
    console.log('cook',Cookies.get("password"));
    $("#profile-firstname").val('User.email');
    
}
function initProfileView() {
    
    function populateHistoryView() {
        UserInfo.getHistory({
            success: function(history){
                if(history.code == 201) {
                    $("#profile-Name").val(history.result.nickname);
                    $("#profile-mobile").val(history.result.phone);
                    $("#profile-remark").val(history.result.remark);
                    $("#profile-email").val(history.result.email);
                    userinfo.userName = history.result.username;
                    userinfo.password = history.result.password;
                    userinfo.uid = history.result.uid;
                    userinfo.priv = history.result.privilege;
                    if(history.result.privilege< 3){
                        var priv_ch='普通用户';
                    }else{
                        var priv_ch='超级管理员';
                    }
                    console.log('history.result.privilege',priv_ch)
                    $("#profile-priv").val(priv_ch);
                }    
            },
            error: function() {

            }
        })
    }

    populateHistoryView();
        $("#profile-edit-card form").submit(function(e){
            //console.log('$("#profile-userName").val()',userinfo.userName);
            e.preventDefault();
            var data = {
                "nickname": $("#profile-Name").val(),
                "username": userinfo.userName,
                "uid": userinfo.uid,
                "email": $("#profile-email").val(),
                "phone": $("#profile-mobile").val(),
                "password": userinfo.password,
                "priv": userinfo.priv
            };
            console.log('$("#profile-userName").val()',data);
            var error_alert = $(".error-message", this);
            error_alert.hide();
            User.change(data, {
                success: function() {
                    //updateProfileView()
                    toastr.success("updated successfully");
                    $("#profile-edit-card form").get(0).reset();
                },
            error: function(res) {
                var errors = JSON.parse(res.responseText);
                error_alert.show()
                for(var i in errors) {
                    error_alert.find("span").html(i + ": " + errors[i]);
                    break;
                }
                console.log(res)
            }
        });

    });
}



$(document).ready(function(){
    User.onAuthenticated(function(){
        console.log('ddddddd');
        //initProfile();
        initProfileView();
         
    });
})