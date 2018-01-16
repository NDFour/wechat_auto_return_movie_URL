# -*- coding: utf-8 -*-

import requests
import re
import werobot
import string

robot=werobot.WeRoBot(token='wx123')
robot.config['SESSION_STORAGE'] = False

@robot.subscribe
def subscribe(message):
    msg="注意：\n1  发送电影名字的时候请不要带其他特殊符号，只要电影名字即可；\n2  电影名字中请不要出现错别字\n\n<a href='http://18.18.2499dy.com/plays/23544-0-0.html'>《前任3》点我观看</a>\n<a href='http://18.18.2499dy.com/plays/23555-0-0.html'>《妖铃铃》点我观看</a>\n<a href='http://18.18.2499dy.com/plays/23500-0-0.html'>《芳华》点我观看</a> \n<a href='https://pan.baidu.com/s/1c3giAty'>《无问西东》点击观看</a> 密码: i9uj"
    return msg

@robot.text
def hello(message):
    print('《%s》'%message.content)
    wwxd="无问西东"
    wwxd2="无问东西"
    qr3="前任三"
    yll="妖玲玲"
    cfzzx="超凡蜘蛛侠"
    ttnkh="泰坦尼克号"
    if(wwxd in message.content):
        return('《无问西东》\n百度网盘链接： https://pan.baidu.com/s/1c3giAty 密码: i9uj')
    elif(wwxd2 in message.content):
        return('《无问西东》\n百度网盘链接： https://pan.baidu.com/s/1c3giAty 密码: i9uj')
    elif(qr3 in message.content):
        message.content="前任3"
    elif(yll in message.content):
        message.content="妖铃铃"
    elif(cfzzx in message.content):
        return('《超凡蜘蛛侠》\n百度网盘链接: https://pan.baidu.com/s/1drcdgq 密码: 2ru9')
    elif(ttnkh in message.content):
        return('《泰坦尼克号》\n百度网盘链接: https://pan.baidu.com/s/1pMbc6nD 密码: t7ce')
    else:
        return getUrl(message.content)


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

    after_re_url=re_url.findall(r.text)
    cnt=0
    msg='【以下是搜索到的相关影片】\n▾▾▾▾▾▾▾▾\n\n\n'
    for i in after_re_url:
        cnt+=1
        #msg+='【'+str(cnt)+'】 '+re_url_title.search(i).group()+'\n'+'<a href="'+pre_url+re_url_href.search(i).group()+'">点我观看</a>'+'\n\n'
        msg+='【'+str(cnt)+'】 '+re_url_title.search(i).group()+'\n'+'<a href="'+pre_url+re_url_href.search(i).group()+'">点我观看</a>'+'\n\n'
        # 数据过多造成溢出
        if cnt==10:
            break
    #print('cnt=',cnt)
    msg=msg.replace('.html','-0-0.html')
    msg=msg.replace('title=','')
    msg=msg.replace('videos','plays')
    if cnt==0:
        msg='未查找到相关结果，请联系我私人微信 ndfour001'
    msg+='\n▴▴▴▴▴▴▴▴\n\n未搜索到结果？\n<a href="http://mp.weixin.qq.com/s/X0EqQJ803aSL-9WLTwatTg">视频无法播放？点我</a>\n\n>> 私人微信号:ndfour001\n>> 有问题加我'
    return (msg)

#main()

# 让服务器监听在　0.0.0.0:4444
#robot.config['HOST']='0.0.0.0'
#robot.config['PORT']=4444
robot.config['HOST']='0.0.0.0'
robot.config['PORT']=80
robot.run()

