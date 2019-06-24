# 简介
一个在linux命令行提交题目的简单脚本
目前实现了codeforces网站的c++代码的提交
# 使用说明
## 目录结构说明
脚本默认会从work_path工作目录的mian.cpp文件读取你将要提交的代码(work_paht和main.cpp可以在配置文件中更改),在题目通过后你的工作目录的main.cpp会被保存到save_path/cf/比赛类型/比赛场次/题目编号.cpp
* 比赛类型有:div1,div2,div3,edu,Codeforces_Global
* 比赛场次就是 div1 round 111 那个111
* 题目编号就是ABCD等等
save_path可以在配置文件中更改
save_path下的目录结构如图:
![](http://img.startcraft.cn/github/img/1.png)
## 使用说明
将脚本下载到本地，填写配置文件config.ini,配置文件的说明在配置文件的注释里面,运行submit.sh,参数分别为提交网站(目前只有cf) 比赛id 题目编号
如: submit.sh cf 1182 a ,这样会把work_path下的mian.cpp作为第1182场cf比赛的A题提交
比赛id可以从地址栏获得
![](http://img.startcraft.cn/github/img/submit2.png)