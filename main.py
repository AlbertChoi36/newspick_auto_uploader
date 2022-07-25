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
from datetime import datetime

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






print('Please login with Kakao account')
user, password = input('user: '), input('password: ')
account = (user, password)

print('Please login with Facebook account')
user, password = input('user: '), input('password: ')
fb_account = (user, password)


# driver
dir_ChromeDriver = './chromedriver.exe'
driver = webdriver.Chrome(service=Service(dir_ChromeDriver))


# initialize
my_newspick = np.NewsPick(driver, account)
my_kakaoview = kv.KakaoView(driver, account)
my_facebook = fb.Facebook(driver, fb_account)
time.sleep(1)
#kakaoView.create_channel(generate_news_icon(), generate_channel_name(kakaoView), 'news'+str(random.randint(10000000000, 100000000000)), '매일 매일 새로운 뉴스!', category=(2, 1))
print(my_kakaoview.CHANNEL_LIST)


# login
my_newspick.login()
time.sleep(2)

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





