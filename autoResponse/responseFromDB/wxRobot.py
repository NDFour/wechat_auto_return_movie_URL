# -*- coding: utf-8 -*-

from werobot import WeRoBot
import re
import configparser


# 默认启用 Session
robot = WeRoBot(token='wx123')

# 判断回复用户的方式 （在线 or 网盘）
reply_info_state = 1

# 在线播放
baseUrl1 = 'http://tnt1024.com/movie/search/?movie_name='
# 百度网盘链接
baseUrl2 = 'http://tnt1024.com/movie/search/?movie_name='
# 小说URL
novelUrl1 = ''


@robot.subscribe
def subscribe(message):
    outlist=[]
    outlist.append(['公众号免费看电影教程','','https://s1.ax1x.com/2018/06/02/CogADx.png','https://w.url.cn/s/AGW9n4L'])

    return outlist


@robot.text
def hello(message, session):
    # lynn 微信号的 source ID
    master_root = 'o2NddxHhZloQV55azmx8zVXv9mAQ'
    # master_root = 'oBo_Y1akWzT_4_i38mzpiRo7z-uo'

    # 返回公众号 target ID
    if message.content=='showtarget':
        return message.target

    # 读取配置文件
    loadConfigMsg = loadConfig()

    # 用户消息纯数字，由掌上大学接管自动回复
    try:
    	int(message.content)
    	return ''
    except:
    	pass

    # 公众号相关接口
    if message.source == master_root:
        msg = toolsforAdmin(message.content)
        if len(msg) > 0:
            return msg

    # print the name of the movie and source
    print('《%s》 from [%s]' %(message.content, message.source))

    if (len(message.content) > 30):
    	return '电影名长度过长，请精简后重新发送。'

    v_name = modefy_name(message.content)

    global reply_info_state
    articles = []
    if reply_info_state == 1:
    	articles = reply_info_bygenurl(v_name)
    elif reply_info_state == 2:
    	articles = reply_info_bygenurl(v_name)

    # 如果当天第一次使用,重定向到小说
    if 'first' not in session:
        articles = redirettoNovel(articles)

    # List to String
    rel_str = genHtml(articles)

    # 如果当天第一次使用,重定向到小说
    if 'first' not in session:
        rel_str += '\n\n★ 如果点击上方无法跳转到影片搜索页，请尝试重新发送片名'
        session['first'] = True

    return rel_str


# List to String
def genHtml(articles):
    rel_str=''
    ar_str_cnt=0
    for ar in articles:
        ar_str_cnt += 1
        rel_str+='['+str(ar_str_cnt)+']  '+'<a href="'+ar[-1]+'">'+ar[0]+'</a>'+'\n\n\n'

    return rel_str.strip()


# Is first to use  -- Redirect to wx novels
def redirettoNovel(articles):
    config=configparser.ConfigParser()
    config.read("config.ini")

    articles[0][3] = config.get('werobot','novelUrl1')
    return articles


# 替换用户发来的电影名字中的错别字
def modefy_name(v_name):
    # 先把电影名字中的特殊符号去除
    v_name=v_name.replace('《','')
    v_name=v_name.replace('》','')
    v_name=v_name.replace('。','')

    return v_name


# 构造查询 url 返回给用户
def reply_info_bygenurl(v_name):
    out_list=[]
    global baseUrl1
    url = baseUrl1 + v_name + '&onlineplay_search=onlineplay_search'
    name='《'+v_name+'》点我在线观看'
    picurl='https://s1.ax1x.com/2018/08/11/P6L2sU.jpg'

    in_list=[]
    in_list.append(name)
    in_list.append(name)
    in_list.append(picurl)
    in_list.append(url)

    out_list.append(in_list)

    return out_list


# 公众号相关接口
def toolsforAdmin(content):
    # Switch reply method
    if re.match(r'switch [0-9]', content):
        reply_info_state = int(content[7])
        msg = writeToConfigFile('reply_info_state', str(reply_info_state))
        return msg

    # Change baseUrl1
    elif re.match(r'changebaseurl1 .*', content):
        global baseUrl1
        baseUrl1 = content[15:]
        msg = writeToConfigFile('baseUrl1', baseUrl1)
        return msg + '\n更改 baseUrl1 成功!'

    # Change baseUrl2
    elif re.match(r'changebaseurl2 .*', content):
        global baseUrl2
        baseUrl2 = content[15:]
        msg = writeToConfigFile('baseUrl2', baseUrl2)
        return msg + '\n更改 baseUrl2 成功!'

    # Change novelUrl1
    elif re.match(r'changenovelurl1 .*', content):
        global novelUrl1
        novelUrl1 = content[16:]
        msg = writeToConfigFile('novelUrl1', novelUrl1)
        return msg + '\n更改 novelUrl1 成功!'

    # Return content of config.ini
    elif content == 'showConfig':
    	msg = showConfig()
    	return msg

    else:
        return ''


# Read config from config.ini
def loadConfig():
    global reply_info_state
    global baseUrl1
    global baseUrl2
    global novelUrl1

    config=configparser.ConfigParser()
    config.read("config.ini")

    # 各位置adarticles状态开关
    try:
        reply_info_state = config.getint('werobot','reply_info_state')
        baseUrl1 = config.get('werobot','baseUrl1')
        baseUrl2 = config.get('werobot','baseUrl2')
        novelUrl1 = config.get('werobot','novelUrl1')
    except:
        return 'config.ini配置文件加载失败'

    return 'config.ini配置文件加载完毕'


# 接受两个参数 ： 配置项名称、配置项的值
def writeToConfigFile(configName,configValue):
    config=configparser.ConfigParser()
    config.read('config.ini')
    try:
        config.set('werobot',configName,configValue)
        config.write(open('config.ini','w'))
    except:
        return '写入 %s 到配置文件 config.ini 时失败' % configName
    return '写入 %s 到配置文件 config.ini 成功' % configName


# Return content of config.ini
def showConfig():
    global reply_info_state
    global baseUrl1
    global baseUrl2
    global novelUrl1

    msg = 'config.ini:\n'
    msg += '\nreply_info_state:' + str(reply_info_state)

    msg += '\n\nbaseUrl1:' + baseUrl1
    msg += '\nbaseUrl2:' + baseUrl2

    msg += '\n\nnovelUrl1:' + novelUrl1

    return msg



# 让服务器监听在 0.0.0.0:80
# robot.config['HOST']='0.0.0.0'
# robot.config['PORT']=80
# robot.run()
