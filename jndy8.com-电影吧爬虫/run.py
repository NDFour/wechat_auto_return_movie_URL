#
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-03-16 23:45:56
# Last Modified: 2018-03-17 02:01:27
#

import requests
import os
import re 
import pymysql

def getHtml(url):
    print('--> getHtml')
    html_text=''

    headers={
            'Host': 'www.jndy8.com',
            'Referer': 'http://www.jndy8.com/dy.asp?ToPage=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }
    try:
        r=requests.get(url,timeout=10)
        r.status_code 
        r.encoding=r.apparent_encoding
        html_text=r.text
    except:
        html_text=''

    print('--> getHtml end')
    return html_text

def generateUrls(baseurl,pages):
    urls=[]
    #for i in range(1,int(pages)+1):
    for i in range(int(pages)+1):
        print(i)
        urls.append(baseurl+str(i))
    return urls

def getMovieList(html_text):
#   根据给定的目录 url 解析出目录中包含的电影信息
    print('--> getMovieList')

    # get show.asp?id=4802
    reId=re.compile(r'show.asp\?id=[0-9]*')
    # get <img src="https://wx4.sinaimg.cn/mw690/005yF2tCgy1fpdaqdaoorj30b40fkwk4.jpg" wid
    rePic=re.compile(r'<img src=".*" wid')
    # get alt="上位2之盛筵"/>
    reName=re.compile(r'alt=".*"/>')

    listId=reId.findall(html_text)
    listPic=rePic.findall(html_text)
    listName=reName.findall(html_text)

    # 对解析到的数据进行完善
    # /upload/***.jpg 加前缀 http://www.jndy8.com
    outId=listId
    outPic=[]
    outName=[]
    for i in listPic:
        i=i.replace('<img src="','').replace('" wid','')
        if 'upload' in i:
            i='http://www.jndy8.com'
        outPic.append(i)
    for j in listName:
        j=j.replace('alt="','').replace('"/>','')
        outName.append(j)

    # 根据在目录页找到的视频信息进一步解析 得到 mp4 直链
    # 传参 video id 然后 getInfo() 构造 url 进行访问
    cntRealUrl=0
    outRealUrl=[]
    # 无效直链的个数
    cntNull=0
    for id in outId:
        realUrl=getInfo(id)
        # getInfo() 返回值不为空
        if realUrl:
            outRealUrl.append(realUrl)
            cntNull+=1
            print(outName[cntRealUrl-cntNull])
            print(outPic[cntRealUrl-cntNull])
            print(realUrl)
        # 直链无效
        else:
            print('该直链无效')

        cntRealUrl+=1

    print('--> getMovieList end')


def getInfo(id):
#   构造播放页 url 进而从网页源码中得到播放链接
    print('--> getInfo')
#   http://www.jndy8.com/jxplay.asp?id=3582&j=1
    baseurl='http://www.jndy8.com/jxplay'
    url=baseurl+id.replace('show','')+'&j=1'

    html_text=getHtml(url)
    # get http://api.coolnan.net/vip.asp?url=https://tbm.alicdn.com/vUAdB2SRl6Uwi7hn7WB/QyLdbhoz7X1ZMqvon7v@@hd.mp4
    reUrl=re.compile(r'http://api.cool.*mp4')
    # 可能有的视频用的其他解析线路
    try:
        realUrl=reUrl.search(html_text).group()
        print('--> getInfo end')
        return realUrl
    except:
        print('--> getInfo end')
        return ''

def main():
    print('run')
    baseUrl='http://www.jndy8.com/dy.asp?ToPage='
    # 手动输入每一栏目的页数
    dyPages=input('Movie pages:')
    urls=generateUrls(baseUrl,dyPages)
    
    cntGetList=0
    for i in urls:
        print('getMovieList  page : %s\n'%cntGetList)
        html_text=getHtml(i)
        getMovieList(html_text)
        cntGetList+=1

main()
