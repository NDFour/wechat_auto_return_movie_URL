### Help
1. `run`程序在后台运行后需要手动输入使程序加载数据库中的一些预配置
2. `showanalyze`查看各公众号调用程序次数
3.
```
insertadarticles
INSERT INTO adarticles
(title,picurl,url,canbeuse,tab)
VALUES ( , , , 1, 1); #tab对应插入到图文中的位置
```
插入已发送的广告图文
4. `updatevideoinfo .*.sql`更新**videoinfo**表*已基本弃用*
5. `showtarget`查看公众号对应的ID，添加和删除公众号时需要
6. `adduser ID`和`deluser ID`分别给公众号添加和删除一个公众号(ID对应**showtarget**获得的id)
7. `outserve ID`和`renewal ID`分别对应公众号**服务到期**和**续费成功**
8. `switch [0-9]`切换返回电影观看链接图文的方式
 - switch 1 : 数据库检索
 - switch 2 : 构造搜索页url
9. `ad[0-9]change [0-1]`选择关闭某条**adarticles**(adarticles开始运行程序后默认打开)
**如：**
 - ad1change 0 : 关闭第1条adarticle
 - ad1change 1 : 开启第1条adarticle
 - ad2change 0 : 关闭第2条adarticle
10. `changebaseurl .*`更改`reply_info_bygenurl`函数中的`baseUrl`以构造新的搜索页url

**教程到此结束，以下是更新日志**

---

### UpdateLog
####  V 5.0.0 (2018年5月15日)
- 增加插入adarticles时可选择插入位置
- 增加可关闭adarticles显示
> ad[0-9]articles [0-1]
(** 0 is disable && 1 is enable **)

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
