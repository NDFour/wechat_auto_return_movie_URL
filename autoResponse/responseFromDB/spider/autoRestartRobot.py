import os

os.system('supervisorctl stop weapi')
print('stop weapi')

os.system('rm /root/wechat_auto_return_movie_URL/autoResponse/responseFromDB/werobot_session.sqlite3')
print('rm sqlite3')

os.system('supervisorctl start weapi')
print('start weapi')
