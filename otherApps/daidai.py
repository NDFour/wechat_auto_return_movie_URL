#
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-04-27 00:30:00
# Last Modified: 2018-04-27 01:13:07
#

import re
import requests
import pymysql

def getHtml(url):
    html_text=''
    try:
        r=requests.get(url,timeout=10)
        # r.encoding=r.apparent_encoding
        html_text=r.text
    except:
        html_text=''
    return html_text

def genUrl(baseUrl,pages):
    urls=[]
    for i in range(1,int(pages)+1):
        urls.append(baseUrl+str(i))
    return urls

def parseHtml(html_text):
    # get > <a href="/movie/14459.html"  target="_blank" title="爱与黑暗的故事">
    rawInfo=re.compile(r'<a href="/movie/[0-9].*?>')
    # get > /movie/14459.html
    rawUrl=re.compile(r'/movie/.*.html')
    # get > title="爱与黑暗的故事"
    rawTitle=re.compile(r'title=".*')
    # get > "http://ww2.sinaimg.cn/large/006qfx1Tjw1f29pij13ruj30bo0go40d.jpg" alt
    rawPic=re.compile(r'".*" alt')

    outTitle=[]
    outUrl=[]
    outPic=[]

    # 存储 url和title到列表
    listRawInfo=rawInfo.findall(html_text)
    iCnt=0
    for i in listRawInfo:
        iCnt+=1
        # 去除48条数据中重复的24条
        if iCnt%2:
            continue
        urlTmp=rawUrl.findall(i)[0]
        titleTmp=rawTitle.findall(i)[0]
        outUrl.append('http://www.dduiyy.com'+urlTmp)
        outTitle.append(titleTmp.replace('title=','').replace('"','').replace('>',''))
    # 存储 pic到列表
    listRawPic=rawPic.findall(html_text)
    for i in listRawPic:
        outPic.append(i.replace('"','').replace(' alt',''))


#    print('---------------------')
#    print(outTitle)
#    print(outUrl)
#    print(outPic)
#    print()
    

    outList=[]
    iCnt=0
    for i in outTitle:
        inList=[]
        inList.append(outTitle[iCnt])
        inList.append(outUrl[iCnt])
        inList.append(outPic[iCnt])

        outList.append(inList)
        iCnt+=1
#    print(outList)

    # 将解析到的视频信息添加到数据库
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='cqmygpython2',db='wechatmovie',charset='utf8')
    cursor=conn.cursor()

    for i in outList:
        print(i[0])
        try:
            sql_insert="INSERT INTO daidai(name,videourl,picurl) VALUES ('%s','%s','%s');"%(i[0],i[1],i[2])
            cursor.execute(sql_insert)
            conn.commit()
            print('Save to mysql success')
        except:
            conn.rollback()
            print('Save to mysql failed')

    cursor.close()
    conn.close()


def main():
    print("hello")
    # 电影
    bUrl1='http://www.dduiyy.com/movie/list.html?page='
    # 电视剧
    bUrl2='http://www.dduiyy.com/tv/list.html?page='
    # 动漫
    bUrl3='http://www.dduiyy.com/anime/list.html?page='
    # 综艺
    bUrl4='http://www.dduiyy.com/variety/list.html?page='

    pageOf1=input('电影标签的页数：')
    pageOf2=input('电视剧标签的页数：')
    pageOf3=input('动漫标签的页数：')
    pageOf4=input('综艺标签的页数：')

    urls1=genUrl(bUrl1,pageOf1)
    urls2=genUrl(bUrl2,pageOf2)
    urls3=genUrl(bUrl3,pageOf3)
    urls4=genUrl(bUrl4,pageOf4)

    for i in urls1:
        html_text=getHtml(i)
        parseHtml(html_text)
    for j in urls2:
        html_text=getHtml(j)
        parseHtml(html_text)
    for k in urls3:
        html_text=getHtml(k)
        parseHtml(html_text)
    for l in urls4:
        html_text=getHtml(l)
        parseHtml(html_text)

main()
