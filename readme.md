# WeChat Discover
总体而言，这是一个**面向扩展**的分析与展示微信历史数据的框架。举个例子，通过这个框架，使用20行左右的代码，便可以为我的名为“雪城研究生新生群”生成一个下面的微信群词云：

![新生群词云.jpg](https://raw.githubusercontent.com/ZzzGin/WeChatDiscover/master/img/example1.png)

**普通用户**可以通过易于理解的Python调用，自定义一个“流水线(Pipeline)”来使用预先备好的“分析组件(Analysis)”来分析并展示需要的信息。

**开发者用户**也可以自定义分析组件，来实现自己的想要分析逻辑与展示效果。

目前本框架适用于iOS微信数据，安卓版本支持正在研究中。

本项目是基于个人兴趣的开源项目，采用MIT协议。

## Contents:
1. [Todos](#todos-pr-is-welcomed)
2. [Requirements](#requirements)
3. [A Perspective of This Project](#a-perspective-of-this-project)
4. [How to Use(iOS)](#how-to-useios)
---

## Todos (PR is Welcomed):
1. [DbManager] 对于安卓数据的支持
2. [Analysis] 一个将聊天记录转变为易于阅读的HTML文件的分析组件
3. [Analysis] 针对好友（而非群）聊天纪录的分析组件
4. [Analysis] 其他可能的、有趣的、有预先准备必要的分析组件
5. [GUI] 一个基于QT的GUI
---

## Requirements:
框架**本身**基于Python 3.5开发，不需要第三方模块。其他版本的Python并未测试，但是基于记忆，没有使用过Python3以后新版本的特性，理应无痛使用，未来会有所测试。Python2恕不再测试。

但，由于本框架预先提供了一些有趣的分析组件，这些组件会需要第三方模块，可参阅项目文件: requirements.txt。当然，也可通过：
``` bash
pip install -r requirements.txt
```
直接安装所需模块。

> 获得手机中的微信后台数据文件可能需要其他第三方程序，参阅[How to Use(iOS)](#how-to-useios)以获得详细内容。

> 致开发者：如果您想要PR，且您PR中包含了使用新第三方模块的内容，你可以通过：`pip freeze > requirements.txt` 将你的第三方库信息放到相应文件中。
---

## A Perspective of This Project:
本项目源代码位于Git根文件目录中的`src`文件夹中。以branch v0.5为例介绍项目文件。
```
./src                           --------------- 源文件目录
│   Clocked_Deco.py             --------------- 记录单个work的运行时间
│   DbManager.py                --------------- 数据提取类
│   Errors.py                   --------------- 异常类
│   Executor.py                 --------------- 流水线类
│
├───Analysis                    --------------- 分析组件目录（自定义组件放在这里）
│   │   CacheNeeds.py           --------------- @needs()装饰器
│   │   Middlewares.py          --------------- 预置分析组件：中间件
│   │   Wordcloud.py            --------------- 预置分析组件：词云
│   │   __init__.py
│   │
│   └───DataMapper              --------------- 数据应对关系目录
│           Mapper06082019.py   --------------- 预置对应关系：06/08/2019时适用关系
│           __init__.py
│
└───WorkPipelines               --------------- 流水线目录（自定义流水线放在这里）
        Example.py              --------------- 流水线的一个样例
```
框架逻辑很简单。分两步：
* 使用DbManager从微信的Document（如何获得参阅[How to Use(iOS)](#how-to-useios)）中读取数据库并缓存到Discoverer
* 设计流水线，运行之。Logger负责输出日志。
```
                                                   
 ┌───────────┐            ╔═══════════╗            
 │ DbManager │            ║         ▼ ║            
 └─────┬─────┘     ┌─────>║         │ ║            
       │           │      ║  work 1 │ ╠─┐          
  ┌────┴───┐       │┌─────╣         P ║ │          
  │Raw Data│       ││     ║         i ║ │          
  └────┬───┘       ││     ║         p ║ │          
       │           ││     ╠─────────e─╣ │  ┌──────┐
       │           ││     ║         l ║ └──>Logger│
  .────▼───┬.──────┘│     ║         i ║ ┌──>      │
 │         │ │      │     ║  work 2 n ╠─┘  └──────┘
 │`┬───────┼'│<─────┘     ║         e ║            
 │ │       │ │     ┌─────>║         │ ║            
 │ │ Cache │ ├─────┘┌─────╣         │ ║            
 │ │       │ │<─────┘     ╠─────────┼─╣            
 │.┼───────┴.│            ║         │ ║            
 │ │         │ Data       ║   ...   │ ║            
  `┴────────'  exchange   ║         ▼ ║            
               with cache ╚═══════════╝            
```
---

## How to Use(iOS):
> 注：此样式的文字供开发者用户阅读
1. 获取WeChat备份文件（可以使用其他第三方应用获得，这里推荐iMazing）
    * 下载[iTunes](https://www.apple.com/itunes/)；
    * 下载[iMazing](https://imazing.com/)；
    * 运行iMazing，这个软件会提示向iTunes安装插件，同意即可；
    * 如果使用的是Windows10商店内的iTunes，这个插件会在每次重启iTunes时被删除，重新安装即可；
    * 连接iPhone，此时能在iMazing上看到当前手机的信息；
    * 在iTunes中，如果这里被勾选，取消勾选，这个设置将使你的iPhone备份文件不再被加密，以便读取；
    ![取消勾选备份加密](https://raw.githubusercontent.com/ZzzGin/WeChatDiscover/v0.5/img/example2.png)
    * 在iMazing中，备份当前手机；
    ![备份手机](https://raw.githubusercontent.com/ZzzGin/WeChatDiscover/v0.5/img/example3.png)
    * 备份完毕后，右上角选择备份并双击；
    ![选择备份](https://raw.githubusercontent.com/ZzzGin/WeChatDiscover/v0.5/img/example4.png)
    * 左侧选择File System，在Navigator中找到App，并在目录内选择WeChat应用根目录，右键复制Documents文件夹到电脑。
    ![复制Documents](https://raw.githubusercontent.com/ZzzGin/WeChatDiscover/v0.5/img/example5.png)
    * 至此，前期准备工作完毕，微信核心数据文件目录获取。
2. 普通用户，调用预定义的分析组件自定义工作流水线：
    * 进入之前获取的Documents目录，除去全“0”，会看到1个或多个由32位数字与字母组成名称的目录，数量与用户在当前手机上登录过的微信号数量相同。如果只有一个，记录这个目录的名称，为便于后面步骤的描述，这里记[0123456789abcdef0123456789abcdef]；如果有多个，可以通过目录大小确定主账号的目录名，或者随机选择一个继续接下来的步骤多次尝试确认；
    > 理论上而言，这个32位数应当是与用户ID相关的字符串的hash值，但是目前而言未发现规律，因此无法找到寻找账号目录的简便方法，欢迎issue或者PR。
    * 记录Documents目录在系统中的路径，为便于后面步骤的描述，这里记[D:/WeChatDiscover/Documents]；
    * 进入src/WorkPipelines目录，创建一个自定义名称的py文件以定义pipeline，这里以Example.py为例：
    ```python
    import sys 
    import os
    # 增添这个目录以搜索项目文件
    sys.path.append(os.path.abspath('./src')) 
    from DbManager import DbManager 
    from Executor import Discoverer
    # import需要的分析组件
    from Analysis import Wordcloud, Middlewares

    # 关注的群名
    queryName = "17年雪城大学新生群"
    # 实例化一个DbManager，三个参数分别为Documents的路径，账号目录名称，是否为群
    dbm = DbManager("D:/WeChatDiscover/Documents", "0123456789abcdef0123456789abcdef", True)
    # 读取该群名的历史记录
    dbm.update(queryName)
    # 返回一个tuple，记录所有历史记录
    history = dbm.mergeAllTrunksToTuple()
    # 返回一个dict，记录所有微信ID和昵称对应关系
    friendList = dbm.getFrindList()

    # 实例化一个Discoverer
    disc = Discoverer()
    # 添加一个文件logger，默认为新建文件夹
    disc.addFileForLogger()
    # 像Discoverer输入历史记录
    disc.data = history
    # 在cache中加入friendlist
    disc.cache["friendList"] = friendList
    # 在cache中加入groupName以便输出文件名
    disc.cache["groupName"] = queryName
    # 定义Pipeline， 添加一个work
    disc.addWork(Wordcloud.WordcloudForChatRoom)
    # 你可以通过这种方式添加多个works
    # disc.addWorks(  Middlewares.textMessagesSplitedByIdInGroupChat,
    #                 Wordcloud.WordcloudForEachMembersInChatRoom)
    # 执行Pipeline
    disc.doWorks()
    pass
    ```