import requests
from Daemon.DataProcessor.request_interface import interface

class covidRequest(interface):

    _instance = None
    __dataKey = "Covid19"

    # Singleton Pattern
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls,*args,**kwargs)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.blocks = self._get_data_block(self.__dataKey)

    def request_to_api(self):
        pass

    def preprocess_json_result(self):
        pass


if __name__ == "__main__":
    c = covidRequest()
    c.request_to_api()