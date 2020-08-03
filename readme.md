# 购物党爬虫
## 简介
使用Selenium+Chrome Headless爬取自己设定好的商品的[购物党](gwdang.com)的价格信息,如果达到设定好的条件,就调用python的stmplib模块,给邮箱发邮件
## 使用
### 准备条件
python环境安装selenium

google-chrome(在PATH里)

chromedriver(在PATH里)
### 设定邮箱
改一下[email_config.json](.email_config.json)
标题和消息
### 设定要爬取的商品信息
改一下[gwdang_product_list.csv](.gwdang_product_list.csv)
其中notification_condition是发送邮件的决定条件,要求是python的表达式.需要使用变量写表达式,其中NL,NH,NM,NC分别是本次爬取时的[180天内最低价(不凑单)],[180天内的最高价],[180天内最低价(凑单)],[现在的价格(当然是指使用了gwdang提供的优惠卷后的价格)];OL,OH,OM,OC类似
### 运行
python gwdang.py

### 日常使用
安在crontab里使用,好不好用我先用一阵再说
