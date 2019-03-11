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
        //更新算法的star同时更新用户级star总数，注意同时需要通过attr传回页面标示变动
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
    
    /*获取URL传过来的参数*/
    function get_request_args(argname){  
        var url = decodeURI(document.location.href);//需要解码，一些参数有空格等
        var arrStr = url.substring(url.indexOf("?")+1).split("/");//根据实际页面修改
        //console.log('arrStr',arrStr);
        for(var i = 0; i < arrStr.length; i++) {
            var loc = arrStr[i].indexOf(argname+"=");  
            if(loc != -1){
                //console.log('loc',loc);
                return arrStr[i].replace(argname+"=","").replace("?","");
                break;
            }
        }
        return "";
    }
    var TagName = get_request_args("tag"); 
    //console.log(TagName,"TagName",typeof TagName,decodeURI("http://0.0.0.0:9010/tags/tag=Machine%20Learning"));
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
    
    //加载zoo算法list
    if (!isEmpty(TagName)) {
        getMyServiceList('zoo','notnewest',TagName);
    }else{
        getMyServiceList('zoo','notnewest','NonetagQuery');
    }
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
                    console.log(myalgo_list);
                    var userName = data.result.user;//登陆用户
                    var star_info = data.result.star_info;
                    var algo_request_info =data.result.algo_request_info;
                    var algo_User_star_all = data.result.algo_User_star_all;
                    var algo_User_algocnt = data.result.algo_User_algocnt;  
                    myServiceListHtml('popularity',star_info,algo_request_info,algo_User_star_all,algo_User_algocnt,Uname,userName,myalgo_list);
                    myServiceListHtml('staredinfo',star_info,algo_request_info,algo_User_star_all,algo_User_algocnt,Uname,userName,myalgo_list);
                    myServiceListHtml('newest',star_info,algo_request_info,algo_User_star_all,algo_User_algocnt,Uname,userName,myalgo_list);
                    setTimeout(function(){
                        $('.time-ago-service').relativeTime();
                        $('.dataPages-ServiceList').dataTable({"bFilter": false,"bLengthChange": false,"bSort": false});//分页功能，需要在回调内执行才有效
                        $('.dataPages-ServiceStarList').dataTable({"bFilter": false,"bLengthChange": false,"bSort": false});//分页功能，需要在回调内执行才有效
                        
                        },0) 
        }//end of 201
                
        }//end of sucess
        });
    }
    //排序函数
    function sortServices(services, sortKey,staredinfo,algo_request_info) {
        var self = this;
        // Sort by popularity
        if(sortKey == 'popularity') {
            services.sort(function(serviceA, serviceB) {
                var pointsOfA = algo_request_info[serviceA.algoname];
                var pointsOfB = algo_request_info[serviceB.algoname];
                if(pointsOfB != pointsOfA) {
                    return pointsOfB - pointsOfA;
                } else {
                    // Return newer if popularity is the same
                    var createdA = new Date(serviceA.insert_tm).getTime();
                    var createdB = new Date(serviceB.insert_tm).getTime();
                    return createdB - createdA;
                }
            });
        } else if(sortKey == 'staredinfo'){//Sort by stared
            services.sort(function(serviceA, serviceB){
                var pointsOfA = staredinfo[serviceA.algoname]['star_cnt'];
                var pointsOfB = staredinfo[serviceB.algoname]['star_cnt'];
                if(pointsOfB != pointsOfA) {
                    return pointsOfB - pointsOfA;
                } else {
                    // Return newer if popularity is the same
                    var createdA = new Date(serviceA.insert_tm).getTime();
                    var createdB = new Date(serviceB.insert_tm).getTime();
                    return createdB - createdA;
                }
            });
        }else {// Sort by date
            services.sort(function(commentA, commentB) {
                var createdA = new Date(commentA.insert_tm).getTime();
                var createdB = new Date(commentB.insert_tm).getTime();
                console.log(createdA,createdB)
                if(sortKey == 'oldest') {
                    return createdA - createdB;
                } else {
                    return createdB - createdA;
                }
            });
        }
    }
    
    //加载service list 页面渲染信息
    function myServiceListHtml(display_type,star_info,algo_request_info,algo_User_star_all,algo_User_algocnt,Uname,userName,service_list){
        var servicelistHtmlMostStared,servicelistHtmlMostCalled;
        var servicelistHtmlRecentlyAdded;
        var servicelistHtml='';
        var serviceStatusContent = '';
        var serviceStatusCss= '';
        var actionBtn = '';
        var actionBtnIcon = '';
        var _span_status,i_css,action_type;
        var sort_service_list;
        
        sortServices(service_list,display_type,star_info,algo_request_info);

        if(service_list.length<1){
            servicelistHtmlMostStared = '<td>暂无 该状态下的 服务</td>';
            servicelistHtmlMostCalled = '<td>暂无 该状态下的 服务</td>';
            servicelistHtmlRecentlyAdded = '<td>暂无 该状态下的 服务</td>';
        }else{
            //for(var i=0; i < service_list.length; i++)
            service_list.forEach(function(serviceModel,i){
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
                
                //页面展示内容
                servicelistHtml += '<tr>'
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
            
            })}//end of list是否为空的判断
        $("#algo_User_algocnt").html(algo_User_algocnt);
        $("#algo_User_star_all").html(algo_User_star_all);
        
        if(display_type=='popularity'){
            if(isEmpty(servicelistHtmlMostCalled)){
                 servicelistHtmlMostCalled= '<td>暂无 该状态下的 服务</td>';
            }
            $(".servicelistHtmlMostCalled").html(servicelistHtml); 
        }else if(display_type=='staredinfo'){
            if(isEmpty(servicelistHtmlMostStared)){
                servicelistHtmlMostStared = '<td>暂无 该状态下的 服务</td>';
            }
            $(".servicelistHtmlMostStared").html(servicelistHtml); 
        }else if(display_type=='newest'){
          if(isEmpty(servicelistHtmlRecentlyAdded)){
                servicelistHtmlRecentlyAdded = '<td>暂无 该状态下的 服务</td>';
            }  
            $(".servicelistHtmlRecentlyAdded").html(servicelistHtml); 
        }
    }

})//end of layui.use
