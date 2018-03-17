#
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-03-16 23:45:56
# Last Modified: 2018-03-17 14:15:08
#

import requests
import os
import re 
import pymysql

def getHtml(url):
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

    return html_text

def generateUrls(baseurl,pages):
    urls=[]
    #for i in range(1,int(pages)+1):
    for i in range(1,int(pages)+1):
        urls.append(baseurl+str(i))
    return urls

def getMovieList(html_text):
#   根据给定的目录 url 解析出目录中包含的电影信息

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
    # len(outId)=40 获取到的id是电影条目数的2倍
    cntId=0
    # 一次性存入一个目录页 page 的电影信息
    outSqlList=[]
    for id in outId:
        # 消重 取消 outId 中重复的 id
        cntId+=1
        if cntId % 2:
            continue
        print('\n%s'%outName[cntRealUrl])

        inSqlList=[]

        realUrl=getInfo(id)
        # getInfo() 返回值不为空
        if realUrl:
            outRealUrl.append(realUrl)
            #print(outName[cntRealUrl])
            #print(outPic[cntRealUrl])
            #print(realUrl)

            inSqlList.append(outName[cntRealUrl])
            inSqlList.append(outPic[cntRealUrl])
            inSqlList.append(realUrl)

            outSqlList.append(inSqlList)

        # 直链无效
        else:
            print('该直链无效')

        cntRealUrl+=1

    # 将电影信息写入数据库
    db=pymysql.connect(host='localhost',user='root',password='cqmygpython2',db='wechatmovie',port=3306,charset='utf8')
    cur=db.cursor()

    for i in outSqlList:
        sql_insert='INSERT INTO jndy8 (name,videourl,picurl) VALUES ("%s","%s","%s");' % (i[0],i[2],i[1])
        try:
            cur.execute(sql_insert)
            db.commit()
        except:
            db.rollback()

    cur.close()
    db.close()


def getInfo(id):
#   构造播放页 url 进而从网页源码中得到播放链接
#   http://www.jndy8.com/jxplay.asp?id=3582&j=1
    baseurl='http://www.jndy8.com/jxplay'
    url=baseurl+id.replace('show','')+'&j=1'

    html_text=getHtml(url)
    # get http://api.coolnan.net/vip.asp?url=https://tbm.alicdn.com/vUAdB2SRl6Uwi7hn7WB/QyLdbhoz7X1ZMqvon7v@@hd.mp4
    reUrl=re.compile(r'http://api.cool.*(mp4|html)')
    # 可能有的视频用的其他解析线路
    try:
        realUrl=reUrl.search(html_text).group()
        return realUrl
    except:
        return ''

def main():
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
