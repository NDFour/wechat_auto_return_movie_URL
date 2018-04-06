# -*- coding: utf-8 -*-

from email.mime.text import MIMEText
from datetime import datetime
from werobot import WeRoBot
import smtplib
import pymysql
import re
import os

robot=WeRoBot(token='wx123')
robot.config['SESSION_STORAGE'] = False

### global isdebugi TO JUDGE IF THE PROGRAM IS IN DEBUG (test account)
# 0 > 一起来电影; 1 > NDFour登录的测试号；2 > 电影资源搜
isdebug=0

#   程序开始运行时的时间
#global start_datetime
start_datetime=''

#global last_use_cnt
last_use_cnt=0
#global total_use_cnt
total_use_cnt=0
#global use_cnt
use_cnt={}
#global name_dic  用来验证公众号是否在该列表中以判断是否非法调用
name_dic={}
#last_movie 用来记录用户取关前的发送的一条消息记录
last_movie=''

#@robot.subscribe
#def subscribe(message):
#    msg="注意：\n1  发送电影名字的时候请不要带其他特殊符号，只要电影名字即可；\n2  电影名字中请不要出现错别字"
#    return msg

@robot.unsubscribe
def unsubscribe(message):
    global last_movie
    print('有用户取关啦！！！上一条消息是：[%s]'%last_movie)

def main():
    v_name=input('请输入要检索的电影名字')
    print(reply_info(v_name))

@robot.text
def hello(message):
#    return '        【系统升级】\n\n  公众号系统进行服务升级，预计24小时内完成。\n  请耐心等待升级完成！'

#   the account of 'Lynn'
    master_root='o2NddxHhZloQV55azmx8zVXv9mAQ'
    if isdebug==1:
        master_root='ozDqGwZ__sjgDwZ2yRfusI84XeAc'
    elif isdebug==2:
        master_root='onD430y7UUrFB8sDV6W8PU4Skwy8'

#   预留 查看公众号 message.target 接口
    if message.content=='showtarget':
        return message.target

    if message.source==master_root:
#   预留 接口，发送后 run 后程序开始工作
        if message.content=='run':
            updatename_dic()
            return 'Program startting success!'
#   预留数据查看接口，发送'showanalyze',返回各公众号调用次数统计
        elif message.content=='showanalyze':
            return showanalyze()
#   预留adarticles添加接口，发送'insertadarticles .*',执行sql语句插入adarticles
        elif re.match(r'insertadarticles .*',message.content):
            return insertadarticles(message.content)
#   预留更新电影数据表videoinfo接口，发送'updatevideoinfo **.sql',更新videoinfo数据表，返回执行结果（成功或失败）
        elif re.match(r'updatevideoinfo .*.sql',message.content):
            return updatevideoinfo(message.content)
#   预留公众号添加接口，发送'adduser target_id target_name',执行sql语句插入user
        elif re.match(r'adduser .*',message.content):
            return manageuser(message.content,1)
#   预留公众号删除接口，发送'deluser id',执行sql语句删除user
        elif re.match(r'deluser [0-9]*',message.content):
            return manageuser(message.content,0)


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


    v_name=message.content
    
    if(len(v_name) > 30):
        return '电影名长度过长，请精简关键字后重新发送。'

    v_name=modefy_name(v_name)
    bdpan=pre_process(v_name)
    if len(bdpan):
        return bdpan

    articles=reply_info(v_name)
    global last_movie
    last_movie=v_name
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
        sql_select="SELECT name,videourl,picurl FROM xiaoheju WHERE name LIKE '%v_name%'" 
        sql_select=sql_select.replace('v_name',v_name)
        cursor.execute(sql_select)

        out_list=[]
        cnt=0

        for i in cursor.fetchmany(7):
            in_list=[]
            in_list.append(i[0])
            in_list.append(i[0])
            in_list.append(i[2])
            in_list.append('http://idy007.xyz/movie.php?vurl='+i[1].replace('fiml','player').replace('.html','-1-1.html'))
      
            # 旧域名被封，更改域名
            # in_list.append(i[2].replace('gooddianying.net','nicedianying.com'))

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

#   图文消息加上一条之前的广告推文链接
    ad_select="SELECT title,picurl,url FROM adarticles Where canbeuse=1 ORDER BY id DESC"
    adtuple=[]
    try:
        cursor.execute(ad_select)
        adarticles_list=cursor.fetchone()

        adtuple.append(adarticles_list[0])
        adtuple.append(adarticles_list[0])
        adtuple.append(adarticles_list[1])
        adtuple.append(adarticles_list[2])

        # 在第二条图文消息处添加 adarticles
        out_list.insert(1,adtuple)
    except:
        pass

    conn.close()

    if int(cnt)<7:
        out_list.append(['如果无法播放点我查看教程','','https://t1.picb.cc/uploads/2018/01/27/Lz2KR.png','http://t.cn/R8hJGC7'])

    return out_list

