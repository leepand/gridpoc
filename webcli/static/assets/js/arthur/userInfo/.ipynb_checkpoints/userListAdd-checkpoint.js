/**
 * project: Arthur
 * author: leepand
 * update: 2019-02-14
 */

/*编辑用户*/
function edit_user(uid){
        var params = "uid=" + uid;
        window.open("user_edit.html?"+params,null,null,true);
        //popWin.showWin("500","530","用户编辑","user_edit.html", params);
        layer.closeAll("iframe");
}
function del_user(uid){
    swal({
        title: "您确定要删除该用户吗",
        text: "删除后将无法恢复，请谨慎操作！",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "确定！",
        cancelButtonText: "取消…",
        closeOnConfirm: false,
        closeOnCancel: false
    },
    function (isConfirm) {
        if (isConfirm) {
            del_user_api(uid);
            swal("删除成功！", "您已经永久删除了这个用户信息。", "success");
        } else {
            swal("已取消", "您取消了删除操作！", "error");
        }});
}

function del_user_api(uid){
    $.ajax({
        type: "POST",
        async: true,
        dataType: "json",
        url: "/api/user/del",
        data: {"uid": uid},
        error: function() {
            console.log("/api/user/del/error");
        },
        success: function(data){
            if(data.code == 101){
                swal({
                    title: "",
                    text: data.message
                });
                //alert(data.message);
            }
            if(data.code == 201){
                get_user_list();
            }else{
                //alert("删除用户失败[Error:" + data.message + "]");
                swal({
                    title: "删除用户失败",
                    text: data.message
                });
            }
        }
    });  
}
   

/*编辑页面-获取用户信息*/
function get_user_info(){
    var uid = get_request_args("uid");

    $.ajax({
        type: "GET",
        async: true,
        dataType: "json",
        url: "/api/user/info",
        data: {"uid":uid},
        error: function(){
            console.log("/api/user/info/error");
        },
        success: function(data){
            if(data.code == 101){
                alert(data.message);
            }
            if(data.code == 201){
                if(!data.result){
                    return;
                }
                result = data.result;
                $("#form_uid").val(uid);
                $("#form_nickname").val(result.nickname);
                $("#form_username").val(result.username);
                $("#form_password").val(result.password);
                $("#form_phone").val(result.phone);
                $("#form_email").val(result.email);

                var priv = result.priv;
                if(priv == 3){
                    priv = "最强王者";
                }else if(priv == 2){
                    priv = "永恒钻石";
                }else if(priv == 1){
                    priv = "倔强青铜";
                }else{
                    priv = "??";
                }

                $("#test").children("div").html(priv);
                //document.getElementById("test").value=priv;
                //$("#test").val(priv);
            }
        }
    });
}

/*提交修改后的数据*/
function update_user_info(){
    var uid = $("#form_uid").val();
    var nickname = $("#form_nickname").val();
    var username = $("#form_username").val();
    var password = $("#form_password").val();
    var phone = $("#form_phone").val();
    var email = $("#form_email").val();
    var priv = $('#test option:selected').val();
    //var priv = $(".select").children("dt").html();

    if(priv == "最强王者"){
        priv = 3;         
    }else if(priv == "永恒钻石"){
        priv = 2;
    }else if(priv == "倔强青铜"){
        priv = 1;
    }else{
        alert("用户等级输入错误!");
        return;
    }

    $.ajax({
        type: "POST",
        async: true,
        dataType: "json",
        url: "/api/user/update",
        data: {
            "uid":uid,
            "nickname": nickname,
            "username": username,
            "password": password,
            "phone": phone,
            "email": email,
            "priv": priv
        },
        error: function(){
            console.log("/api/user/update/error");
        },
        success: function(data){
            if(data.code == 101){
                //alert(data.message);
                swal({
                    title: "缺少参数",
                    text: data.message
                });
            }
            if(data.code == 201){
                //alert("更新成功,请关闭窗口并刷新！");
                 swal({
                    title: "OK",
                    text: "成功添加用户",
                    type: "success"
                },function(){
                     layer.closeAll("iframe");
                     location.href='/user_list.html';
                 }//end of swal callback
                     );
            }
        }
    });
}

/*获取URL传过来的参数*/
function get_request_args(argname){  
    var url = document.location.href;
    var arrStr = url.substring(url.indexOf("?")+1).split("&");

    for(var i = 0; i < arrStr.length; i++) {
        var loc = arrStr[i].indexOf(argname+"=");  
        if(loc != -1){
            return arrStr[i].replace(argname+"=","").replace("?","");
            break;
        }
    }
    return "";
}

