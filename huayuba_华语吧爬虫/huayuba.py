import re
import pymysql
import requests

def getHtml(url):
    try:
        r=requests.get(url)
        return r.text
    except:
        return ''

def genUrl(baseUrl,pages):
    urlLists=[]
    for i in list(range(1,pages+1)):
        urlLists.append(baseUrl+'-'+str(i)+'.html')
    return urlLists

def parseMenu(html_text):
    # get /videos/23333.html 
    re_url=re.compile(r'/videos/[0-9]*.html')
    # get title="比的腿"
    re_name=re.compile(r'title=".*?"')
    # get original="http://img.xzpifu.com/uploads/allimg/180318/a9ef0d42658ebbec.jpg"
    re_pic=re.compile(r'original=".*?"')

    urllist=[]
    namelist=[]
    piclist=[]

    try:
        urlLists=re_url.findall(html_text)
        namelist=re_name.findall(html_text)
        piclist=re_pic.findall(html_text)
    except:
        print('--> 利用 re 正则表达式库匹配失败')

    urllist_final=[]
    namelist_final=[]
    piclist_final=[]

    for i in namelist:
        namelist_final.append(i.replace('title=','').replace('"',''))
    for j in piclist:
        piclist_final.append(j.replace('original=','').replace('"',''))
    for k in urlLists:
        urllist_final.append('http://wx.hyb222.com'+k.replace('videos','plays').replace('.html','')+'-0-0.html')


    # 链接数据库，准备存储数据到数据库
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='cqmygpython2',db='wechatmovie',charset='utf8')
    cursor=conn.cursor()

    cnt_name=0
    for i in namelist_final:
        sql_insert="INSERT INTO wxhyb222com(name,videourl,picurl) VALUES ('%s','%s','%s');"%(namelist_final[cnt_name],urllist_final[cnt_name],piclist_final[cnt_name])
        cnt_name+=1
        try:
            cursor.execute(sql_insert)
            conn.commit()
            #print('Save success')
        except:
            conn.rollback()
            print('Save failed >> %s'%sql_insert)

    cursor.close()
    conn.close()

def main():
    # 电影标签
    baseUrlLists=[
            'http://wx.hyb222.com/lists/1',
            'http://wx.hyb222.com/lists/2',
            'http://wx.hyb222.com/lists/3',
            'http://wx.hyb222.com/lists/4',
            'http://wx.hyb222.com/lists/31',
            ]
    # 页数标签
    pagesList=[
            713,
            121,
            52,
            125,
            8
            ]
    #pagesList=[713]

    cnt_Pages=0
    for baseUrl in baseUrlLists:
        urlLists=genUrl(baseUrlLists[cnt_Pages],pagesList[cnt_Pages])
        cnt_Pages+=1
        for url in urlLists:
            print('--> Parseing %s' % url)
            # 开始对每一页目录进行解析
            html_text=getHtml(url)
            if html_text:
                parseMenu(html_text)
            else:
                print('--> 获取 %s 网页源码失败' % url)



main()