#   showanalyze 查询各公众号调用次数
def showanalyze():
    # DEMO: showanalyze
    global name_dic 
    global total_use_cnt
    global use_cnt

    # 链接数据库，查询其他公众号对应数据库中的 id
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='cqmygpython2',db='wechatmovie',charset='utf8')
    cursor=conn.cursor()
    sql_select_id="SELECT id FROM users WHERE target_name=target_account_name"

    analyze_info='*已累计调用 %s 次*\n'%total_use_cnt
    for pub_account in use_cnt:
        #try:
         #  cursor.execute("w
        analyze_info+=('----------\n')
        analyze_info+='%s : %d\n' % (name_dic[pub_account] , use_cnt[pub_account])
    analyze_info+=('----------\n')
    analyze_info+='\nStart: %s' % start_datetime
    # analyze_info+='\nEnd: %s' % datetime.now()
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

def insertadarticles(message_content):
    # DEMO: inertadarticles INERT INTO adarticles(title,picurl,url,canbeuse) VALUES ('**','**','**',1);

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

def updatevideoinfo(message_content):
   # DEMO: updatevideoinfo ***.sql

    source_name=message_content.replace('updatevideoinfo ','')
    source_name=source_name.replace(' ','')
    bak_sql_dir=os.path.abspath('..')+'/mysql_python/%s'%source_name
    sql_source=('mysql -uroot -pcqmygpython2 wechatmovie < %s'%bak_sql_dir)

#   judge if the file is exist
    if os.path.exists(bak_sql_dir):
        try:
            os.system(sql_source)
            return '更新电影信息 videoinfo 数据表备份 %s 成功！'%source_name
        except:
            return '更新电影信息 videoinfo 数据表备份 %s 失败！'%source_name
 
        return 'File:\n---------\n%s\n---------\nnot exists!'%source_name

def manageuser(message_content,func):
    if len(message_content)<23:
        return '语法错误，请检查语法后重新发送指令！'

    # adduser
    if func==1:
        target_id=message_content[8:23]
        target_name=message_content[24:]
        sql_content="INSERT INTO users(target_id,target_name) VALUES ('%s','%s');" % (target_id,target_name)
    # deluser
    elif func==0:
        target_id=message_content[8:]
        sql_content="DELETE FROM users WHERE id='%s';" % target_id

    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='cqmygpython2',db='wechatmovie',charset='utf8')
    cursor=conn.cursor()

    msg=''

    try:
        cursor.execute(sql_content)
        conn.commit()
        if func==1:
            msg = '添加公众号【%s : %s】成功！'%(target_name,target_id)
        elif func==0:
            msg = 'Delete success!'
    except:
        conn.rollback()
        if func==1:
            msg = '添加公众号【%s : %s】失败！'%(target_name,target_id)
        if func==0:
            msg = 'Delete failed!'
    finally:
        cursor.close()
        conn.close()

    rel=updatename_dic()
    if rel==1:
        pass 
    elif rel==0:
        msg = '添加公众号在 updatename_dic 时出错！'

    return msg


# 更新 公众号列表 name_dic 
def updatename_dic():
# 被 manageuser 调用以更新 name_dic 
    global name_dic
    global use_cnt 
    name_dic={}
    use_cnt_bak=use_cnt
    use_cnt={}

    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='cqmygpython2',db='wechatmovie',charset='utf8')
    cursor=conn.cursor()
    sql_select="SELECT target_id,target_name FROM users;"

    msg=1

    try:
        cursor.execute(sql_select)
        users_tuple=cursor.fetchall()
        # 存放 tuple中的字tuple的下标为0的项
        tuple_list=[]
        for i in users_tuple:
            tuple_list.append(i[0])
            name_dic[i[0]]=i[1]
            # 更新 use_cnt 
            if i[0] in use_cnt:
                pass 
            else:
                use_cnt[i[0]]=0
        # Judge if the use_cnt[*] has been deleted
        for i2 in use_cnt_bak:
            if i2 in tuple_list:
                use_cnt[i2]=use_cnt_bak[i2]
            else:
                pass

    except:
        msg = 0
    finally:
        cursor.close()
        conn.close()

    return msg
   
#main()

# 让服务器监听在　0.0.0.0:4444
robot.config['HOST']='0.0.0.0'
robot.config['PORT']=80
robot.run()

