#项目中各文件说明
- requirements.txt:所需第三方库
- manage.py:程序入口文件
- menu.py；用于更新自定义菜单，需单独执行

- /log 该文件夹下存储log文件

- /app
--__init__.py app生成函数
--config.py　配置文件，微信的配置文件在weixin/weixinconfig.py里
--/auth 该文件夹下文件用于管理员发布消息
--/bind 用于新生绑定账号
--/lib 包括一些功能性函数，如数据库功能封装函数
--/weixin 微信主程序
--/nova 有关用户信息的一些函数
--/main 象征性主函数……………………………没什么用
