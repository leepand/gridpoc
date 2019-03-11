/**
 * project: Arthur
 * author: leepand
 *
 */



 /*更新用户算法服务star状态及cnt*/
    function update_algo_star(uName,algoname,algoUser,status_star,cnt_star){
    var parmData = {'viewdUser':uName,'algoname':algoname,'algoUser':algoUser,'star_status':status_star,'star_cnt':cnt_star};

    $.ajax({
        type: "POST",
        async: true,
        dataType: "json",
        url: "/api/service/algostarupdate",
        data: parmData,
        error: function(){
            console.log("/api/service/algostarupdate/error");
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
                
                 console.log('成功更新star状态!')
                
            }
        }
    });
}
//获取收藏信息并持久化从div的子节点寻找（埋点）
    function algo_ifnot_star(obj,uname,algoname,algoUser){
    //var req_data = {"UName": uname,"algoname":algoname};
    var span=$(obj).find("span");
    var status=$(obj).attr('status');
    var num=$(obj).attr('num');
    var algo_User_star_all = $(obj).attr('algo_User_star_all');
    //console.log(num);
    //console.log(status);
    if(status=='star'){
        $(obj).attr('status','nostar');
        num=Number(num)-1;
        $(obj).attr('num',num);
        // num = Number(v)+1;
        //function(n,v){
        //      return Number(v)+1;}
        //console.log('newnums',num);
        //更新算法的star同时更新用户级star总数，注意同时需要通过attr传回页面标示变动
        //algo_User_star_all=Number(algo_User_star_all)-1;
        //$(obj).attr('algo_User_star_all',algo_User_star_all);
        //$("#algo_User_star_all").html(algo_User_star_all);
        update_algo_star(uname,algoname,algoUser,'nostar',num);
        $(obj).html('<a class="layui-btn layui-btn-mini layui-btn-xs layui-btn-normal msg_collect" ><i class="layui-icon">&#xe600;</i> <span>收藏</span><strong>'+ num+'</strong></a>');
    }
    else
        {
        $(obj).attr('status','star');
        num=Number(num)+1;
        $(obj).attr('num',num);

        update_algo_star(uname,algoname,algoUser,'star',num);
        $(obj).html('<a class="layui-btn layui-btn-mini layui-btn-xs layui-btn-normal msg_collect" ><i class="iconfont icon-star"></i> <span>已收藏</span><strong>'+ num+'</strong></a>');
        }

}



