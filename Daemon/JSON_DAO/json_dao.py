import json,os
from pathlib import Path

class dao(object):
    @classmethod
    def __get_json_to_pyobj(cls,dir:str,mode:str) -> dict:
        with open(dir,mode) as j:
            return json.load(j)

    @classmethod
    def get_data_json(cls) -> dict:
        p = str(Path(os.getcwd()).parent.parent)
        return cls.__get_json_to_pyobj(p + "/data_info.json","r")

    @classmethod
    def get_db_json(cls) -> dict:
        p = str(Path(os.getcwd()).parent.parent)
        return cls.__get_json_to_pyobj(p + "/db.json","r")


if __name__ == "__main__":
    print(dao.get_data_json())
    print(dao.get_db_json())