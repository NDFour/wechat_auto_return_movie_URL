### UpdateLog

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

