User = {
    login_data: false,
    authenticated: true
}
function LoginInfo(info){
    $('#loginModal .modal-dialog').addClass('shake');
             $('.error').addClass('alert alert-danger').html(info);//"Invalid username/password combination"
             $('input[type="password"]').val('');
             setTimeout( function(){ 
                $('#loginModal .modal-dialog').removeClass('shake'); 
    }, 1000 ); 
}


User.login = function(email, password, options) {
    if(email=="undefined" || password==""){
        return false;
    }
    User._ajax = User.ajax({
        url: "/login",
        method: "POST",
        dataType: "json",
        data: {"username":email,"password":password}
    }).success(function(res){
        //console.log('fff',res);
        if(res.code == 101){
            options.error(res.message);
            return false;
        }
        if(res.code == 201){  
            toastr.success("login success!");  
        }
        User.update(res.result);
        User.authenticated = true;
        User.data =  {name:"Tom",age:21};
        User.password = password;
        User.setCookies();
        if (options && options.success)
            options.success(res)
    }).error(function(res){
        console.log('error',res.code);
        if (options && options.error)
            options.error(res)
    });
    
    return User._ajax;
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
        User.onAuthenticated = false;
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
    console.log('daodadsdsd',User.authenticated,User._ajax);
    if (User.authenticated){
        
        f();
    } else if (User._ajax){
        User._ajax.done(f);
    }
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
    $.extend(User, data);
    this.password = password;
    //User.set('result22',$.extend({},{name:"Tom",age:21},{name:"Jerry",sex:"Boy"}));
    console.log(User,'hahahah');
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

User.change2222 = function(data, options) {
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

User.change = function(data, options) {
    User.ajax({
        url: "/api/user/update",
        method: "POST",
        //contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: data//JSON.stringify(data)
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

/*User.ajax = function(options) {
    var defaults = {
        headers: {
            "Authorization": "Basic " + btoa(this.username + ":" + this.password)
        }
    };
    $.extend(options,defaults);
    return $.ajax(options);
}*/

User.ajax = function(options) {
    /*var defaults = {
        headers: {
            "Authorization": "Basic " + btoa(this.username + ":" + this.password)
        }
    };*/
    var defaults = {
        headers: {
            "Accept": "application/json; charset=utf-8"
         }
    }
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