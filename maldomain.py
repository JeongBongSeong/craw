from craw_driver import Craw_Driver
from craw_info import Acc_info
from bs4 import BeautifulSoup as bs
import os
import time
import hashlib
import json
import pickle
from multiprocessing import Pool,Process

class MalDomain:

    _chrome_driver = None #d_river 클래스용
    _craw_info = None #acc_info 클래스용

    def domain_run(self):
        self._craw_info = Acc_info(get_url='http://www.malwaredomainlist.com/mdl2.php?inactive=&sort=Date&search=&colsearch=All&ascordesc=DESC&quantity=100&page=')
        self._chrome_driver = Craw_Driver()

        _page = 0 #페이지 이동을 위한 값
        _result = [] #
        self._chrome_driver.driver_run() # 드라이버 실행
        while True:
            self._chrome_driver._driver.get(self._craw_info.get_url()+str(_page)) # 웹 접근
            
            time.sleep(3)

            _page += 1

            _soup = bs(self._chrome_driver._driver.page_source,'html.parser') #파서 지정
            _soup = _soup.findAll("tr",bgcolor = ['#d8d8d8','#ffffff']) #findAll함수를 이용하여 사용자가 정의한 값에 해당하는 모든 값을 찾아준다.

            if _soup == []: #값이 없다면 종료
                print('exit')
                return _result

            for _test in _soup:
                _format ={"Data":None,"Domain":None,"IP":None,"Reverse_Lookup":None,"Description":None,"ASN":None}
                _bs_list = []

                for _domain in _test.findAll("td"): #soup에 포함된 값중 td값을찾아낸다.
                #j.appends(test = _domain.get_text('\",\"'))
                #print(_domain.get_text())
                    _bs_list.append(_domain.get_text()) #bs_list에 찾은 값을 추가해 준다.
                _i = 0
                for ex in _format.keys(): #json포멧을 맞추기 위해 위에 정의한format에 keys()에 맞춰 values()를 넣어준다.
                    _format[ex] = _bs_list[_i]
                    _i += 1
                    #j.append(_domain.get_text())
                _result.append(_format)


if __name__ == "__main__":
    maldomain = MalDomain()
    _result = maldomain.domain_run()

    with open('domain','w',encoding='utf-8') as _f:
            json.dump(_result,_f,ensure_ascii=False,indent=4)
    _f.close()