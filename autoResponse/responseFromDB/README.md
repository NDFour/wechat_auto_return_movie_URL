### UpdateLog

####  V 4.9.5 (2018年5.6日)
- 增加**adarticles**选项，在插入数据到**adarticles**表中时设置**tab**的值为1时表示为第一条**adarticles**，为2时表示为第二条**adarticles**

####  V 4.9.4 (2018年5.1日)
- 添加新功能 `switch [0-9]`切换`reply_info()`模式，从数据库检索数据或者**genurl**
> 1. 1--reply_info()从数据库检索数据
> 2. 2--reply_info_bygenurl()根据关键词构造搜索页url

####  V 4.9.3 (2018年4.29日)
- 添加新功能 `outserve target_id` ,公众号到期后将会回复引流文章和 `adArticles`
- 添加新功能 `renewal target_id` ,公众号**续费**成功

####  V 4.9.2 (2018年4.27日)

- 更改 `reply_info()`函数的 **236**行`return reply_info(v_name[0:len_v_name])`为`out_list=reply_info(v_name[0:len_v_name])`

  ![](https://t1.picb.cc/uploads/2018/04/27/2OkUxe.png)

  ![](https://t1.picb.cc/uploads/2018/04/27/2Okzks.png)

  - 先前的代码导致直接返回下一层递归的结果，无法执行本层递归的`cursor.close()`和`conn.close()`函数释放资源

#### V 4.9.1 (2018年4月9日)

- 添加关注后回复`adarticles`

#### V 4.9 (2018年4月9日)

- 添加全局变量 `global adtuple[]`，每次响应用户**message**时无需再次访问**adarticle.db**
- 程序开始运行，执行`run()`指令时，`updatename_dic()`函数自动更新 `global adtuple[]`

#### V xxx

YOU HAVE LOST YOUR MIND.

