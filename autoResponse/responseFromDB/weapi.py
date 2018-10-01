# -*- coding:utf-8 -*-
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-09-27 16:58:49
# Last Modified: 2018-10-01 22:04:30
#

from flask import Flask, jsonify
import pymysql
import sys
import re
from reply_from_pymysql import robot
from werobot.contrib.flask import make_view

app = Flask(__name__)

# werobot
app.add_url_rule(rule='/robot/',
    endpoint='werobot',
    view_func=make_view(robot),
    methods=['GET','POST'])

@app.route('/')
def index():
    return 'hello'

@app.route('/getmovie')
def hello():
    conn = pymysql.connect('127.0.0.1', port=3306, user='root', password='cqmygpython2', db='bdpan', charset='utf8')
    cursor = conn.cursor()

    sql_select = "SELECT id,v_href,v_pic,v_name,v_views,v_type,v_playurl FROM onlineplay_onlineplay;"
    movies = []

    try:
        cursor.execute(sql_select)
        sql_date = cursor.fetchmany(20)
        for movie in sql_date:
            # print(movie)
            # print()
            # 创建一个 movie 字典插入 movies 数组
            movie_dic = {}
            movie_dic['v_id'] = movie[0]
            movie_dic['v_href'] = movie[1]
            movie_dic['v_pic'] = movie[2]
            movie_dic['v_name'] = movie[3]
            movie_dic['v_views'] = movie[4]
            # v_playurl 为数组
            # 调用函数将 字符串 转换为数组
            movie_dic['v_playurl'] = getList(movie[6])
            # print(movie_dic)
            # print('----------')
            movies.append(movie_dic)
    except:
        print('err')
        print(sys.exc_info())
    finally:
        cursor.close()
        conn.close()

    rel_json = {}
    rel_json['movies'] = movies

    return jsonify(rel_json)

@app.route('/detail/<int:movie_id>')
def getmovieDetail(movie_id):
        conn = pymysql.connect('127.0.0.1', port=3306, user='root', password='cqmygpython2', db='bdpan', charset='utf8')
        cursor = conn.cursor()

        sql_select = "SELECT id,v_href,v_pic,v_name,v_views,v_type,v_playurl FROM onlineplay_onlineplay WHERE id=%d;" % movie_id
        movies = []
        try:
            cursor.execute(sql_select)
            sql_date = cursor.fetchone()
            movie_dic = {}
            movie_dic['v_id'] = sql_date[0]
            movie_dic['v_href'] = sql_date[1]
            movie_dic['v_pic'] = sql_date[2]
            movie_dic['v_name'] = sql_date[3]
            movie_dic['v_views'] = sql_date[4]
            movie_dic['v_playurl'] = sql_date[6]
            # print(movie_dic)
            # print('----------')
            movies.append(movie_dic)

        except:
            pass
        finally:
            cursor.close()
            conn.close()
        rel_json = {}
        rel_json['movies'] = movies
        return jsonify(rel_json)

# 用于将 v_playurl 长字符串转化为数组返回
def getList(str_url):
    # 分割视频播放 url
    playurls = []
    sourceurls = str_url.split('$$')
    for s in sourceurls:
        urls_tmp = s.split('$')
        # 免费解析接口
        urls_tmp2 = []
        for url_tmp in urls_tmp:
            if re.match(r'.*www.mgtv.com.*',url_tmp):
                urls_tmp2.append('https://jiexi.gysc88.cn//mdparse/index.php?id=' + url_tmp)
            elif re.match(r'.*v.qq.com.*',url_tmp):
                urls_tmp2.append('https://api.flvsp.com/?url=' + url_tmp)
            elif re.match(r'.*letv.com.*',url_tmp):
                urls_tmp2.append('https://jiexi.gysc88.cn//mdparse/index.php?id=' + url_tmp)
            elif re.match(r'.*iqiyi.com.*',url_tmp):
                urls_tmp2.append('https://www.1616v.com/1616/?url=' + url_tmp)
            else:
                urls_tmp2.append(url_tmp)
        playurls.append(urls_tmp2)
    playurls.pop()
    return playurls[0]

if __name__ == '__main__':
    app.run()
