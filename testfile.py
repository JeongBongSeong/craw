from craw_driver import Craw_Driver
from craw_info import Acc_info
from bs4 import BeautifulSoup as bs
import os
import time
import hashlib
import json
import pickle
from multiprocessing import Pool,Process
import urllib.request
import re
from selenium.common.exceptions import NoSuchElementException


class Contagio:
    _chrome_driver = None
    _craw_info = None
    
    def contagio_run(self):
        
        self._chrome_driver = Craw_Driver()
        #self._chrome_driver.hide()
        self._chrome_driver.driver_run() # 드라이버 실행
        self._chrome_driver._driver.set_window_size(1200,600)


        _down_link = ["a1","a2","a3","a4","a5","a6","a7","a8","a9","a1","a2","a3","a4","a5","a6","a7","a8","a9","a1","a2","a3","a4","a5","a6","a7","a8","a9","a1","a2","a3","a4","a5","a6","a7","a8","a9","a1","a2","a3","a4","a5","a6","a7","a8","a9","a1","a2","a3","a4","a5","a6","a7","a8","a9","a1","a2","a3","a4","a5","a6","a7","a8","a9","a1","a2","a3","a4","a5","a6","a7","a8","a9","a1","a2","a3","a4","a5","a6","a7","a8","a9","a1","a2","a3","a4","a5","a6","a7","a8","a9","a1","a2","a3","a4","a5","a6","a7","a8","a9","a10","a4"]
        print(_down_link)
        _down_no = 4
        try:
            _n = int(len(_down_link)/_down_no) #멀티프로세스 분할
            _down_link = list(self.divide_list(_down_link,_n)) #멀티프로세스 이용하기위해 분할하는 함수 이용
        except Exception as _e:
            print(_e)
        print(_down_link)

    def divide_list(self,l,n): #mulit processing을 위한 해시값 분할 작업
        #n=len(l)/4
        for i in range(0,len(l),n):
            yield l[i:i + n]
#http://contagio.deependresearch.org/APT/China/CalypsoAPT_win_samp.zip
if __name__ == "__main__":
    contagio = Contagio()
    contagio.contagio_run()

'''

    def contagio_run(self):
        url = "https://www.dropbox.com/s/htzh42yrze5045m/pakfil.zip?dl=0"
        self._craw_info = Acc_info(get_url=url)
        
        self._chrome_driver = Craw_Driver()
        #self._chrome_driver.hide()
        
        self._chrome_driver.driver_run() # 드라이버 실행
        self._chrome_driver._driver.set_window_size(1200,600)
        self._chrome_driver._driver.get(self._craw_info.get_url())
        time.sleep(6)
        _component = bs(self._chrome_driver._driver.page_source,'html.parser')
        _component = _component.find('div',id=re.compile("component+")).attrs['id']
        
        try:
            self._chrome_driver._driver.find_element_by_xpath('//*[@id="'+_component+'"]/div/div/div/div[4]/div[2]/aside/div[2]/div[1]/div[1]/div[2]/div/span/div/span').click()
        except NoSuchElementException as e:
            print(e)
        self._chrome_driver._driver.find_element_by_xpath('//*[@id="'+_component+'"]/div/div/div/div[3]/div[2]/aside/div[2]/div[1]/div[1]/div[2]/div/div/nav/div/div/span[1]').click()
        
    def contagio_run(self):
        a = "https://www.dropbox.com/s/0irdeszs9j1ty8o/DDE_Office_Samp.zip?dl=0"
        if "/s/" in a:
            print("s")
        elif "/sh/" in a:
            print("sh")
        
    def contagio_run(self):
        links = 'http://contagio.deependresearch.org/crime/kpotstealer_win_samp.zip,'
        for test in links:
            _file_name = test.split("/")
            print(_file_name[-1])
            urllib.request.urlretrieve(test,"/home/jbs/mal/contagio/"+_file_name[-1])

    def contagio_run(self):
        
        self._craw_info = Acc_info(get_url="http://contagiodump.blogspot.com/2019/10/masad-clipper-and-stealer-windows.html")
        
        self._chrome_driver = Craw_Driver()
        #self._chrome_driver.hide()
        self._chrome_driver.driver_run() # 드라이버 실행
        
        self._chrome_driver._driver.get(self._craw_info.get_url())
        
        
        ###각 페이지에서 링크를 수집한다.
        _db_link = []       #dropbox
        _air_link = []       #air
        _down_link = []       #link


        _link_soup = bs(self._chrome_driver._driver.page_source,'html.parser')
        _link_soup = _link_soup.findAll('div',class_='post-body entry-content')

        for _link_soup1 in _link_soup:
            
            for _db_soup in _link_soup1.findAll('a',href=re.compile("https://www.dropbox+")):
                _db_link.append(_db_soup.attrs['href'])
            
            for _air_soup in _link_soup1.findAll('a',href=re.compile("https://airtable+")):
                _air_link.append(_air_soup.attrs['href'])

            for _link_soup in _link_soup1.findAll('a',href=re.compile("http://contagio+")):
                _down_link.append(_link_soup.attrs['href'])
        print('aaaaaaaaaaaaaaa'*6)
        print(_db_link)
        print('aaaaaaaaaaaaaaa'*6)
        print(_air_link)
        print('aaaaaaaaaaaaaaa'*6)
        print(_down_link)
'''