# -*- coding: utf-8 -*-

from werobot import WeRoBot
import pymysql
import re
import os

robot=WeRoBot(token='wx123')
robot.config['SESSION_STORAGE'] = False

iterative=0
ifrun=0

@robot.subscribe
def subscribe(message):
    return "嗨你终于来啦遇见你，真美好！直接回复电影名字，即可在线观看最新电影！"


'''
@robot.unsubscribe
def unsubscribe(message):
    #global last_movie
    print('有用户取关啦！！！上一条消息是：[%s]'%last_movie)
'''

@robot.text
def hello(message):
#    return '        【系统升级】\n\n  公众号系统进行服务升级，预计24小时内完成。\n  请耐心等待升级完成！'
    global ifrun
    masterRoot='orPeKwuaLwcbS4_rxlGA-Mv5Q3q8'
    v_name=message.content
    if(len(v_name) > 30):
        return '电影名长度过长，请精简关键字后重新发送。'
    print(message.source)
    if message.source==masterRoot:
        if(v_name=="run"):
            ifrun=1
        elif(v_name=="stop"):
            ifrun=0
        elif(v_name=="iterative"):
            iterative=1
        elif(v_name=="uniterative"):
            iterative=0
        elif(v_name="shutdown"):
            os.system('shutdown -h now')
    if ifrun==0:
        return '非付费用户，无法使用该功能！'
 
    articles=reply_info(v_name)
    if len(articles)==0:
        return "No Result"
    return articles

# 通过查询数据库将结果返回给用户
def reply_info(v_name):
    global iterative
#   递归调用时，如电影名为空，直接返回
    if v_name == '':
        return '数据库中暂无该影片，请先观看其他影片。\n\n-想让你的公众号也具有发送名字即可在线观看电影功能？\n-欢迎加我微信 ndfour001 洽谈合作。' 

    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='cqmygpython2',db='wechatmovie',charset='utf8')
    cursor=conn.cursor()

    try:
        sql_select="SELECT name,videourl,picurl FROM daidai WHERE name LIKE '%v_name%';" 
        sql_select=sql_select.replace('v_name',v_name)
        cursor.execute(sql_select)

        out_list=[]
        cnt=0

        for i in cursor.fetchmany(7):
            in_list=[]
            in_list.append(i[0])
            in_list.append(i[0])
            in_list.append(i[2])
            in_list.append(i[1])
      
            out_list.append(in_list)
            cnt+=1
    except:
        cursor.close()
        conn.close()
        return '查询数据失败，错误代码 0x_reply_info_().SELECT ERROR\n\n-想让你的公众号也具有发送名字即可在线观看电影功能？\n-欢迎加我微信 ndfour001 洽谈合作。 '

    len_v_name=len(v_name)
#   如果搜索不到数据，则将电影关键词长度一再缩小
    while (iterative and (cnt == 0) and len_v_name):
        len_v_name-=1
        return reply_info(v_name[0:len_v_name])

    # 关闭数据库链接
    cursor.close()
    conn.close()

    return out_list
   
#main()

# 让服务器监听在　0.0.0.0:4444
robot.config['HOST']='0.0.0.0'
robot.config['PORT']=80
robot.run()


