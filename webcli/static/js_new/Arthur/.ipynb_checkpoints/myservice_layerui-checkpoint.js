/**
 * project: Arthur
 * author: leepand
 *
 */

/*获取用户算法服务star状态及cnt----错误示范，ajax为异步，无法在循环中做返回值操作，所以该函数作废*/
function get_algo_star(uName,algoname,algoUser){
    var parmData = {'viewdUser':uName,'algoname':algoname,'algoUser':algoUser};
    var result = {};
    $.ajax({
        type: "POST",
        async: true,
        dataType: "json",
        url: "/api/service/algostarget",
        data: parmData,
        error: function(){
            console.log("/api/service/algostarget/error");
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
                //console.log('data.result;',data.result);
                result = data.result;
                
            }
        }
    });
    return result;
}
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
function layer_class(){
    var form = layui.form;
    form.on('select(selectMsg)',function(data){
        var len = $(".msgHtml tr").length;
        for(var i=0;i<len;i++){
            if(data.value == "0"){
                $(".msgHtml tr").eq(i).show();
                $(".msgHtml tr.no_msg").remove();
            }else{
                if($(".msgHtml tr").eq(i).find(".msg_collect i").hasClass("icon-star")){
                    $(".msgHtml tr").eq(i).show();
                }else{
                    $(".msgHtml tr").eq(i).hide();
                }
            }
        }
        if(data.value=="1" && $(".msgHtml tr").find(".msg_collect i.icon-star").length=="0"){
            $(".msgHtml").append("<tr class='no_msg' align='center'><td colspan='4'>暂无收藏消息</td></tr>")
        }
    });
}
/*算法服务列表*/
function get_algo_serv_list(Uname,sort_type,tagInfo){
    //Uname：登陆用户
    var req_data = {"UName": Uname,"Tag": tagInfo};
    
    $.ajax({
        type: "GET",
        async: true,
        dataType: "json",
        url: "/api/service/algolist",
        data: req_data,
        error: function(){
            console.log("/api/service/algolist/error");
        },
        success: function(data){
            var  algotable = '';
            var  search_star = '';
            if(data.code == 101){
                //alert(data.message);
                swal({
                    title: "缺少权限，请联系管理员",
                    text: data.message
                });
            }
            if(data.code == 201){
                if(!data.result){
                    //$("table tr").append("<p>当前算法服务列表为空，请先添加算法！</p>");
                    //$(".algotable").html("<p>当前算法服务列表为空，请先添加算法！</p>");
                    $(".algotable").html("<p>当前算法服务列表为空，请先添加算法！</p>");
                    return;
                }
                
                //$("table tr:not(:first)").empty();
                
                var dataLen = data.result.algolist.length;
                var userName = data.result.user;//登陆用户
                var star_info = data.result.star_info;
                var algo_User_star_all = data.result.algo_User_star_all;
                var algo_User_algocnt = data.result.algo_User_algocnt;
                //$("#algo_User_algocnt").html(algo_User_algocnt);
                //$("#algo_User_star_all").html(algo_User_star_all);
                var _span_status = '';
                var i_css='';
                var newestalgo_list=data.result.algolist;
                var algo_list_process=[];
            
                if(sort_type=='newest'){
                    newestalgo_list.sort(function(a,b){ 
                        var value1 = a.insert_tm, value2 = b.insert_tm; 
                        if(value1 === value2){ 
                            return b.algo_tm - a.algo_tm; }
                        return value2 - value1; 
                    });

                   algo_list_process=newestalgo_list;
                }
                
                else{
                   algo_list_process= newestalgo_list;
                }
                search_star='<blockquote class="layui-elem-quote news_search">'+
                    '<div class="layui-inline selectMsg">'+
                    '<select name="msgColl" lay-filter="selectMsg">'+
                    '<option value="0">全部</option>'+
                    '<option value="1">已收藏</option>'+
                    '</select></div>'+
                    '<div class="layui-inline">'+
                    '<div class="layui-form-mid layui-word-aux"></div></div></blockquote>';
  
                //algotable=search_star;
                for(var i = 0; i < dataLen; i++){
                    var algo_info = algo_list_process[i];
                    var insert_tm = algo_info["insert_tm"];
                    var algoname = algo_info["algoname"];
                    var algodesc = algo_info["algodesc"];
                    var algouser = algo_info["user_name"];//算法发布者
                    var algotable_inter='';

                    var star_status = star_info[algoname]['star_status'];
                    var star_cnt = star_info[algoname]['star_cnt'];
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
                    
                    if(star_status=='star'){
                      _span_status= '已收藏' ;
                      i_css = '"iconfont icon-star">';
                    }
                    else{
                      _span_status= '收藏' ;  
                      i_css = '"layui-icon">&#xe600;'
                    }
            
                    algotable_inter = '<div class="feed-element">'+
                        '<a href="#" class="pull-left">'+
                        '<img alt="image" class="img-circle" src="../static/images/people.png">'+
                        '</a>'+
                        '<div class="media-body ">'+
                        '<small class="pull-right text-navy list-time">'+insert_tm+'</small>'+
                        '<a href="/username='+algouser+'&;projectname='+algoname+'">'+
                        '<strong>'+algoname+'</strong>.</a>'+'<br>'+
                        '<small class="text-muted">'+algouser+'/'+algoname+'</small>'+'<br>'+
                        '<p>'+algodesc+'</p>'+
                        '<div class="actions" algo_User_star_all='+algo_User_star_all+' status='+star_status+' num='+star_cnt+' onclick=algo_ifnot_star(this,"'+userName+'","'+algoname+'","'+algouser+'")>'+
                        '<a class="layui-btn layui-btn-mini layui-btn-xs layui-btn-normal msg_collect" ><i class='+i_css+'</i> <span>'+_span_status+'</span><strong>'+ star_cnt+'</strong></a>'+
                        '</div></div></div>';
            algotable+=algotable_inter;
                       
                }
                $("#algo_User_algocnt").html(algo_User_algocnt);
                $("#algo_User_star_all").html(algo_User_star_all);
                $("#search_star").html(search_star);
                $(".algotable").html(algotable);
                $(".list-time").relativeTime();
                //$(".algotable").html(algotable);
                //$('.dataTables-UserList').dataTable();
                //渲染选择框的样式
                layui.use(['form','layer','layedit'], function(){
                var form = layui.form,
                layer = parent.layer === undefined ? layui.layer : parent.layer,
                layedit = layui.layedit;
                $ = layui.jquery;
		  
                form.on('select(selectMsg)',function(data){
                    var len = $(".algotable div").length;
                    for(var i=0;i<len;i++){
                        if(data.value == "0"){
                            $(".algotable div").eq(i).show();
                            $(".algotable div.no_msg").remove();
                        }else{
                            if($(".algotable div").eq(i).find(".msg_collect i").hasClass("icon-star")){
                                $(".algotable div").eq(i).show();
                            }
                            else{
                                $(".algotable div").eq(i).hide();
                            }
                        }
                    }
                    if(data.value=="1" && $(".algotable div").find(".msg_collect i.icon-star").length=="0"){
                        $(".algotable").html("<tr class='no_msg' align='center'><td colspan='4'>暂无收藏算法</td></tr>")
                    }
                    })
                });
                
                
                
   
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
        // num = Number(v)-1;
       // console.log('newnums2',num);
        //algo_User_star_all=Number(algo_User_star_all)+1;
        //$(obj).attr('algo_User_star_all',algo_User_star_all);
        //$("#algo_User_star_all").html(algo_User_star_all);
        update_algo_star(uname,algoname,algoUser,'star',num);
        $(obj).html('<a class="layui-btn layui-btn-mini layui-btn-xs layui-btn-normal msg_collect" ><i class="iconfont icon-star"></i> <span>已收藏</span><strong>'+ num+'</strong></a>');
        }

}

 


