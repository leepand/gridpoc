User = {
    login_data: false,
    authenticated: false,
}
User.login = function(email, password, options) {
    //console.log(email,password,'email')
    if(email=="undefined" || password==""){
        return false;
    }
    $.ajax({
        url: "/login",
        method: "POST",
        headers: {
        Accept: "application/json; charset=utf-8"
    },
        //contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: {"username":email,"password":password}
    }).success(function(res){
        //console.log('sucess',res.code);
        console.log('fff',res);
        if(res.code == 101){
            options.error(res.message);
            return false;
          //toastr.error(res.message); 
        //res.message
        }
        if(res.code == 201){   
        toastr.success("login success!");  
        // return false;
        }
        
        User.update(res.result);
        User.password = password;
        User.setCookies();
        if (options && options.success)
            options.success(res)
    }).error(function(res){
        console.log('error',res.code);
        if (options && options.error)
            options.error(res)
    });
}
/*User.login = function(email, password, options) {
    User.clearCookies();

    this.email = email;
    this.username = email;
    this.password = password;

    User._ajax = User.ajax({
        url: "/login"
    }).error(function(e){
        if (options && options.error)
            options.error(e)
        User.authenticated = false;
    }).success(function(res){
        if (options && options.success)
            options.success(res)
        console.log('res',options);
        User.update(res)
        User.authenticated = true;
        User.setCookies();
    });
    return User._ajax;
}*/
/*User.login = function(email, password,options) {
    console.log('fldlsfsdl',email, password);
    $.ajax({
        url: "/login",
        type: "POST",
        async: true,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: {"username":email,"password":password},//JSON.stringify(data),
        error: function(){
            console.log("/login/error");
        },
        success: function(res){
        User.update(res);
        User.password = password;
        User.setCookies();
        if (options && options.success)
            options.success(res)
    }
    });
    }
*/
User.logout = function() {
    this.clearCookies();
}

User.onAuthenticated = function(f) {
    if (User.authenticated)
        f()
    else if (User._ajax)
        User._ajax.done(f)
}

User.setCookies = function() {
    Cookies.set("email", this.email);
    Cookies.set("username", this.username);
    Cookies.set("password", this.password);
}

User.clearCookies = function() {
    Cookies.remove("email");
    Cookies.remove("username");
    Cookies.remove("password");
}

User.getBasicAuth = function() {
    return "Basic " + btoa(this.username + ":" + this.password)
}

User.update = function(data) {
    var password = this.password;
    this.data = data;
    $.extend(User, data)
    this.password = password;
    console.log(data,'hahahah');
}

User.register = function(data, options) {
    $.ajax({
        url: "/api/users/",
        method: "POST",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: JSON.stringify(data)
    }).success(function(res){
        User.update(res);
        User.password = data.password;
        User.setCookies();
        if (options && options.success)
            options.success(res)
    }).error(function(res){
        if (options && options.error)
            options.error(res)
    });
}

User.change = function(data, options) {
    User.ajax({
        url: "/api/users/" + this.id + "/",
        method: "PUT",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: JSON.stringify(data)
    }).success(function(res){
        User.update(res);
        User.setCookies();
        if (options && options.success)
            options.success(res)
    }).error(function(res){
        if (options && options.error)
            options.error(res)
    });
}

User.changePassword = function(new_password, options) {
    var data = $.extend(this.data, {"password": new_password});
    this.change(data, {
        success: function(res) {
            User.password = new_password;
            User.setCookies();
            if (options && options.success)
                options.success(res)
        },
        error: function(e) {
            if (options && options.error)
                options.error(res)
        }
    })
}

User.ajax = function(options) {
    var defaults = {
        headers: {
            "Authorization": "Basic " + btoa(this.username + ":" + this.password)
        }
    };
    $.extend(options,defaults);
    return $.ajax(options);
}

User.autoLogin = function() {
    var email = Cookies.get("email");
    var password = Cookies.get("password");

    if (email && password) {
        this.login_data = true;
        User.login(email, password)
    }
}

User.autoLogin()