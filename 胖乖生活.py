# 脚本名称: 胖乖生活
# 变量名 tz_pgsh   格式 token#备注   多账号@分割
# 抓包 抓token
#需要推送的自己填token，把False改为True
pushplus = True
pushplus_token = 'e1cde036a1c34b2384ec3d1c1c55cba5'

import requests
import json
import os
from urllib.parse import quote
import time as timesleep
from datetime import datetime, timedelta, time
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
sum = 0
msg = ''
def pushplus_ts(token,rw,msg):
    url = 'https://www.pushplus.plus/send/'
    data = {
        "token": token,
        "title": rw,
        "content": msg
    }
    r = requests.post(url, json=data)
    msg = r.json().get('msg', None)
    print('pushplus推送结果：{}'.format(msg))

def get_user():
    account = os.getenv('tz_pgsh').split('@')
    if not account:
        print('环境变量未设置，请检查')
        return None

    account_list = os.environ.get('tz_pgsh').strip().split('@')
    return account_list

def get_headers(token):
    headers = {
        "Host": "userapi.qiekj.com",
        "Authorization": token,
        "Version": "1.38.0",
        "channel": "android_app",
        "content-length": "60",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.14.9",
    }
    return headers

def sign(token,headers):
    print('-----🌟签到🌟-----')
    url1 = "https://userapi.qiekj.com/signin/signInAcList"
    data1 = {"token":token}
    response = requests.post(url1, headers=headers, data=data1).json()["data"]["id"]
    url2 = "https://userapi.qiekj.com/signin/doUserSignIn"
    data2 = {"activityId": response, "token": token}
    qiandao = requests.post(url2, headers=headers, data=data2).json()
    if qiandao["msg"] == '成功':
        print("🌈🌈🌈签到成功获得:", qiandao["data"]["totalIntegral"])
    else:
        print('-----💮{}💮-----'.format(qiandao['msg']))
        timesleep.sleep(2)
def vedio_task1(token,headers):
    url = "https://userapi.qiekj.com/task/completed"
    print('-----🌟看视频赚积分🌟-----')
    for i in range(10):
        try:
            data = "taskType=2&token={}".format(token)
            response = requests.post(url, headers=headers, data=data).json()
            timesleep.sleep(5)
            if response['data'] == True:
                print("---🌈已完成{}次🌈---".format(i+1))
            else:
                print("---💮看视频赚积分任务完成💮---")
                break
        except:
            print('执行任务错误')

def vedio_task2(token,headers):
    url = "https://userapi.qiekj.com/task/completed"
    print('-----🌟看广告赚积分🌟-----')
    for i in range(10):
        data = "taskCode=18893134-715b-4307-af1c-b5737c70f58d&token={}".format(token)
        response = requests.post(url, headers=headers, data=data).json()
        timesleep.sleep(5)
        if response['data'] == True:
            print("---🌈已完成{}次🌈---".format(i+1))
        else:
            print("---💮看广告赚积分任务完成💮---")
            break
def check_in(token,headers):
    print('-----🌟积分报名打卡🌟-----')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    encoded_current_time = quote(current_time)
    url1 = "https://userapi.qiekj.com/markActivity/queryMarkTaskByStartTime"
    url2 = "https://userapi.qiekj.com/markActivity/doApplyTask"
    data1 = {'startTime': encoded_current_time, 'token': token}
    respones = requests.post(url1, headers=headers, data=data1).json()["data"]["taskCode"]
    data2 = {"taskCode": respones, "token": token, }
    respones = requests.post(url2, headers=headers, data=data2).json()["msg"]
    print('🌈🌈🌈积分报名结果：{}'.format(respones))
    timesleep.sleep(2)


def gua_fen(token,headers):
    print("-----🌟瓜分积分🌟-----")
    url1 = "https://userapi.qiekj.com/markActivity/queryMarkTaskByStartTime"
    url2 = "https://userapi.qiekj.com/markActivity/doMarkTask"
    url3 = "https://userapi.qiekj.com/markActivity/markTaskReward"
    current_datetime = datetime.now()
    yesterday_datetime = current_datetime - timedelta(days=1)
    yesterday_now = yesterday_datetime.replace(hour=current_datetime.hour, minute=current_datetime.minute,
                                               second=current_datetime.second)
    t = quote(yesterday_now.strftime("%Y-%m-%d %H:%M:%S"))
    data = {"startTime": t, "token": token}
    respones = requests.post(url1, headers=headers, data=data).json()["data"]["taskCode"]
    data1 = {"taskCode": respones, "token": token, }
    respone = requests.post(url2, headers=headers, data=data1).json()["msg"]
    current_time = datetime.now().time()
    afternoon_two = time(14, 10, 0)
    if current_time > afternoon_two:
        guafen = requests.post(url3, headers=headers, data=data1).json()["data"]
        print("🌈🌈🌈获得:", guafen)
    else:
        print("❗❗❗当前未到瓜分时间")
        timesleep.sleep(2)

def query0(token,headers):
    url = "https://userapi.qiekj.com/signin/getTotalIntegral"
    data1 = "token={}".format(token)
    response = requests.post(url, headers=headers, data=data1)
    data2 = response.json()['data']
    if data2 is not None:
        return data2
    else:
        return False

def query1(token,headers):
    print(f"-----🌟查询积分🌟-----")
    url = "https://userapi.qiekj.com/signin/getTotalIntegral"
    data1 = "token={}".format(token)
    response = requests.post(url, headers=headers, data=data1)
    data2 = response.json()['data']
    if data2 is not None:
        print('🌈🌈🌈账户总积分：{}'.format(data2))
        return data2

if __name__ == '__main__':
    account_list = get_user()
    cnt = len(account_list)
    print('---🌸共获取到{}个账号🌸---'.format(cnt))
    for i,value in enumerate(account_list):
        parts = value.split('#')
        token = parts[0]
        name = parts[1]
        headers = get_headers(token)
        timesleep.sleep(2)
        print('---🥝开始执行第{}个账号{}🥝---'.format(i+1,name))
        if query0(token, headers) != False:
            start = query0(token, headers)
            sign(token, headers)
            timesleep.sleep(2)
            headers = get_headers(token)
            timesleep.sleep(2)
            vedio_task1(token, headers)
            timesleep.sleep(2)
            vedio_task2(token, headers)
            timesleep.sleep(2)
            check_in(token, headers)
            timesleep.sleep(2)
            gua_fen(token,headers)
            timesleep.sleep(2)
            end = query1(token, headers)
            timesleep.sleep(2)
            inter_msg = '账号[{}]本次获得{}积分,现有积分[{}]'.format(name,end - start,end)
            msg += inter_msg + os.linesep
        else:
            print('❗❗用户[{}]token失效，请更新❗❗'.format(name))
            continue
    if pushplus:
        pushplus_ts(pushplus_token,'胖乖生活运行成功',msg)