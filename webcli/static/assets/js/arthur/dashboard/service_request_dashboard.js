/**
 * project: Arthur
 * author: leepand
 * index 服务调用排序
 */




layui.use(['form','layer','laydate','table','upload','layedit'],function(){
    var form = layui.form,
        layer = parent.layer === undefined ? layui.layer : top.layer,
        $ = layui.jquery,
        laydate = layui.laydate,
        upload = layui.upload,
        table = layui.table;


    //判断字符是否为空的方法
    function isEmpty(obj){
        if(obj == "undefined" || obj == null || obj == ""){
            return true;
        }else{
            return false;
        }
    }

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
    
    //加载zoo算法list
    getMyServiceList('zoo','notnewest','NonetagQuery');
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
            success: function(data){
                if(data.code == 101){
                    alert(data.message);
                }
                if(data.code == 201){
                    if(!data.result){
                        return;
                    }
                    var myalgo_list=data.result.algolist;
                    var star_info = data.result.star_info;
                    var algo_request_info =data.result.algo_request_info;
                    var algo_User_algocnt = data.result.algo_User_algocnt;
                    var serviceRequestCntHtml="";
                    console.log("algo_request_info",algo_request_info);
                    
                    
                    // Create items array
                    var items = Object.keys(algo_request_info).map(function(key) {
                        return [key, algo_request_info[key]];
                    });
                    // Sort the array based on the second element
                    items.sort(function(first, second) {
                        return second[1] - first[1];
                    });
                    // Create a new array with only the first 5 items
                    var top15service = items.slice(0, 15);
                    console.log(top15service,'top15service');
                    top15service.forEach(function(serviceModel,i){
                    console.log(top15service[i][0],top15service[i][1]);
                        if(top15service[0][1]>0){
                            var rate=top15service[i][1]/top15service[0][1];
                        }else{
                           var rate= 0; 
                        }
                        //console.log(rate,'dd');
                        serviceRequestCntHtml+='<div data-toggle="tooltip" class="algo-info"   data-placement="top" data-original-title="服务调用次数:'+top15service[i][1].toString()+'次" >'
                        +'<strong>'+my.addCommas(top15service[i][1])+' 次</strong> <a class="algo-info__name algo-info-link" href="service_zoo_list.html">'+ top15service[i][0]+'</a>'
                        +    '<span class="pull-right text-success text-sm">'+(100*rate).toFixed(1)+'% </span>'
                        +    '<div class="progress progress-hairline">'
                        +        '<div class="progress-bar progress-bar-primary-dark" style="width:'+(100*rate).toFixed(1)+'%"></div>'
                        +    '</div>'
                        + '</div>';
                
                    });
                    $("#serviceRequestCntHtml").html(serviceRequestCntHtml);
                    setTimeout(function(){
                        console.log('done!');
                    },0) 
        }//end of 201
                
        }//end of sucess
        });
    }
   
    


})//end of layui.use