layui.use(['form','layer','laydate','table','upload','layedit'],function(){
    var form = layui.form,
        layer = parent.layer === undefined ? layui.layer : top.layer,
        $ = layui.jquery,
        laydate = layui.laydate,
        upload = layui.upload,
        table = layui.table;
    //给数字添加逗号--美元数字:10,000
    // Add commas to a number
    my={
    }
    my.addCommas = function (n) {
      while (/(\d+)(\d{3})/.test(n.toString())) {
        n = n.toString().replace(/(\d+)(\d{3})/, '$1'+','+'$2');
      }
      return n;
    };
    //判断字符是否为空的方法
    function isEmpty(obj){
        if(obj == "undefined" || obj == null || obj == ""){
            return true;
        }else{
            return false;
        }
    }
    function buildTdActionStatus(aid,status,tdtype){
        var serviceStatusContent=status;
        var serviceStatusCss="";
        var actionBtn = '';
        var actionBtnIcon = '';
        var tdContent,actionBtnColor;
        if (status=="normal"){
            //如果服务的status：normal-正常，unpublished-未发布，stop-停止
            serviceStatusContent = 'RUNNING';
            serviceStatusCss = '<a class="layui-btn layui-btn-xs layui-btn-green">';
            actionBtn = ' UNPUBLISH';
            actionBtnIcon='<i class="fa fa-cloud-download"></i>';
            actionBtnColor='layui-bg-cyan';
        }else if(status=="notpublish"){
            serviceStatusContent = ' UNPUBLISH';
            serviceStatusCss = '<a class="layui-btn layui-btn-xs layui-btn-warm">'; 
            actionBtn = ' PUBLISH'; 
            actionBtnIcon='<i class="fa fa-cloud-upload"></i>';
            actionBtnColor='layui-bg-blue';
        }else{
            serviceStatusContent = 'FAILED';
            serviceStatusCss = '<a class="layui-btn layui-btn-xs layui-btn-danger">';  
            actionBtn = ' PUBLISH';
            actionBtnIcon='<i class="fa fa-cloud-upload"></i>';
            actionBtnColor='layui-bg-blue';
        }
    if(tdtype=="status"){
        tdContent = serviceStatusCss+serviceStatusContent;
    }else{
        tdContent = '    <a class="layui-btn layui-btn-xs '+actionBtnColor+' serviceActions" aId='+aid+'>'+actionBtnIcon+ actionBtn+'</a>';
    }
        //'<a class="layui-btn layui-btn-xs layui-bg-green serviceActions" aId='+aId+'>'+actionBtnIcon+ actionBtn+'</a>'
    //var action_type= '    <a class="layui-btn layui-btn-xs layui-bg-green serviceActions" aId='+aId+'>'+actionBtnIcon+ actionBtn+'</a>';
    //var span='<span class="layui-btn '+clsName+' layui-btn-xs" id="spStatus'+aid+'">'+statusName+'</span>';
    return tdContent;
    }
    var index2 = layer.load(1, {
        shade: [2.9,'#fff'] //0.1透明度的白色背景
    });

    function fechServLoding(){
        return layer.load(1, {
            shade: [0.8,'#fff'] //0.1透明度的白色背景
        });//layer.msg('加载算法...', {icon: 16,time:false,shade:0.8}) ;//{icon: 16,shade: [0.5, '#f5f5f5'],scrollbar: false,offset: '0px', time:100000}
    }

    function fechServLodingClose(index){
        layer.close(index);
    }
     
       //排序函数
    function sortServices(services, sortKey) {
            var self = this;

            // Sort by popularity
            if(sortKey == 'popularity') {
                services.sort(function(serviceA, serviceB) {
                    var pointsOfA = serviceA.childs.length;
                    var pointsOfB = serviceB.childs.length;

                    if(self.options.enableUpvoting) {
                        pointsOfA += serviceA.upvoteCount;
                        pointsOfB += serviceB.upvoteCount;
                    }

                    if(pointsOfB != pointsOfA) {
                        return pointsOfB - pointsOfA;

                    } else {
                        // Return newer if popularity is the same
                        var createdA = new Date(serviceA.created).getTime();
                        var createdB = new Date(serviceB.created).getTime();
                        return createdB - createdA;
                    }
                });

            // Sort by date
            } else {
                services.sort(function(commentA, commentB) {
                    var createdA = new Date(commentA.insert_tm).getTime();
                    var createdB = new Date(commentB.insert_tm).getTime();
                    //console.log(createdA,createdB)
                    if(sortKey == 'oldest') {
                        return createdA - createdB;
                    } else {
                        return createdB - createdA;
                    }
                });
            }
    }
    
    
    //加载我的算法list
    getMyServiceList('myself','notnewest','NonetagQuery');
    function getMyServiceList(Uname,sort_type,tagInfo){
        //Uname：登陆用户
        var req_data = {"UName": Uname,"Tag": tagInfo};
        var loading;
        $.ajax({
            type: "GET",
            async: true,
            dataType: "json",
            url: "/api/service/algolist",
            data: req_data,
            error: function(){
                console.log("/api/service/algolist/error");
            },
            beforeSend: function(){
            loading = fechServLoding();
            // Handle the beforeSend event
            },
            
            success: function(data){
                fechServLodingClose(loading);
                if(data.code == 101){
                    alert(data.message);
                }
                if(data.code == 201){
                    if(!data.result){
                        return;
                    }
                    var myalgo_list=data.result.algolist;
                    var userName = data.result.user;//登陆用户
                    var star_info = data.result.star_info;
                    var algo_request_info =data.result.algo_request_info;
                    var algo_User_star_all = data.result.algo_User_star_all;
                    var algo_User_algocnt = data.result.algo_User_algocnt;
                    /*// Create items array
                    var items = Object.keys(algo_request_info).map(function(key) {
                        return [key, algo_request_info[key]];
                    });
                    var cnt_req=0;
                    $(items).each(function(index, item) {
                        //console.log(items[index][1],'cnt_req');
                        cnt_req+=items[index][1];
                    });*/
                   
                    myServiceListHtml('self',star_info,algo_request_info,algo_User_star_all,algo_User_algocnt,Uname,userName,myalgo_list);
                    myServiceListHtml('star',star_info,algo_request_info,algo_User_star_all,algo_User_algocnt,Uname,userName,myalgo_list);
                    setTimeout(function(){
                        $('.time-ago-service').relativeTime();
                        $('.dataPages-ServiceList').dataTable({"bFilter": false,"bLengthChange": false,"bSort": false});//分页功能，需要在回调内执行才有效
                        $('.dataPages-ServiceStarList').dataTable({"bFilter": false,"bLengthChange": false,"bSort": false});//分页功能，需要在回调内执行才有效
                        
                        },0) 
        }//end of 201
                
        }//end of sucess
        });
    }
    //加载service list 页面渲染信息
    
    function myServiceListHtml(display_type,star_info,algo_request_info,algo_User_star_all,algo_User_algocnt,Uname,userName,service_list){
        var servicelistHtmlStar,servicelistHtmlSelf;
        var servicelistHtml='';
        var serviceStatusContent = '';
        var serviceStatusCss= '';
        var actionBtn = '';
        var actionBtnIcon = '';
        var _span_status,i_css,action_type;
        var cnt_req=0;

        sortServices(service_list,"newest");
        if(service_list.length<1){
            servicelistHtmlStar = '<td>暂无 该状态下的 服务</td>';
            servicelistHtmlSelf = '<td>暂无 该状态下的 服务</td>';
        }else{
            for(var i=0; i < service_list.length; i++){
                var star_status = star_info[service_list[i].algoname]['star_status'];
                var star_cnt = star_info[service_list[i].algoname]['star_cnt'];
                var algouser = service_list[i].user_name;//算法发布者
                var algoname = service_list[i].algoname;
                var aId = service_list[i].aid;
                if(Uname!='myself' && Uname!='zoo'){
                       if(algouser!=Uname){
                        //剔除掉收藏算法的作者的星星数和算法发布数
                           algo_User_algocnt= Number(algo_User_algocnt)-1;
                           algo_User_star_all = Number(algo_User_star_all)-Number(star_cnt);
                        } 
                    }else{
                        if(algouser!=userName){
                            //传进来的Uname如果不是zoo或myself，则为other页面传去的参数，即开发者名字
                            algo_User_algocnt= Number(algo_User_algocnt)-1;
                            algo_User_star_all = Number(algo_User_star_all)-Number(star_cnt);
                            
                        }else{
                            if(display_type=="self"){
                                //新增算法服务调用次数总和/user 2019-03-04
                                cnt_req+=algo_request_info[algoname];
                                
                                //console.log(algo_request_info[algoname],'algonamealgonamealgoname',algoname);  
                            }
                          
                        }
                    }
                
                if (service_list[i].status=="normal"){
                    //如果服务的status：normal-正常，unpublished-未发布，stop-停止
                    serviceStatusContent = 'RUNNING';
                    serviceStatusCss = '<a class="layui-btn layui-btn-xs layui-btn-green">';
                    actionBtn = ' UNPUBLISH';
                    actionBtnIcon='<i class="fa fa-cloud-download"></i>';
                }else if(service_list[i].status=="notpublish"){
                    serviceStatusContent = ' UNPUBLISH';
                    serviceStatusCss = '<a class="layui-btn layui-btn-xs layui-btn-warm">';  
                    actionBtn = ' PUBLISH'; 
                    actionBtnIcon='<i class="fa fa-cloud-upload"></i>';
                }else{
                    serviceStatusContent = 'FAILED';
                    serviceStatusCss = '<a class="layui-btn layui-btn-xs layui-btn-danger">';  
                    actionBtn = ' PUBLISH';
                    actionBtnIcon='<i class="fa fa-cloud-upload"></i>';
                }
                //区分收藏的服务和自己的服务action
                if(star_status=='star'){
                      _span_status= '已收藏' ;
                      i_css = '"iconfont icon-star">';
                    }else{
                      _span_status= '收藏' ;  
                      i_css = '"layui-icon">&#xe600;';
                    }
                
                if(service_list[i].user_name==userName){
                    action_type= '  <td class="msg_opr" id="tdAction'+aId+'">'
                    + buildTdActionStatus(aId,service_list[i].status,'action')
                    + '  </td>';
                   }else{
                       action_type = '  <td class="msg_opr">'
                           + '<div class="actions" algo_User_star_all=' + algo_User_star_all
                           + ' status=' + star_status
                           + ' num=' + star_cnt
                           + ' onclick=algo_ifnot_star(this,"'+ userName+'","'+algoname+'","'+algouser+'")>'
                           + '<a class="layui-btn layui-btn-mini layui-btn-xs layui-btn-normal msg_collect" ><i class='+i_css
                           +'</i> <span>'+_span_status
                           +'</span><strong>'+ star_cnt
                           +'</strong></a></div>'
                           + '  </td>';
                   }
                //页面展示内容
                servicelistHtml = '<tr>'
                 + '  <td class="myablist_info">'
                 + '    <div class="algo-info">'
                 + '        <a href="/username='+service_list[i].user_name+'&;projectname='+service_list[i].algoname+'" " class="algo-info__name algo-info-link">'+service_list[i].algoname+'</a><br>'
                 +     '<small class="text-muted algo-url">'+service_list[i].user_name+'/'+service_list[i].algoname+'</small>'+'<br></br>'
                 + '        <p class="algo-list-body">'+service_list[i].algodesc+'</p>'
                 + '    </div>'
                 + '  </td>'
                 + '  <td class="ab_status" id="tdStatus'+aId+'">'+buildTdActionStatus(aId,service_list[i].status,'status')+'</a></td>'//serviceStatusCss+serviceStatusContent
                 + '  <td class="ab_createtime666"><small class="text-navy"> <span class="time-ago-service">'+service_list[i].insert_tm+'</span></small></td>'
                 //+ '  <td class="msg_opr" id="tdAction'+aId+'">'
                 + action_type
                 //+ '  </td>'
                 + '</tr>';
                
                if(service_list[i].user_name==userName){
                    servicelistHtmlSelf += servicelistHtml;
                    servicelistHtmlStar += '';
                }else{
                    servicelistHtmlStar += servicelistHtml;
                    servicelistHtmlSelf += ''; 
                }
            }}//end of list是否为空的判断
        $("#algo_User_algocnt").html(algo_User_algocnt);
        $("#algo_User_star_all").html(algo_User_star_all);
        if(display_type=='self'){
            
            if(isEmpty(servicelistHtmlSelf)){
            servicelistHtmlSelf = '<td>暂无 该状态下的 服务</td>';
            }
            $(".My_servicelistHtml").html(servicelistHtmlSelf); 
            //新增算法服务调用次数总和/user 2019-03-04
            $("#cnt_req").html(my.addCommas(cnt_req));
        }else{
            if(isEmpty(servicelistHtmlStar)){
                servicelistHtmlStar = '<td>暂无 该状态下的 服务</td>';
            }
             $(".MyStar_servicelistHtml").html(servicelistHtmlStar); 
        }
    }
    
    $("body").on("click",".serviceActions",function(){
        var servName = $(this).parents("tr").find(".algo-info .algo-info-link").text();
        var servStatus = $(this).parents("tr").find(".ab_status").text();
        var aid_btn = $(this).attr('aId');
        if(servStatus=='RUNNING'){
            var _msg_info='下线服务';
        }else{
            var _msg_info='发布服务';
        }
        layer.confirm('你确定'+_msg_info+'「'+servName+'」吗?', {icon: 3, title: _msg_info}, function () {
          
            if(servStatus=='RUNNING'){
                unpublish_service(aid_btn);
            }else{
                publish_service(aid_btn);
            }
                
                // })
            },function(){
                  layer.msg('我再想想', {icon: 1});
               });       
        })
    
    function ityzl_SHOW_LOAD_LAYER(){
        return layer.msg('发布中...', {icon: 16,time:false,shade:0.8}) ;//{icon: 16,shade: [0.5, '#f5f5f5'],scrollbar: false,offset: '0px', time:100000}
    }
    function ityzl_SHOW_LOAD_LAYER_down(){
        return layer.msg('下线中...', {icon: 16,time:false,shade:0.8}) ;//{icon: 16,shade: [0.5, '#f5f5f5'],scrollbar: false,offset: '0px', time:100000}
    }
    function ityzl_CLOSE_LOAD_LAYER(index){
        layer.close(index);
    }
    
         
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
                //$("#tdStatus"+aid).html(buildSpan(aid,'normal'));
                $("#tdStatus"+aid).html(buildTdActionStatus(aid,'normal','status'));
                $("#tdAction"+aid).html(buildTdActionStatus(aid,'normal','action'));
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
                
                //$("#tdStatus"+aid).html(buildSpan(aid,'stop'));
                $("#tdStatus"+aid).html(buildTdActionStatus(aid,'stop','status'));
                $("#tdAction"+aid).html(buildTdActionStatus(aid,'stop','action'));
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


})//end of layui.use
