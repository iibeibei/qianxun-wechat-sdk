# 千寻微信框架的 Python SDK

## 介绍

千寻微信框架的 Python SDK，基于千寻微信框架的 HTTP API 接口，封装了一些常用的接口，方便开发者使用。

## 安装

```shell

pip install qianxun-wechat-sdk

```

## 使用示例

```python
import qianxun.Emoji as Emoji       # 导入 qianxun Emoji 表情模块
from qianxun.SDK import Robot       # 导入 qianxun SDK 框架

# 创建一个回调函数来接收 qianxun 框架的回调事件
def callback(request):
    print('=' * 50 + '回调事件' + '=' * 50, end='\n\n')
    print(request)

    if request['event'] == 10014:
        print('账号变动事件(10014)')

    if request['event'] == 10008:
        print('收到群聊消息(10008)')

    if request['event'] == 10009:
        print('收到私聊消息(10009)')

    if request['event'] == 10010:
        print('自己发出消息(10010)')

    if request['event'] == 10006:
        print('收到转账事件(10006)')

    if request['event'] == 10013:
        print('撤回事件(10013)')

    if request['event'] == 10011:
        print('好友请求(10011)')

    if request['event'] == 10007:
        print('支付事件(10007)')


if __name__ == '__main__':

    # 创建一个机器人实例，传入机器人的 ip 和端口，以及机器人的 wxid (可选)
    robot = Robot(host='127.0.0.1', port=7777, bot_wxid='')

    # 调用机器人的登录接口, 获取机器人的 wxid
    robot.bot_wxid = robot.getWeChatList()['result'][0]['wxid']

    # 创建一个机器人的回调事件，传入回调函数和端口
    robot.callbackEvents(callback_fun=callback, port=5000)

    # 调用机器人的发送文本消息接口，传入机器人的 wxid 和消息内容
    robot.sendTextMessage(wxid='filehelper', msg=f'你好 {Emoji.小丑脸} 测试 {Emoji.表情_捂脸}')

```
