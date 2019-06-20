# WeChat Discover
总体而言，这是一个**易于扩展的**分析与展示微信历史数据的迷你框架。举个例子，通过这个框架，使用20行左右的代码便可以生成一个下面的微信群词云：

![新生群词云.jpg](https://raw.githubusercontent.com/ZzzGin/WeChatDiscover/master/img/example1.png)

**普通用户**可以通过易于理解的Python调用，自定义一个“流水线(Pipeline)”来使用预先备好的“分析组件(Analysis)”来分析并展示需要的信息。

**开发者用户**也可以自定义分析组件，来实现自己的想要分析逻辑与展示效果。

目前本框架适用于iOS微信数据，安卓版本支持正在开发中。

本项目是基于个人兴趣的开源项目，采用MIT协议。

1. [Todos](#todos-pr-is-welcomed)

## Todos (PR is welcomed):
1. [DbManager] 对于安卓数据的支持
2. [Analysis] 一个将聊天记录转变为HTML文件的分析组件
3. [Analysis] 针对好友（而非群）聊天纪录的分析组件
4. [Analysis] 其他可能的、有预先准备必要的分析组件