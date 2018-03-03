#
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-03-02 01:14:34
# Last Modified: 2018-03-02 16:44:00
#

import requests
import re
import pymysql

def gethtml(url,if_ua):
    headers={'Host':'list.iqiyi.com',
            'Referer':'http://list.iqiyi.com/www/1/-------------11-201-1-iqiyi--.html',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    try:
        # 判断是否需要添加 headers
        if if_ua:
            r=requests.get(url,headers=headers,timeout=10)
        else:
            r=requests.get(url,timeout=20)
        r.status_code
        r.encoding="utf-8"
    except:
        print('--> [gethtml] GetHtml failed: %s' %url)
        return ''
    print('--> [gethtml] GetHtml success: %s' % url)
    return r.text

def parseinfo(html_text):
    # Get the sql cursor
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='cqmygpython2',db='wechatmovie',charset='utf8')
    cursor=conn.cursor()

    # get bigTitle" title="神秘巨星"  href="http://www.iqiyi.com/v_19rre31w14.html#vfrm=2-4-0-1"                                              target="_blank"
    title_and_href_re=re.compile(r'bigTitle.*"')

    # get title="神秘巨星"
    title_re_raw=re.compile(r'title=".*?"')

    # get href="http://www.iqiyi.com/v_19rre31w14.html#vfrm=2-4-0-1"
    href_re_raw=re.compile(r'href=".*?"')

    # get pic8.qiyipic.com/image/20180226/1b/05/v_113729778_m_601_m4_180_236.jpg
    pic_url_re=re.compile(r'pic[0-9].qiyipic.com/image.*.jpg')

    pic_list=[]
    title_list=[]
    href_list=[]
    intro_list=[]

    pic_list_tmp=pic_url_re.findall(html_text)

    # get pic_list
    for p in pic_list_tmp:
        pic_list.append('http://'+p)

    # get title_and_href_list
    title_and_href=title_and_href_re.findall(html_text)
    for i in title_and_href:
        # get title 
        title_tmp=title_re_raw.search(i)
        if title_tmp:
            title_t=title_tmp.group().replace('title="','').replace('"','')
            title_list.append(title_t)
        else:
            print('--> [parseinfo] 无效 title\n')
            title_t='无效数据'
            title_list.append(title_t)

        # get href 
        href_tmp=href_re_raw.search(i)
        if href_tmp:
            href_list.append(href_tmp.group().replace('href="','').replace('"',''))
        else:
            print('--> [parseinfo] 无效 href\n')
            href_list.append('无效href')


    # get intro 
    for i in href_list:
        intro_list.append(getintro(i))

    # 打印获得的结果
    i_cnt=0
    for i in title_list:
        sql_insert='INSERT INTO 7cdyjiexi(name,href,picurl,intro) VALUES("%s","%s","%s","%s")' % (title_list[i_cnt],href_list[i_cnt],pic_list[i_cnt],intro_list[i_cnt])

        try:
            cursor.execute(sql_insert)
            conn.commit()
        except:
            conn.rollback()

        i_cnt+=1

    cursor.close()
    conn.close()

'''
    print(title_list)
    print(len(title_list))
    print()
    print(href_list)
    print(len(href_list))
    print()
    print(pic_list)
    print(len(pic_list))
    print(intro_list)
    print(len(intro_list))
'''

def getintro(url):
    print('--> [getintro] Getting intro of %s' % url)
    intro_re=re.compile(r'name="description" content=.*"')
    html_text=gethtml(url,0)
    intro_list_tmp=intro_re.search(html_text)
    if intro_list_tmp:
        intro=intro_list_tmp.group().replace('name="description" content="','').replace('"','')
        print('--> Get intro success\n')
        return intro 
    else:
        print('--> Get intro failed\n')
        return '暂无简介'

def main():
#    url='http://list.iqiyi.com/www/1/-------------11-1-1-iqiyi--.html'
    print('--> Crwaler startting...\n')
    base_url1='http://list.iqiyi.com/www/1/-------------11-'
    base_url2='-1-iqiyi--.html'
    for i in range(1,31):
        url=base_url1+str(i)+base_url2
        html_text=gethtml(url,1)
        print('-->[main] Parseing url of %s' % url)
        parseinfo(html_text)

main()
