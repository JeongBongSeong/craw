from craw_driver import Craw_Driver
from craw_info import Acc_info
from bs4 import BeautifulSoup as bs
import os
import time
import hashlib
import json
import pickle
import urllib.request
from multiprocessing import Pool,Process
import re
from selenium.common.exceptions import NoSuchElementException

class Contagio:
    
    _chrome_driver = None
    _craw_info = None
    _process_db = None
    _process_air = None
    _process_link = None

    def contagio_run(self,url):
        self._craw_info = Acc_info(get_url=url)
        
        self._chrome_driver = Craw_Driver()
        #self._chrome_driver.hide()
        self._chrome_driver.driver_run() # 드라이버 실행
        
        self._chrome_driver._driver.get(self._craw_info.get_url())

        if self._craw_info.get_url() == "http://contagiominidump.blogspot.com/":
            _select_site = "http://contagiomobile.+"
        elif self._craw_info.get_url() == "http://contagiodump.blogspot.com/":
            _select_site = "http://contagio.+"
        #time.sleep(4)
        #게시판 열기   
        #_ysoup = bs(self._chrome_driver._driver.page_source,'html.parser')
        #_ysoup = _ysoup.findAll()

        #test = []
        #test = self._chrome_driver._driver.find_elements_by_class_name('toggle')
        _ycount = 1
        _mcount = 0
        _total_count = 0

        while True:
            try:
                _ycount += 1
                self._chrome_driver._driver.find_element_by_xpath('//*[@id="BlogArchive1_ArchiveList"]/ul['+str(_ycount)+']/li/a/span').click()
                time.sleep(1)
            except Exception:
                _ycount -= 1
                break

            while True:
                try:
                    _mcount += 1
                    self._chrome_driver._driver.find_element_by_xpath('//*[@id="BlogArchive1_ArchiveList"]/ul['+str(_ycount)+']/li/ul['+str(_mcount)+']/li/a[1]/span').click()
                    _total_count += 1
                    time.sleep(1)
                except Exception as e:
                    _mcount -= 1
                    print(e)
                    break
            _mcount = 0
            
        #print(_ycount)
        #print(_total_count)
        
        _soup_link = bs(self._chrome_driver._driver.page_source,'html.parser')
        _soup_link = _soup_link.findAll('ul',class_='posts')

        
        _test_count = 1

        _link_list = []     #게시글 링크를 담는다.
        for _link in _soup_link:
            for test in _link.findAll('a'):
                _link_list.append(test.attrs['href'])
        
        _db_count = 0
        _air_count = 0
        _down_count = 0
        _media_count = 0

        _db_link = []       #dropbox
        _air_link = []       #air
        _down_link = []       #link
        _media_link = []       #test용 

        for _link_url in _link_list:
            self._chrome_driver._driver.get(_link_url)
            ###각 페이지에서 링크를 수집한다.

            
            #dropbox link
            _link_soup = bs(self._chrome_driver._driver.page_source,'html.parser')
            _link_soup = _link_soup.findAll('div',class_='post-body entry-content')
            
            for _link_soup1 in _link_soup:
                
                for _db_soup in _link_soup1.findAll('a',href=re.compile("https://www.dropbox+")):
                    test = _db_soup.attrs['href']
                    _db_link.append(test)
                    _db_count += 1
                    print("db : "+str(_db_count))
                
                for _air_soup in _link_soup1.findAll('a',href=re.compile("https://airtable+")):
                    _air_link.append(_air_soup.attrs['href'])
                    _air_count += 1
                    print("air : "+str(_air_count))

                for _link_soup in _link_soup1.findAll('a',href=re.compile(_select_site)):
                    _down_link.append(_link_soup.attrs['href'])
                    _down_count += 1
                    print("down : "+str(_down_count))

                for _link_soup in _link_soup1.findAll('a',href=re.compile("http://www.mediafire.com/download/+")):
                    _media_link.append(_link_soup.attrs['href'])
                    _media_count += 1
                    print("media : "+str(_media_count))
        # divide를 이용해서 링크를 나눠줘야함
        
        print("-"*60)
        print(_db_link)
        print("-"*60)
        print(_air_link)
        print("-"*60)
        print(_down_link)
        print("-"*60)

        self._process_db = []
        self._process_air = []
        self._process_down = []

        _db_no = 1
        _air_no = 1
        _down_no = 1

        if _db_count > 12 :
            _db_no = 4
        if _air_count > 12 :
            _air_no = 4
        if _down_count > 12 :
            _down_no = 4

        ### dropbox
        try:
            if _db_no != 1:
                _n = int(len(_db_link)/_db_no) #멀티프로세스 분할
                _db_link = list(self.divide_list(_db_link,_n)) #멀티프로세스 분할
        except Exception as _e:
            print(_e)
        
        for _slc in _db_link:
            try: #멀티 프로세스 이용
                _p = Process(target=self.dropbox,args=(_slc,))
                self._process_db.append(_p)
                _p.start()
            except Exception as e:
                print(e)
        for _p in self._process_db: #프로세스가 끝날때까지 대기
            _p.join()
        
        ### airtable
        try:
            if _air_no != 1:
                _n = int(len(_air_link)/_air_no) #멀티프로세스 분할
                _air_link = list(self.divide_list(_air_link,_n)) #멀티프로세스 분할
        except Exception as _e:
            print(_e)
        
        for _slc in _air_link:
            try: #멀티 프로세스 이용
                _p = Process(target=self.airtable,args=(_slc,))
                self._process_air.append(_p)
                _p.start()
            except Exception as e:
                print(e)
        for _p in self._process_air: #프로세스가 끝날때까지 대기
            _p.join()
        
        ### down_link
        try:
            if _down_no != 1:
                _n = int(len(_down_link)/_down_no) #멀티프로세스 분할
                _down_link = list(self.divide_list(_down_link,_n)) #멀티프로세스 분할
        except Exception as _e:
            print(_e)
        
        for _slc in _down_link:
            try: #멀티 프로세스 이용
                _p = Process(target=self.down_link,args=(_slc,))
                self._process_down.append(_p)
                _p.start()
            except Exception as e:
                print(e)
        for _p in self._process_down: #프로세스가 끝날때까지 대기
            _p.join()

    def dropbox(self, urls):
        _chrome_driver = Craw_Driver()
        #_chrome_driver.hide()
        _chrome_driver.driver_run() # 드라이버 실행
        _chrome_driver._driver.set_window_size(1200,600)

        _no_popup = False
        for _url in urls:
            _chrome_driver._driver.get(_url)
            time.sleep(5)

            _component = bs(self._chrome_driver._driver.page_source,'html.parser')
            _component = _component.find('div',id=re.compile("component+")).attrs['id']
            
            if "/s/" in _url:
                try:
                    #팝업 창이 존재하지 않는 경우
                    _chrome_driver._driver.find_element_by_xpath('//*[@id="'+_component+'"]/div/div/div/div[3]/div[2]/aside/div[2]/div[1]/div[1]/div[2]/div/span/div/span/span/svg')
                    _chrome_driver._driver.find_element_by_xpath('//*[@id="'+_component+'"]/div/div/div/div[3]/div[2]/aside/div[2]/div[1]/div[1]/div[2]/div/div/nav/div/div/span[1]')
                except NoSuchElementException as _e:
                    _no_popup = True
                    print(_e)
                if _no_popup:
                    _chrome_driver._driver.find_element_by_xpath('//*[@id="'+_component+'"]/div/div/div/div[2]/div[2]/aside/div[2]/div[1]/div[1]/div[2]/div/span/div/span/span/svg')
                    _chrome_driver._driver.find_element_by_xpath('//*[@id="'+_component+'"]/div/div/div/div[2]/div[2]/aside/div[2]/div[1]/div[1]/div[2]/div/div/nav/div/div/span[1]')

            elif "/sh/" in _url:
                print("sh")


    def airtable(self,links):
        print('1')

    def down_link(self,links):
        for test in links:
            _file_name = test.split("/")
            print(_file_name[-1])
            urllib.request.urlretrieve(test,"/home/jbs/mal/contagio/"+_file_name[-1])
      
    def divide_list(self,l,n): #mulit processing을 위한 해시값 분할 작업
        #n=len(l)/4
        for i in range(0,len(l),n):
            yield l[i:i + n]




if __name__ == "__main__":
    contagio = Contagio()
    contagio.contagio_run('http://contagiominidump.blogspot.com/')
    contagio.contagio_run('http://contagiodump.blogspot.com/')