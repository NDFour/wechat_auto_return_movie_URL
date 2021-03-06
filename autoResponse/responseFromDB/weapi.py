# -*- coding:utf-8 -*-
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-09-27 16:58:49
# Last Modified: 2018-10-02 11:54:03
#

from flask import Flask, jsonify, render_template, url_for
import pymysql
import sys
import codecs
import re
from wxRobot import robot
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
    rel = '/root/wechat_auto_return_movie_URL/autoResponse/responseFromDB/spider/spiderlog/autoSpider_update_sql.txt'
    # rel = '/home/lynn/github_project/Python/wechat_auto_return_movie_URL/autoResponse/responseFromDB/spider/spiderlog/autoSpider_update_sql.txt'
    movies = []
    try:
        f = codecs.open(rel, 'r', 'utf-8')
        for line in f:
            movies.append(line)
        f.close()
    except:
        pass

    '''
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
    '''

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

@app.route('/spiderlog')
def spiderlog():
    # log_list
    log_list = []
    rel =  '/root/wechat_auto_return_movie_URL/autoResponse/responseFromDB/spider/spiderlog/autoSpider_log.txt'
    # rel = '/home/lynn/github_project/daily/pandy/spider/autoSpider_log.txt'
    try:
        f = codecs.open(rel, 'r', 'utf-8')
        for line in f:
            log_list.append(line)
        f.close()
    except:
        log_list.append('The log file doesn^t exsist')

    # log_list_err
    log_list_err = []
    rel =  '/root/wechat_auto_return_movie_URL/autoResponse/responseFromDB/spider/spiderlog/autoSpider_log_error.txt'
    try:
        f = codecs.open(rel, 'r', 'utf-8')
        for line in f:
            log_list_err.append(line)
        f.close()
    except:
        log_list_err.append('The log_err file doesn^t exsist')

    # log_list_update 本次完成更新资源列表
    log_list_update = []
    rel = '/root/wechat_auto_return_movie_URL/autoResponse/responseFromDB/spider/spiderlog/autoSpider_update_log.txt'
    try:
        f = codecs.open(rel, 'r', 'utf-8')
        for line in f:
            log_list_update.append(line)
        f.close()
    except:
        log_list_update.append('The log_list_update doesn^t exsist')

    # log_list_sql 本次完成更新资源 sql语句 列表
    log_list_sql = []
    rel = '/root/wechat_auto_return_movie_URL/autoResponse/responseFromDB/spider/spiderlog/autoSpider_update_sql.txt'
    # rel = '/home/lynn/github_project/Python/wechat_auto_return_movie_URL/autoResponse/responseFromDB/spider/spiderlog/autoSpider_update_sql.txt'
    try:
        f = codecs.open(rel, 'r', 'utf-8')
        for line in f:
            log_list_sql.append(line)
        f.close()
    except:
        log_list_sql.append('The log_list_sql doesn^t exsist')

    context = {}
    context['log_list'] = log_list
    if len(log_list):
        context['start'] = log_list[0]
        context['end'] = log_list[-1]
    else:
        context['start'] = ''
        context['end'] = ''
    context['log_list_err'] = log_list_err
    context['log_list_update'] = log_list_update
    context['log_list_sql'] = log_list_sql

    context['clean_spiderlog'] = url_for('clean_spiderlog')
    return render_template('spiderlog.html', context = context)

@app.route('/clean_spiderlog')
def clean_spiderlog():
    msg = ''
    # 爬虫运行日志
    rel = '/root/wechat_auto_return_movie_URL/autoResponse/responseFromDB/spider/spiderlog/autoSpider_log.txt'
    try:
        with open(rel, 'w') as f:
            f.write('')
            msg += '清空 spiderlog 成功'
    except Exception as e:
        msg += '清空 spiderlog 失败'
    msg += '<br />'

    # 爬虫运行错误日志
    rel = '/root/wechat_auto_return_movie_URL/autoResponse/responseFromDB/spider/spiderlog/autoSpider_log_error.txt'
    try:
        with open(rel, 'w') as f:
            f.write('')
            msg += '  清空 spiderlog_err 成功'
    except Exception as e:
        msg += '  清空 spiderlog_err 失败'
    msg += '<br />'

    # 爬虫更新资源名日志
    rel = '/root/wechat_auto_return_movie_URL/autoResponse/responseFromDB/spider/spiderlog/autoSpider_update_log.txt'
    try:
        with open(rel, 'w') as f:
            f.write('')
            msg += '  清空 spiderlog_update_log 成功'
    except Exception as e:
        msg += '  清空 spiderlog_update_log 失败'
    msg += '<br />'

    # 爬虫更新资源 sql 日志
    rel = '/root/wechat_auto_return_movie_URL/autoResponse/responseFromDB/spider/spiderlog/autoSpider_update_sql.txt'
    # rel = '/home/lynn/github_project/Python/wechat_auto_return_movie_URL/autoResponse/responseFromDB/spider/spiderlog/autoSpider_update_sql.txt'
    try:
        with open(rel, 'w') as f:
            f.write('')
            msg += '  清空 spiderlog_update_sql 成功'
    except Exception as e:
        msg += '  清空 spiderlog_update_sql 失败'
    msg += '<br />'

    return msg


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
