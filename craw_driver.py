from selenium import webdriver
#from bs4 import BeautifulSoup as bs
#import os
#import time
#import hashlib
#import json
#import pickle
#from multiprocessing import Pool,Process
#import urllib.request
#import threading
class Craw_Driver:
    _driver = None #
    _down_path = None #구글 자체 다운로드 경로 변경을 위함
    _driver_path = None #구글드라이버 경로
    _chrome_options = None #옵션 설정
    
    def __init__(self,down_path='/home/jbs/mal/',driver_path ='/usr/local/bin/chromedriver'):
        self._down_path = down_path
        self._driver_path = driver_path
        self._chrome_options = webdriver.ChromeOptions()
        _prefs = {  "download.default_directory" : self._down_path}
                    #,"download.prompt_for_download": False
                    #,"download.directory_upgrade": True
                    #,"safebrowsing.enabled": True}
        self._chrome_options.add_experimental_option('prefs', _prefs)
    
    def hide(self):
        try:
            self._chrome_options.add_argument('headless') #웹 브라우저 띄우지 않음
            self._chrome_options.add_argument('disable-gpu') #GPU 사용 안함
            self._chrome_options.add_argument('lang=ko_KR') #언어 설정
        except Exception as e:
            print(e)

    def driver_run(self): #드라이브 실행
        try:
            self._driver = webdriver.Chrome(self._driver_path,options=self._chrome_options)
        except Exception as e:
            print(e)