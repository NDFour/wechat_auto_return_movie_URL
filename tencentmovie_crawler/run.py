#
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-03-04 02:37:44
# Last Modified: 2018-03-04 03:08:23
#

import requests
import re
import pymysql

def gethtml(url):
    html_text=''
    try:
        r=requests.get(url)
        r.status_code
        html_text=r.text
    except:
        html_text=''

    return html_text

def parsehtml(html_text):
    # Get the sql cursor
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='cqmygpython2',db='wechatmovie',charset='utf8')
    cursor=conn.cursor()

    # get  r-lazyload="//puui.qpic.cn/vcover_vt_pic/0/esb9yas9hjdbadw1519365163/220" alt="神秘巨星" r-imgerr="v">
    pic_name_re=re.compile(r'r-lazyload=.*>')
    # get https://v.qq.com/x/cover/esb9yas9hjdbadw.html" class="figure
    movie_url_re=re.compile(r'http.*class="figure')
    # get https://v.qq.com/x/cover/esb9yas9hjdbadw.html" class="figure
    url_re=re.compile(r'http.*class="figure')

    pic_name_raw_list=pic_name_re.findall(html_text)
    # get //puui.qpic.cn/vcover_vt_pic/0/esb9yas9hjdbadw1519365163/220"
    pic_raw_re=re.compile(r'//.*?"')
    # get alt="神秘巨星"
    name_raw_re=re.compile(r'alt=".*?"')

    pic_list=[]
    name_list=[]

    for i in pic_name_raw_list:
        pic='http:'+pic_raw_re.search(i).group().replace('"','')
        name=name_raw_re.search(i).group().replace('alt=','').replace('"','')

        pic_list.append(pic)
        name_list.append(name)

    url_list=[]

    url_list_re=url_re.findall(html_text)
    for i in url_list_re:
        url=i.replace('" class="figure','')
        url_list.append(url)

    i_cnt=0
    for i in name_list:
        sql_insert='INSERT INTO tencentmovie(name,url,picurl) VALUES("%s","%s","%s")' % (i,url_list[i_cnt],pic_list[i_cnt])

        try:
            cursor.execute(sql_insert)
            conn.commit()
        except:
            conn.rollback()

        i_cnt+=1

    cursor.close()
    conn.close()



def main():
    print('--> Start running')
    base_url='https://v.qq.com/x/list/movie?&offset='
    for i in range(0,167):
        index=i*30
        url=base_url+str(index)
        print('--> %s'%url)
        html_text=gethtml(url)
        parsehtml(html_text)

main()
