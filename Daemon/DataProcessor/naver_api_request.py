import requests
from urllib.parse import quote_plus
from Daemon.DataProcessor.request_interface import  interface

class naverRequest(interface):
    _instance = None
    __dataKey = "NaverNews"
    __basicTags = ["코로나 바이러스", "코로나 백신", "변이 바이러스"]

    #Singleton Pattern
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls,*args,**kwargs)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.blocks = self._get_data_block(self.__dataKey)

    def request_to_api(self):
        response_bucket = dict()

        #If tags are empty get default tags
        tag = naverRequest.__basicTags

        # Build Request URLs
        request_urls = [(i,f"{self.blocks['endpoint']}?query={quote_plus(j)}") for i,j in enumerate(tag)]

        #Request Header
        headers = {
            'X-Naver-Client-Id' : self.blocks["data"]["id"],
            'X-Naver-Client-Secret' : self.blocks["data"]["secret"]
        }
        try:
            for i,j in request_urls:
                pass
        except requests.exceptions.RequestException as e:
            pass


    def preprocess_json_result(self):
        pass