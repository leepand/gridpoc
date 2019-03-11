-- Adminer 4.2.1 MySQL dump
create database Arthur_manage;
use Arthur_manage;
SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

-- 用户操作-abtest
DROP TABLE IF EXISTS `tb_user_abtesting`;
CREATE TABLE `tb_user_abtesting` (
    `abid` int(10) NOT NULL AUTO_INCREMENT,
    `uid` int(10) NOT NULL,
    `abname` varchar(50) NOT NULL,
    PRIMARY KEY (`abid`),
    KEY `uid` (`uid`),
    CONSTRAINT `tb_abtesting_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `tb_user` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



--点赞、收藏等信息持久化
DROP TABLE IF EXISTS `tb_algo_star_thumb`;
CREATE TABLE `tb_algo_star_thumb` (
    `sid` int(10) NOT NULL AUTO_INCREMENT,
    `algouid` int(10) NOT NULL,
    `uid` int(10) NOT NULL,
    `algoname` varchar(50) NOT NULL,
    `star_cnt` int(30) DEFAULT 1,
    `thumb_cnt` int(30) DEFAULT 1,
    `star_status` enum('star','nostar') DEFAULT 'nostar',
    `thumb_status` enum('thumb','nothumb') DEFAULT 'nothumb',
    `insert_tm` datetime NOT NULL,
    PRIMARY KEY (`sid`),
    KEY `uid` (`uid`),
    CONSTRAINT `tb_star_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `tb_user` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--评论管理表
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

--算法管理表
DROP TABLE IF EXISTS `tb_algo`;
CREATE TABLE `tb_algo` (
    `aid` int(10) NOT NULL AUTO_INCREMENT,
    `uid` int(10) NOT NULL,
    `algoname` varchar(50) NOT NULL,
    `algodesc` varchar(50) NOT NULL,
    `version` varchar(50) NOT NULL  DEFAULT 'v1.0.0',
    `opertype` enum('publish','register')  DEFAULT 'publish',
    `token` varchar(50) NOT NULL,
    `pyfile` varchar(50) NOT NULL,
    `funcslist` text NOT NULL,
    `tags` text NOT NULL,
    `field` int(10) NOT NULL,
    `host` varchar(50) NOT NULL  DEFAULT '0.0.0.0',
    `port` int(10) NOT NULL,
    `atype` varchar(10) NOT NULL DEFAULT 'REST',
    `algo_tm` datetime NOT NULL,
    `status` enum('normal','stop','notpublish') DEFAULT 'notpublish',
    `is_email` varchar(10) NOT NULL DEFAULT 'no',
    `remark` text NOT NULL,
    `insert_tm` datetime NOT NULL,
    PRIMARY KEY (`aid`),
    KEY `uid` (`uid`),
    CONSTRAINT `tb_algo_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `tb_user` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



DROP TABLE IF EXISTS `tb_user`;
CREATE TABLE `tb_user` (
    `uid` int(10) NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
    `nickname` varchar(50) NOT NULL,
    `password` varchar(50) NOT NULL,
    `phone` varchar(50) DEFAULT NULL,
    `email` varchar(50) DEFAULT NULL,
    `privilege` int(1) NOT NULL DEFAULT '1',
    `remark` text,
    `lastlogin` datetime DEFAULT NULL,
    PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 2019-02-19 09:56:02
