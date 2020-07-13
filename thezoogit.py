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
from un_zip import Un_Zip
from urllib.error import HTTPError

class TheZooGit:
    _chrome_driver = None
    _craw_info = None
    _down_path = "/home/jbs/mal/thezoo/"
    def thezoogit_run(self,url):
        try:
            if not os.path.exists('/home/jbs/mal/thezoo'):
                os.makedirs('/home/jbs/mal/thezoo')
        except OSError:
            print('Error: Creating directory. '+'/home/jbs/mal/thezoo')
            
        self._chrome_driver = Craw_Driver()
        #self._chrome_driver.hide()
        self._chrome_driver.driver_run() # 드라이버 실행
        
        self._chrome_driver._driver.set_window_size(1200,600)
        self._chrome_driver._driver.get(url)

        _soup_git = bs(self._chrome_driver._driver.page_source,"html.parser")
        _soup_git = _soup_git.findAll("a",class_="js-navigation-open link-gray-dark")
        
        _name = []
        for _link in _soup_git:
            #_name = _link.attrs["href"]
            _name.append(_link.get_text())    
        
        self.down_link(url,_name)

        for _file_name in _name:
            self.file_rename(_file_name+".zip")
    
    def down_link(self,_url,_name):
        for _name_url in _name:
            print(_url+_name_url+"/"+_name_url+".zip"+"?raw=true")
            try:
                urllib.request.urlretrieve(_url+_name_url+"/"+_name_url+".zip"+"?raw=true","/home/jbs/mal/thezoo/"+_name_url+".zip")
            except HTTPError as _e:
                print(_e)

                _chrome_driver = Craw_Driver()
                _chrome_driver.driver_run()
                _chrome_driver._driver.get(_url+_name_url)
                _soup = bs(_chrome_driver._driver.page_source,"html.parser")
                _soup = _soup.findAll("a",class_="js-navigation-open link-gray-dark")
                suc = False
                for __name in _soup:
                    if ".zip" in __name.get_text():
                        _file_name2 = __name.get_text()
                        suc = True
                if suc:
                    urllib.request.urlretrieve(_url+_name_url+"/"+_file_name2+"?raw=true","/home/jbs/mal/thezoo/"+_name_url+".zip")



                

    def file_rename(self,file_name): #hash_test함수는 파일 해시 참고해서 이름바꾸는데 사용하지만 사용안함
        try:
            f = open(self._down_path+file_name, 'rb')
            _data = f.read()
        except Exception as _e:
            print(_e)
            return
        f.close()
        
        #self._md5 = hashlib.md5(_data).hexdigest()
        #self._sha_1 = hashlib.sha1(_data).hexdigest()
        self._sha_256 = hashlib.sha256(_data).hexdigest()
        self._f_size = str(os.stat(self._down_path+file_name).st_size)

        os.rename(self._down_path+file_name,self._down_path+self._sha_256) #malwares는 이미 해쉬값

        #print("MD5: " + self._md5)
        #print("SHA-1: " + self._sha_1)
        print("SHA-256: " + self._sha_256)
        print("file_size: "+ self._f_size+" bytes")

if __name__ == "__main__":
    thezoogit = TheZooGit()
    thezoogit.thezoogit_run("https://www.github.com/ytisf/theZoo/tree/master/malwares/Binaries/")