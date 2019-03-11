UserInfo = {

}


UserInfo.getHistory = function(options) {
    User.ajax({
        url: "/api/users/me",
        method: "GET",
    }).success(function(res){
        //console.log('get user info',res);
        if (options && options.success)
            options.success(res)
    }).error(function(res){
        if (options && options.error)
            options.error(res)
    });
}

UserInfo.insertUserInfo = function(date, weight, options) {
    User.ajax({
        url: "/api/users/me",
        method: "POST",
        data: {"date": date, "weight": weight}
    }).success(function(res){
        if (options && options.success)
            options.success(res)
    }).error(function(res){
        if (options && options.error)
            options.error(res)
    });
}





$(document).ready(function(){
   //initWeightView();
    
   /* User.onAuthenticated(function(){
        updateProfileView()
        $("#change-photo").click(function(){
            activaTab("avatar-form-card")
        });

        initProfile();
        initWeightView();
        initPasswordChangeView();
    });*/
})
