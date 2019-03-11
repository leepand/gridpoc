layui.use(['form','layer','laydate','table','upload','layedit'],function(){
    var form = layui.form,
        layer = parent.layer === undefined ? layui.layer : top.layer,
        $ = layui.jquery,
        laydate = layui.laydate,
        upload = layui.upload,
        table = layui.table;


    //加载实验list数据/api/abtest/myablist
    //渲染页面
    get_myablist();
    function get_myablist(){
        var msgHtml = '',msgReply;
        $.ajax({
            type: "GET",
            async: true,
            dataType: "json",
            url: "/api/abtest/myablist",
            //data: {"uid":uid},
            error: function(){
                console.log("/api/abtest/myablist/error");
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
                    my_ab_list_all=result.my_ab_list_all;
                    my_ab_list_win= result.my_ab_list_win;
                    my_ab_list_archived = result.my_ab_list_archived;
                    my_ab_list_paused = result.my_ab_list_paused;
                    my_ab_list_end =result.my_ab_list_end;
                    my_ab_list_running = result.my_ab_list_running;
                    myablist_style('all',my_ab_list_all);
                    myablist_style('paused',my_ab_list_paused);
                    myablist_style('running',my_ab_list_running);
                    myablist_style('end',my_ab_list_archived);
                    myablist_style('publish',my_ab_list_win);
                    setTimeout(function(){
                         $('.list-time').relativeTime();
                        },0)
                    //$('[data-timestamp]').relativeTime();
 
        }//end of 201
                
        }//end of sucess
        });
    }
    
    function myablist_style(exp_status,exp_list){
        var ablistHtml = '';
        var Abstatus = '';
        var Winstatus = '';
        var Abstatus_css= '';
        if(exp_list.length<1){
          ablistHtml = '<td>暂无 当前状态 的试验</td>'
        }else{
            
        for(var i=0; i<exp_list.length; i++){
            
            if (exp_list[i].is_archived){
                //如果实验is_archived：判断是否决胜，如果决胜了推送，否则实验结束
                if (exp_list[i].has_winner){
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
                //如果实验没有is_archived：判断是否决胜，如果决胜了推送，继续判断是否暂停，如果暂停标注暂停状态，否则运行中
                if (exp_list[i].has_winner){
                    Winstatus = "win";
                    Abstatus="已决出";
                    Abstatus_css = '<a class="layui-btn layui-btn-xs layui-btn-warm">';
                 }
                else{
                   if(exp_list[i].is_paused){
                       Abstatus="已暂停"; 
                       Abstatus_css = '<a class="layui-btn layui-btn-xs layui-btn-danger">';  
                       
                   }
                    else{
                       Abstatus="运行中"; 
                       Abstatus_css = '<a class="layui-btn layui-btn-xs layui-btn-green">';  
                    }
                   
                }                  

            }
            //console.log('Abstatus_css',Abstatus_css);
            ablistHtml += '<tr>';
            ablistHtml += '  <td class="myablist_info">';
            ablistHtml += '    <div class="abmeta_info">';
            ablistHtml += '        <h2>'+exp_list[i].abname+'</h2>';
            ablistHtml += '        <p>'+exp_list[i].description+'</p>';
            ablistHtml += '    </div>';
            ablistHtml += '  </td>';
            ablistHtml += '  <td class="ab_status">'+Abstatus_css+Abstatus+'</a></td>';
            ablistHtml += '  <td class="ab_createtime"> <span class="list-time">'+exp_list[i].created_at+'</span></td>';
            ablistHtml += '  <td class="msg_opr">';
            //ablistHtml += '    <a class="layui-btn layui-btn-xs layui-btn-normal msg_collect"><i class="layui-icon">&#xe600;</i> 收藏</a>';
            ablistHtml += '    <a class="layui-btn layui-btn-xs layui-bg-gray del_abtest"><i class="layui-icon">&#xe640;</i> 删除</a>';
            ablistHtml += '  </td>';
            ablistHtml += '</tr>';                                 
        }}//end of list是否为空的判断
        if(exp_status=="all"){
        $(".All_ablistHtml").html(ablistHtml);     
        }
        if(exp_status=="publish"){
        $(".Win_ablistHtml").html(ablistHtml);     
        }
        if(exp_status=="end"){
        $(".End_ablistHtml").html(ablistHtml);     
        }
        if(exp_status=="running"){
        $(".Run_ablistHtml").html(ablistHtml);     
        }
        if(exp_status=="paused")
        {
        $(".Paused_ablistHtml").html(ablistHtml);     
        }
        //
      
       
    }
     
    //$(".del_abtest").click(function(){
     //   layer.msg("请输入搜索的内容");
     //   console.log('haha');
    //})
    $("body").on("click",".del_abtest",function(){
       var abName = $(this).parents("tr").find(".abmeta_info h2").text();
        layer.confirm('你确定删除实验「'+abName+'」吗?', {icon: 3, title: 'Delete Experiment'}, function () {
                // $.get("删除文章接口",{
                //     newsId : newsId  //将需要删除的newsId作为参数传入
                // },function(data){
                abexp_actions(abName,'altName',"del_exp");          
                
                // })
            },function(){
                  layer.msg('我再想想', {icon: 1});
               });       
        })
    
    
    
    $("body").on("click",".abmeta_info h2",function(){
        layer.msg("dddddd");
        var abName = $(this).parents("tr").find(".abmeta_info h2").text();
        location.href='/name='+abName;//跳转到ABtesting详情页：expdetails.html
    })
    /*$("body").on("click",".del_abtest i,.All_ablistHtml .abmeta_info h2,.msgHtml .myablist_info p",function(){
        var id = $(this).parents("tr").find(".del_abtest i");
        var abName = $(this).parents("tr").find(".abmeta_info h2").text();
        console.log('dd',abName,id);
        })*/
    //删除操作api其他操作参见myabtest_details.js           
    function abexp_actions(abName,altName,actionType){
        
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

    
    //添加实验
    function addLink(edit){
        var index = layer.open({
            title : "创建实验",
            type : 2,
            area : ["460px","485px"],
            content : "my_abexpAdd.html",
            success : function(layero, index){
                
                var body = $($(".layui-layer-iframe",parent.document).find("iframe")[0].contentWindow.document.body);
                //var w = layui.getStyle(body.find(".leepand"), 'width'); 
                var w =  body.find(".leepand").css("width");
                var w_val = parseInt(w);
                body.find(".layui-btn").css("width",parseInt(w_val-30)/2);//减去取消按钮左右距离（10+20）
  
                if(edit){
                    console.log("dddddd",body.find("#fluxsetMethod_select").val());
                    body.find(".linkLogo").css("background","#fff");
                    body.find(".linkLogoImg").attr("src",edit.logo);
                    body.find(".linkName").val(edit.websiteName);
                    body.find(".linkUrl").val(edit.websiteUrl);
                    //body.find("#fluxset").val(edit.fluxset);
                    body.find(".showAddress").prop("checked",edit.showAddress);
                    form.render();
                }
                setTimeout(function(){
                    layui.layer.tips('点击此处返回实验列表', '.layui-layer-setwin .layui-layer-close', {
                        tips: 3
                    });
                    body.find('.layui-btn-primary').on('click', function(){
                      layer.close(index);
                      body.focus();
                    });//取消按钮
                    
                },500)
            }
        })
    }
    $(".addLink_btn").click(function(){
        addLink();
    })
    

    
     form.on("radio(release)",function(data){
        if(data.elem.title == "手动设置"){
            
            $(".releaseFlux").removeClass("layui-hide");
            
        }else{
            
            $(".releaseFlux").addClass("layui-hide");
        }
         
    });
   
    
    //批量删除
    $(".delAll_btn").click(function(){
        var checkStatus = table.checkStatus('linkListTab'),
            data = checkStatus.data,
            linkId = [];
        if(data.length > 0) {
            for (var i in data) {
                linkId.push(data[i].newsId);
            }
            layer.confirm('确定删除选中的友链？', {icon: 3, title: '提示信息'}, function (index) {
                // $.get("删除友链接口",{
                //     linkId : linkId  //将需要删除的linkId作为参数传入
                // },function(data){
                tableIns.reload();
                layer.close(index);
                // })
            })
        }else{
            layer.msg("请选择需要删除的文章");
        }
    })



    function ityzl_SHOW_LOAD_LAYER(){
	   		return layer.msg('正在创建实验...', {icon: 16,time:false,shade:0.8}) ;
	   	}
	 function ityzl_SHOW_LOAD_LAYER_down(){
	   		return layer.msg('正在删除实验...', {icon: 16,time:false,shade:0.8}) ;
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
         
    form.on("submit(addLink)",function(data){
        //弹出loading
        //var index = top.layer.msg('数据提交中，请稍候',{icon: 16,time:false,shade:0.8});
        //var flux_new = body.find("#fluxset").val();
     
        console.log('exp_type',$("#exp_type").val());
        console.log('exp_id',$("#exp_id").val());
        console.log('exp_list',$("#exp_list").val());
        console.log('flux_new',$("#fluxset").val());
        var expid=$("#exp_id").val();
        var explist=$("#exp_list").val();
        var clientid=$("#exp_type").val();
        var expdesc=$("#exp_desc").val();
        //$.post(
        var index;
        $.ajax({
        type: "POST",
        async: true,
        dataType: "json",
        url: "/api/abtest/add",
        data: {
            "expid": expid,
            "explist": explist,
            "clientid": clientid,
            "expdesc": expdesc
        },
        error: function(){
            console.log("/api/abtest/add/error");
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
                        parent.location.reload();
                    });
                //top.layer.msg(data.message);
                //top.layer.close(index);
                //layer.closeAll("iframe");
                
            }
            if(data.code == 201){
                //top.layer.msg("实验创建成功！");
                swal({
                    title: "成功提交",
                    text: "可以到实验列表页查看",
                    type: "success",
                    closeOnConfirm: true
                },function(){
                        parent.location.reload();
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
    
        
    })

    function create_abtest(expid,explist,clientid,index){
    //var expid = $("#expid").val();
    //var explist = $("#singleFieldTags2").val();
    //var clientid = $("#version").val();

    $.ajax({
        type: "POST",
        async: true,
        dataType: "json",
        url: "/api/abtest/add",
        data: {
            "expid": expid,
            "explist": explist,
            "clientid": clientid
        },
        error: function(){
            console.log("/api/abtest/add/error");
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
                //top.layer.msg("实验创建成功！");
                //alert("添加成功,请关闭窗口！");
                swal({
                    title: "成功提交",
                    text: "可以到实验列表页查看",
                    type: "success"
                });
            top.layer.close(index);
            //top.layer.msg("文章添加成功！");
           
                
            }
        }
    });
}
    
 
    

    
})//end of layui.use