# -*- coding: utf-8 -*-

import requests
import re
from werobot import WeRoBot
import string

robot=WeRoBot(token='wx123')
robot.config['SESSION_STORAGE'] = False

@robot.subscribe
def subscribe(message):
    msg="注意：\n1  发送电影名字的时候请不要带其他特殊符号，只要电影名字即可；\n2  电影名字中请不要出现错别字\n\n<a href='http://18.18.2499dy.com/plays/23544-0-0.html'>《前任3》点我观看</a>\n<a href='http://18.18.2499dy.com/plays/23555-0-0.html'>《妖铃铃》点我观看</a>\n<a href='http://18.18.2499dy.com/plays/23500-0-0.html'>《芳华》点我观看</a> \n"
    return msg

@robot.text
def hello(message):
    print('《%s》'%message.content)

#   纠正用户发的电影名字中的错别字
    v_name=modefy_name(message.content)
#   对于搜索不到的影视资源用百度网盘链接代替
    bdpan=pre_process(v_name)
    if len(bdpan) > 84:
        return bdpan

#   构建图文消息,返回的是一个内嵌列表的列表
    articles=getUrl(v_name)
    return articles


#   对于搜索不到的影视资源用百度网盘链接代替
def pre_process(v_name):
    url=''
    author_info='\n\n-----------------\n>> 如果网盘链接失效不能用请加QQ群进行反馈或者加我微信\n>> QQ群： 282223892\n>> 微信: ndfour001'

#   电影名字
    cfzzx="超凡蜘蛛侠"
    ttnkh="泰坦尼克号"
    dhxy="大话西游"

    if(cfzzx in v_name):
        url='《超凡蜘蛛侠》\n百度网盘链接: https://pan.baidu.com/s/1drcdgq 密码: 2ru9'
    elif(ttnkh in v_name):
        url='《泰坦尼克号》\n百度网盘链接: https://pan.baidu.com/s/1pMbc6nD 密码: t7ce'
    elif(dhxy in v_name):
        url='《大话西游》\n百度网盘链接:https://pan.baidu.com/s/1hsXnGOG 密码:jr4k'
    
        url+=author_info
    return url
   

# 替换用户发来的电影名字中的错别字
def modefy_name(v_name):

# 先把电影名字中的特殊符号去除
    v_name=v_name.replace('《','')
    v_name=v_name.replace('》','')

    wwxd2="无问东西"
    qr3="前任三"
    yll="妖玲玲"
    qgw="七个我"
    lry='龙日一'

    if(wwxd2 in v_name):
        return "无问西东"
    elif(qr3 in v_name):
        return "前任3"
    elif(yll in v_name):
        return "妖铃铃"
    elif(qgw in v_name):
        return '柒个我'
    elif(lry in v_name):
        return '龙日一，你死定了'

    return v_name


def main():
    print(getUrl('hello'))

def getUrl(keyword):
    url='http://www.lantuyingshi.com/search.php?searchword='
    url=url+keyword
    #print(url)
# 目前而言，headers加与不加效果一样
    headers={
    'Host':'18.18.2499dy.com',
#    'Referer':'http://18.18.2499dy.com/lists/1.html',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'
}
    try:
        r=requests.get(url,headers=headers,timeout=30)
    except:
        return '查找失败，请联系我私人微信 ndfour001'

    # 得到是class="list-link" href="/videos/23500.html" title="芳华" target="_blank">
    re_url=re.compile(r'class="list-link" href=".*"?')
    # 得到的是/videos/23500.html
    re_url_href=re.compile(r'/videos/[0-9]*.html')
    # 得到title="芳华"
    re_url_title=re.compile(r'title=".*?"')
    pre_url='http://18.18.2499dy.com'
    # 得到/../.*.jpg
    re_url_picurl=re.compile(r'/uploads/.*?"')
    pic_url_list=re_url_picurl.findall(r.text)
    # 返回一个list，list内是dic
    video_list=[]

    after_re_url=re_url.findall(r.text)
    cnt=0

    for i in after_re_url:
        in_list=[]
        cnt+=1
        if cnt>0:
           pic_cnt=cnt-1
        full_pic_url='http://img.xzpifu.com'+pic_url_list[pic_cnt]
        full_pic_url=full_pic_url.replace('"','')
        full_video_title=re_url_title.search(i).group()
        full_video_title=full_video_title.replace('title=','')
        full_video_title=full_video_title.replace('"','')
        full_video_url=pre_url+re_url_href.search(i).group()
        full_video_url=full_video_url.replace('.html','-0-0.html')
        full_video_url=full_video_url.replace('videos','plays')
        in_list.append(full_video_title)
        in_list.append(full_video_title)
        in_list.append(full_pic_url)
        in_list.append(full_video_url)

        video_list.append(in_list)

        # 图文消息最多有8条
        if cnt==7:
            break
# 返回图文消息
    if cnt==0:
       return '没有搜索到影片？请加入下方QQ群进行反馈或添加我微信：\nQQ群: 282223892\n我的微信：ndfour001' 
# 加入帮助信息
    video_list.append(['如果无法播放点我查看教程','','https://t1.picb.cc/uploads/2018/01/27/Lz2KR.png','http://t.cn/R8hJGC7'])
    return video_list

#main()

# 让服务器监听在　0.0.0.0:4444
#robot.config['HOST']='0.0.0.0'
#robot.config['PORT']=4444
robot.config['HOST']='0.0.0.0'
robot.config['PORT']=80
robot.run()

