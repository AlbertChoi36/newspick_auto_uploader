# -*- coding: utf-8 -*-

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


class KakaoView:
    def __init__(self, driver, account):
        self.driver = driver
        self.ACCOUNT = account

        self.login()

        self.CHANNEL_LIST = self._get_channels()

    def _find_element(self, by, x):
        loop = True
        while(loop):
            try:
                return self.driver.find_element(by, x)
            except:
                pass


    def login(self):
        self.driver.get('https://creators.kakao.com/my-channels')
        time.sleep(1)

        input_email = self.driver.find_element(By.CSS_SELECTOR, '#id_email_2')
        input_password = self.driver.find_element(By.CSS_SELECTOR, '#id_password_3')

        input_email.send_keys(self.ACCOUNT[0])
        input_password.send_keys(self.ACCOUNT[1])
        input_password.send_keys(Keys.ENTER)
        time.sleep(1)

    def upload_by_url(self, title, url, channel_code):
        self.driver.get(f'https://creators.kakao.com/channel/{channel_code}/board/create')
        time.sleep(0.5)

        boardTitle = self._find_element(By.CSS_SELECTOR, '#boardTitle')
        boardTitle.send_keys(title)

        link_btn = self.driver.find_element(By.LINK_TEXT, '링크 직접입력')
        link_btn.click()
        #time.sleep(0.5)

        link_box = self.driver.find_element(By.CSS_SELECTOR,
                                       '#mainContent > div.editor_board > div > div.area_contents > div.cont_tab > form > div.item_form.type_search > div > input')
        link_box.send_keys(url)
        link_box.send_keys(Keys.ENTER)
        #time.sleep(5)

        put_btn = self._find_element(By.XPATH,
                                      '//*[@id="mainContent"]/div[2]/div/div[2]/div[3]/form/div[2]/ul/li[1]/div[3]/button')
        put_btn.click()

        size_btn = self.driver.find_element(By.CSS_SELECTOR,
                                       '#mainContent > div.editor_board > div > div.area_editor > div:nth-child(3) > div.edit_template > ul > li:nth-child(3) > button')
        size_btn.click()
        #time.sleep(0.5)

        upload_btn = self.driver.find_element(By.CSS_SELECTOR,
                                         '#mainContent > div.wrap_btn > div.align_r > button.btn_g.btn_primary.btn_icon')
        upload_btn.click()
        #time.sleep(5)

        news_category = self._find_element(By.CSS_SELECTOR,
                                            '#layer > div > div > div.layer_body > div > div:nth-child(3) > dl > dd > div > div:nth-child(1) > label')
        upload_btn = self._find_element(By.CSS_SELECTOR,
                                         '#layer > div > div > div.layer_body > div > div.wrap_btn.align_r > button.btn_g.btn_primary.btn_icon')
        news_category.click()
        upload_btn.click()
        #time.sleep(5)

        OK_btn = self._find_element(By.CSS_SELECTOR, '#layer > div > div > div.layer_foot > div > button')
        OK_btn.click()
        time.sleep(0.5)

    def _get_channels(self):
        self.driver.get('https://creators.kakao.com/my-channels')
        time.sleep(1)

        channel_list = []
        name, id = (0, 0)
        run = True
        i = 1
        while(run):
            try :
                id = self.driver.find_element(By.XPATH, f'//*[@id="mainContent"]/ul/li[{i}]/a')
            except :
                run = False
                continue
            id = id.get_attribute('href').split('/')[-2]
            name = self.driver.find_element(By.XPATH, f'//*[@id="mainContent"]/ul/li[{i}]/a/div[2]/div/strong')
            name = name.text
            channel_list.append((name, id))
            i += 1
        return channel_list


    def create_channel(self, prof_img, name, id, intr, category=(2, 1)):
        self.driver.get('https://creators.kakao.com/my-channels/create')
        time.sleep(1)
        img_input = self.driver.find_element(By.CSS_SELECTOR, '#profileAttach')
        name_input = self.driver.find_element(By.CSS_SELECTOR, '#channelName')
        id_input = self.driver.find_element(By.CSS_SELECTOR, '#searchId')
        intr_input = self.driver.find_element(By.CSS_SELECTOR, '#statusMessage')
        publicize_btn = self.driver.find_element(By.CSS_SELECTOR, '#mainContent > form > fieldset > div.regist_channel > div.area_regist > div:nth-child(2) > div > div > div.bundle_regist > div > div:nth-child(1) > label > span.ico_creators.ico_radio')


        img_input.send_keys(prof_img)
        time.sleep(0.2)
        name_input.send_keys(name)
        time.sleep(0.2)
        id_input.send_keys(id)
        time.sleep(0.2)
        intr_input.send_keys(intr)
        time.sleep(0.2)
        publicize_btn.click()

        #카테고리 설정
        fold1 = self.driver.find_element(By.CSS_SELECTOR, '#mainContent > form > fieldset > div.regist_channel > div.area_regist > div:nth-child(2) > div > div > div:nth-child(1) > div > a > span')
        fold1.click()
        time.sleep(0.2)

        category_large = self.driver.find_element(By.XPATH,
                                                  f'//*[@id="mainContent"]/form/fieldset/div[1]/div[1]/div[2]/div/div/div[1]/div/div/ul/li[{category[0]}]/a')
        category_large.click()
        time.sleep(0.5)

        fold2 = self.driver.find_element(By.CSS_SELECTOR, '#mainContent > form > fieldset > div.regist_channel > div.area_regist > div:nth-child(2) > div > div > div:nth-child(2) > div > a > span')
        fold2.click()
        time.sleep(0.2)

        category_small = self.driver.find_element(By.XPATH,
                                                  f'//*[@id="mainContent"]/form/fieldset/div[1]/div[1]/div[2]/div/div/div[2]/div/div/ul/li[{category[1]}]/a')
        category_small.click()
        time.sleep(0.2)

        #확인
        verify_btn = self.driver.find_element(By.CSS_SELECTOR, '#mainContent > form > fieldset > div.notice_regist > div > label > span.ico_creators.ico_check')
        verify_btn.click()
        time.sleep(0.2)

        #생성
        done_btn = self.driver.find_element(By.CSS_SELECTOR, '#mainContent > form > fieldset > div.wrap_btn > div > button')
        done_btn.click()
        time.sleep(0.2)

        self.CHANNEL_LIST = self._get_channels()
