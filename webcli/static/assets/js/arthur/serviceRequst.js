/*
 *
 * ServiceRequest
 * Autor: Leepand
 * Date: 2019-02-21
 * 
 */
var ServiceRequest = (function(){
    //var $container = $("#food-menus");

    function fetch_request_cnt(callback) {
        User.ajax({
            url: '/api/service/request',
            type: 'POST',
            data: {},
            error: callback.onError,
            success: callback.onSuccess,
        });
    }
    
    function init() {
        fetch_request_cnt({
            onSuccess: function(res) {
                //console.log(res,'res');
                var experiment=res.result;
                var ablistHtml="";
                var Winstatus,Abstatus,Abstatus_css;
                var expAllCnt=0,expDoneCnt=0,expPausedCnt=0,expEndCnt=0,expRunningCnt=0;
                var expDoneRate,expPausedRate,expEndRate,expRunningRate;
                if(experiment.length<1){
                    ablistHtml = '<td>暂无 实验</td>';
                }else{
                    $(experiment).each(function (alt, index) {
                        //$(experiment).eachexperiment.alternatives
                        //console.log('alt.name',index,index.confidence_level);
                        //console.log(index,index.length);
                        //计算实验概况信息
                        expAllCnt+=1;
                        if(index.is_archived){
                            expEndCnt+=1;
                        } 
                        if(index.has_winner){
                           expDoneCnt+=1;
                           }
                        if(index.is_paused){
                           expPausedCnt+=1;
                           }   
                        if(!index.is_paused & !index.is_archived & !index.has_winner){
                           expRunningCnt+=1;
                           }
                        
                        //计算实验列表
                        if (index.is_archived){
                            //如果实验is_archived：判断是否决胜，如果决胜了推送，否则实验结束
                            if (index.has_winner){
                                Winstatus = "win";
                                Abstatus="已决出";
                                Abstatus_css = '<a class="layui-btn layui-btn-xs layui-btn-warm">';
                            }
                            else{
                                Abstatus="已结束";
                                Abstatus_css = '<a class="layui-btn layui-btn-xs label-default">';
                            }  
                        }else{
                            //如果实验没有is_archived：判断是否决胜，如果决胜了推送，继续判断是否暂停，如果暂停标注暂停状态，否则运行中
                            if (index.has_winner){
                                Winstatus = "win";
                                Abstatus="已决出";
                                Abstatus_css = '<a class="layui-btn layui-btn-xs layui-btn-warm">';
                            }
                            else{
                                if(index.is_paused){
                                    Abstatus="已暂停"; 
                                    Abstatus_css = '<a class="layui-btn layui-btn-xs layui-btn-danger">';  
                                }
                                else{
                                    Abstatus="运行中"; 
                                    Abstatus_css = '<a class="layui-btn layui-btn-xs layui-btn-green">';  
                                }
                            }  
                        }
                        
                        ablistHtml += '<tr>';
                        ablistHtml += ' <td class="project-status">'+Abstatus_css+Abstatus+'</a>';
                        //ablistHtml += '<td class="ab_status text-left">'+Abstatus_css+Abstatus+'</a></td>';
                        ablistHtml += '  </td>';
                        ablistHtml += ' <td class="project-title">';
                        ablistHtml += '<div class="ab-info">';
                        ablistHtml += '<a href="/name='+index.name+'" class="ab-info__name ab-info-link">'+index.name+'</a>';
                        ablistHtml += '</div>';
                        ablistHtml += '<small class="text-muted ab-url">创建于 </small><small class="text-muted ab-url list-time">'+index.created_at+'</small>';
                        ablistHtml += '</td>';
                        ablistHtml += ' <td class="project-title">';
                        ablistHtml += ' <a href="#">总曝光数</a></br>';
                        ablistHtml += '<small>'+index.total_participants+'</small> </td>';
                        ablistHtml += '<td class="project-title">';
                        ablistHtml += '<a href="#">总转化数</a></br>';
                        ablistHtml += '<small>'+index.total_conversions+'</small></td>';
                        ablistHtml += '<td class="project-actions">';
                        ablistHtml += '<a href="/name='+index.name+'" class="btn btn-white btn-sm pull-right"><i class="fa fa-eye"></i> 查看详情</a></td>';
                        ablistHtml += '</tr>';
                        //console.log('alt.name',index.created_at,alt);
                        //if(index.name=="test2"){
                        //    console.log('alt.name',index,index.confidence_level);
                        //}
                    });
                }
                //实验概况
                $("#expAllCnt").html(expAllCnt);
                $("#expRunningCnt").html(expRunningCnt);
                $("#expDoneCnt").html(expDoneCnt);
                $("#expPausedCnt").html(expPausedCnt);
                $("#expEndCnt").html(expEndCnt);
                expRunningRate =(expRunningCnt) / (expAllCnt) * 100;
                expDoneRate=(expDoneCnt) / (expAllCnt) * 100;
                expPausedRate=(expPausedCnt) / (expAllCnt) * 100;
                expEndRate=(expEndCnt) / (expAllCnt) * 100;
                $("#expDoneRate").html(expDoneRate.toFixed(1)+'%');
                $("#expPausedRate").html(expPausedRate.toFixed(1)+'%');
                $("#expEndRate").html(expEndRate.toFixed(1)+'%');
                $("#expRunningRate").html(expRunningRate.toFixed(1)+'%');
                $("#expDoneProcess").html('<div class="progress-bar progress-bar-primary-dark" style="width:'+expDoneRate.toFixed(1)+'%"></div>');
                $("#expPausedProcess").html('<div class="progress-bar progress-bar-danger" style="width:'+expPausedRate.toFixed(1)+'%"></div>');
                $("#expEndProcess").html('<div class="progress-bar progress-bar-primary-dark" style="width:'+expEndRate.toFixed(1)+'%"></div>');
                $("#expRunningProcess").html('<div class="progress-bar progress-bar-primary-dark" style="width:'+expRunningRate.toFixed(1)+'%"></div>');
                //实验列表
                $(".ablistHtml").html(ablistHtml); 
                $(".list-time").relativeTime();
                $('.dataPages-ABList').dataTable({"bFilter": false,"bLengthChange": false,"bSort": false});//分页功能，需要在回调内执行才有效
            },
            onError: function() {
                toastr.error("A/B Testing experiments could not be fetched :(")
            }
        })

    }
    init();
});



$(document).ready(function(){
    t = ServiceRequest();
    //$('[data-toggle="tooltip"]').tooltip({container: 'body'});
});
