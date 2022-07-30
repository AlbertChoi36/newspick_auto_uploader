import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import os
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
import clipboard
import pyautogui as pg
from datetime import date

import news_pick as np
import kakao_view as kv
import facebook as fb

def generate_news_icon():
    icon_list = os.listdir('./Resources/news_icon')
    return os.getcwd() + '/Resources/news_icon/' + random.choice(icon_list)


def generate_channel_name(k_view):
    with open('./Resources/channel_name.txt', 'r', encoding='utf-8') as f:
        name_list = [name.strip('\n') for name in f.readlines()]
        channel_list = [x[0] for x in k_view.CHANNEL_LIST]
        name_list = list(filter(lambda x: not x in channel_list, name_list))
        return random.choice(name_list)

def parse_accounts(file):
    account_list = []
    with open(file, 'r') as f:
        line = f.readline()
        while line:
            user, pw = line.strip('\n').split(' ')
            account_list.append((user, pw))
            line = f.readline()
    return account_list

def parse_history(file):
    try:
        open(file)
    except:
        return []

    title_list = []
    with open(file, 'r') as f:
        line = f.readline()
        while line:
            title_list.append(line.strip('\n'))
            line = f.readline()
    return title_list

def write_history(file, content_list):
    with open(file, 'a+') as f:
        for content in content_list:
            f.write(content[0]+'\n')

print('Please login with Kakao account')
user, password = input('user: '), input('password: ')
account = (user, password)

'''
print('Please login with Facebook account')
user, password = input('user: '), input('password: ')
fb_account = (user, password)
'''

# driver
dir_ChromeDriver = './chromedriver.exe'
driver = webdriver.Chrome(service=Service(dir_ChromeDriver))

# initialize
my_newspick = np.NewsPick(driver, account)
#my_kakaoview = kv.KakaoView(driver, account)

#kakaoView.create_channel(generate_news_icon(), generate_channel_name(kakaoView), 'news'+str(random.randint(10000000000, 100000000000)), '매일 매일 새로운 뉴스!', category=(2, 1))
#print(my_kakaoview.CHANNEL_LIST)
'''
#crawl
title, url, image = my_newspick.crawl_content_populer()
content = list(zip(title[:], url[:]))
time.sleep(2)

# kakaoview upload
id_list = [x[1] for x in my_kakaoview.CHANNEL_LIST[:]]
for id in id_list:
    random.shuffle(content)
    for t, u in content[:10]:
        my_kakaoview.upload_by_url(t, u, id)

# facebook upload
random.shuffle(content)
for t, u in content[:10]:
    my_facebook.upload(t, u)
    '''



# login
my_newspick.login()

# crawl
history = parse_history(f'C:/Users/admin/Desktop/newspick_history/{date.today()}.txt')
print(history)
content_list = []
for i in [0, 1, 4, 10]:
    my_newspick.set_category([i])
    title, url, image = my_newspick.crawl_content_populer()
    if not title in history:
        content_list.append(list(zip(title, url)))
content_list = sum(content_list, [])
random.shuffle(content_list)

# upload on fb accounts
fb_list = []
for acc in parse_accounts('C:/Users/admin/Desktop/fb_accounts.txt')[0:1]:
    my_fb = fb.Facebook(driver, acc)
    fb_list.append(my_fb)
    for content in content_list[:10]:
        my_fb.upload(*content)
    write_history(f'C:/Users/admin/Desktop/newspick_history/{date.today()}.txt', content_list[:10])
    content_list = content_list[11:]

    my_fb.logout()
    time.sleep(2)

