#
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-05-16 22:41:51
# Last Modified: 2018-05-16 23:07:11
#

import configparser

config=configparser.ConfigParser()
config.read("config.ini")

# 写入配置文件
try:
    config.add_section('werobot')
    config.set('werobot','ad1_state','1')
    config.set('werobot','ad2_state','1')
    config.set('werobot','reply_info_state','1')
    config.set('werobot','baseUrl','http://m.bjwxzs.com.cn/index.php/home/index/search.html?k=')
except:
    print('load config.ini failed')

config.write(open('config.ini','w'))
