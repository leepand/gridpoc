/**
 * project: Arthur-run api example
 * author: leepand
 * date: 2019-01-31
 */


/*服务详情页查看被收藏者信息*/
function get_serv_staredInfo(userName,projectName){
    var req_data = {"username": userName,"algoname": projectName};
    
    $.ajax({
        type: "POST",
        async: true,
        dataType: "json",
        url: "/api/service/staredinfo",
        data: req_data,
        error: function(){
            console.log("/api/service/staredinfo/error");
        },
        success: function(data){
            var  staredUserTable = '';
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
                    $(".staredUserTable").html("<p>暂无收藏者！</p>");
                    return;
                }
                
                var stared_user_infoList =data.result.stared_info.stared_user_infoList;
                var stared_cnt =data.result.stared_info.stared_cnt;
                var dataLen = data.result.stared_info.stared_user_infoList.length;
                //console.log(data.result.request_cnt.body,'fff');
                var request_cnt = data.result.request_cnt.body;
                 //$("#staredCnt").html(stared_cnt);
                var li_focusOrNo;
                //if (dataLen>0){
                staredUserTable += '<li><small>服务信息</small></li>';
                staredUserTable += '<li><a style="font:12px;">收藏数 <small class="pull-right text-bold opacity-75">'+stared_cnt+'</small></a></li>';
                staredUserTable += '<li><a style="font:12px;">请求数 <small class="pull-right text-bold opacity-75">'+request_cnt+'</small></a></li>';
                //<!--<li><a >调用数 <small class="pull-right text-bold opacity-75">30</small></a></li>-->
                if (dataLen>0){
                staredUserTable += '<li class="hidden-xs"><small>最近收藏</small></li>';     
                }
                
                /*if(dataLen<1){
                    staredUserTable +='<p><small>暂无收藏者！</small></p>';
                }*/
                if(dataLen>6){
                    var top_star=6;
                }else{
                    var top_star=dataLen;
                }
                for(var i = 0; i < top_star; i++){//dataLen
                    
                    var userName_stared=stared_user_infoList[i]["userName"];
                    var phone_satred = stared_user_infoList[i]["phone"];
                    if(i<1){
                        li_focusOrNo ='<li class="hidden-xs focus">';
                    }else{
                        li_focusOrNo ='<li class="hidden-xs">';
                    }
            
                    staredUserTable += li_focusOrNo;
                    staredUserTable += '  <a href="/services/username='+userName_stared+'">';
                    staredUserTable += '<img class="img-circle img-responsive pull-left width-1" src="../static/assets/img/new_logo.png" alt="" />';
                    staredUserTable += ' <span class="text-medium" >'+userName_stared+'</span><br/> ';
                    staredUserTable += '<span class="opacity-50">'; 
                    staredUserTable += '<span class="glyphicon glyphicon-phone text-sm"></span> &nbsp;'+phone_satred+'</span>';       
                    staredUserTable += '    </a>';
                    staredUserTable += ' </li>';
                }
                $("#staredUserTable").html(staredUserTable);
            }
        }
    });
}
