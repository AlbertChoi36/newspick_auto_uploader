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

class Facebook:
    def __init__(self, driver, account):
        self.driver = driver
        self.ACCOUNT = account

        self.login()
        time.sleep(1.5)

    def login(self):
        self.driver.get('https://www.facebook.com/login/')
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#email')))
        input_email = self.driver.find_element(By.CSS_SELECTOR, '#email')
        input_pw = self.driver.find_element(By.CSS_SELECTOR, '#pass')

        input_email.send_keys(self.ACCOUNT[0])
        input_pw.send_keys(self.ACCOUNT[1])
        input_pw.send_keys(Keys.ENTER)

    def logout(self):
        self.driver.get('https://www.facebook.com/')
        profile_icon = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[4]/div[1]/span/div/div[1]')))
        #ActionChains(self.driver).move_to_element(profile_icon).perform()
        profile_icon.click()

        logout_btn = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[4]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div[1]/div/div/div[1]/div[2]/div/div[5]/div')))
        logout_btn.click()

    def register(self, name, email, password):
        pass

    def upload(self, title, url):
        self.driver.get('https://www.facebook.com/groups/2576868295699576')
        new_btn = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'oajrlxb2.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.i1ao9s8h.esuyzwwr.f1sip0of.abiwlrkh.p8dawk7l.lzcic4wl.bp9cbjyn.b3i9ofy5.orhb3f3m.czkt41v7.fmqxjp7s.emzo65vh.j83agx80.btwxx1t3.buofh1pr.jifvfom9.l9j0dhe7.idiwt2bm.kbf60n1y.cxgpxx05.d1544ag0.sj5x9vvc.tw6a2znq')))
        new_btn.send_keys(Keys.ENTER)

        '''
        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div/div')))
        upload_pic = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]')
        ActionChains(self.driver).move_to_element(upload_pic).perform()
        time.sleep(0.5)
        upload_pic.send_keys(pic)
        '''

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[2]/div/div')))
        input_text = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div')
        input_text.send_keys(title+'\n'+url)

        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div/div/a/div[1]/div/div/div/img')))
        WebDriverWait(self.driver, 10).until(EC.element_attribute_to_include((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div/div/a/div[1]/div/div/div/img'), 'alt'))
        is_pic = False
        while not is_pic:
            print(self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div/div/a/div[1]/div/div/div/img').get_attribute('alt'))
            if self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div/div/a/div[1]/div/div/div/img').get_attribute('alt') \
                    != '사진 없음':
                is_pic = True
        print('waited until pic')

        upload_btn = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[2]/div/div')
        upload_btn.click()

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'always-enable-animations.r7fvqmod.ev399l9o.ee40wjg4.emdzj9jj.pf5603km.d34kznaq')))
        WebDriverWait(self.driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'always-enable-animations.r7fvqmod.ev399l9o.ee40wjg4.emdzj9jj.pf5603km.d34kznaq')))
        time.sleep(0.5)