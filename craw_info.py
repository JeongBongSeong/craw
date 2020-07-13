
class Acc_info: #공유 값 사용용도
    _url = None
    _api_key = None
    _user_id = None
    _user_pwd = None
    def __init__(self,get_url = None,apikey = None,userid = None,userpwd =None):
        self._url = get_url
        self._api_key = apikey
        self._user_id = userid
        self._user_pwd = userpwd

    def get_url(self):
        return self._url

    def get_api_key(self):
        return self._api_key

    def get_user_id(self):
        return self._user_id
        
    def get_user_pwd(self):
        return self._user_pwd