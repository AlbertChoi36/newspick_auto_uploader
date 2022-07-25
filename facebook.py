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


    def register(self, name, email, password):
        pass

    def upload(self, title, url):
        self.driver.get('https://www.facebook.com/groups/2576868295699576')
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div[1]/div[1]/div/div/div/div[2]/div/div[2]')))
        new_btn = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div[1]/div[1]/div/div/div/div[2]/div/div[2]')
        new_btn.send_keys(Keys.ENTER)

        '''
        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div/div')))
        upload_pic = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]')
        ActionChains(self.driver).move_to_element(upload_pic).perform()
        time.sleep(0.5)
        upload_pic.send_keys(pic)
        '''

        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[2]/div/div')))
        input_text = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div')
        input_text.send_keys(title+'\n'+url)

        upload_btn = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[2]/div/div')
        upload_btn.click()
        time.sleep(9)