'''
股票api：  “http://qt.gtimg.cn/q=”
关于返回值的介绍：”https://blog.51cto.com/u_15127704/4740983“
time：2023-02-01
author：lingchen-jiager
开盘后每5min获取一次股票价格，当达到预定盈利时，给手机发送提醒。
带#-----需要自行配置，
默认使用ntfy通知，需要自行在mail_to_you()中的subscribed_link设置ntfy的订阅链接；
如果要使用邮件通知，请自行设置好email_to_you()中的邮箱参数，并在mail_to_you()中将subscribed_link设置为None。
'''
import smtplib,requests
from email.mime.text import MIMEText
def mail_to_you(subscribed_link,subject,data_content):
    def email_to_you(mail_content,subject): #使用smtp授权码发邮件通知，以163邮箱为例
        #设置服务器所需信息
        #163邮箱服务器地址
        mail_host = 'smtp.163.com'
        #163用户名
        mail_user = '1xxxxxxx'
        #密码(部分邮箱为授权码)
        mail_pass = 'xxxxxxx'
        #邮件发送方邮箱地址
        sender = '13xxxxxxx@163.com'
        #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        receivers = ['2xxxxxxx@qq.com']

        #设置email信息
        #邮件内容设置

        message = MIMEText(mail_content,'plain','utf-8')
        #邮件主题
        message['Subject'] = subject
        #发送方信息
        message['From'] = sender
        #接受方信息
        message['To'] = receivers[0]

        #登录并发送邮件
        try:
            smtpObj = smtplib.SMTP()
            #连接到服务器
            smtpObj.connect(mail_host,25)
            #登录到服务器
            smtpObj.login(mail_user,mail_pass)
            #发送
            smtpObj.sendmail(
                sender,receivers,message.as_string())
            #退出
            smtpObj.quit()
            print('success')
        except smtplib.SMTPException as e:
            print('error',e) #打印错误

    def ntfy_to_you(subscribed_link,subject,data_content): #需要填入ntfy的订阅链接https://ntfy.sh/xxxxx(或者你可以自行搭建)
        requests.post(url=subscribed_link,
                      data=data_content.encode(encoding='utf-8'),headers={ "Title": subject.encode("utf-8").decode("latin") }) #data_content是正文内容




    if subscribed_link is None :
        email_to_you(mail_content=data_content,subject=subject)
    else:
        ntfy_to_you(subscribed_link=subscribed_link,subject=subject,data_content=data_content)

import time

import datetime
import requests

url = "http://qt.gtimg.cn/q="
headers = {
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"zh-CN,zh;q=0.9",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"Host":"qt.gtimg.cn",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}

while 1 :
    # 利润达到多少提醒
    earn = 300                                 #-----
    # 持有此股票多少股
    own_shares = 9100                          #-----
    # 购入时候的平均价格（含税）
    price_in = 3.349                           #-----
    # 股票代码
    shares_code = "sh601618"                   #-----
    # 股票名称
    share_name = "中国中冶"                     #-----
    # 范围时间
    d_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '9:30', '%Y-%m-%d%H:%M')#开盘时间
    d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '11:30', '%Y-%m-%d%H:%M')#休市
    d_time2 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '13:00', '%Y-%m-%d%H:%M')#开盘时间
    d_time3 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '15:00', '%Y-%m-%d%H:%M')#收盘时间
    # 当前时间
    n_time = datetime.datetime.now()
    # print(n_time)
    # 判断当前时间是否在范围时间内
    if n_time > d_time and n_time < d_time1:
        req = requests.get(url=url+shares_code, headers=headers).text
        shares_data = req.split("~")
        if (float(shares_data[3]) - price_in) * own_shares > earn:  #卖出利润大于earn提醒
            earn = (float(shares_data[3]) - price_in) * own_shares  #现在卖出能赚多少。
            today_date = str(datetime.date.today())
            hour_minu = datetime.datetime.now().strftime("%H-%M")
            mail_to_you(subscribed_link="https://ntfy.sh/123",subject=share_name + "盈",data_content="现在卖盈："+str(earn))
        time.sleep(300)

    elif n_time > d_time2 and n_time < d_time3:
        req = requests.get(url=url+shares_code, headers=headers).text
        #print(n_time.hour)
        shares_data = req.split("~")
        if int(n_time.hour) == 14 and int(n_time.minute)>45:
            #print(123)
            mail_to_you(subscribed_link="https://ntfy.sh/123",subject=str(datetime.date.today()) + "总结", data_content=share_name +"盈亏："+str((float(shares_data[3]) - price_in) * own_shares))
            time.sleep(5)
        print(shares_data[3])
        if (float(shares_data[3]) - price_in) * own_shares > earn:  # 卖出利润大于100提醒
            earn = (float(shares_data[3]) - price_in) * own_shares  # 现在卖出能赚多少。
            today_date = str(datetime.date.today())
            hour_minu = datetime.datetime.now().strftime("%H-%M")
            mail_to_you(subscribed_link="https://ntfy.sh/123",subject=share_name + "盈", data_content="现在卖盈：" + str(earn))
        time.sleep(300)
    else:
        # print("未开盘",end='')
        # mail_to_you(subscribed_link="https://ntfy.sh/123",subject="ceshi", data_content="ceshi")
        pass
        time.sleep(60)
