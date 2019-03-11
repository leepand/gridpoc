/**
 * project: Arthur-run api example
 * author: leepand
 *
 */

//tag_edit
 // Actions
/*textFormatter: function(text) {return text}
var actions = $('<span/>', {
    'class': 'actions'
});
var editButton = $('<button/>', {
    'class': 'action edit',
    text: textFormatter(this.options.editText)
});
actions.append(editButton);

$("body").on("click",".tag_edit",function(){
   //var aid_btn = $(this).attr('aId');
    return;
})//end of use this function
*/

    //更新实验描述
    $("body").on("click",".edit_tags",function(){
     //var abName = get_request_args("name"); 
      var index =  layer.open({
        id:1,
        type: 1,
        title:'Update Tags',
        skin:'layui-layer-rim',
        area:['450px','auto'],
            
        content: ' <div class="row" style="width: 420px;  margin-left:7px; margin-top:10px;">'
            +'<div class="col-sm-12">'
            +'<div class="input-group">'
            //+'<span class="input-group-addon"> 新 密 码   :</span>'
            +'<textarea name="desc" placeholder="请输入标签内容" class="layui-textarea" id="form_edit_desc" style="width: 390px;"></textarea>'
            +'</div>'
            +'</div>'
            +'</div>'
          ,
        
      
        btn:['保存标签','取消'],
        btn1: function (index,layero) {
        //console.log('edit_desc',$("#form_edit_desc").val())  
        //abexp_actions(abName,$("#form_edit_desc").val(),"update_desc");
        },
        btn2:function (index,layero) {
             layer.close(index);
        }
 
    });    
        
    })

function genComments(userName,projectName) {
    var commentsArray;
    $.get("/api/service/msg/list",{userName:userName, projectName:projectName },function(comments,status){
        commentsArray = comments.result;
        console.log('comments：', commentsArray);
        //alert("comments: " + comments.result + "nStatus: " + status);
    });
    var usersArray;
    $.get("/api/service/msg/user",function(data,status){
        usersArray = data.result;
        console.log('users：', usersArray);
        //alert("user: " + data.result + "nStatus: " + status);
    });
    //console.log('comments：', $$.get("/api/service/msg/user"));
    var _username=userName;
    var saveComment = function(data) {
        // Convert pings to human readable format
        $(data.pings).each(function(index, id) {
            var user = usersArray.filter(function(user){return user.id == id})[0];
            data.content = data.content.replace('@' + id, '@' + user.fullname);
        });
        //console.log('comments：', data);
        data.projectname=projectName;
        data.username=userName;
        $.post("/api/service/msg",data);//,function (text, status) { alert(text); });//{"suggest":data}
        console.log('data：', data);
        return data;
    };
    $('#comments-container').comments({
        profilePictureURL: '../static/images/user-icon.png',
        currentUserId: 1,
        roundProfilePictures: true,
        textareaRows: 1,
        enableAttachments: true,
        enableHashtags: true,
        enablePinging: true,
        getUsers: function(success, error) {
            setTimeout(function() {
                success(usersArray);
            }, 500);
        },
        getComments: function(success, error) {
            setTimeout(function() {
                success(commentsArray);
            }, 500);
        },
        postComment: function(data, success, error) {
            setTimeout(function() {
                success(saveComment(data));
            }, 500);
        },
        putComment: function(data, success, error) {
            setTimeout(function() {
                success(saveComment(data));
            }, 500);
        },
        deleteComment: function(data, success, error) {
            setTimeout(function() {
                success();
            }, 500);
        },
        upvoteComment: function(data, success, error) {
            setTimeout(function() {
                success(data);
            }, 500);
        },
        uploadAttachments: function(dataArray, success, error) {
            setTimeout(function() {
                success(dataArray);
            }, 500);
        },
    });
};//end of comments


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