#!/usr/bin/python# -*- coding:utf8 -*-# =============== 欢 迎 语 ================ ## 欢迎消息 , 在 handle_group_increase 中 添加HelpMenu['菜单']字符串WelcomeMsg = """欢迎[CQ:at,qq={}]加入本群，如有问题, 请发 公告 命令阅读提问要求后描述清楚问题,你可以发送以下命令获取帮助："""# ================ 关 键 字================ ## 帮助菜单HelpMenu = {    '菜单': """[CQ:at,qq={}]公告          |  社区文档          |  教程 样式          |  例子pip换源      |  查找eric6         |  pycharmtools         |  5.11pyinstaller | """,    '公告': """[CQ:at,qq={}]1.请仔细阅读 群公告里的[ 入群须知 ]及其余公告 ;2.可以发送 菜单 来获取帮助菜单选项 ;3.复杂问题不好用语言描述, 请到群文件下载动画录制工具 ;3.注意 请百度问题或查看帮助文档(看不来帮助文档请到5.ii的4-5-6节看视频) ,百度不到后 描述清楚问题, 禁止长篇黏贴, 长代码请黏贴到 https://paste.ubuntu.com/;4.(PY)QT文档的帮助文档如下：http://doc.qt.io/qt-5/classes.htmlhttp://www.kuqin.com/qtdocument/index.html5.一些经典的例子可以到 https://github.com/892768447/PyQt 去浏览 ;6.如果你刚入门 , 有以下教程可以参考:i.免费视频教程(麦子学院，Pyqt4+py2.7)：http://www.maiziedu.com/course/577-8221/(如果说需要报班, 需要在每讲的视频地址前加m.前缀,如: m.maiziedu.com/course/577-8221/)ii.录制的一些视频:https://space.bilibili.com/1863103/#/iii.传智python系统教程http://j.mp/2OlSYHe""",    '社区': """[CQ:at,qq={}]欢迎加入 https://pyqt5.com一些经典的例子可以到 https://github.com/PyQt5/PyQt 去浏览 ;""",    '文档': """[CQ:at,qq={}](PY)QT文档的帮助文档如下：1.pyside2:https://doc-snapshots.qt.io/qtforpython/2.C++ QThttp://doc.qt.io/qt-5/classes.html3.C++ QT中文老版本http://www.kuqin.com/qtdocument/index.html4.pyqt 使用qt本地帮助文档https://blog.csdn.net/qq842977873/article/details/829510615.如何把C++ QT的代码  转为python PYQT代码https://space.bilibili.com/1863103/#/""",    '文档4.': """[CQ:at,qq={}]pyqt 使用qt本地帮助文档https://blog.csdn.net/qq842977873/article/details/82951061""",    '教程': """[CQ:at,qq={}]5.如果你刚入门 , 建议打好基础 , 简单api自查文档 , 有以下教程可以参考:i.免费视频教程(麦子学院，Pyqt4+py2.7)：http://www.maiziedu.com/course/577-8221/(如果说需要报班, 需要在每讲的视频地址前加m.前缀,如: m.maiziedu.com/course/577-8221/)ii.录制的一些视频:https://space.bilibili.com/1863103/iii.传智python系统教程http://j.mp/2OlSYHe""",    '样式': """[CQ:at,qq={}]1.语法：https://www.cnblogs.com/wangqiguo/p/4960776.html2.官方案例：http://doc.qt.io/qt-5/stylesheet-examples.html3.Qt样式表参考：http://doc.qt.io/qt-5/stylesheet-reference.html4.图标字体：webdings 或者 fontawesome-webfont    http://www.cnblogs.com/luke0011/p/9056515.html    4.1对照码：    http://www.bootcss.com/p/font-awesome/design.html5.阿里云字体图标:http://iconfont.cn/6.https://github.com/892768447/PyQt""",    'pyinstaller': """[CQ:at,qq={}]1.如果安装anaconda, 请别用这个环境的python;2.设置pyqt5的环境变量;3.如果在pycharm中把文件夹设置为了根路径 , 请在终端(cmd)中 运行脚本来确认 模块导入无错误;4.-> 如果需要打包成单文件 , 先别用-w 命令, 最后打包无错误后再加上-w;-------------------------------------------------------错误处理: 4. module PyQt5.sip not found: 确保在cmd下可以导入这个模块后,再在程序中手动导入这个模块;5. Failed to load platform plugin “windows”...:-- 5.1 百度有解决方法 , 拷贝 python目录下的\\PyQt5\\Qt\\plugins\\platforms到exe目录;-- 5.2 还是失败的话检查 电脑用户名是否是中文, 如果是中文:----- 5.2.1 @mt 对那个路径名进行编码;----- 5.2.2 @上海-开发-韩 则改变spec中 exe= EXE(.....)里的runtime_tmpdir指定为英文路径;6.QPixmap处理/样式 问题 都是同5.一样都是dll丢失 , 到目录下找对应的文件件拷贝到exe目录;7.--add-data 打包非python模块文件 , 可能出现的问题及办法:    https://github.com/pyinstaller/pyinstaller/issues/3749;""",    'pyi4.': """[CQ:at,qq={}] 4.-> 如果需要打包成单文件 , 先别用-w 命令, 最后打包无错误后再加上-w;""",    'pycharm': """[CQ:at,qq={}]Pycharm 的pyqt5环境配置1. https://blog.csdn.net/px41834/article/details/793839852. pycharm调试pyqt 没有错误信息提示 原因 :https://www.jianshu.com/p/47b6e7ce46393. pycharm不识别pyqt5模块:    3.1 你新建的项目使用了新建的虚拟环境的python.exe解释器，更换已经安装过pyqt5的解释器再更新索引即可.        设置python解释器路径在pycharm的菜单File->Settings->Project:->Project Interpreter.        ————不要问我什么是虚拟环境；    3.2 在尝试网上搜索的办法都没解决的情况下 ,一般就是pycharm的配置出问题了 ,        找到C:\\Users\\XXX\\.PyCharm2018.1 路径, 删除之后重启pycharm ,重新配置.""",    'pycharm2.': """[CQ:at,qq={}]2. pycharm调试pyqt 没有错误信息提示 原因 :https://www.jianshu.com/p/47b6e7ce4639""",    'eric6': """[CQ:at,qq={}] 请参考 第一讲https://space.bilibili.com/1863103/#/""",    'tools': """[CQ:at,qq={}] 如果pip无法安装 pyqt5-tools:1.如果安装的是python3.7请更换python3.6以下版本;2.windows尝试 pip install pyqt5designer ;""",    '5.11': '[CQ:at,qq={}] 32位python 的 pyqt5.11版本没有qwebEngine模块 , 换成5.10.1或者64位Python',    '查找': """[CQ:at,qq={}]注意指令之后带空格1.百度 关键字 —— 返回百度搜索链接;2.谷歌 关键字 —— 返回谷歌搜索链接;3.-f 控件类名 —— 返回QT官方文档(如果类名错误则地址错误,自行点击左侧All Qt C++ Classes 后, 在浏览器中按ctrl+F查找);4.-g 关键字 —— 返回github搜索;5.-s 关键字 —— 返回StackOverflow搜索;""",    '例子': """[CQ:at,qq={}]在群文件的例子文件夹中已经有2. 3.压缩包, 自行下载;## 1. 和2. 是qt官方自带的例子, 1.是C++版本，对例子简略介绍, 2.是python版本1. http://doc.qt.io/qt-5/qtexamples.html2. https://github.com/baoboa/pyqt5/tree/master/examples 运行examples\qtdemo\qtdemo.py##3. https://github.com/cxinping/PyQt5 看.doc的目录4 .https://github.com/892768447/PyQt5. https://github.com/mfitzp/15-minute-apps""",    'pip': """[CQ:at,qq={}]pip默认使用的源速度比较慢, 通过以下命令来换源:pip install pqipqi lspqi use aliyun""",}