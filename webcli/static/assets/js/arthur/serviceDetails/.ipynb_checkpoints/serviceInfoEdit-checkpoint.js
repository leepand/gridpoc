
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