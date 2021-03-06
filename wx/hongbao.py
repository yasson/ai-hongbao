# -*- coding: utf-8 -*-
from wxpy import Bot, FRIENDS
from wxpy import embed
import requests
import re
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# 扫码登录
bot = Bot(cache_path=True)

"""
默认消息处理方法
==============================================================================
"""


def _get_red_pack(user, link, mobile):
    try:
        data = {'url': link, 'mobile': mobile}
        geturl = 'http://101.132.113.122:3007/hongbao'
        r = requests.post(url=geturl, data=data)
        response = r.text
        if response is not None:
            result = json.loads(response)
            result = '领取结果：\n%s' % result['message']
            user.send(result)
    except Exception as e:
        print e


def _default_text_register(text_msg):
    print str(text_msg.sender.name)
    my_friends = bot.friends().search(str(text_msg.sender.name))
    for user in my_friends:
        user.mark_as_read()
        if text_msg.text == 'Q':
            if not str(user.remark_name):
                user.send('您还未绑定手机号'.decode("UTF-8"))
            else:
                remark_name = re.findall(r"^[1][3,4,5,6,7,8][0-9]{9}$", str(user.remark_name))
                if remark_name:
                    user.send(('当前绑定的手机号码为：%s' % str(user.remark_name)).decode("UTF-8"))
                else:
                    user.send('绑定的号码有误，请正确绑定'.decode("UTF-8"))
        elif text_msg.text == 'H':
            user.send('******使用说明******\n'
                      '首次使用需绑定手机号码\n'
                      '*绑定方法*\n'
                      '**直接发送手机号码给我\n\n'
                      '*领取红包方法*\n'
                      '**直接将外卖红包分享给我\n'
                      '**或发送外卖红包链接地址'.decode("UTF-8"))
        else:
            new_remark_name = re.findall(r"^[1][3,4,5,6,7,8][0-9]{9}$", text_msg.text)
            if new_remark_name:
                new_remark_name = '' + str(new_remark_name).replace('[u\'', '').replace('\']', '')
                user.set_remark_name(new_remark_name)
                user.send(('成功将手机号码绑定为：%s' % str(new_remark_name)).decode("UTF-8"))
            elif 'h5.ele.me/hongbao' in text_msg.text or 'activity.waimai.meituan.com' in text_msg.text:
                if not user.remark_name:
                    user.send('您还未绑定手机号'.decode("UTF-8"))
                else:
                    remark_name = re.findall(r"^[1][3,4,5,6,7,8][0-9]{9}$", user.remark_name)
                    if remark_name:
                        user.send('红包领取中…'.decode("UTF-8"))
                        _get_red_pack(user, text_msg.text, remark_name)
                    else:
                        user.send('绑定的号码有误，请正确绑定'.decode("UTF-8"))

            else:
                user.send('我是机器人，你说的啥我不懂'.decode("UTF-8"))
        break


def _default_share_register(share_msg):
    my_friends = bot.friends().search(share_msg.sender.name)
    for user in my_friends:
        user.mark_as_read()
        if user.remark_name:
            remark_name = re.findall(r"^[1][3,4,5,6,7,8][0-9]{9}$", user.remark_name)
            if remark_name:
                mobile = '' + str(remark_name).replace('[u\'', '').replace('\']', '')
                url = share_msg.raw["Url"]
                url = str(url).replace("&amp;", "&")
                # print url
                # print mobile
                user.send('红包领取中…'.decode("UTF-8"))
                _get_red_pack(user, url, mobile)
            else:
                user.send('领取红包前请先绑定要领取的手机号（直接发送号码即可）'.decode("UTF-8"))
        else:
            user.send('领取红包前请先绑定要领取的手机号（直接发送号码即可）'.decode("UTF-8"))

        break


@bot.register()
def deal_with_msg(msg):
    # step 1. 打印到console
    print(str(msg.receive_time), msg)

    # step 2. 保存TEXT类型消息的txt文件
    if msg.type == 'Text':
        _default_text_register(msg)

    elif msg.type == 'Sharing':
        _default_share_register(msg)

        # elif msg.type == "Picture":
        #     _default_picture_register(msg)


# 自动接受新的好友请求
@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    # 接受好友请求
    new_friend = msg.card.accept()
    # 向新的好友发送消息
    new_friend.send('本项目为自动领取美团、饿了么红包，自动手气最佳 \n'
                    '项目已开源\n'
                    'https://github.com/chengzijian/ai-hongbao\n'
                    '感谢以下项目的支持\n'
                    'https://github.com/game-helper/hongbao\n'
                    'https://github.com/youfou/wxpy\n'
                    '查看使用说明请扣 H\n'
                    '查询绑定的手机号码请扣 Q\n'
                    '使用前请先绑定手机号'
                    .decode("UTF-8"))


# 堵塞线程，以保持监听状态
embed()
