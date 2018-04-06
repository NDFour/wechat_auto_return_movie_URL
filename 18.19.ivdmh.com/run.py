#
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-03-13 17:14:51
# Last Modified: 2018-04-06 13:05:48
#

import requests
import os
import re 
import pymysql

def getHtml(url):
    url=url+'.html'
    html_text=''
    try:
        r=requests.get(url)
        r.status_code 
        html_text=r.text
        print('getHtml %s success'%url)
    except:
        print('getHtml %s failed'%url)
        html_text=''
    return html_text

def genUrls(baseurl,pages):
    urls=[]
    for i in range(pages+1):
        urls.append(baseurl+str(i))
    return urls

def parseHtml(html_text):
    # 得到 <li><a href="/fiml/36981.html" title="巴霍巴利王(下)：终结" target="_self"><div class="picsize"><img class="loading lazy" data-src="http://images.odoukei.com/upload/vod/2017-05-16/201705161494936558.jpg" alt
    rawInfo=re.compile(r'<li>.*alt')

    # 得到 /fiml/36981.html 
    rawHref=re.compile(r'/fiml/.*.html')
    # 得到 title="巴霍巴利王(下)：终结"
    rawTitle=re.compile(r'title=".*?"')
    # 得到 http://images.odoukei.com/upload/vod/2017-05-16/201705161494936558.jpg"
    rawPic=re.compile(r'http.*."')

    outList=[]
    rawInfos=rawInfo.findall(html_text)
    print('%s' %len(rawInfos))
    for i in rawInfos:
        rawHrefs=rawHref.search(i)
        rawTitles=rawTitle.search(i)
        rawPics=rawPic.search(i)
       
        inList=[]
        inList.append(rawTitles.group(0).replace('title=','').replace('"',''))
        inList.append(rawPics.group(0).replace('"',''))
        href='http://18.19.ivdmh.com'+rawHrefs.group(0)
        inList.append(href)

        outList.append(inList)

    # 将解析到的视频信息添加到数据库
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='cqmygpython2',db='wechatmovie',charset='utf8')
    cursor=conn.cursor()

    for i in outList:
        try:
            sql_insert="INSERT INTO xiaoheju(name,videourl,picurl) VALUES ('%s','%s','%s');"%(i[0],i[2],i[1])
            cursor.execute(sql_insert)
            conn.commit()
            print('Save to mysql success')
        except:
            conn.rollback()
            print('Save to mysql failed')

    cursor.close()
    conn.close()

def main():
    tabList=[
            'http://18.19.ivdmh.com/lists/5-',
            'http://18.19.ivdmh.com/lists/6-',
            'http://18.19.ivdmh.com/lists/7-',
            'http://18.19.ivdmh.com/lists/8-',
            'http://18.19.ivdmh.com/lists/9-',
            'http://18.19.ivdmh.com/lists/10-',
            'http://18.19.ivdmh.com/lists/19-',
            'http://18.19.ivdmh.com/lists/11-',

            'http://18.19.ivdmh.com/lists/12-',
            'http://18.19.ivdmh.com/lists/13-',
            'http://18.19.ivdmh.com/lists/14-',
            'http://18.19.ivdmh.com/lists/15-',
            'http://18.19.ivdmh.com/lists/18-',

            'http://18.19.ivdmh.com/lists/3-',

            'http://18.19.ivdmh.com/lists/4-',
            ]

    pageList=[
            114,
            88,
            41,
            28,
            59,
            177,
            27,
            10,
            
            106,
            13,
            17,
            23,
            2,
            
            7,
            
            59
            ]
    # test pageList
#    pageList=[2,3,4,2,3,4,2,4]

    iCnt=0
    for i in tabList:
        urls=genUrls(i,pageList[iCnt])
        for url in urls:
            print('Parsing %s.html' % url)
            html_text=getHtml(url)
            parseHtml(html_text)
        print('--------------------------\n\n')
        iCnt+=1

main()

'''
电影
5-1 动作片
6-1 喜剧片
7-1 爱情片
8-1 科幻片
9-1 恐怖片
10-1剧情片
19-1伦理片
11-1战争片

电视剧
12-1国产剧
13-1港台剧
14-1日韩剧
15-1欧美剧
18-1海外剧

综艺
3-1 综艺

动漫
4-1 动漫
'''
