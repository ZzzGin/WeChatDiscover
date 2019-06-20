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
1. 获取WeChat备份文件（可以使用其他第三方应用获得，这里推荐iMazing）
    * 下载[iTunes](https://www.apple.com/itunes/)；
    * 下载[iMazing](https://imazing.com/)；
    * 运行iMazing，这个软件会提示向iTunes安装插件，同意即可；
    * 如果使用的是Windows10商店内的iTunes，这个插件会在每次重启iTunes时被删除，重新安装即可；
    * 连接iPhone，此时能在iMazing上看到当前手机的信息；
    * 在iTunes中，如果这里被勾选，取消勾选，这个设置将使你的iPhone备份文件不再被加密，以便读取；
    ![取消勾选备份加密]()
    * 在iMazing中，备份当前手机；
    ![备份手机]()
    * 备份完毕后，右上角选择备份并双击；
    ![选择备份]()
    * 左侧选择File System，在Navigator中找到App，并在目录内选择WeChat应用根目录，右键复制Documents文件夹到电脑。
    ![复制Documents]()