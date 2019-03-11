/**
 * project: Arthur-run api example
 * author: leepand
 *
 */






function getData222(){
  console.log( $("#expid").val());
  var  jboxapi=new jBox('Modal', {
  width: 450,
  height: 250,
  closeButton: 'title',
  animation: false,
  title: 'AJAX request',
});
    jboxapi.open({
    ajax: {
    url: '/api/service/runapi',
      //contentType:"application/x-www-form-urlencoded",
      method: "GET",
      data:eval("("+ $("#expid").val()+")"),
      dataType:"json",
    setContent: false,
       reload:true,
    beforeSend: function() {
    //this.data=eval("("+ $("#expid").val()+")");
      //this.setContent();
      this.setTitle('<div class="ajax-sending">Sending Arthur service request...</div>');
    },
    complete: function(response) {
      this.setTitle('<div class="ajax-complete">Arthur request complete</div>');
    },
    success: function(response) {
  this.setContent('<div class="ajax-success">Response:<tt>' + JSON.stringify(response) + '</tt></div>');
    },
    error: function() {
      this.setContent('<div class="ajax-error">Oops, something went wrong</div>');
    }
  }
  })
}
    
   

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
	   		return layer.msg('运行中...', {icon: 16,time:false,shade:0.8}) ;//{icon: 16,shade: [0.5, '#f5f5f5'],scrollbar: false,offset: '0px', time:100000}
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

//onclick=publish_service('"+aid+"')
    //重设winner
$("body").on("click",".runApiExample",function(){
   //var aid_btn = $(this).attr('aId');
    Run_Api();
    })//end of use this function

/*发布服务*/
function Run_Api(){
    var modelInfo = $("#modelInfo").val();//eval("("+ $("#dataInfo").val()+")")
    var dataInfo = $("#dataInfo").val();
    var i;
    $.ajax({
        type: "POST",
        async: true,
        dataType: "json",
        url: "/api/service/runapi",
        data: {"dataInfo":JSON.stringify(dataInfo),
            "modelInfo":JSON.stringify(modelInfo)
        },//eval("("+ $("#expid").val()+")"),
        error: function() {
            console.log("/api/service/runapi/error");
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
                
                swal({
                    title: "Service running success！",
                    text: 'Response:' + JSON.stringify(data.result)
                });
                //get_user_list();
            }else{
                ityzl_CLOSE_LOAD_LAYER(i);
                //ityzl_SHOW_TIP_LAYER_ERROR()---也可以用layerui的信息弹窗
                //alert("删除用户失败[Error:" + data.message + "]");
                swal({
                    title: "运行服务失败！",
                    text: data.message
                });
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






})//end of layui-use