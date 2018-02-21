# -*- coding: utf-8 -*-

from werobot import WeRoBot
import pymysql
from datetime import datetime

robot=WeRoBot(token='wx123')
robot.config['SESSION_STORAGE'] = False

#   程序开始运行时的时间
global start_datetime
start_datetime=''
global use_cnt
use_cnt={'gh_a987c1f298e2':0}

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

#   客户公众号列表，用于识别消息来自哪个公众号的粉丝
    name_dic={'gh_a987c1f298e2':'测试账号'}
    print('《%s》来自 [%s]'%(message.content,name_dic[message.target]))

#   预留数据查看接口，发送'showusecnt',返回各公众号调用次数统计
#   记录每个公众号的调用程序次数
    global use_cnt
    use_cnt[message.target]+=1
    # 更新常旭开始运行时间
    global start_datetime
    if start_datetime=='':
        start_datetime=datetime.now()
    if message.content=='showanalyze':
        if message.source=='ozDqGwZ__sjgDwZ2yRfusI84XeAc':
            analyze_info='[公众号调用次数统计]\n\n'
            for pub_account in use_cnt:
                analyze_info+='%s : %d\n' % (name_dic[pub_account] , use_cnt[pub_account])
            analyze_info+='\nStart: %s' % start_datetime
            analyze_info+='\nEnd: %s' % datetime.now()
            # 返回公众号调用程序次数统计
            return analyze_info

    v_name=message.content
    
    if(len(v_name) > 30):
        return '电影名长度过长，请精简关键字后重新发送。'

#   纠正用户发的电影名字中的错别字
    v_name=modefy_name(v_name)
#   对于搜索不到的影视资源用百度网盘链接代替
    bdpan=pre_process(v_name)
    if len(bdpan):
        return bdpan

#   构建图文消息,返回的是一个内嵌列表的列表 或 错误信息字符串
    articles=reply_info(v_name)
    return articles


# 替换用户发来的电影名字中的错别字
def modefy_name(v_name):

# 先把电影名字中的特殊符号去除
    v_name=v_name.replace('《','')
    v_name=v_name.replace('》','')
    v_name=v_name.replace('。','')

    bbdw='卑鄙的我'
    lhbdhq='灵魂摆渡'
    lry='龙日一'
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
    elif(lhbdhq in v_name):
        return "灵魂摆渡"
    elif(yll in v_name):
        return "妖铃铃"
    elif(qgw in v_name):
        return '柒个我'
    elif(lry in v_name):
        return '龙日一，你死定了'
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

    print('共查询到 %s 条记录' % cnt)

    conn.close()

    out_list.append(['如果无法播放点我查看教程','','https://t1.picb.cc/uploads/2018/01/27/Lz2KR.png','http://t.cn/R8hJGC7'])
    return out_list

#main()

# 让服务器监听在　0.0.0.0:4444
robot.config['HOST']='0.0.0.0'
robot.config['PORT']=80
robot.run()

