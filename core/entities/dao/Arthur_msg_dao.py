# -*- coding: UTF-8 -*-

# author: leepand
# time: 2018-11-30
# desc: model discussion
'''
#评论管理表
DROP TABLE IF EXISTS `tb_discussion_msg`;
CREATE TABLE `tb_discussion_msg` (
`msgid` int(10) NOT NULL AUTO_INCREMENT,
`id` varchar(50) NOT NULL,
`username` varchar(50) NOT NULL,
`projectname` varchar(50) NOT NULL,
`creator` varchar(50) NOT NULL,
`created` varchar(50) NOT NULL,
`modified` varchar(50) NOT NULL,
`parent` varchar(50),
`content` text NOT NULL,
`pings` varchar(50) NOT NULL DEFAULT '[1]',
`fullname` varchar(50) NOT NULL,
`profile_picture_url` varchar(50) NOT NULL,
`created_by_admin` enum('true','false') DEFAULT 'false',
`created_by_current_user` enum('true','false') DEFAULT 'false',
`user_has_upvoted` enum('true','false') DEFAULT 'false',
`is_new` enum('true','false') DEFAULT 'true',
`upvote_count` int(10) NOT NULL,
PRIMARY KEY (`msgid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
#update 2019-01-25
from Arthur.core.entities.arthur_web_cfg import *
from Arthur.core.entities.base.bs_util import *
from Arthur.core.entities.base.bs_database_pid import DataBase


class ArthurMsg:
    @staticmethod
    def insert_node_user_msg(id, username,projectname,creator,created, modified, parent, content, pings,fullname,profile_picture_url,\
                created_by_admin,created_by_current_user,user_has_upvoted,is_new,upvote_count):
        dataBase = DataBase()
        sql = "insert into tb_discussion_msg(id, username,projectname,creator, \
        created, modified, parent, content, pings,fullname,profile_picture_url,\
        created_by_admin,created_by_current_user,user_has_upvoted,is_new,upvote_count) \
        values(%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s)"
        param = (id, username,projectname,creator,created, modified, parent, content, pings,fullname,profile_picture_url,\
                created_by_admin,created_by_current_user,user_has_upvoted,is_new,upvote_count)

        bRet, sRet = dataBase.insert_data(sql, param)
        if not bRet:
            return False, sRet
        
        return True, sRet
    @staticmethod
    def update_node_user_msg(Id, content, modified,user_has_upvoted="false",upvote_count=0):
        dataBase = DataBase()
        sql = "update tb_discussion_msg set content = %s, modified = %s, upvote_count= %s,  user_has_upvoted = %s where id = %s"
        param = (content, modified,upvote_count, user_has_upvoted,Id)

        bRet, sRet = dataBase.update_data(sql, param)
        if not bRet:
            return False, sRet
        
        return True, sRet

    @staticmethod
    def query_node_by_id(Id,uName,pName):
        dataBase = DataBase()
        sql = "select * from tb_discussion_msg where id = %s and username=%s and projectname= %s "
        param = (Id, uName, pName)

        bRet, sRet = dataBase.query_data(sql, param)
        #print bRet,sRet
        if not bRet:
            return False, sRet
        if len(sRet)>0:
            msginfo=sRet[0]
        else:
            msginfo={}
        return True, msginfo#sRet[0]
    @staticmethod
    def query_node_msg_list():
        dataBase = DataBase()
        sql = "select * from tb_discussion_msg"

        bRet, sRet = dataBase.query_data(sql, None)
        if not bRet:
            return False, sRet
        
        return True, sRet
    @staticmethod
    def query_node_msg_list_by_usrproj(user,proj):
        dataBase = DataBase()
        sql = "select * from tb_discussion_msg where username=%s and projectname=%s"
        param = (user,proj)
        bRet, sRet = dataBase.query_data(sql, param)
        if not bRet:
            return False, sRet
        
        return True, sRet
if __name__ == "__main__":
    x={'username': 'leepand6', 'parent':'null', 'created': '2018-12-22T02:07:29.646Z', 'projectname': 'leepand', 'modified': '2018-12-22T02:07:29.646Z', 'content': '@leepand3 test you are best', 'pings': '34', 'profile_picture_url': '../static/images/user-icon.png', 'fullname': 'You', 'upvote_count': '1', 'user_has_upvoted': 'false', 'id': 'c12', 'created_by_current_user': 'true'}
    id=x['id'] 
    username=x['username']
    projectname=x['projectname']
    creator=1
    created= x['created']
    modified = x['modified']
    parent = 'null'
    content='lepadada'
    #pings=''
    fullname='leepand'
    profile_picture_url=x['profile_picture_url']
    created_by_admin='false'
    created_by_current_user=x['created_by_current_user']
    user_has_upvoted=x['user_has_upvoted']
    is_new=x.get('is_new','false')
    upvote_count=x.get('upvote_count','false')
    #ArthurMsg.insert_node_user_msg(id, username,projectname,creator,created, modified, parent, content, pings,fullname,profile_picture_url,\
    #            created_by_admin,created_by_current_user,user_has_upvoted,is_new,upvote_count)
    #yy=ArthurMsg.query_node_by_id('c13')
    #zz=ArthurMsg.query_node_msg_list()
    #ArthurMsg.update_node_user_msg('c12','hahhhhha','2018-12-29')
    #fdf=ArthurMsg.query_node_msg_list_by_usrproj('leepand6','leepand3')