layui.use(['form','layer','layedit','laydate','upload'],function(){
    var form = layui.form
        layer = parent.layer === undefined ? layui.layer : top.layer,
        laypage = layui.laypage,
        upload = layui.upload,
        layedit = layui.layedit,
        laydate = layui.laydate,
        $ = layui.jquery;
    //更新实验描述
    //值小于10时，在前面补0
function dateFilter(date){
    if(date < 10){return "0"+date;}
    return date;
}   
    var newDate;
    var dateObj = new Date(); //表示当前系统时间的Date对象
    var year = dateObj.getFullYear(); //当前系统时间的完整年份值
    var month = dateObj.getMonth()+1; //当前系统时间的月份值
    var date = dateObj.getDate(); //当前系统时间的月份中的日
    var day = dateObj.getDay(); //当前系统时间中的星期值
    var weeks = ["星期日","星期一","星期二","星期三","星期四","星期五","星期六"];
    var week = weeks[day]; //根据星期值，从数组中获取对应的星期字符串
    var hour = dateObj.getHours(); //当前系统时间的小时值
    var minute = dateObj.getMinutes(); //当前系统时间的分钟值
    var second = dateObj.getSeconds(); //当前系统时间的秒钟值
    var timeValue = "" +((hour >= 12) ? (hour >= 18) ? "晚上" : "下午" : "上午" ); //当前时间属于上午、晚上还是下午
    newDate = dateFilter(year)+"-"+dateFilter(month)+"-"+dateFilter(date)+" "+dateFilter(hour)+":"+dateFilter(minute)+":"+dateFilter(second);
    //console.log(newDate);
                                
                                
    $("body").on("click",".edit_desc",function(){
     var abName = get_request_args("name"); 
      var index =  layer.open({
        //id:1,
        type: 2,
        title:'Create algo online Service',
        shade: 0.8,  //遮罩透明度
        skin:'layui-layer-rim',
        area:['850px', '750px'],
        content: ['wizard-create-profile.html','no']
        ,
        style:'width:100%;heigth:100%;',
        //btn:['保存描述','取消'],
        btn1: function (index,layero) {
        //console.log('edit_desc',$("#form_edit_desc").val())  
        abexp_actions(abName,$("#form_edit_desc").val(),"update_desc");
        },
        btn2:function (index,layero) {
             layer.close(index);
        }
 
    });    
        
    })
//注册服务弹窗  
function addService(edit){
        var index =  layer.open({
        //id:1,
        type: 2,
        title:'Create algo online Service',
        shade: 0.8,  //遮罩透明度
        skin:'layui-layer-rim',
        area:['850px', '750px'],
        content: ['service_add.html','no']
        ,
        style:'width:100%;heigth:100%;',
        //btn:['保存描述','取消'],
        btn1: function (index,layero) {
        //console.log('edit_desc',$("#form_edit_desc").val())  
        abexp_actions(abName,$("#form_edit_desc").val(),"update_desc");
        },
        btn2:function (index,layero) {
             layer.close(index);
        }
 
    });  
    }
    $(".addService_btn").click(function(){
        addService();
    })
      
      function ityzl_SHOW_LOAD_LAYER(){
	   		return layer.msg('正在创建服务...', {icon: 16,time:false,shade:0.8}) ;
	   	}
	 function ityzl_SHOW_LOAD_LAYER_down(){
	   		return layer.msg('正在删除服务...', {icon: 16,time:false,shade:0.8}) ;
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
         
    form.on("submit(addService)",function(data){
        //弹出loading
  
    var projectname = $("#form_projname").val();
    var projectdesc = $("#form_projectdesc").val();
    var tags = $("#form_tags").val();
    var funcspath = $("#form_funcspath").val();
    var funclist = $("#form_funclist").val();
    var host = '0.0.0.0';//$("#form_host").val();
    var port = $("#form_port").val();
    var algo_field = $("#form_algo_field").val();
    var opertype = $("#form_opertype").val();
    var projecttm = newDate;
    var emailmsg = $("#form_emailmsg").val();
    var remark = $("#form_remark").val();
    if(opertype=="注册"){
                opertype = "register";
                }else if(opertype == "发布"){
                opertype = "publish";
                }
        console.log(emailmsg,opertype,'opertype')
        //$.post(
        var index;
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
        beforeSend: function(){
        //index = top.layer.msg('数据提交中，请稍候',{icon: 16,time:false,shade:0.8});
        index = ityzl_SHOW_LOAD_LAYER();
        // Handle the beforeSend event
        },
        success: function(data){
            ityzl_CLOSE_LOAD_LAYER(index);
            if(data.code == 101){
                //alert(data.message);
                swal({
                    title: "缺少参数",
                    text: data.message,
                    closeOnConfirm: true
                },function(){
                        layer.closeAll("iframe");
                        //parent.location.reload();
                    location.href='/service_list.html';
                    });
                //top.layer.msg(data.message);
                //top.layer.close(index);
                //layer.closeAll("iframe");
                
            }
            if(data.code == 201){
                
                //top.layer.msg("实验创建成功！");
                swal({
                    title: "成功提交",
                    text: "可以到服务列表页查看",
                    type: "success",
                    closeOnConfirm: true
                },function(){
                    setTimeout(function () {
                    //layer.close(index);需要在父级定位，不然会停留在弹窗内
                    parent.location.href ='service_list.html';
                }, 500);
                    
              //parent.location.reload();
                    });
            
            }
        }
        });
        return false;
        //setTimeout(function(){
        //    create_abtest(expid,explist,clientid,index);
            //top.layer.close(index);
            //top.layer.msg("文章添加成功！");
        //    layer.closeAll("iframe");
            //刷新父页面
        //    $(".layui-tab-item.layui-show",parent.document).find("iframe")[0].contentWindow.location.reload();
       // },500);
       // return false;
    
        
    })//end of form
    
    
    
    
    
    

/*添加服务*/
/*function add_service(){
    var projectname = $("#form_projname").val();
    var projectdesc = $("#form_projectdesc").val();
    var tags = $("#form_tags").val();
    var funcspath = $("#form_funcspath").val();
    var funclist = $("#form_funclist").val();
    var host = $("#form_host").val();
    var port = $("#form_port").val();
    var algo_field = $("#form_algo_field").val();
    var opertype = $("#form_opertype").val();
    var projecttm = newDate;
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
                        
                        location.href='service_list.html';
                    });
            }
        }
    });
}*/
    
})//end of layui.use