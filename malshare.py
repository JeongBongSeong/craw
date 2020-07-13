from craw_driver import Craw_Driver
from craw_info import Acc_info
from bs4 import BeautifulSoup as bs
import os
import time
import hashlib
import json
import pickle
from multiprocessing import Pool,Process

class MalShare: #malshare 사이트 크롤링 클래스
    _md5 = None
    _sha_1 = None
    _sha_256 = None
    _f_size = None
    _chrome_driver = None
    _process = None
    _craw_info = None #acc_info 클래스용


    _down_path = None
    #url_hash = None malwares.com 용
    ### 사용한다면 이 부분도 빼서 사용해야 할 듯
    def hash_test(self,file_name): #hash_test함수는 파일 해시 참고해서 이름바꾸는데 사용하지만 사용안함
        f = open(self._down_path+file_name, 'rb')
        _data = f.read()
        f.close()
        
        self._md5 = hashlib.md5(_data).hexdigest()
        self._sha_1 = hashlib.sha1(_data).hexdigest()
        self._sha_256 = hashlib.sha256(_data).hexdigest()
        self._f_size = str(os.stat(self._down_path+file_name).st_size)

        #os.rename(file_name,self._sha_256) #malwares는 이미 해쉬값

        print("MD5: " + self._md5)
        print("SHA-1: " + self._sha_1)
        print("SHA-256: " + self._sha_256)
        print("file_size: "+ self._f_size+" bytes")
###
    def malshare_run(self):
#따로 클래스 정의
        self._chrome_driver = Craw_Driver()
        #self._chrome_driver.hide() #web 띄우지 않음
        self._craw_info = Acc_info(get_url='https://malshare.com/',apikey='9980eac30a5abbad392e1ea61c9317227189c77516f08b6c145cbe3d0af576b9')

        self._chrome_driver.driver_run()
        self._chrome_driver._driver.get(self._craw_info.get_url())
        time.sleep(5)
        
        self._chrome_driver._driver.find_element_by_name('api_key').send_keys(self._craw_info.get_api_key())
        self._chrome_driver._driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/form/button').click()
        time.sleep(5)
###여기부터 날짜 정보 받아오는 부분
        self._chrome_driver._driver.get('https://malshare.com/daily/')
        self._chrome_driver._driver.implicitly_wait(3)

        soup = bs(self._chrome_driver._driver.page_source,'html.parser')
        soup = soup.findAll('a')

        test = []
        
        for text in soup:
            test.append(text.get_text())
        ### 값 수정
            
        _date = test[5:-6]
        _date = "".join(_date)
        _date = _date.split("/")
        _date = _date[0:-1]
### 여기 까지
#현재 실행중인 크롬드라이브의 쿠키를 저장하여 멀티프로세스 적용 시에 새로 띄울 때쿠키 파일을 이용하여 계정정보를 공유한다.
        pickle.dump(self._chrome_driver._driver.get_cookies(), open("cookies.pkl","wb"))

        for _data in _date:
            self._chrome_driver._driver.get("https://malshare.com/daily/"+_data+"/malshare_fileList."+_data+".sha256.txt")
            self._chrome_driver._driver.implicitly_wait(3)
            
            soup1 = bs(self._chrome_driver._driver.page_source,'html.parser')
            soup1 = soup1.findAll('pre',style='word-wrap: break-word; white-space: pre-wrap;')
            
            _hash_values = [] #나눈 값을 리스트 형태로 받아오기 위함
            # bs를 통해서 받아온 값을 각각의 hash로 나누는 작업

            for text in soup1: #get_text()를 이용하기 위함
                _value = str(text.get_text()) #text 추출
            
            _hash_values = _value.split("\n") #text 나누는 작업
            _hash_values = _hash_values[0:-1] #리스트 끝에 ''가 존재함 그래서 잘라냄
            
            _n = int(len(_hash_values)/4) #멀티프로세스 4개를 이용하기위해 4분할
            print(_n)
            
            _hash_values = list(self.divide_list(_hash_values,_n)) #멀티프로세스 4개를 이용하기위해 4분할하는 함수 이용
            
            self._process = []

            for _slc in _hash_values:
                try: #멀티 프로세스 이용
                    _p = Process(target=self.multi_down,args=(_slc,))
                    self._process.append(_p)
                    _p.start()
                except Exception as e:
                    print(e)
            for _p in self._process: #프로세스가 끝날때까지 대기
                _p.join()
                
        time.sleep(10)
        self._chrome_driver._driver.quit() #드라이버 종료
        
    def multi_down(self,hashs): #멀티프로세스로 실행시킬 함수
        try:
            #print(hashs)
            _proc = os.getpid()
            _a = Craw_Driver()
            #_a.hide()
            _a.driver_run()
            _a._driver.set_window_size(800,200)
            _cookies = pickle.load(open("cookies.pkl","rb")) #쿠키 로드
            _a._driver.get("https://malshare.com/") #인증을 위한 접속

            for _cookie in _cookies: #쿠키 적용
                _a._driver.add_cookie(_cookie)
                
            for _sha256 in hashs: #파일 다운로드
                _a._driver.get("https://malshare.com/sampleshare.php?action=getfile&hash="+_sha256)
                print("{}///{}".format(_proc,_sha256))
                
        except Exception as e:
            print(e)
        finally:
            time.sleep(5)
            _a._driver.quit()

    
    def divide_list(self,l,n): #mulit processing을 위한 해시값 분할 작업
        #n=len(l)/4
        for i in range(0,len(l),n):
            yield l[i:i + n]


if __name__ == "__main__":
    malshare = MalShare()
    malshare.malshare_run()