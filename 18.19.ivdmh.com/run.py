# -*- coding:utf-8 -*-
#
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-03-13 17:14:51
# Last Modified: 2018-06-14 00:52:18
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
    rawHref=re.compile(r'/videos/.*.html')
    # 得到 title="巴霍巴利王(下)：终结"
    rawTitle=re.compile(r'title=".*?"')
    # 得到 data-original="http://img.xzpifu.com/uploads/allimg/170618/a06ad9f89c6a1e24.jpg"
    rawPic=re.compile(r'data-original=".*?"')

    outList=[]
    rawHrefs=rawHref.findall(html_text)
    rawTitles=rawTitle.findall(html_text)
    rawPics=rawPic.findall(html_text)

    for i in range(len(rawHrefs)):
        inList=[]
        inList.append(rawTitles[i].replace('title=','').replace('"',''))
        inList.append("http://wx.261shiping.com/"+rawHrefs[i].replace('videos','plays').replace('.html','-0-0.html'))
        inList.append(rawPics[i].replace('data-original=','').replace('"',''))
        outList.append(inList)


    # 将解析到的视频信息添加到数据库
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='cqmygpython2',db='wechatmovie',charset='utf8')
    cursor=conn.cursor()

    for i in outList:
        try:
            sql_insert="INSERT INTO weixunmi(name,videourl,picurl) VALUES ('%s','%s','%s');"%(i[0],i[2],i[1])
            cursor.execute(sql_insert)
            conn.commit()
            print('SUCCESS [%s]' %i[0])
        except:
            conn.rollback()
            print('FAILED [%s]' %i[0])

    cursor.close()
    conn.close()

def main():
    tabList=[
            'http://wx.261shiping.com/lists/5-',
            'http://wx.261shiping.com/lists/6-',
            'http://wx.261shiping.com/lists/7-',
            'http://wx.261shiping.com/lists/8-',
            'http://wx.261shiping.com/lists/9-',
            'http://wx.261shiping.com/lists/10-',
            'http://wx.261shiping.com/lists/11-',
            'http://wx.261shiping.com/lists/12-',
            'http://wx.261shiping.com/lists/29-',
            'http://wx.261shiping.com/lists/30-',
            'http://wx.261shiping.com/lists/28-',

            'http://wx.261shiping.com/lists/13-',
            'http://wx.261shiping.com/lists/14-',
            'http://wx.261shiping.com/lists/15-',
            'http://wx.261shiping.com/lists/16-',

            'http://wx.261shiping.com/lists/3-',

            'http://wx.261shiping.com/lists/4-',

            'http://wx.261shiping.com/lists/32-',
            'http://wx.261shiping.com/lists/34-'
           ]

    pageList=[
            102,
            64,
            42,
            57,
            189,
            90,
            30,
            39,
            67,
            1,
            43,

            55,
            15,
            15,
            40,

            52,

            127,

            7,
            1
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

