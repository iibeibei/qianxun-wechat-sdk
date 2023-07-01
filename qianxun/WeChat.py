import os
import sys
import time
import requests
import information
import xml.etree.ElementTree as ET
from multiprocessing import Process, Queue
from flask import Flask, jsonify, request


class Robot:
    def __init__(self, host: str, port: str, bot_wxid: str):
        """初始化

        Args:
            host (str): 服务器地址 \r\n
            port (str): 服务器端口 \r\n
            bot_wxid (str): 机器人wxid
        """

        self.host = host
        self.port = port
        self.bot_wxid = bot_wxid
        self.url = f"http://{self.host}:{self.port}/DaenWxHook/httpapi/"

    # 获取微信列表(X0000)
    def getWeChatList(self) -> dict:
        """获取微信列表(X0000)

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": [{ \r\n
                        "startTimeStamp": "1657508562", # 开始运行时间戳 \r\n
                        "startTime": "2022年7月11日11时2分42秒", # 开始运行时间 \r\n
                        "runTime": "2时39分46秒", # 已运行时间 \r\n
                        "recv": 184, # 接收消息数 \r\n
                        "send": 3, # 发送消息数 \r\n
                        "wxNum": "DaenMax", # 微信号 \r\n
                        "nick": "Daen", # 昵称 \r\n
                        "wxid": "wxid_3sq4tklb6c3121", # wxid \r\n
                        "pid": "17600", # 进程PID \r\n
                        "port": "7614" # 端口 \r\n
                    }],
                "timestamp": "1657518149909"
            }
        """
        data = {'type': 'X0000', 'data': {}}
        return self.post_(data=data)

    # 微信状态检测(Q0000)
    def checkWeChatStatus(self, bot_wxid: str = '') -> dict:
        """微信状态检测(Q0000)

        Args:
            bot_wxid (str, optional):  机器人 WXID, 不填则默认为初始化时的 WXID

        Returns:
            dict: {
                "code":
                "msg": "正常",
                "result": { \r\n
                    "startTimeStamp": "1657120790", # 开始运行时间戳 \r\n
                    "startTime": "2022年7月6日23时19分50秒", # 开始运行时间 \r\n
                    "runTime": "5分53秒", # 已运行时间 \r\n
                    "recv": 4, # 接收消息数 \r\n
                    "send": 0, # 发送消息数 \r\n
                    "wxNum": "DaenMax", # 微信号 \r\n
                    "nick": "Daen[emoji=E057]我", # 昵称 \r\n
                    "wxid": "wxid_3sq4tklb6c3121" # 机器人 WXID \r\n
                }, \r\n
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7716,
                "pid": 20872,
                "flag": "7777",
                "timestamp": "1657121143876"
            }
        """

        data = {"type": "Q0000", "data": {}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 发送文本消息(Q0001)
    def sendTextMessage(self, wxid: str, msg: str, bot_wxid: str = '') -> dict:
        """发送文本消息(Q0001)

        1.消息内支持文本代码，详情见文本代码章节 \r\n
        2.微信最多支持4096个字符,相当于2048个汉字,请勿超出否则崩溃

        Args:
            wxid (str): 要发给谁，支持好友、群聊、公众号等 \r\n \r\n
            msg (str): 信息 例: "[@,wxid=wxid_ephbxwk13k0022,nick=阿,isAuto=true]\n 你好\n [emoji=D83D]测试[捂脸][奸笑]"

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": {},
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7716,
                "pid": 20872,
                "flag": "7777",
                "timestamp": "1657121302946"
            }
        """
        data = {"type": "Q0001", "data": {"wxid": wxid, "msg": msg}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 修改下载图片(Q0002)
    def changeDownloadPicture(self, type: str, bot_wxid: str = '') -> dict:
        """修改下载图片(Q0002)

        建议登录成功之后，延迟几秒后执行

        Args:
            bot_wxid (str, optional):  机器人wxid, 不填则默认为初始化时的wxid
            type (str): '23:30-23:30' 为全天下载， '00:01-23:59' 为全天不下载

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": {},
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7716,
                "pid": 20872,
                "flag": "7777",
                "timestamp": "1657121302946"
            }
        """

        data = {"type": "Q0002", "data": {"type": type}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 获取个人信息(Q0003)
    def getPersonalInformation(self, bot_wxid: str = '') -> dict:
        """获取个人信息(Q0003)

        Args:
            bot_wxid (str, optional):  机器人wxid, 不填则默认为初始化时的wxid

        Returns:
            dict: {
                "code":
                "msg":
                "result": { \r\n
                    "wxid": "wxid_3sq4tklb6c3121", # wxid \r\n
                    "wxNum": "DaenMax", # 微信号 \r\n
                    "nick": "Daen[emoji=E057]我", # 昵称 \r\n
                    "device": "iphone", # 设备 \r\n
                    "phone": "18733355555", # 手机号 \r\n
                    "avatarUrl": "http://wx.qlogo.cn/mmhead/ver_1/", # 头像 \r\n
                    "country": "", # 国家 \r\n
                    "province": "", # 省份 \r\n
                    "city": "", # 城市 \r\n
                    "email": "", # 邮箱 \r\n
                    "qq": "1330166564" # QQ \r\n
                },
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7716,
                "pid": 20872,
                "flag": "7777",
                "timestamp": "1657121263722"
            }
        """

        data = {"type": "Q0003", "data": {}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 查询对象信息(Q0004)
    def queryObjectInformation(self, query_wxid: str, bot_wxid: str = '') -> dict:
        """查询对象信息(Q0004)

        Args:
            bot_wxid (str, optional):  机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            query_wxid (str): 查询对象的

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": { \r\n
                    "wxid": "wxid_3sx9sjgq99kd22", # 查询对象的wxid \r\n
                    "wxNum": "DaenMin", # 查询对象的微信号 \r\n
                    "nick": "叽里咕噜测试[emoji=D83D][emoji=DE01]", # 查询对象的昵称 \r\n
                    "remark": "小号", # 查询对象的备注 \r\n
                    "nickBrief": "JLGLCS?", # 查询对象的昵称简拼 \r\n
                    "nickWhole": "jiliguluceshi?", # 查询对象的昵称全拼 \r\n
                    "remarkBrief": "XH", # 查询对象的备注简拼 \r\n
                    "remarkWhole": "xiaohao", # 查询对象的备注全拼 \r\n
                    "enBrief": "JLGLCS?", # 查询对象的英文简拼 \r\n
                    "enWhole": "jiliguluceshi?", # 查询对象的英文全拼 \r\n
                    "v3": "v3_020...e@stranger", # 查询对象的v3 \r\n
                    "sign": "Daen robot", # 查询对象的签名 \r\n
                    "country": "CN", # 查询对象的国家 \r\n
                    "province": "Shandong", # 查询对象的省份 \r\n
                    "city": "Jinan", # 查询对象的城市 \r\n
                    "momentsBackgroudImgUrl": "", # 查询对象的朋友圈背景图 \r\n
                    "avatarMinUrl": "http://wx.qlogo.cn/mmhead/ver_1/...", # 查询对象的头像小图 \r\n
                    "avatarMaxUrl": "http://wx.qlogo.cn/mmhead/ver_1/..." # 查询对象的头像大图 \r\n
                },
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7496,
                "pid": 20792,
                "flag": "7777",
                "timestamp": "1657443960827"
            }
        """
        data = {"type": "Q0004", "data": {"wxid": query_wxid}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 获取好友列表(Q0005)
    def getFriendList(self, type: str = '1', bot_wxid: str = '') -> dict:
        """获取好友列表(Q0005)

        Args:
            bot_wxid (str, optional):  机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            type (int): 1 = 从缓存中获取, 2 = 重新遍历二叉树并刷新缓存

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": [{ \r\n
                    "wxid": "wxid_3sx9sjgq99kd22", # 好友wxid \r\n
                    "wxNum": "DaenMin", # 好友微信号 \r\n
                    "nick": "叽里咕噜测试[emoji=D83D][emoji=DE01]", # 好友昵称 \r\n
                    "remark": "小号", # 好友备注 \r\n
                    "nickBrief": "JLGLCS?", # 好友昵称简拼 \r\n
                    "nickWhole": "jiliguluceshi?", # 好友昵称全拼 \r\n
                    "remarkBrief": "XH", # 好友备注简拼 \r\n
                    "remarkWhole": "xiaohao", # 好友备注全拼 \r\n
                    "enBrief": "", # 好友英文简拼 \r\n
                    "enWhole": "", # 好友英文全拼 \r\n
                    "v3": "v3_020b3826fd03...e@stranger", # 好友的v3 \r\n
                    "sign": "Daen robot", # 好友的签名 \r\n
                    "country": "CN", # 好友的国家 \r\n
                    "province": "Shandong", # 好友的省份 \r\n
                    "city": "Jinan", # 好友的城市 \r\n
                    "momentsBackgroudImgUrl": "", # 好友的朋友圈背景图 \r\n
                    "sex": "", # 好友的性别 \r\n
                    "avatarMinUrl": "http://wx.qlogo.cn/mmhead/ver_1/...", # 好友的头像小图 \r\n
                    "avatarMaxUrl": "http://wx.qlogo.cn/mmhead/ver_1/..."  # 好友的头像大图 \r\n
                }],
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7496,
                "pid": 20792,
                "flag": "7777",
                "timestamp": "1657443688400"
            }
        """
        data = {"type": "Q0005", "data": {"type": type}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 获取群聊列表(Q0006)
    def getChatroomList(self, type: str = '1', bot_wxid: str = '') -> dict:
        """获取群聊列表(Q0006)

        Args:
            bot_wxid (str, optional):  机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            type (int): 1 = 从缓存中获取, 2 = 重新遍历二叉树并刷新缓存

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": [{ \r\n
                        "wxid": "20335634491@chatroom", # 群聊wxid \r\n
                        "wxNum": "", # 群聊微信号 \r\n
                        "nick": "东更道点心行草山岭团购群", # 群聊昵称 \r\n
                        "remark": "", # 群聊备注 \r\n
                        "nickBrief": "DGDDXXCSLTGQ", # 群聊昵称简拼 \r\n
                        "nickWhole": "donggengdaodianxinxingcaoshanlingtuangouqun", # 群聊昵称全拼 \r\n
                        "remarkBrief": "", # 群聊备注简拼 \r\n
                        "remarkWhole": "", # 群聊备注全拼 \r\n
                        "enBrief": "", # 群聊英文简拼 \r\n
                        "enWhole": "", # 群聊英文全拼 \r\n
                        "v3": "", # 群聊的v3 \r\n
                        "sign": "", # 群聊的签名 \r\n
                        "country": "", # 群聊的国家 \r\n
                        "province": "", # 群聊的省份 \r\n
                        "city": "", # 群聊的城市 \r\n
                        "momentsBackgroudImgUrl": "", # 群聊的朋友圈背景图 \r\n
                        "avatarMinUrl": "", # 群聊的头像小图 \r\n
                        "avatarMaxUrl": "", # 群聊的头像大图 \r\n
                        "sex": "", # 群聊的性别 \r\n
                        "memberNum": 4 # 群聊的成员数量 \r\n
                    }],
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7552,
                "pid": 20104,
                "flag": "7777",
                "timestamp": "1657445177665"
            }
        """
        data = {"type": "Q0006", "data": {"type": type}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 获取公众号列表(Q0007)
    def getSubscriptionList(self, type: str = '1', bot_wxid: str = '') -> dict:
        """_summary_

        Args:
            bot_wxid (str, optional):  机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            type (str, optional): 1 = 从缓存中获取, 2 = 重新遍历二叉树并刷新缓存

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": [{ \r\n
                    "wxid": "gh_a19ea6bab60c", # 公众号wxid \r\n
                    "wxNum": "wpsbgzs", # 公众号微信号 \r\n
                    "nick": "WPS办公助手", # 公众号昵称 \r\n
                    "remark": "", # 公众号备注 \r\n
                    "nickBrief": "WPSBGZS", # 公众号昵称简拼 \r\n
                    "nickWhole": "WPSbangongzhushou", # 公众号昵称全拼 \r\n
                    "remarkBrief": "", # 公众号备注简拼 \r\n
                    "remarkWhole": "", # 公众号备注全拼 \r\n
                    "enBrief": "", # 公众号英文简拼 \r\n
                    "enWhole": "", # 公众号英文全拼 \r\n
                    "v3": "", # 公众号的v3 \r\n
                    "sign": "", # 公众号的签名 \r\n
                    "country": "", # 公众号的国家 \r\n
                    "province": "", # 公众号的省份 \r\n
                    "city": "", # 公众号的城市 \r\n
                    "momentsBackgroudImgUrl": "", # 公众号的朋友圈背景图 \r\n
                    "avatarMinUrl": "", # 公众号的头像小图 \r\n
                    "avatarMaxUrl": "" # 公众号的头像大图 \r\n
                }],
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7552,
                "pid": 20104,
                "flag": "7777",
                "timestamp": "1657445357355"
            }
        """

        data = {"type": "Q0007", "data": {"type": type}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 获取群成员列表(Q0008)
    def getGroupMemberList(self, group_wxid: str, bot_wxid: str = '') -> dict:
        """获取群成员列表(Q0008)

        Args:
            bot_wxid (str, optional): 机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            group_wxid (str): 群聊 WXID

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": [{ \r\n
                        "wxid": "wxid_3sq4tklb6c3121", # 群成员wxid \r\n
                        "groupNick": "" # 群成员群昵称 \r\n
                    }],
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7395,
                "pid": 7528,
                "flag": "7777",
                "timestamp": "1657460988497"
            }
        """

        data = {"type": "Q0008", "data": {"wxid": group_wxid}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 发送聊天记录(Q0009)
    def sendChatroomMsg(self, wxid: str, title: str, data_list: list, bot_wxid: str = '') -> dict:
        """发送聊天记录(Q0009)

        Args:
            bot_wxid (str, optional): 机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            wxid (str): 要发给谁，支持好友、群聊、公众号等 \r\n
            title (str): 仅供电脑上显示用，手机上的话微信会根据[显示昵称]来自动生成 谁和谁的聊天记录 \r\n
            data_list (list): 聊天记录列表,每条聊天记录是一个dict,格式如下: \r\n
            {
                "wxid": "wxid_3sx9sjgq99kd22", 发送此条消息的人的wxid \r\n
                "nickName": "叽里咕噜", 显示的昵称, 可随意伪造 \r\n
                "timestamp": "1657461281", 10位时间戳 \r\n
                "msg": "嘿嘿，我也是" 消息内容 \r\n
            }

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": {},
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7305,
                "pid": 12384,
                "flag": "7777",
                "timestamp": "1657462661814"
            }
        """

        data = {
            "type": "Q0009",
            "data": {
                "wxid": wxid,
                "title": title,
                "dataList": data_list,
            },
        }
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 发送图片(Q0010)
    def sendImage(self, wxid: str, image_path: str, bot_wxid: str = '') -> dict:
        """发送图片(Q0010)

        Args:
            bot_wxid (str, optional):  机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            wxid (str):  要发给谁，支持好友、群聊、公众号等 \r\n
            image_path (str):  图片路径 \r\n

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": {},
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7305,
                "pid": 12384,
                "flag": "7777",
                "timestamp": "1657462661814"
            }
        """

        data = {"type": "Q0010", "data": {"wxid": wxid, "path": image_path}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 发送本地文件(Q0011)
    def sendFile(self, wxid: str, file_path: str, bot_wxid: str = '') -> dict:
        """发送本地文件(Q0011)

        Args:
            bot_wxid (str, optional):  机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            wxid (str):  要发给谁，支持好友、群聊、公众号等 \r\n
            file_path (str):  文件路径 \r\n

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": {},
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7305,
                "pid": 12384,
                "flag": "7777",
                "timestamp": "1657462661814"
            }
        """

        data = {"type": "Q0011", "data": {"wxid": wxid, "path": file_path}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 发送分享链接(Q0012)
    def sendLink(self, wxid: str, title: str, content: str, jump_url: str, path: str, app: str = '', bot_wxid: str = '') -> dict:
        """发送分享链接(Q0012)

        Args:
            bot_wxid (str, optional):  机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            wxid (str):  要发给谁，支持好友、群聊、公众号等 \r\n
            title (str):  标题 \r\n
            content (str):  内容 \r\n
            jump_url (str):  点击跳转地址 \r\n
            app (str): 可空, 例如QQ浏览器为:wx64f9cf5b17af074d \r\n
            path (str): 图片，本地路径或者网络直链

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": {},
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7305,
                "pid": 12384,
                "flag": "7777",
                "timestamp": "1657462661814"
            }
        """

        data = {"type": "Q0012", "data": {"wxid": wxid, "title": title, "content": content, "jumpUrl": jump_url, "app": app, "path": path}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 发送小程序(Q0013)
    def sendApp(self, wxid: str, title: str, content: str, jump_url: str, gh: str, path: str, bot_wxid: str = '') -> dict:
        """发送小程序(Q0013)

        Args:
            bot_wxid (str, optional):  机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            wxid (str):  要发给谁，支持好友、群聊、公众号等 \r\n
            title (str):  标题 \r\n
            content (str):  内容 \r\n
            jump_url (str):  点击跳转地址, 例如饿了么首页为:pages/index/index.html \r\n
            gh (str):  小程序原始ID, 例如饿了么为: gh_6506303a12bb\r\n
            path (str):  图片，本地路径或者网络直链 \r\n

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": {},
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7305,
                "pid": 12384,
                "flag": "7777",
                "timestamp": "1657462661814"
            }
        """

        data = {"type": "Q0013", "data": {"wxid": wxid, "title": title, "content": content, "jumpPath": jump_url, "gh": gh, "path": path}}
        response = requests.post(url=f'{self.url}?wxid={bot_wxid}', json=data)
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 发送音乐分享(Q0014)
    def sendMusic(self, wxid: str, name: str, author: str, app: str, jump_url: str, music_url: str, image_url: str, bot_wxid: str = '') -> dict:
        """发送音乐分享(Q0014)

        Args:
            bot_wxid (str, optional):  机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            wxid (str):  要发给谁，支持好友、群聊、公众号等 \r\n
            name (str):  歌名 \r\n
            author (str):  作者 \r\n
            app (str): 例如：酷狗 wx79f2c4418704b4f8, 网易云 wx8dd6ecd81906fd84,QQ音乐 wx5aa333606550dfd5 \r\n
            jump_url (str): 点击跳转地址 \r\n
            music_url (str): 网络歌曲直链\r\n
            image_url (str): 网络图片直链 \r\n

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": {},
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7305,
                "pid": 12384,
                "flag": "7777",
                "timestamp": "1657462661814"
            }
        """

        data = {
            "type": "Q0014",
            "data": {"wxid": wxid, "name": name, "author": author, "app": app, "jumpUrl": jump_url, "musicUrl": music_url, "imageUrl": image_url},
        }
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 发送XML(Q0015)
    def sendXml(self, wxid: str, xml: str, bot_wxid: str = '') -> dict:
        """发送XML(Q0015)

        Args:
            bot_wxid (str, optional):  机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            wxid (str):  要发给谁，支持好友、群聊、公众号等 \r\n
            xml (str):  xml内容 \r\n

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": {},
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7305,
                "pid": 12384,
                "flag": "7777",
                "timestamp": "1657462661814"
            }
        """

        data = {"type": "Q0015", "data": {"wxid": wxid, "xml": xml}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 确认收款(Q0016)
    def confirmMoney(self, wxid: str, transferid: str, bot_wxid: str = '') -> dict:
        """确认收款(Q0016)

        Args:
            bot_wxid (str, optional): 机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            wxid (str): 对方 WXID \r\n
            transferid (str): 转账 ID \r\n

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": {},
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7668,
                "pid": 4452,
                "flag": "7777",
                "timestamp": "1657950074378"
            }
        """

        data = {"type": "Q0016", "data": {"wxid": wxid, "transferid": transferid}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 同意好友请求(Q0017)
    def agreeFriend(self, scene: str, v3: str, v4: str, bot_wxid: str = '') -> dict:
        """同意好友请求(Q0017)

        Args:
            bot_wxid (str, optional):  机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            scene (str):  来源 1=qq 3=微信号 6=单向添加 10和13=通讯录 14=群聊 15=手机号 17=名片 30=扫一扫 \r\n
            v3 (str):  v3 数据 \r\n
            v4 (str):  v4 数据 \r\n

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": {},
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7668,
                "pid": 4452,
                "flag": "7777",
                "timestamp": "1657950074378"
            }
        """

        data = {"type": "Q0017", "data": {"scene": scene, "v3": v3, "v4": v4}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 添加好友_通过v3(Q0018)
    def addFriendByV3(self, v3: str, content: str, scene: str, type: int, bot_wxid: str = '') -> dict:
        """添加好友_通过v3(Q0018)

        Args:
            bot_wxid (str, optional):  机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            v3 (str):  v3 可通过查询陌生人信息获得 \r\n
            content (str): 附加内容
            scene (str):  来源 1=qq 3=微信号 6=单向添加 10和13=通讯录 14=群聊 15=手机号 17=名片 30=扫一扫 \r\n
            type (int): 类型 1=新朋友, 2=互删朋友(此时来源将固定死为3)

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": {},
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7668,
                "pid": 4452,
                "flag": "7777",
                "timestamp": "1657950074378"
            }
        """

        data = {"type": "Q0018", "data": {"v3": v3, "content": content, "scene": scene, "type": type}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 添加好友_通过wxid(Q0019)
    def addFriendByWxid(self, wxid: str, content: str, scene: str, bot_wxid: str = '') -> dict:
        """添加好友_通过wxid(Q0019)

        Args:
            bot_wxid (str, optional): 机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            wxid (str): 对方 WXID \r\n
            content (str): 附加内容 \r\n
            scene (str): 来源 1=qq 3=微信号 6=单向添加 10和13=通讯录 14=群聊 15=手机号 17=名片 30=扫一扫 \r\n

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": {},
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7668,
                "pid": 4452,
                "flag": "7777",
                "timestamp": "1657950074378"
            }
        """

        data = {"type": "Q0019", "data": {"wxid": wxid, "content": content, "scene": scene}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 查询陌生人信息(Q0020)
    def getStrangerInfo(self, pq: str, bot_wxid: str = '') -> dict:
        """查询陌生人信息(Q0020)

        Args:
            bot_wxid (str, optional):  机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            pq (str): 手机号或者QQ \r\n

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": { \r\n
                    "pq": "1649364566", # 手机号或QQ  如果已是好友，那么此参数将为wxid \r\n
                    "v3": "v3_000b708f0b040@stranger", # v3数据 加好友时用\r\n
                    "v4": "v4_000b708f0b040@stranger", # v4数据 加好友时用\r\n
                    "province": "Shandong", # 省份 \r\n
                    "city": "Qingdao", # 城市 \r\n
                    "avatarMinUrl": "http://wx.qlogo.cn/mmhead/ver_1/", # 头像小图 \r\n
                    "avatarMaxUrl": "http://wx.qlogo.cn/mmhead/ver_1/", # 头像大图 \r\n
                    "nick": "", # 昵称 \r\n
                    "sex": "1", # 性别 1=男 2=女 \r\n
                    "isFriend": "2" # 是否为好友 1=是 2=否 \r\n
                },
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7302,
                "pid": 6400,
                "flag": "7777",
                "timestamp": "1658042992580"
            }
        """

        data = {"type": "Q0020", "data": {"pq": pq}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 邀请进群(Q0021)
    def inviteInGroup(self, group_wxid: str, friend_wxid: str, type: int, bot_wxid: str = '') -> dict:
        """邀请进群(Q0021)

        Args:
            bot_wxid (str, optional):  机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            group_wxid (str):  群wxid \r\n
            friend_wxid (str):  好友wxid \r\n
            type (int):  类型 1=直接拉，2=发送邀请链接\r\n

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": {},
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7668,
                "pid": 4452,
                "flag": "7777",
                "timestamp": "1657950074378"
            }
        """

        data = {"type": "Q0021", "data": {"wxid": group_wxid, "objWxid": friend_wxid, "type": type}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 删除好友(Q0022)
    def deleteFriend(self, friend_wxid: str, bot_wxid: str = '') -> dict:
        """删除好友(Q0022)

        Args:
            bot_wxid (str, optional): 机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            friend_wxid (str): 好友 WXID \r\n

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": {},
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7668,
                "pid": 4452,
                "flag": "7777",
                "timestamp": "1657950074378"
            }
        """

        data = {"type": "Q0022", "data": {"wxid": friend_wxid}}
        response = requests.post(url=f'{self.url}?wxid={bot_wxid}', json=data)
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 修改对象备注(Q0023)
    def setFriendRemark(self, friend_wxid: str, remark: str, bot_wxid: str = '') -> dict:
        """修改对象备注(Q0023)

        Args:
            bot_wxid (str, optional):  机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            friend_wxid (str): 对象 WXID 支持好友 WXID、群 WXID \r\n
            remark (str): 备注 支持 Emoji、微信表情

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": {},
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7668,
                "pid": 4452,
                "flag": "7777",
                "timestamp": "1657950074378"
            }
        """

        data = {"type": "Q0023", "data": {"wxid": friend_wxid, "remark": remark}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 修改群聊名称(Q0024)
    def setGroupName(self, group_wxid: str, nick: str, bot_wxid: str = '') -> dict:
        """修改群聊名称(Q0024)

        Args:
            bot_wxid (str, optional):  机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            group_wxid (str): 群 WXID \r\n
            nick (str):  群名称 支持 Emoji、微信表情

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": {},
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7668,
                "pid": 4452,
                "flag": "7777",
                "timestamp": "1657950074378"
            }
        """

        data = {"type": "Q0024", "data": {"wxid": group_wxid, "nick": nick}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 发送名片(Q0025)
    def sendCard(self, friend_wxid: str, xml: str, bot_wxid: str = '') -> dict:
        """发送名片(Q0025)

        Args:
            bot_wxid (str, optional):  机器人 WXID, 不填则默认为初始化时的 WXID \r\n
            friend_wxid (str):  好友wxid \r\n
            xml (str):  名片xml 不懂的话，就自己发一个，然后看日志

        Returns:
            dict: {
                "code": 200,
                "msg": "操作成功",
                "result": {},
                "wxid": "wxid_3sq4tklb6c3121",
                "port": 7210,
                "pid": 10228,
                "flag": "7777",
                "timestamp": "1658317739774"
            }
        """

        data = {"type": "Q0025", "data": {"wxid": friend_wxid, "xml": xml}}
        return self.post_(bot_wxid=bot_wxid, data=data)

    # 创建名片xml
    def createCardXml(self, nickname: str, wxid: str, headimg: str) -> str:
        root = ET.Element("msg")
        root.attrib["bigheadimgurl"] = "http://wx.qlogo.cn/mmhead/0"
        root.attrib["smallheadimgurl"] = "http://wx.qlogo.cn/mmhead/132"
        root.attrib["username"] = "wxid_jah3fozezery22"
        root.attrib["nickname"] = "〆无所不能。"
        root.attrib["fullpy"] = "wusuobuneng"
        root.attrib["shortpy"] = ""
        root.attrib["alias"] = "PQAPQB"
        root.attrib["imagestatus"] = "3"
        root.attrib["scene"] = "17"
        root.attrib["province"] = "云南"
        root.attrib["city"] = "中国大陆"
        root.attrib["sign"] = ""
        root.attrib["sex"] = "2"
        root.attrib["certflag"] = "0"
        root.attrib["certinfo"] = ""
        root.attrib["brandIconUrl"] = ""
        root.attrib["brandHomeUrl"] = ""
        root.attrib["brandSubscriptConfigUrl"] = ""
        root.attrib["brandFlags"] = ""
        root.attrib["regionCode"] = "CN_Yunnan_Kunming1"
        root.attrib["biznamecardinfo"] = ""

        tree = ET.ElementTree(root)
        declaration = '<?xml version="1.0"?>'
        xml_str = declaration + ET.tostring(root, encoding="utf-8").decode()
        print(xml_str)

        return xml_str

    # 回调事件
    def callbackEvents(self, callback_fun, port: int = 5000, log: bool = False):
        """回调事件

        Args:
            callback_fun (_type_): 回调方法
            port (int, optional): 回调端口. 默认 5000.
            log (bool, optional): 是否打印日志. 默认 False.
        """

        Process(target=self.callbackMessage, args=(port, callback_fun, log)).start()

    # 回调消息
    def callbackMessage(self, port, callback_fun, log):
        """回调消息

        Args:
            port (_type_): 回调端口
            callback_fun (_type_): 回调方法
            log (_type_): 是否打印日志

        Returns:
            _type_: _description_
        """
        with open(os.devnull, 'w') as f:
            if not log:
                sys.stdout = f
                sys.stderr = f

            app = Flask(__name__)

            @app.route('/', methods=['GET', 'POST'])
            def callback():
                if request.method == 'GET':
                    return jsonify({'code': 404, 'msg': '需要POST请求'})
                elif request.method == 'POST':
                    callback_fun(request.json)
                    return jsonify({'code': 200, 'msg': '回调成功'})

            app.run(port=port)


if __name__ == '__main__':
    xx = Robot(host='127.0.0.1', port=7668, bot_wxid='')
    xx.callbackEvents(callback_fun=None, port=5000)
