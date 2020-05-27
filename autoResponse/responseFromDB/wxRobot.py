# -*- coding: utf-8 -*-

from werobot import WeRoBot
import re
import configparser
import sqlite3


# 默认启用 Session
robot = WeRoBot(token='wx123')

@robot.subscribe
def subscribe(message):
    outlist=[]
    outlist.append(['公众号免费看电影教程','','https://s1.ax1x.com/2018/06/02/CogADx.png','https://w.url.cn/s/AGW9n4L'])

    return outlist


@robot.text
def hello(message, session):
    # return '【通知】\n\n    因公众号提供电影服务的服务器压力增加，导致价格上涨。公众号免费提供电影服务，无任何盈利，现需要暂时暂停电影服务。望谅解！\n\n    服务恢复时间请关注本公众号通知！\n\n<a href="https://mp.weixin.qq.com/s/IV9we9FYrPxi5w68fuLb9A">点我留言反馈</a>'

    str_input = message.content.strip()
    msg = ''
    try:
        # 该回复为 电影 ID
        str_input = int(str_input)

        # 根据 ID 搜索 详情
        msg = get_by_id(str_input)
        # print(msg)
        # print()     
    except Exception as e:
        # 该回复为 电影名
        # 若 将用户发送消息 转为 int 失败，则表示 用户发送的是 片名，而不是 电影 ID
        str_input = str_input.replace('《', '').replace('》', '')
        msg = get_rel(str_input)
        # print(msg)
        # print()


    return msg


def get_rel(name):
    # 回复给用户的消息体
    msg = ''
    try:
        conn = sqlite3.connect('scrapy.sqlite3')
        cursor = conn.cursor()

        sql = "select id,name from movies where name" + " like '%" + name + "%' order by length(name) limit 15"
        # print(sql)
        cursor.execute(sql)
        rel = cursor.fetchall()

        '''
        搜索「城南旧事」的结果,
        发送前面编码获得网盘，注册用户直接点击书名查看
        - - - - - - - - - - - - - - - - - - 
        [ 103704 ]城南旧事
        [ 112760 ]城南旧事
        [ 114159 ]城南旧事
        - - - - - - - - - - - - - - - - - - 
        ◎ 参加辣豆瓣每天读书5分钟打卡
        ◎ 查看书单，发送数字 3 
        ◎ 加入书友群求助书友。
        '''

        if len(rel):
            msg = '搜索 《' + name + '》 的结果，\n发送前面编码获得播放链接。\n\n- - - - - - - - - - - - - - - - - - \n'
            for m in rel:
                msg += '[ ' + str(m[0]) + ' ]' + m[1] + '\n'
            msg += '- - - - - - - - - - - - - - - - - - \n'
            msg += '⚠️ 名字可以不完整，但是一定不要有错别字哦 ~'

        else:
            msg = '你好，没有找到跟《' + name + '》相符合的电影哦\n你可以换一个电影试试~~~'
    except Exception as e:
        # print(e)
        msg = '你好，没有找到跟《' + name + '》相符合的电影哦\n你可以换一个电影试试~~~'
    finally:
        cursor.close()
        conn.close()
        # print('finally 这里执行了')

    return msg


def get_by_id(id):
    msg = ''
    try:
        conn = sqlite3.connect('scrapy.sqlite3')
        cursor = conn.cursor()

        # sql = "select name,url_m3u8 from movies where id=" + str(id)
        sql = "select name,url from movies where id=" + str(id)
        # print(sql)
        cursor.execute(sql)
        rel = cursor.fetchall()

        msg = '《' + rel[0][0] + '》 \n\n点击下面蓝字播放~'
        msg += '\n- - - - - - - - - - - - - - - - - - \n'
        chatper_list = rel[0][1].split('##')

        # 从 url_m3u8 中分割每一集
        for url in chatper_list:
            if len(url):
                name_url = url.split('$')
                msg += '<a href="' + name_url[1] + '">' + name_url[0] + '集</a>\n'
            else:
                pass
    except Exception as e:
        # print(e)
        msg = '你好，没有找到 ID 为 ' + str(id) + ' 的影片，请检查你的输入 ~\n\n⚠️ 如果果片名为纯数字，在发送片名的时候请加上书名号，如《1984》，其中 1984 为片名，否则会搜索不出结果'
    finally:
        # print('get_by_id finally 执行了')
        cursor.close()
        conn.close()

    return msg



# 让服务器监听在 0.0.0.0:80
# robot.config['HOST']='0.0.0.0'
# robot.config['PORT']=80
# robot.run()