//使用layer样式，更新01-11
layui.use(['form','layer'],function(){  
var form = layui.form
        layer = parent.layer === undefined ? layui.layer : top.layer,
        $ = layui.jquery;


function get_user_list(){
      
    
    $.ajax({
        type: "GET",
        async: true,
        dataType: "json",
        url: "/api/user/list",
        error: function(){
            console.log("/api/user/list/error");
        },
        success: function(data){
            var  usertable = '';
            if(data.code == 101){
                //alert(data.message);
                swal({
                    title: "缺少权限，请联系管理员",
                    text: data.message
                });
            }
            if(data.code == 201){
                if(!data.result){
                    $(".usertable").html("<p>当前用户列表为空，请先添加用户！</p>");
                    return;
                }
                //$("table tr:not(:first)").empty();
                var dataLen = data.result.length;
                for(var i = 0; i < dataLen; i++){
                    var user_info = data.result[i];
                    var uid = user_info["uid"];
                    var nickname = user_info["nickname"];
                    var username = user_info["username"];
                    var password = user_info["password"];
                    var phone = user_info["phone"];
                    var email = user_info["email"];
                    var priv = user_info["priv"];
                    var lastlogin = user_info["lastlogin"];


                    if(priv == 3){
                        priv = "最强王者";
                    }else if(priv == 2){
                        priv = "永恒钻石";
                    }else if(priv == 1){
                        priv = "倔强青铜";
                    }else{
                        priv = "--";
                    }

                    //$("table").append(
                    usertable+=
                        "<tr><td>"+ uid +"</td>"+
                        "<td>"+ nickname +"</td>"+
                        "<td>"+ username +"</td>"+
                        "<td>"+ password +"</td>"+
                        "<td>"+ phone +"</td>"+
                        "<td>"+ email +"</td>"+
                        "<td>"+ priv +"</td>"+
                        "<td>"+ lastlogin +"</td>"+
                        "<td><div><a  class='layui-btn layui-btn-xs'  onclick=edit_user('"+uid+"') >编辑</a>  <a class='layui-btn layui-btn-xs layui-btn-danger'  onclick=del_user('"+ uid +"')>删除</a></div></td></tr>"//需要加载layui的样式
                    ;
                }
                $(".usertable").html(usertable);
                $('.dataTables-UserList').dataTable();
            }
        }
    });
    
  
}

/*用户列表*/
var tmp = get_user_list();







$(".addUser_btn").click(function(){
    add_user();
 })

/*添加用户*/
function add_user(){
    var nickname = $("#form_nickname").val();
    var username = $("#form_username").val();
    var password = $("#form_password").val();
    var phone = $("#form_phone").val();
    var email = $("#form_email").val();
    var remark = $("#form_remark").val();
    var priv = $('#test option:selected').val();
    //var priv = $(".userGrade").children("dt").html();

    if(priv == "最强王者"){
        priv = 3;
    }else if(priv == "永恒钻石"){
        priv = 2;
    }else if(priv == "倔强青铜"){
        priv = 1;
    }else{
        alert("用户等级输入错误!");
        return;
    }
    $.ajax({
        type: "POST",
        async: true,
        dataType: "json",
        url: "/api/user/add",
        data: {
            "nickname": nickname,
            "username": username,
            "password": password,
            "phone": phone,
            "email": email,
            "remark":remark,
            "priv": priv
        },
        error: function(){
            console.log("/api/user/add/error");
        },
        success: function(data){
            if(data.code == 101){
                //alert(data.message);
                swal({
                    title: "缺少参数",
                    text: data.message
                });
            }
            if(data.code == 201){
                //alert("添加成功,请关闭窗口！");
                get_user_list();//添加成功后更新用户列表
                swal({
                    title: "OK",
                    text: "成功添加用户",
                    type: "success"
                });
                return;       
        }
     }
});
}








    

    form.on("submit(addUser)",function(data){
        //弹出loading
        var index = top.layer.msg('数据提交中，请稍候',{icon: 16,time:false,shade:0.8});
        // 实际使用时的提交信息
        // $.post("上传路径",{
        //     userName : $(".userName").val(),  //登录名
        //     userEmail : $(".userEmail").val(),  //邮箱
        //     userSex : data.field.sex,  //性别
        //     userGrade : data.field.userGrade,  //会员等级
        //     userStatus : data.field.userStatus,    //用户状态
        //     newsTime : submitTime,    //添加时间
        //     userDesc : $(".userDesc").text(),    //用户简介
        // },function(res){
        //
        // })
               // 实际使用时的提交信息
        $.post("/api/user/add",{
            userName : $(".userName").val(),  //登录名
            userEmail : $(".userEmail").val(),  //邮箱
            userSex : data.field.sex,  //性别
            userGrade : data.field.userGrade,  //会员等级
            userStatus : data.field.userStatus,    //用户状态
        //     newsTime : submitTime,    //添加时间
        //     userDesc : $(".userDesc").text(),    //用户简介
            },function(res){
        
            })
        
        setTimeout(function(){
            top.layer.close(index);
            top.layer.msg("用户添加成功！");
            layer.closeAll("iframe");
            //刷新父页面
            parent.location.reload();
        },2000);
        return false;
    })

    //格式化时间
    function filterTime(val){
        if(val < 10){
            return "0" + val;
        }else{
            return val;
        }
    }
    //定时发布
    var time = new Date();
    var submitTime = time.getFullYear()+'-'+filterTime(time.getMonth()+1)+'-'+filterTime(time.getDate())+' '+filterTime(time.getHours())+':'+filterTime(time.getMinutes())+':'+filterTime(time.getSeconds());

}) //end of layerui