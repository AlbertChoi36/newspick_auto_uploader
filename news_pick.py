# -*- coding: utf-8 -*-

import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
import clipboard
import pyautogui as pg
from datetime import datetime


class NewsPick:
    def __init__(self, driver, account):
        self.driver = driver
        self.ACCOUNT = account

    def login(self):
        self.driver.get('https://partners.newspic.kr/login?ref=NO_LOGIN&redirect=%2Fmain%2Findex')

        time.sleep(1.2)

        kakao_login = self.driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-kakao')
        kakao_login.click()

        time.sleep(1.5)
        try:
            tabs = self.driver.window_handles
            self.driver.switch_to.window(tabs[1])

            input_email = self.driver.find_element(By.CSS_SELECTOR, '#id_email_2')
            input_password = self.driver.find_element(By.CSS_SELECTOR, '#id_password_3')

            input_email.send_keys(self.ACCOUNT[0])
            time.sleep(0.1)
            input_password.send_keys(self.ACCOUNT[1])
            time.sleep(0.1)
            input_password.send_keys(Keys.ENTER)
            time.sleep(2)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(1.5)
        except:
            pass

    def set_category(self, category):
        self.driver.get('https://partners.newspic.kr/member/channel?ref=MAIN')
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cate1"]')))
        for i in range(20):
            this_cat = self.driver.find_element(By.XPATH, f'//*[@id="cate{i+1}"]')
            checked = False
            try:
                if this_cat.get_attribute('checked'):
                    checked = True
            except:
                pass
            if ((i in category) and not checked) or ((i not in category) and checked):
                this_cat.click()
            #print(f'[{i+1}] {checked}')

        done_btn = self.driver.find_element(By.CSS_SELECTOR, 'body > div.newspic-wrap.single-wrap > section > div.section-body.mt-60 > button')
        done_btn.click()
        time.sleep(0.2)


    def crawl_content_populer(self):
        self.driver.get('https://partners.newspic.kr/main/index')

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="profitNewsList"]/li[1]/div[1]/img')))
        time.sleep(0.5)

        title_list, url_list, img_list = [], [], []
        next = self.driver.find_element(By.CSS_SELECTOR, '#swiper-next')
        for i in range(0, 5):
            for j in range(0, 4):
                THUMBNAIL = self.driver.find_element(By.XPATH,
                                                     f'//*[@id="profitNewsList"]/li[{i * 4 + j + 1}]/div[1]/img')
                TITLE = self.driver.find_element(By.XPATH, f'//*[@id="profitNewsList"]/li[{i * 4 + j + 1}]/div[2]/a/span')

                ActionChains(self.driver).move_to_element(THUMBNAIL).perform()
                try:
                    button = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH,
                                             f'//*[@id="profitNewsList"]/li[{i * 4 + j + 1}]/div[1]/div[2]/ul/li[1]/button')))
                except:
                    continue
                button.click()
                time.sleep(0.5)

                alert = self.driver.switch_to.alert
                alert.accept()
                URL = clipboard.paste()

                title_list.append(TITLE.text)
                img_list.append(THUMBNAIL.get_attribute('src'))
                url_list.append(URL)
            if j == 3 and i<4:
                next.click()
                time.sleep(0.5)

        return title_list, url_list, img_list

    def save_news(self, title, url, img, name=str(datetime.today().strftime("%Y%m%d%H%M%S"))):
        with open(f'./contents/{name}.txt', 'w', encoding='UTF-8') as f:
            for i in title:
                f.write(i + '###')
            f.write('\n')
            for i in url:
                f.write(i + '###')
            f.write('\n')
            for i in img:
                f.write(i + '###')

    def load_news(self, file):
        title, url, img = [], [], []
        with open(f'./contents/{file}', 'r', encoding='UTF-8') as f:
            title, url, img = f.readlines()
        title = title.strip().split('$$$')[:-1]
        url = url.strip().split('$$$')[:-1]
        img = img.strip().split('$$$')[:-1]

        return title, url, img
'''
def download_image(img_url):
    urlretrieve(img_url, IMG_DERECTORY+'thumbnail.jpg')
'''