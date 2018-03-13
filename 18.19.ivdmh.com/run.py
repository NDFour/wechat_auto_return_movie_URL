#
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-03-13 17:14:51
# Last Modified: 2018-03-13 18:20:49
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
    conn=MySQLdb.Connection(host='127.0.0.1',port=3306,user='root',passwd='cqmygpython2',db='wechatmovie',charset='utf8')
    cursor=conn.cursor()

    for i in outList:
        try:
            sql_insert="INSERT INTO xiaoheju (name,videourl,picurl) VALUES ('%s','%s','%s');"%(i[0],i[1],i[2])
            cursor.execute(sql_insert)
            print('Save to mysql success')
        except:
            conn.rollback()
            print('Save to mysql failed')

    cursor.close()
    conn.close()

def main():
    tabList=['http://18.19.ivdmh.com/lists/5-','http://18.19.ivdmh.com/lists/6-','http://18.19.ivdmh.com/lists/7-','http://18.19.ivdmh.com/lists/8-','http://18.19.ivdmh.com/lists/9-','http://18.19.ivdmh.com/lists/10-','http://18.19.ivdmh.com/lists/19-','http://18.19.ivdmh.com/lists/11-']

    pageList=[113,87,41,28,58,174,24,9]
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
