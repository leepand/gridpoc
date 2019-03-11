/**
 * project: Arthur
 * author: leepand
 *
 */
//layerui加载层函数;!function()
layui.use(['element','form','layer'], function(){

var form = layui.form
        layer = parent.layer === undefined ? layui.layer : top.layer,
        $ = layui.jquery;	    	
	    
	   	function ityzl_SHOW_LOAD_LAYER(){
	   		return layer.msg('发布中...', {icon: 16,time:false,shade:0.8}) ;//{icon: 16,shade: [0.5, '#f5f5f5'],scrollbar: false,offset: '0px', time:100000}
	   	}
	   	function ityzl_SHOW_LOAD_LAYER_down(){
	   		return layer.msg('下线中...', {icon: 16,time:false,shade:0.8}) ;//{icon: 16,shade: [0.5, '#f5f5f5'],scrollbar: false,offset: '0px', time:100000}
	   	}
	   	function ityzl_CLOSE_LOAD_LAYER(index){
	   		layer.close(index);
	   	}
	   	function ityzl_SHOW_TIP_LAYER(){
	   		layer.msg('恭喜您，加载完成！',{time: 1000,offset: '10px'});
	   	}
        function ityzl_SHOW_TIP_LAYER_ERROR(){
	   		layer.msg('很遗憾，加载失败！',{time: 1000,offset: '10px'});
        }
/*服务列表-展示*/
var tmp = get_user_service_list();
function get_user_service_list(){
    var req_type = "GET";
    var req_url = "/api/service/user/list";
    var req_data = {"page": 1, "length":1000};
    ajax_request_service(req_type, req_url, req_data);
}

function buildSpan(aid,status){
    var statusName=status;
    var clsName="";
     if(status=="normal"){
                        statusName = "已上线";
         clsName=" layui-btn-green";
                    }else if(status == "stop"){
                        statusName = "已取消";
                         clsName=" layui-btn-danger";
                    }else if(status == "notpublish"){
                        statusName = "未上线";
                         clsName=" layui-btn-normal";
                    }
    var span='<span class="layui-btn '+clsName+' layui-btn-xs" id="spStatus'+aid+'">'+statusName+'</span>';
    return span
}

/* ajax 请求用户级的服务列表数据*/
function ajax_request_service(req_type, req_url, req_data){
    

    $.ajax({
        type: req_type,
        async: true,
        dataType: "json",
        url: req_url,
        data: req_data,
        error: function(){
            console.log("/api/service/user/list/error");
        },
        success: function(data){
            if(data.code == 101){
                //alert(data.message);
                swal({
                    title: "出错了！",
                    text: data.message
                });
            }
            if(data.code == 201){
                var serviceList="";
                
                if(!data.result){
                    $(".serviceList").html('<td>暂无 服务可发布，赶快添加吧</td>');
                    $("#data_count").html("0");
                    return;
                }
                
                var dataLen = data.result.service_list.length;
                //console.log('dddd',dataLen);
                //if(dataLen.length<1){
                //    $("table").append('<tr><td>暂无 服务可发布，赶快添加吧</td></tr>'); 
                //}
                
                
                for(var i = 0; i < dataLen; i++){
                    var algo_info = data.result.service_list[i];
                    var aid = algo_info["aid"];
                    //var uid = algo_info["uid"];
                    var algoname = algo_info["algoname"];
                    var atype= algo_info["atype"];
                    var algo_tm = algo_info["algo_tm"];
                    var token = algo_info["token"];
                    var host = algo_info["host"];
                    var _port = algo_info["port"];
                    var field = algo_info["field"];
                    var status = algo_info["status"];
                    var remark = algo_info["remark"];
                    var insert_tm = algo_info["insert_tm"];

                    if(field=="0"){
                        field = "文本分析";
                    }else if(field =='1'){
                        field = "机器学习";
                    }else if(field =='2'){
                         field = "计算机视觉";
                    }else if(field =='3'){
                         field = "深度学习";
                    }else{
                        field = "其他";
                    }
           
                    
            serviceList+= 
                "<tr><td>"+ aid +"</td>"+
                        //"<td>"+ uid +"</td>"+
                        "<td>"+ algoname +"</td>"+
                        "<td>"+ atype +"</td>"+
                        "<td>"+ token +"</td>"+
                        "<td>"+ host +"</td>"+
                        "<td>"+ _port +"</td>"+
                        "<td>"+ field +"</td>"+
                        "<td>"+ algo_tm +"</td>"+
                        "<td id='tdStatus"+aid+"'>"+buildSpan(aid,status)+"</td>"+
                        "<td>"+ remark +"</td>"+
                        "<td>"+ insert_tm +"</td>"+
                        "<td><div><a  class='layui-btn layui-btn-xs publishService' aId="+aid+">发布</a>  <a class='layui-btn layui-btn-xs layui-btn-danger' onclick=unpublish_service('"+ aid +"')>下线</a></div></td></tr>"//需要加载layui的样式del_user
                    ;
                    
                }
                $(".serviceList").html(serviceList);
                $('.dataTables-UserList').dataTable();//分页功能，需要在回调内执行才有效
            }
        }
    });
}

//onclick=publish_service('"+aid+"')
    //重设winner
$("body").on("click",".publishService",function(){
   var aid_btn = $(this).attr('aId');
    publish_service(aid_btn);
    })//end of use this function

/*发布服务*/
function publish_service(aid){
    var i;
    $.ajax({
        type: "POST",
        async: true,
        dataType: "json",
        url: "/api/service/algo_deploy",
        data: {"aid": aid},
        error: function() {
            console.log("/api/service/algo_deploy/error");
        },
        beforeSend: function(){
        i = ityzl_SHOW_LOAD_LAYER();
        // Handle the beforeSend event
        },
        
        success: function(data){
            if(data.code == 101){
                ityzl_CLOSE_LOAD_LAYER(i);
                swal({
                    title: "",
                    text: data.message
                });
                //alert(data.message);
            }
            if(data.code == 201){
                ityzl_CLOSE_LOAD_LAYER(i);
                $("#tdStatus"+aid).html(buildSpan(aid,'normal'));
                swal({
                    title: "发布服务成功！",
                    text: data.message
                });
                //get_user_list();
            }else{
                ityzl_CLOSE_LOAD_LAYER(i);
                //ityzl_SHOW_TIP_LAYER_ERROR()---也可以用layerui的信息弹窗
                //alert("删除用户失败[Error:" + data.message + "]");
                swal({
                    title: "发布服务失败！",
                    text: data.message
                });
            }
        }
    });  
}

/*服务下线*/
function unpublish_service(aid){
    var i;
    $.ajax({
        type: "POST",
        async: true,
        dataType: "json",
        url: "/api/service/algo_undeploy",
        data: {"aid": aid},
        error: function() {
            console.log("/api/service/algo_undeploy/error");
        },
        beforeSend: function(){
        i = ityzl_SHOW_LOAD_LAYER_down();
        // Handle the beforeSend event
        },
        
        success: function(data){
            ityzl_CLOSE_LOAD_LAYER(i);
            if(data.code == 101){
                
                swal({
                    title: "",
                    text: data.message
                });
                //alert(data.message);
            }
            if(data.code == 201){
                
                $("#tdStatus"+aid).html(buildSpan(aid,'stop'));
                swal({
                    title: "服务下线成功！",
                    text: data.message
                });
                //get_user_list();
            }else{
                //ityzl_SHOW_TIP_LAYER_ERROR()---也可以用layerui的信息弹窗
                //alert("删除用户失败[Error:" + data.message + "]");
                swal({
                    title: "服务下线失败！",
                    text: data.message
                });
            }
        }
    });  
}





/*添加服务*/
function add_service(){
    var projectname = $("#form_projname").val();
    var projectdesc = $("#form_projectdesc").val();
    var tags = $("#form_tags").val();
    var funcspath = $("#form_funcspath").val();
    var funclist = $("#form_funclist").val();
    var host = $("#form_host").val();
    var port = $("#form_port").val();
    var algo_field = $("#form_algo_field").val();
    var opertype = $("#form_opertype").val();
    var projecttm = $("#form_projecttm").val();
    var emailmsg = $("#form_emailmsg").val();
    var remark = $("#form_remark").val();
    if(opertype=="注册"){
                opertype = "register";
                }else if(opertype == "发布"){
                opertype = "publish";
                }
    $.ajax({
        type: "POST",
        async: true,
        dataType: "json",
        url: "/api/service/user/add",
        data: {
            "projectname":projectname,
            "projectdesc": projectdesc,
            "tags": tags,
            "funcspath": funcspath,
            "funclist": funclist,
            "host": host,
            "port": port,
            "algo_field": algo_field,
            "opertype": opertype,
            "projecttm": projecttm,
            "emailmsg": emailmsg,
            "remark": remark
        },
        error: function(){
            console.log("/api/service/user/add/error");
        },
        success: function(data){
            if(data.code == 101){
                //alert(data.message);
                swal({
                    title: "出错了！",
                    text: data.message
                });
            }
            if(data.code == 201){
                //alert("添加订单成功,请关闭窗口并刷新！");
                swal({
                    title: "Success！",
                    text: "添加订单成功,请关闭窗口并刷新！",
                    showCancelButton:false,
                    closeOnConfirm:true
                },function(){
                        location.href='/service_list.html';
                    });
            }
        }
    });
}










/*用户服务列表*/
function get_user_service_list2(){
    $.ajax({
        type: "GET",
        async: true,
        dataType: "json",
        url: "/api/service/user/list",
        error: function(){
            console.log("/api/service/user/list/error");
        },
        success: function(data){
            if(data.code == 101){
                //alert(data.message);
                swal({
                    title: "缺少权限，请联系管理员",
                    text: data.message
                });
            }
            if(data.code == 201){
                if(!data.result){
                    $("table tr").append("<p>当前用户列表为空，请先添加用户！</p>");
                    return;
                }
                $("table tr:not(:first)").empty();
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

                    $("table").append(
                        "<tr><td>"+ uid +"</td>"+
                        "<td>"+ nickname +"</td>"+
                        "<td>"+ username +"</td>"+
                        "<td>"+ password +"</td>"+
                        "<td>"+ phone +"</td>"+
                        "<td>"+ email +"</td>"+
                        "<td>"+ priv +"</td>"+
                        "<td>"+ lastlogin +"</td>"+
                        "<td><div><a  class='layui-btn layui-btn-xs'  onclick=edit_user('"+uid+"') >编辑</a>  <a class='layui-btn layui-btn-xs layui-btn-danger' href='#' onclick=del_user('"+ uid +"')>删除</a></div></td></tr>"//需要加载layui的样式
                    );
                }
                $('.dataTables-UserList').dataTable();
            }
        }
    });
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

/*编辑用户*/
function edit_user(uid){
    var params = "uid=" + uid;
     window.open("user_edit.html?"+params,null,null,true);
    //popWin.showWin("500","530","用户编辑","user_edit.html", params);
    layer.closeAll("iframe");
}
    //添加用户



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
                });
            }
        }
    });
}


/*添加用户*/
function add_user(){
    var nickname = $("#form_nickname").val();
    var username = $("#form_username").val();
    var password = $("#form_password").val();
    var phone = $("#form_phone").val();
    var email = $("#form_email").val();
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





/*layui.use(['form','layer'],function(){
    var form = layui.form
        layer = parent.layer === undefined ? layui.layer : top.layer,
        $ = layui.jquery;

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



<script>
//渲染service add form中所属领域/操作类型和邮件通知的样式
$$(function(){
layui.use(['form','layer'],function(){
    var form = layui.form
        layer = parent.layer === undefined ? layui.layer : top.layer,
        $$ = layui.jquery;
})  
});
</script>

})*/


})//end of layui-use