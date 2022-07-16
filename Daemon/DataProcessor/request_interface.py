from Daemon.JSON_DAO.json_dao import dao
from abc import *


class interface(object):
    __jsonBlock = None

    def __init__(self):
        self.__jsonBlock = dao.get_data_json()

    def json_parser(self):
        pass

    def get_bs_instance(self):
        pass

    def _get_data_block(self, key: str) -> dict:
        return self.__jsonBlock[key]

    @abstractmethod
    def request_to_api(self):
        pass

    @abstractmethod
    def preprocess_json_result(self):
        pass
