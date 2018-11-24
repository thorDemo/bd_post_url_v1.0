# -*-coding=utf-8-*-
# @Author Nicholas
# @Function 提交URL 可以选择 提交url时间 提交url的数量 提交url的格式 不一样的Token 提交失败的要输出日志
# @Function 检测网站是否添加到百度里面
import subprocess
import logging
import datetime
import time
import os
import requests
from random import sample, randint
from datetime import datetime, timedelta
# 参数定义
# ————————————
post_url_path = 'url/result.txt'                 # 推送哪些url
post_num_every_index = 2000                     # 每次每个目录推送多少条数据，最大值是2000
post_frequency = 10                             # 推送延迟每隔离多少分钟推送一次,单位分钟 m
post_token = 'mckuWUsS5ljr4Roh'                 # 推送的token
# ————————————
# ————————————
logger = logging.getLogger(__name__)            # 日志配置
logger.setLevel(logging.INFO)
handler = logging.FileHandler('log/my_log.log', encoding='utf-8')
handler.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(handler)
logger.addFilter(ch)

# ————————————


def random_time():
    today = datetime.today()
    yesterday = today + timedelta(days=randint(-7, 0))
    return yesterday.strftime("%Y%m%d")


# 生成额定数量需要推送的url
def rand_char():
    char = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    return ''.join(sample(char, 5))


def create_post_url(num):
    urls = open(post_url_path, "r")
    for url in urls:
        index = open('url/index.txt', "r+")
        for line in index:
            post_url = open('url/cache/' + post_url_path[4:], 'w+')
            print('当前列表页为' + line)
            for x in range(0, num):
                value = rand_char()
                # now_time = datetime.datetime.now().strftime('%Y%m%d')  # 现在
                post_url.write('http://www.' + url.strip('\n') + '/' + line.strip('\n') + random_time() + value + '.html\n')
            post_url.close()
            post_all_url(post_token)


# # 推送url到百度
def post_all_url(token):
    temp = 1
    while True:
        path = 'url/cache/' + post_url_path[4:]
        urls = open(path, 'r')
        url = urls.readline().split('/')[2]
        print(url)
        post = 'curl -H "Content-Type:text/plain" --data-binary @' + path + ' "http://data.zz.baidu.com/urls?site=' + url + '&token=' + token + '"'
        output = subprocess.Popen(post, shell=True, stdout=subprocess.PIPE)
        out, err = output.communicate()
        try:
            for line in out.splitlines():
                print(str(line) + '\n')
            if str(out.splitlines()[0]).count('error') == 0 and str(out.splitlines()[0]).count('success') == 1:
                logger.info('提交成功 post=' + url)
                break
            elif temp == 3:
                logger.error('提交失败 post=' + url)
                break
            else:
                temp += 1
                logger.debug('提交失败重试！')
        except IndexError as e:
            logger.debug(e)
            time.sleep(3)


def push_urls():
    '''根据百度站长提供的API推送链接'''
    path = 'url/cache/post_url_need.txt'
    headers = {
        'User-Agent': 'curl/7.12.1',
        'Host': 'data.zz.baidu.com',
        'Content - Type': 'text / plain',
        'Content - Length': str(len(str(open(path, 'rb'))))
    }
    urls = open(path, 'r')
    line = urls.readline().split('/', 2)[0]
    url = 'http://data.zz.baidu.com/urls?site=' + line + '&token=' + post_token
    try:
        html = requests.post(url, headers=headers, data=open(path, 'rb'), timeout=5).text
        return html
    except Exception as e:
        print(e)
        return "{'error':404,'message':'请求超时，接口地址错误！'}"


def main():
    global post_frequency
    while post_frequency > 0:
        logger.debug('还需要推送 ' + str(post_frequency) + '次')
        create_post_url(post_num_every_index)
        time.sleep(60*post_frequency)
        post_frequency -= 1


if __name__ == '__main__':
    main()



