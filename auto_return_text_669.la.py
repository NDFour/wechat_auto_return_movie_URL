# -*- coding: utf-8 -*-

import requests
import re
import werobot
import string

robot=werobot.WeRoBot(token='wx123')
robot.config['SESSION_STORAGE'] = False

@robot.subscribe
def subscribe(message):
    msg="注意：\n1  发送电影名字的时候请不要带其他特殊符号，只要电影名字即可；\n2  电影名字中请不要出现错别字\n\n<a href='http://18.18.2499dy.com/plays/23544-0-0.html'>《前任3》点我观看</a>\n<a href='http://18.18.2499dy.com/plays/23555-0-0.html'>《妖铃铃》点我观看</a>\n<a href='http://18.18.2499dy.com/plays/23500-0-0.html'>《芳华》点我观看</a> "
    return msg

@robot.text
def hello(message):
    print('《%s》'%message.content)
    wwxd2="无问东西"
    qr3="前任三"
    yll="妖玲玲"
    cfzzx="超凡蜘蛛侠"
    ttnkh="泰坦尼克号"
    lry="龙日一"
    if(wwxd2 in message.content):
        message.content="无问西东"
    elif(qr3 in message.content):
        message.content="前任3"
    elif(yll in message.content):
        message.content="妖铃铃"
    elif(cfzzx in message.content):
        return('《超凡蜘蛛侠》\n百度网盘链接: https://pan.baidu.com/s/1drcdgq 密码: 2ru9')
    elif(ttnkh in message.content):
        return('《泰坦尼克号》\n百度网盘链接: https://pan.baidu.com/s/1pMbc6nD 密码: t7ce')
    elif(lry in message.content):
        message.content="龙日一，你死定了"
 
    return getUrl(message.content)


def main():
    key=input('please input search key')
    print(getUrl(key))

def getUrl(keyword):
    url='http://m.baqicun.info/search.php?searchword='
    url=url+keyword
    #print(url)
# 目前而言，headers加与不加效果一样
    headers={
        'Cookie':'yunsuo_session_verify=8dd5873049fd395d6f6e88350ef80516; __cfduid=d38d82ad57dbb45afb672ec2ff3e099571516370332; PHPSESSID=l76k51jc3jio2bihofs0ci45k4; Hm_lvt_39a2c04db640aa884d54e6d3a06c84b6=1516370329,1516370335,1516370587,1516371493; Hm_lpvt_39a2c04db640aa884d54e6d3a06c84b6=1516371607',
        'Host':'m.baqicun.info',
        'Referer':'http://m.baqicun.info/m/28134.html',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Mobile Safari/537.36'
		}

    try:
        r=requests.get(url,timeout=10)
    except:
        return '查找失败，请联系我私人微信 ndfour001'

    # 得到是/m/25344.html"><img data-src="/templets/default/images/noimg.gif" src="http://img.baqicun.info/uploads/allimg/201709/3b736ea5edd5102c.jpg" alt="捷德奥特曼" style
    re_url=re.compile(r'/m/.*?style')
    # 得到的是/m/25344.html
    re_url_href=re.compile(r'/m.*.html')
    # alt="捷德奥特曼"
    re_url_title=re.compile(r'alt=.*"')
    # http://m.baqicun.info/p/27367-0-0.html
    pre_url='/mm.baqicun.info/p'

    after_re_url=re_url.findall(r.text)
    cnt=0
    msg='【以下是搜索到的相关影片】\n▾▾▾▾▾▾▾▾\n\n\n'
    for i in after_re_url:
        cnt+=1
        print(i)
        print(type(re_url_title.search(i)))
        msg+='【'+str(cnt)+'】 '+re_url_title.search(i).group()+'\n'+'<a href="'+pre_url+re_url_href.search(i).group()+'">点我观看</a>'+'\n\n'
        # 数据过多造成溢出
        if cnt==10:
            break
    #print('cnt=',cnt)
    msg=msg.replace('.html','-0-0.html')
    msg=msg.replace('alt=','')
    msg=msg.replace('/m','')
    if cnt==0:
        msg='未查找到相关结果，请加入下方QQ群反馈'
    msg+='\n▴▴▴▴▴▴▴▴\n\n<a href="http://mp.weixin.qq.com/s/X0EqQJ803aSL-9WLTwatTg">视频无法播放？点我</a>\n\n>> 有问题请加\n>> QQ群: 282223892\n>> 我的微信: ndfour001'
    return (msg)

#main()

# 让服务器监听在　0.0.0.0:4444
#robot.config['HOST']='0.0.0.0'
#robot.config['PORT']=4444
robot.config['HOST']='0.0.0.0'
robot.config['PORT']=80
robot.run()

