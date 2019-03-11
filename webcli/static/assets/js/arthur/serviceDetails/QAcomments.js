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

function QAcommentsQuerySave(userName,projectName) {
    var msg_query = {"userName":userName,"projectName":projectName};
    var commentsArray,usersArray,loginUser,enableEditingStatus;
    var saveComment = function(data) {
        // Convert pings to human readable format
        $(data.pings).each(function(index, id) {
            var user = usersArray.filter(function(user){return user.id == id})[0];
            data.content = data.content.replace('@' + id, '@' + user.fullname);
            //data.user_has_upvoted = 
        });
       
        //console.log('comments：', data);
        data.projectname=projectName;
        data.username=userName;
        $.post("/api/service/msg/save",data);//,function (text, status) { alert(text); });//{"suggest":data}
        //console.log('data：', data);
        return data;
    };
  $.ajax({
        type: "GET",
        async: true,
        dataType: "json",
        url: "/api/service/msg/query",
        data: msg_query,
        error: function(){
            console.log("/api/service/msg/query/error");
        },
        success: function(data){
            if(data.code == 101){
                layer.msg(data.message);
            }
            if(data.code == 201){
                if(!data.result){
                    return;
                }
                result = data.result;
                usersArray = result.QAuser_list;
                commentsArray = result.QAmsg_list;
                loginUser = result.loginUser;//判断登陆用户和项目用户是同一个人时才可以编辑当前comment
                //console.log(loginUser,userName);
                if(loginUser==userName){
                        enableEditingStatus= true;
                    }
                else{
                        enableEditingStatus= false;
                    }
                $('#comments-container').comments({
                    profilePictureURL: '../static/images/user-icon.png',
                    currentUserId: 1,
                    roundProfilePictures: true,
                    textareaRows: 1,
                    enableAttachments: true,
                    enableHashtags: true,
                    enablePinging: true,
                    enableEditing: enableEditingStatus,
                    
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
                            success(saveComment(data));
                        }, 500);
                    },
                    uploadAttachments: function(dataArray, success, error) {
                        setTimeout(function() {
                            success(dataArray);
                        }, 500);
                    },
                });
            }
        }
    });//end of ajax    
    
};//end of comments




/*function genComments(userName,projectName) {
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
        $.post("/api/service/msg/save",data);//,function (text, status) { alert(text); });//{"suggest":data}
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
};//end of comments*/