from craw_driver import Craw_Driver
from craw_info import Acc_info
from bs4 import BeautifulSoup as bs
import os
import time
import hashlib
import json
import pickle
from multiprocessing import Pool,Process
import re


class Contagio:
    _chrome_driver = None
    _craw_info = None

    def contagio_run(self,url):
        
        self._craw_info = Acc_info(get_url="http://contagiodump.blogspot.com/2019/10/amnesia-radiation-linux-botnet.html")
        
        self._chrome_driver = Craw_Driver()
        #self._chrome_driver.hide()
        self._chrome_driver.driver_run() # 드라이버 실행
        
        self._chrome_driver._driver.get(self._craw_info.get_url())

        _link_soup = bs(self._chrome_driver._driver.page_source,'html.parser')
        _link_soup = _link_soup.findAll('div',class_='post-body entry-content')
        for _link_soup1 in _link_soup:
            for _link_soup2 in _link_soup1.findAll('a',href=re.compile("http://contagio")):
                print(_link_soup2)