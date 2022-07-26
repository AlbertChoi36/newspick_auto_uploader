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
import datetime

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

def run(user, password):
    account = (user, password)

    '''
    print('Please login with Facebook account')
    user, password = input('user: '), input('password: ')
    fb_account = (user, password)
    '''

    # driver
    dir_ChromeDriver = './chromedriver.exe'
    driver = webdriver.Chrome(service=Service(dir_ChromeDriver))
    driver.set_window_size(2160, 1080)

    # initialize
    my_newspick = np.NewsPick(driver, account)
    # my_kakaoview = kv.KakaoView(driver, account)

    # kakaoView.create_channel(generate_news_icon(), generate_channel_name(kakaoView), 'news'+str(random.randint(10000000000, 100000000000)), '매일 매일 새로운 뉴스!', category=(2, 1))
    # print(my_kakaoview.CHANNEL_LIST)
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
    history = []
    for file in os.listdir('./newspick_history'):
        history += parse_history(f'C:/Users/admin/Desktop/newspick_history/{file}')
        print(file)
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
    for acc in parse_accounts('C:/Users/timet/OneDrive/바탕 화면/fb_accounts.txt')[0:1]:
        print(f'Login Facebook as "{acc[0]}"')
        try:
            my_fb = fb.Facebook(driver, acc)
            fb_list.append(my_fb)
            for content in content_list[:5]:
                my_fb.upload(*content)
            write_history(f'./newspick_history/{date.today()}.txt', content_list[:5])
            content_list = content_list[6:]
        except:
            print(f'EXCEPTION : something in wrong while uploading on facebook (account:{acc[0]})')

        my_fb.logout()
        time.sleep(2)

    driver.quit()




run_time = [(2, 00), (4, 00), (6, 00), (8, 00), (10, 00), (12, 00), (14, 00), (16, 00), (18, 00), (20, 00), (22, 00), (24, 0)]
print('Please login with Kakao account')
user, password = input('user: '), input('password: ')


#initiate
current_time = datetime.datetime.now()
i=0
for target in run_time:
    if target[0] < int(current_time.hour) or (target[0]==int(current_time.hour) and target[1] <= int(current_time.minute)):
        i+=1

#start
current_time = datetime.datetime.now()
for target in run_time[i:]:
    print(f'\nWaiting until {target[0]} : {target[1]}')
    while(target[0] >= int(current_time.hour) and (target[0] != int(current_time.hour) or target[1] > int(current_time.minute))):
        current_time = datetime.datetime.now()
    print(f'Run at {target[0]} : {target[1]}')
    print(current_time)
    try:
        run(user, password)
    except:
        print(f'EXCEPTION : failed to run')
