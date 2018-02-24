# -*- coding: utf-8 -*-

from werobot import WeRoBot
import pymysql
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import re

robot=WeRoBot(token='wx123')
robot.config['SESSION_STORAGE'] = False

#   程序开始运行时的时间
#global start_datetime
start_datetime=''

#global last_use_cnt
last_use_cnt=0
#global total_use_cnt
total_use_cnt=0
#global use_cnt
use_cnt={'gh_a987c1f298e2':0,'gh_499743c9649e':0,'gh_2a98dd25db1f':0,'gh_a7d8a272069c':0}
#global isdebugi TO JUDGE IF THE PROGRAM IS IN DEBUG (test account)
isdebug=0

global name_dic
name_dic={'gh_a987c1f298e2':'测试账号','gh_499743c9649e':'一起来电影','gh_2a98dd25db1f':'文艺的小猪','gh_a7d8a272069c':'电影假期'}

#@robot.subscribe
#def subscribe(message):
#    msg="注意：\n1  发送电影名字的时候请不要带其他特殊符号，只要电影名字即可；\n2  电影名字中请不要出现错别字"
#    return msg

def main():
    v_name=input('请输入要检索的电影名字')
    print(reply_info(v_name))

@robot.text
def hello(message):
#    return '        【系统升级】\n\n  公众号系统进行服务升级，预计24小时内完成。\n  请耐心等待升级完成！'

#   判断转发消息的公众号是否在已授权列表中
    if message.target in name_dic:
        print('《%s》'%message.content)
    else:
        return '！！\n未经授权的公众号，请联系微信 ndfour001 购买看电影服务使用权\n\n微信公众号搜索【一起来电影】，关注后发送电影名即可免费观看高清电影！'

#   记录每个公众号的调用程序次数
    global last_use_cnt
    global use_cnt
    global total_use_cnt
    use_cnt[message.target]+=1
    total_use_cnt+=1

#   如果当天调用次数超过 5000 次发送邮件通知
    if (total_use_cnt-last_use_cnt) == 5000:
        send_mail()
        last_use_cnt=total_use_cnt

    # 更新程序开始运行时间
    global start_datetime
    if start_datetime=='':
        start_datetime=datetime.now()

#   the account of 'Lynn'
    master_root='o2NddxHhZloQV55azmx8zVXv9mAQ'
    if isdebug:
        master_root='ozDqGwZ__sjgDwZ2yRfusI84XeAc'
    if message.source==master_root:
#   预留数据查看接口，发送'showusecnt',返回各公众号调用次数统计
        if message.content=='showanalyze':
            return showanalyze()
#   预留数据查看接口，发送'showusecnt',返回各公众号调用次数统计
        if re.match(r'insertadarticles .*',message.content):
            return insert_ad_articles(message.content)

    v_name=message.content
    
    if(len(v_name) > 30):
        return '电影名长度过长，请精简关键字后重新发送。'

    v_name=modefy_name(v_name)
    bdpan=pre_process(v_name)
    if len(bdpan):
        return bdpan

    articles=reply_info(v_name)
    return articles


# 替换用户发来的电影名字中的错别字
def modefy_name(v_name):

# 先把电影名字中的特殊符号去除
    v_name=v_name.replace('《','')
    v_name=v_name.replace('》','')
    v_name=v_name.replace('。','')

    bbdw='卑鄙的我'
    myz='猫妖传'
    qgw="七个我"
    qr3="前任三"
    wwxd2="无问东西"
    yll="妖玲玲"
    yyzx='有言在先'
    zl2='战狼二'
    zndsjasn='在你的世界爱上你'
    zsxd='自杀小队'

    if(wwxd2 in v_name):
        return "无问西东"
    elif(bbdw in v_name):
        return "神偷奶爸"
    elif(qr3 in v_name):
        return "前任3"
    elif(yll in v_name):
        return "妖铃铃"
    elif(qgw in v_name):
        return '柒个我'
    elif(yyzx in v_name):
        return '有言在仙'
    elif(zndsjasn in v_name):
        return '在你的世界爱你'
    elif(myz in v_name):
        return '妖猫传'
    elif(zl2 in v_name):
        return '战狼2'
    elif(zsxd in v_name):
        return 'x特遣队'

    return v_name

#   对于搜索不到的影视资源用百度网盘链接代替
def pre_process(v_name):
    url=''
    author_info='\n\n-----------------\n>> 如果网盘链接失效不能用请加我微信 ndfour001 进行反馈'

