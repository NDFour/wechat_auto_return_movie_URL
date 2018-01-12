import requests
import re
import werobot

robot=werobot.WeRoBot(token='wx123')
@robot.text
def hello(message):
    return getUrl(message.content)

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
    if cnt==0:
        msg='未查找到相关结果，请联系我私人微信 ndfour001'
    msg+='\n▴▴▴▴▴▴▴▴\n\n未搜索到结果？\n<a href="http://mp.weixin.qq.com/s/JhC9UV_1v1ocqGQUCv2bzg">点我看查看更多搜索结果</a>\n\n>> 私人微信号:ndfour001\n>> 有问题加我'
    return (msg)

# 让服务器监听在　0.0.0.0:4444
#robot.config['HOST']='0.0.0.0'
#robot.config['PORT']=4444
robot.config['HOST']='0.0.0.0'
robot.config['PORT']=80
robot.run()
