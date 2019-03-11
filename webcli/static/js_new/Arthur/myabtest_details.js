layui.use(['form','layer','layedit','laydate','upload'],function(){
    var form = layui.form
        layer = parent.layer === undefined ? layui.layer : top.layer,
        laypage = layui.laypage,
        upload = layui.upload,
        layedit = layui.layedit,
        laydate = layui.laydate,
        $ = layui.jquery;

    //用于同步编辑器内容到textarea
    layedit.sync(editIndex);
    /*获取URL传过来的参数*/
    function get_request_args(argname){  
        var url = document.location.href;
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
  //layer.alert('name',parent.layer);//弹出提示 “aaa”
    //渲染abdetails页面
    function gen_echart4exp_alts(exp_name_list4Echart,data_date4Echart,exp_info_list4Echart){
        var lineChart = echarts.init(document.getElementById("echarts-line-chart"));
        var option = {
        title: {
            text: 'Cumulative Conversion Rate'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data:exp_name_list4Echart//['实验1','实验2']
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data:data_date4Echart// ['2018-11-06','2018-11-07','2018-11-08','2018-11-09','2018-11-10','2018-11-11','2018-11-12']
            },
            yAxis: {
                type: 'value'
            },
            series: exp_info_list4Echart
            }
            lineChart.setOption(option);
        }
    gen_ab_details_css();//出发ab详情页的class和id样式
    function gen_ab_details_css(){
        var abName = get_request_args("name"); 
        var exp_alt_info ='';
        var exp_process_info='';
        $.ajax({
            type: "GET",
            async: true,
            dataType: "json",
            url: "/api/abtest/myabdetails",
            data: {"abname":abName},
            error: function(){
                console.log("/api/abtest/myabdetails/error");
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
            var exp_alt_list = result.exp_daily_details ; 
            var exp_total_info = result.obj;
            var Abstatus_css,Abstatus,Winstatus;
            var exp_compute_info= result.exp_compute_info;//for 进度条
            //$("#pause_status").html(exp_total_info.is_paused);
            $("#id_total_participants").html(exp_compute_info.total_participants);
            $("#id_total_conversionss").html(exp_compute_info.total_conversions);  
            $("#id_created_at").html(exp_compute_info.created_at);  
            $("#id_kpis").html(exp_compute_info.kpis.toString());  
            $("#id_description").html(exp_compute_info.description); 
            $("#id_description_title").html(exp_compute_info.description);
            $("#id_abName").html(abName);
            if (exp_total_info.is_paused){
                $(".pause_exp").html('<i class="fa fa-check-circle"></i> 开始实验');     
            }else{
                $(".pause_exp").html('<i class="fa fa-check-circle"></i> 暂停实验');  
            }
                
            $(".edit_desc").html('<i class="fa fa-edit"></i> 编辑实验描述');
            $(".reset_winner").html('<i class="fa fa-refresh"></i> 重选获胜组'); 
            $(".reset_exp").html('<i class="fa fa-refresh"></i> 重设实验');  
            if (exp_total_info.is_archived){
                //如果实验is_archived：判断是否决胜，如果决胜了推送，否则实验结束
                //console.log('ddddd',$("body").find(".pause_exp"));
                //$(".pause_exp").addClass('layui-hide');
                
                if (exp_total_info.has_winner){
                    Winstatus = "win";
                    Abstatus="已决出";
                    Abstatus_css = '<a class="layui-btn layui-btn-xs layui-btn-warm">';
                 }
                else{
                    Abstatus="已结束";
                    Abstatus_css = '<a class="layui-btn layui-btn-xs label-default">';
                }  
             }
            
            else{
                $("body").find(".end_exp").removeClass('layui-hide');//实验结束按钮不会在结束详情页出现
                //$(".end_exp").html('<i class="fa fa-check-circle"></i> 停止实验');
                
                //如果实验没有is_archived：判断是否决胜，如果决胜了推送，继续判断是否暂停，如果暂停标注暂停状态，否则运行中
                if (exp_total_info.has_winner){
                    Winstatus = "win";
                    Abstatus="已决出";
                    Abstatus_css = '<a class="layui-btn layui-btn-xs layui-btn-warm">';
                 }
                else{
                   if(exp_total_info.is_paused){
                       Abstatus="已暂停"; 
                       Abstatus_css = '<a class="layui-btn layui-btn-xs layui-btn-danger">';  
                       
                   }
                    else{
                       Abstatus="运行中"; 
                       Abstatus_css = '<a class="layui-btn layui-btn-xs layui-btn-green">';  
                    }
                   
                }                  

            }//end of 实验状态判断
            console.log('exp_info.total_coversion_rate',exp_compute_info.total_coversion_rate);
            //头部信息生成
            exp_process_info += '<dl class="dl-horizontal">';
            exp_process_info += '<dt>状态：</dt>' ;
            exp_process_info += '<dd>'+Abstatus_css+Abstatus+'</a>' ;   
            exp_process_info += ' </dd><br>';        
            exp_process_info += '<dt>转化情况</dt>';
            exp_process_info += '<dd>';
            exp_process_info += '<div class="progress progress-striped active m-b-sm">';
            exp_process_info += '<div style="width: '+exp_compute_info.total_coversion_rate+'%;" class="progress-bar"></div>';                        
            exp_process_info += '        </div>';
            exp_process_info += '   <small>当前总的转化率 <strong>'+exp_compute_info.total_coversion_rate+'%</strong></small>';                            
            exp_process_info += ' </dd>';
            exp_process_info += ' </dl>';    
            $(".exp_process_info").html(exp_process_info);
            var exp_info_list4Echart = result.exp_info_list4Echart;
            var exp_name_list4Echart = result.exp_name_list4Echart;
            var data_date4Echart = result.data_date4Echart;
            var chose_exp_status;
            $("#id_api_namespace").html(exp_name_list4Echart.toString());
            //update 2019-03-05 将alternatives数组调用格式改成&==&amp;
            var exp_name_list4EchartHtml="";
            $(exp_name_list4Echart).each(function(index, item) {
                exp_name_list4EchartHtml += '&amp;alternatives=<code><span>'+exp_name_list4Echart[index].toString()+'</span></code>';
            })
            $("#id_api_namespace_url").html(exp_name_list4EchartHtml);
            //$("#id_api_namespace_url").html(exp_name_list4Echart.toString());
            gen_echart4exp_alts(exp_name_list4Echart,data_date4Echart,exp_info_list4Echart);//初始化作图
        
            for(var i=0; i< exp_alt_list.length; i++){
            console.log('exp_alt_list[i].is_control_label',exp_alt_list[i].is_control_label);
            //var tot_convert_rate = parseInt(exp_alt_list.completed_count)/exp_alt_list.participant_count;
            //实验数据生成
            var index_exp_circle = Number(i) + 1;
                
            if(exp_alt_list[i].is_winner){
               
                chose_exp_status = '<i class="icon-white icon-ok"></i></span>';//'<i class="fa fa-check-circle-o"></i></span>';
            }else{
                chose_exp_status = '</span>';//'<i class="fa fa-circle-o"></i></span>';
            }
            exp_alt_info += '<tr>';
            exp_alt_info += '  <td>';
            exp_alt_info += '<span class="circle color-'+index_exp_circle+'">'+chose_exp_status+' <div class="alt-name">   <a href="javascript:void(0);" class="exp_name_class">'+exp_alt_list[i].name+'</a> <span class="'+exp_alt_list[i].is_control_label+'">'+exp_alt_list[i].is_control_is+'</span></div>';
            exp_alt_info += '  </td>';
            exp_alt_info += '  <td>';
            exp_alt_info +=         exp_alt_list[i].completed_count+'/'+exp_alt_list[i].participant_count;
            exp_alt_info += '  </td>';   
            exp_alt_info += '  <td>';
            exp_alt_info +=         exp_alt_list[i].conversion_rate+'%<p class="small">';         
            exp_alt_info +=         '±'+exp_alt_list[i].confidence_interval.toFixed(1)+'%</p>';
            exp_alt_info += '  </td>'; 
            exp_alt_info += '  <td>';       
            exp_alt_info +=         exp_alt_list[i].confidence_level.replace('N/A', '&mdash;');
            exp_alt_info += '  </td>';     
            exp_alt_info += '  <td>';       
            exp_alt_info += '   <div class="alt-controls">'+use_exp_alt_winner( exp_alt_list[i].is_winner)+'</div>';
            exp_alt_info += '  </td>';                   
            exp_alt_info += '</tr>';         
    
                }            
            $(".exp_alt_info").html(exp_alt_info); 
            
        //<div id="echarts-line-chart" style="width: 1100px;height:400px;"></div>  
        }//end of 201
                
        }//end of sucess
        });
    }//end of func
     //<div class="alt-controls">  <span class="label label-success">Winner!</span></div>';
    function use_exp_alt_winner(is_winner){
        var _html;
        if(is_winner){
            _html =   '<div class="alt-controls">  <span class="label label-primary">Winner!</span>';
        }else{
          
            _html = ' <form class="layui-form"><a class="layui-btn layui-btn-xs layui-bg-gray use_this"><i class="layui-icon">&#xe66c;</i> Use This</a></form>';    
        }
      return _html        
    }

    //设置实验胜利后选set_winner
    $("body").on("click",".use_this",function(){
        //layer.msg("dddddd");
        var abName = get_request_args("name"); 
        var altName = $(this).parents("tr").find(".exp_name_class").text();
             //layer.msg('后选「'+altName+'」是获胜者'); 
           layer.confirm('你确定要设置后选:「'+altName+'」为获胜者吗?', {icon: 3, title: 'Set Winner'}, function () {
                // $.get("删除文章接口",{
                //     newsId : newsId  //将需要删除的newsId作为参数传入
                // },function(data){
                abexp_actions(abName,altName,"set_winner");
                
                
                // })
            },function(){
                  layer.msg('还需要再跑一跑', {icon: 1});
               });     
    })//end of use this function
    //暂停实验
     $("body").on("click",".pause_exp",function(obj){
         var abName = get_request_args("name"); 
         var msg_push,msg_title,msg_cancel;
         if($(this).text().indexOf("开始实验") > 0){
             msg_push = '你确定要继续实验:「'+abName+'」吗?';   
             msg_title = 'Resume experiment';  
             msg_cancel ='继续暂停吧';
         }else{
             msg_push = '你确定要暂停实验:「'+abName+'」吗?';
             msg_title = 'Pause experiment';
             msg_cancel = '还需要再跑一跑';
         }
         layer.confirm(msg_push, {icon: 3, title: msg_title}, function () {
                // $.get("删除文章接口",{
                //     newsId : newsId  //将需要删除的newsId作为参数传入
                // },function(data){
                abexp_actions(abName,'None',"pause_exp");                
                // })
            },function(){
                  layer.msg(msg_cancel, {icon: 1});
               });   
     })   
    //重设winner
    $("body").on("click",".reset_winner",function(){
        //layer.msg("dddddd");
        var abName = get_request_args("name"); 
           layer.confirm('你确定重新设置实验「'+abName+'」的获胜者吗?', {icon: 3, title: 'Reset Winner'}, function () {
                // $.get("删除文章接口",{
                //     newsId : newsId  //将需要删除的newsId作为参数传入
                // },function(data){
                abexp_actions(abName,'altName',"reset_winner");          
                
                // })
            },function(){
                  layer.msg('我再想想', {icon: 1});
               });     
    })//end of use this function
    //重设实验
    $("body").on("click",".reset_exp",function(){
        //layer.msg("dddddd");
        var abName = get_request_args("name"); 
           layer.confirm('你确定初始化实验「'+abName+'」吗?', {icon: 3, title: 'Reset Experiment'}, function () {
                // $.get("删除文章接口",{
                //     newsId : newsId  //将需要删除的newsId作为参数传入
                // },function(data){
                abexp_actions(abName,'altName',"reset_exp");          
                
                // })
            },function(){
                  layer.msg('我再想想', {icon: 1});
               });     
    })//end of use this function
    //停止实验
    $("body").on("click",".end_exp",function(){
        //layer.msg("dddddd");
        var abName = get_request_args("name"); 
           layer.confirm('你确定停止实验「'+abName+'」吗?', {icon: 3, title: 'Archive Experiment'}, function () {
                // $.get("删除文章接口",{
                //     newsId : newsId  //将需要删除的newsId作为参数传入
                // },function(data){
                abexp_actions(abName,'altName',"end_exp");          
                
                // })
            },function(){
                  layer.msg('我再想想', {icon: 1});
               });     
    })//end of use this function
    //更新实验描述
    $("body").on("click",".edit_desc",function(){
     var abName = get_request_args("name"); 
      var index =  layer.open({
        id:1,
        type: 1,
        title:'Update Description',
        skin:'layui-layer-rim',
        area:['450px', 'auto'],
            
        content: ' <div class="row" style="width: 420px;  margin-left:7px; margin-top:10px;">'
            +'<div class="col-sm-12">'
            +'<div class="input-group">'
            //+'<span class="input-group-addon"> 新 密 码   :</span>'
            +'<textarea name="desc" placeholder="请输入实验描述内容" class="layui-textarea" id="form_edit_desc" style="width: 390px;"></textarea>'
            +'</div>'
            +'</div>'
              +'</div>'
        ,
        btn:['保存描述','取消'],
        btn1: function (index,layero) {
        //console.log('edit_desc',$("#form_edit_desc").val())  
        abexp_actions(abName,$("#form_edit_desc").val(),"update_desc");
        },
        btn2:function (index,layero) {
             layer.close(index);
        }
 
    });    
        
    })

    
    function abexp_actions(abName,altName,actionType){
        if(actionType=="update_desc"){
            var desc_content = altName;
        }
        $.ajax({
        type: "POST",
        async: true,
        dataType: "json",
        url: "/api/abtest/abactions",
        data: {"abname": abName,
              "altname":altName,
              "actiontype":actionType
              },
        error: function(){
            console.log("/api/abtest/abactions/error");
        },
        success: function(data){
            if(data.code == 101){
                alert(data.message);
            }
            if(data.code == 201){
            
              setTimeout(function(){
                   window.location.href=window.location.href; 
                   window.location.reload;
                },0)
  
                }
            }
        });//end of use this(set_winner) ajax
    }//end of abexp_actions



    form.on("radio(release)",function(data){
        if(data.elem.title == "定时发布"){
            $(".releaseDate").removeClass("layui-hide");
            $(".releaseDate #release").attr("lay-verify","required");
        }else{
            $(".releaseDate").addClass("layui-hide");
            $(".releaseDate #release").removeAttr("lay-verify");
            submitTime = time.getFullYear()+'-'+(time.getMonth()+1)+'-'+time.getDate()+' '+time.getHours()+':'+time.getMinutes()+':'+time.getSeconds();
        }
    });

    form.verify({
        form_edit_desc : function(val){
            if(val == ''){
                return "文章标题不能为空";
            }
        },
        content : function(val){
            if(val == ''){
                return "文章内容不能为空";
            }
        }
    })
    form.on("submit(addNews)",function(data){
        //截取文章内容中的一部分文字放入文章摘要
        var abstract = layedit.getText(editIndex).substring(0,50);
        //弹出loading
        var index = top.layer.msg('数据提交中，请稍候',{icon: 16,time:false,shade:0.8});
        // 实际使用时的提交信息
        // $.post("上传路径",{
        //     newsName : $(".newsName").val(),  //文章标题
        //     abstract : $(".abstract").val(),  //文章摘要
        //     content : layedit.getContent(editIndex).split('<audio controls="controls" style="display: none;"></audio>')[0],  //文章内容
        //     newsImg : $(".thumbImg").attr("src"),  //缩略图
        //     classify : '1',    //文章分类
        //     newsStatus : $('.newsStatus select').val(),    //发布状态
        //     newsTime : submitTime,    //发布时间
        //     newsTop : data.filed.newsTop == "on" ? "checked" : "",    //是否置顶
        // },function(res){
        //
        // })
        setTimeout(function(){
            top.layer.close(index);
            top.layer.msg("文章添加成功！");
            layer.closeAll("iframe");
            //刷新父页面
            parent.location.reload();
        },500);
        return false;
    })

    //预览
    form.on("submit(look)",function(){
        layer.alert("此功能需要前台展示，实际开发中传入对应的必要参数进行文章内容页面访问");
        return false;
    })

    //创建一个编辑器
    var editIndex = layedit.build('news_content',{
        height : 535,
        uploadImage : {
            url : "../../json/newsImg.json"
        }
    });

})