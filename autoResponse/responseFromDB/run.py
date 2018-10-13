from werobot import WeRoBot

robot=WeRoBot(token='wx123')
robot.config['SESSION_STORAGE']=False

@robot.handler
def hello(message):
    # return 'hello world'
    return '腾讯封杀免费看电影公众号！！\n  请先点击以下链接观看电影：\n    <a href="http://tnt1024.com/onlineplay/pages/1/">点我观看电影</a>'
    '''
    rel=['hello','des','https://pic3.zhimg.com/80/v2-6f8a2d526ec2943ecae677f9c3db4fc2_hd.jpg','https://baidu.com']
    a=[]
    a.append(rel)
    return a
    '''

robot.config['HOST']='0.0.0.0'
robot.config['PORT']=80
robot.run()