#   电影名字
    lyj="老友记"
    ywar="欲望爱人"

    if(lyj in v_name):
        url='《老友记》\n磁力链接：magnet:?xt=urn:btih:D563EF792A247A5547D8D1191B41F2CBE0B2382E  \n<a href="http://mp.weixin.qq.com/s/PSOi3kK_aRzCHLba2u9qjQ">点我查看如何使用磁力链接</a>'
    elif(ywar in v_name):
        url='《欲望爱人》\n在线观看链接：http://video.tudou.com/v/XMTc4NTg3MTUwOA==.html'

    if url:
        url=url+author_info
        return url
    return ''


# 通过查询数据库将结果返回给用户
def reply_info(v_name):
#   递归调用时，如电影名为空，直接返回
    if v_name == '':
        return '数据库中暂无该影片，请先观看其他影片。\n\n-想让你的公众号也具有发送名字即可在线观看电影功能？\n-欢迎加我微信 ndfour001 洽谈合作。' 

    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='cqmygpython2',db='wechatmovie',charset='utf8')
    cursor=conn.cursor()

    try:
        sql_select="SELECT name,videourl,picurl FROM videoinfo WHERE name LIKE '%v_name%'" 
        sql_select=sql_select.replace('v_name',v_name)
        cursor.execute(sql_select)

        out_list=[]
        cnt=0

        for i in cursor.fetchmany(7):
            in_list=[]
            in_list.append(i[0])
            in_list.append(i[0])
            in_list.append(i[1])
            in_list.append(i[2])

            out_list.append(in_list)
            cnt+=1
    except:
        cursor.close()
        conn.close()
        return '查询数据失败，错误代码 0x_reply_info_().SELECT ERROR\n\n-想让你的公众号也具有发送名字即可在线观看电影功能？\n-欢迎加我微信 ndfour001 洽谈合作。 '

    len_v_name=len(v_name)
#   如果搜索不到数据，则将电影关键词长度一再缩小
    while ((cnt == 0) and len_v_name):
        len_v_name-=1
        return reply_info(v_name[0:len_v_name])

#    有了上面那个递归以及函数开头检查v_name是否为空 , 所以不需要下面两行
#    if cnt == 0:
#        return '数据库中暂无该影片，请先观看其他影片。\n\n-想让你的公众号也具有发送名字即可在线观看电影功能？\n-欢迎加我微信 ndfour001 洽谈合作。' 

#    print('共查询到 %s 条记录' % cnt)

#    如果查询到的电影记录条数少于7，则图文消息加上一条之前的广告推文链接
    if int(cnt)<7:
        ad_select="SELECT title,picurl,url FROM adarticles Where canbeuse=1 ORDER BY id DESC"
        adtuple=[]
        try:
            cursor.execute(ad_select)
            adarticles_list=cursor.fetchone()

            adtuple.append(adarticles_list[0])
            adtuple.append(adarticles_list[0])
            adtuple.append(adarticles_list[1])
            adtuple.append(adarticles_list[2])
#           控制adarticles的插入位置，不要过于靠后
            index=cnt//2
            if index:
                out_list.insert(index,adtuple)
            else:
                index+=1
                out_list.insert(index,adtuple)
        except:
            pass

    conn.close()

    out_list.append(['如果无法播放点我查看教程','','https://t1.picb.cc/uploads/2018/01/27/Lz2KR.png','http://t.cn/R8hJGC7'])
    return out_list

#   showanalyze 查询各公众号调用次数
def showanalyze():
    global name_dic 
    global total_use_cnt
    analyze_info='[公众号调用次数统计]\n\n*已累计调用 %s 次*\n'%total_use_cnt
    for pub_account in use_cnt:
        analyze_info+=('----------\n')
        analyze_info+='%s : %d\n' % (name_dic[pub_account] , use_cnt[pub_account])
    analyze_info+=('----------\n')
    analyze_info+='\nStart: %s' % start_datetime
    analyze_info+='\nEnd: %s' % datetime.now()
    # 返回公众号调用程序次数统计
    return analyze_info


#   发邮件代码
def send_mail():
    _user = "lgang219@qq.com"
    _pwd  = "eehrjkcueceqcaga"
    _to   = "ndfour@foxmail.com"

    msg = MIMEText(showanalyze())
    msg["Subject"] = "[showanalyze] 后台调用次数通知"
    msg["From"] = _user
    msg["To"] = _to

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
    except:
        pass

def insert_ad_articles(message_content):
    sql_insert=message_content.replace('insertadarticles ','')
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='cqmygpython2',db='wechatmovie',charset='utf8')
    cursor=conn.cursor()

    try:
        cursor.execute(sql_insert)
        conn.commit()
        msg = '成功插入一条【广告图文】到数据库！'
    except:
        conn.rollback()
        msg = '插入一条【广告图文】到数据库失败！'
    finally:
        cursor.close()
        conn.close()

    return msg
     
#main()

# 让服务器监听在　0.0.0.0:4444
robot.config['HOST']='0.0.0.0'
robot.config['PORT']=80
robot.run()

