# -*- coding: utf-8 -*-

import requests
import re
import pymysql
import os 
import time 
import datetime


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

    # 将电影信息写入数据库
    db=pymysql.connect(host='localhost',user='root',password='cqmygpython2',db='wechatmovie',port=3306,charset='utf8')
    cur=db.cursor()

    for i in video_list:
        try:
            sql_insert="insert into videoinfo (name,videourl,picurl) values('%s','%s','%s')"%(i[0],i[1],i[2])
#            print(sql_insert)
            cur.execute(sql_insert)
            db.commit()
            print('-> SAVE info of %s to MySQL success !!'%i[0])
        except:
            db.rollback()
            print('-> SAVE info of %s to MySQL failed !!'%i[0])

    cur.close()
    db.close()

def get_mac_url(html_text):
    mac_url_re=re.compile(r'mac_url.*;')
    if len(mac_url=mac_url_re.findall(html_text)):
        # 得到 m3u8 的 vid_id
        mac_url=mac_url[-1].replace('

def set_videoinfo_empty():
    bak_sql_dir=os.path.abspath('..')+'/mysql_python/empty_videoinfo_bak.sql'
    sql_source=('mysql -uroot -pcqmygpython2 wechatmovie < %s'%bak_sql_dir)

    try:
        os.system(sql_source)
        return '清空videoinfo表信息success'
    except:
        return '清空videoinfo表信息failed'
    time.sleep(5)

def main():
    dy_pages=int(input('-> HOW MANY PAGES OF THE TAG [MOVIE] ?\n'))
    '''
    dsj_pages=int(input('-> HOW MANY PAGES OF THE TAG [DIAN SHI JU] ?\n'))
    zy_pages=int(input('-> HOW MANY PAGES OF THE TAG [ZONG YI] ?\n'))
    dm_pages=int(input('-> HOW MANY PAGES OF THE TAG [DONG MAN] ?\n'))
    '''


# base_url 用于构建各标签页url
    dy_base_url='http://m.gooddianying.net/assort/1-'
    '''
    dsj_base_url='http://m.gooddianying.net/assort/2-'
    zy_base_url='http://m.gooddianying.net/assort/3-'
    dm_base_url='http://m.gooddianying.net/assort/4-'
    '''

# **_url gen_url函数返回的各标签下每一页的url列表
    dy_url=gen_dy_url(dy_base_url,dy_pages)
    '''
    dsj_url=gen_dsj_url(dsj_base_url,dsj_pages)
    zy_url=gen_zy_url(zy_base_url,zy_pages)
    dm_url=gen_dm_url(dm_base_url,dm_pages)
    '''

    set_videoinfo_empty()

# 对每个标签的url列表中的url进行解析，得到相关视频信息
    for i in dy_url:
        html_text=get_html(i)
        print('-> PARSING [MOVIE] INFO IN THE : %s ...' % i)
        if len(html_text) == 0:
            continue
        parse_web_save2mysql(html_text)

'''
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
'''

    print('\n\n----------------------------------\n')
    timestamp=str(datetime.now())[:19].replace(' ','.')
    mysqldump='mysqldump -uroot -pcqmygpython2 wechatmovie videoinfo > %s.sql;'%timestamp
    try:
        os.system(mysqldump)
        print('备份数据表到 %s.sql 成功'%timestamp)
    except:
        print('备份数据表到 %s.sql 失败'%timestamp)

main()
