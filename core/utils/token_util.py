# -*- coding: UTF-8 -*-

# token类
# @since 2018-12-20


class Itaken:

    # 获取Hash数据
    @classmethod
    def enmd5(cls, data):
        data = str(data) + "4ITAKEN:)"
        import hashlib
        data = hashlib.md5(data.encode("UTF-8")).hexdigest()  # 昵称hash
        return data

    # list数据不重复
    @classmethod
    def spread_list(cls, i, l=[], step=1, minimum=0):
        if minimum < 0:
            minimum = 0
        i = i < minimum and minimum or i
        step = step < 1 and 1 or step  # < 1 则为 1

        if i in l:
            return cls.spread_list(i+step, l, step, minimum)

        l.append(i)
        return l

class Connector:
    # 加密 token
    @classmethod
    def encrypt_token(cls, uid, access_token, session_token):
        if access_token == "" or session_token == "":
            return {}

        uid = int(uid)
        if uid < 17:  # 防止出现 id 过小的情况
            uid = uid * 19

        if len(access_token) < 32:  # 防止出现长度不足的情况
            access_token = Itaken.enmd5(access_token)
        if len(session_token) < 32:
            session_token = Itaken.enmd5(session_token)

        session_token_list = list(session_token)  # token string转list
        str_key = access_token[8:20]  # 字符替换key

        pos = []
        mod_key = (11, 3, 7, 13, 5, 17)  # 求模key
        for index, i in enumerate(mod_key):
            chart = access_token[index: index + 1]  # 随机数
            point = (uid + int("0x" + chart, 16)) % i  # 获取的位置(16进制转10进制)

            pos = Itaken.spread_list(point, pos, 3, 1)  # 计算前半段
            pos = Itaken.spread_list(point + 16, pos, 3, 1)  # 计算后半段

        for index, i in enumerate(pos):
            session_token_list[i] = str_key[index]  # 密钥替换

        token = "".join(session_token_list)  # 加密后token

        return {
            "position": pos,
            "key": str_key,
            "token": token
        }

    # 验证 token
    #TODO
    @classmethod
    def verify_token(cls, uid, token):
        uid = int(uid)
        if uid < 1 or token == "" or token is None:
            return {"code": 0, "message": "验证内容不合法"}
        #TODO
        token_info = cls.get_user_token_info(uid=uid)  # 获取数据库token信息
        if not token_info:
            return {"code": 0, "message": "没有该用户"}

        encrypt_info = cls.encrypt_token(uid=uid, access_token=token_info["access_token"], session_token=token_info["session_token"])
        if token == encrypt_info["token"]:
            return {"code": 1, "message": "验证成功", "uid": uid}

        token_list = list(token)  # token 转list
        token_key = ""
        for i in encrypt_info["position"]:
            token_key += token_list[i]  # 组装密钥

        if token_key == encrypt_info["key"]:
            return {"code": -1, "message": "session token失效"}

        return {"code": -2, "message": "access token失效"}