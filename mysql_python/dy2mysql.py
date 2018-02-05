# -*- coding: utf-8 -*-

import requests
import re
import MySQLdb



# 生成待爬取的电影列表url,传入pages参数，代表共有多少页，以便生成url
def gen_dy_url(base_url,pages):
    urls=[]
    for i in range(1,pages+1):
        print('-> Generating page %s url of [MOVIE]'%i) 
        urls.append(base_url+str(i)+'.html')
    print('-> Generate url in the tag [MOVIE] complete')
    return urls
	

# 生成待爬取的电视剧列表url
def gen_dsj_url(base_url,pages):
    urls=[]
    for i in range(1,pages+1):
        print('-> Generating page %s url of [DIAN SHI JU]' % i ) 
        urls.append(base_url+str(i)+'.html')
    print('-> Generate url in the tag [DIAN SHI JU] complete')
    return urls
	
# 生成待爬取的综艺列表url
def gen_zy_url(base_url,pages):
    urls=[]
    for i in range(1,pages+1):
        print('-> Generating page %s url of [ZONG YI]'%i) 
        urls.append(base_url+str(i)+'.html')
    print('-> Generate url in the tag [ZONG YI] complete')
    return urls
	

# 生成待爬取的动漫列表url
def gen_dm_url(base_url,pages):
    urls=[]
    for i in range(1,pages+1):
        print('-> Generating page %s url of [DONG MAN]'%i) 
        urls.append(base_url+str(i)+'.html')
    print('-> Generate url in the tag [DONG MAN] complete')
    return urls
	

def get_html(url):
    print('-> Getting the sourcecode of %s ...' % url)

#'''    headers={
 #           'Host':'m.gooddianying.net',
  #          'Referer':'http://m.gooddianying.net/assort/2-3.html',
   #         'Upgrade-Insecure-Requests':1,
    ##       }'''

    try:
        r=requests.get(url,timeout=10)
        html_text=r.text
        print('-> get_html() SUCCESS !!')
    except:
        print('-> get_html() TIMEOUT !!')
        html_text=''
    return html_text


def parse_web_save2mysql(html_text):
    # 得到的是 /movie/33333.html
    re_url=re.compile(r'/movie/[0-9]*.html')
    # 得到title="芳华"
    re_url_title=re.compile(r'alt=".*?"')
    # 得到 http://images.odoukei.com/upload/vod/2017-06-30/201706301498810965.jpg
    re_url_picurl=re.compile(r'http://images.*?.jpg')

    # 返回一个list，list内是包含每条电影信息的List
    video_list=[]

    # 用正则表达式获取电影信息
    after_re_url=re_url.findall(html_text)
    after_re_url_title=re_url_title.findall(html_text)
    after_re_url_picurl=re_url_picurl.findall(html_text)

    cnt=0

    for i in after_re_url_title:
        in_list=[]
        cnt+=1
        try:
		# 插入电影名
            in_list.append(i.replace('alt="','').replace('"',''))
		# 插入图片url
            in_list.append(after_re_url_picurl[cnt-1])
		# 插入视频播放url
            in_list.append((('http://m.gooddianying.net'+after_re_url[cnt-1]).replace('.html','-1-1.html')).replace('movie','play'))
            video_list.append(in_list)
        except:
            print('-> Parsing info of %s failed !!'%i)

    #print(video_list)
    print('-> PARSING INFO SECCESS !!')
    print()

    # SAVE INFO TO MYSQL
    print('-> SAVA info to mysql...')

    conn=MySQLdb.Connection(host='127.0.0.1',port=3306,user='root',passwd='cqmygpython2',db='wechatmovie',charset='utf8')
    cursor=conn.cursor()

    for i in video_list:
        try:
            sql_insert="insert into videoinfo (name,videourl,picurl) values('%s','%s','%s')"%(i[0],i[1],i[2])
            print(sql_insert)
            cursor.execute(sql_insert)
            conn.commit()
            print('-> SAVE info of %s to MySQL success !!'%i[0])
        except:
            conn.rollback()
            print('-> SAVE info of %s to MySQL failed !!'%i[0])

    cursor.close()
    conn.close()


def main():
    dy_pages=int(input('-> HOW MANY PAGES OF THE TAG [MOVIE] ?\n'))
    dsj_pages=int(input('-> HOW MANY PAGES OF THE TAG [DIAN SHI JU] ?\n'))
    zy_pages=int(input('-> HOW MANY PAGES OF THE TAG [ZONG YI] ?\n'))
    dm_pages=int(input('-> HOW MANY PAGES OF THE TAG [DONG MAN] ?\n'))

# base_url 用于构建各标签页url
    dy_base_url='http://m.gooddianying.net/assort/1-'
    dsj_base_url='http://m.gooddianying.net/assort/2-'
    zy_base_url='http://m.gooddianying.net/assort/3-'
    dm_base_url='http://m.gooddianying.net/assort/4-'

# **_url gen_url函数返回的各标签下每一页的url列表
    dy_url=gen_dy_url(dy_base_url,dy_pages)
    dsj_url=gen_dsj_url(dsj_base_url,dsj_pages)
    zy_url=gen_zy_url(zy_base_url,zy_pages)
    dm_url=gen_dm_url(dm_base_url,dm_pages)

# 对每个标签的url列表中的url进行解析，得到相关视频信息
    for i in dy_url:
        html_text=get_html(i)
        print('-> PARSING [MOVIE] INFO IN THE : %s ...' % i)
        if len(html_text) == 0:
            continue
        parse_web_save2mysql(html_text)

    for i in dsj_url:
        html_text=get_html(i)
        print('-> PARSING [DIAN SHI JU] INFO IN THE %s ...' % i)
        if len(html_text) == 0:
            continue
        parse_web_save2mysql(html_text)

    for i in zy_url:
        html_text=get_html(i)
        print('-> PARSING [ZONG YI] INFO IN THE %s ...' % i)
        if len(html_text) == 0:
            continue
        parse_web_save2mysql(html_text)

    for i in dm_url:
        html_text=get_html(i)
        print('-> PARSING [DONG MAN] INFO IN THE %s ...' % i)
        if len(html_text) == 0:
            continue
        parse_web_save2mysql(html_text)

main()
