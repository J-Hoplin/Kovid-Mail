'''
Code written by Hoplin

'''

import os,yaml,base64,getpass,pymysql,platform
from typing import Any

class textColor:
    '''
    Class : For text color in CLI UI
    '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class GlobalUtilities(object):
    __forceCloseWarningMSG = "강제종료가 감지되었습니다. 세션을 정상종료해주시기 바랍니다."
    __configLocation = 'config.yml'
    dataJSONDirectory = 'KovidMail/Datas/smtpSendDatas.json'
    graphDirectory = 'KovidMail/Templates/graph.png'
    wrongInpMSG = "잘못된 입력값입니다. 다시 입력해주세요."
    newsTag = {
        "databasename": "SERVICEDATAS",
        "sqlschema": "newstag",
        "tablename": "newstag",
        "dbKeys": {
            "tag": False
        },
        "newstag": """
                        CREATE TABLE newstag(
                            tag VARCHAR(70) NOT NULL
                        )DEFAULT CHARSET=utf8;
                        """
    }
    kovidMailDB = {
        "databasename": "SUBSCRIBERS",
        "sqlschema": "userlist",
        "tablename": "subslist",
        "dbKeys": {
            "email": False
        },
        "userlist": """
                        CREATE TABLE subslist(
                            ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                            email VARCHAR(70) NOT NULL
                        )DEFAULT CHARSET=utf8;
                        """
    }
    adminDB = {
        "databasename": "SERVICEDATAS",
        "sqlschema": "serviceDB",
        "tablename": "adminDatas",
        "dbKeys": {
            "OPENAPIKEY": True,
            "OPENAPIURL": False,
            "NAVERREQURL": False,
            "NAVERID": False,
            "NAVERKEY": True,
            "HOSTERMAIL": False,
            "HOSTERMAILPW": True
        },
        "serviceDB": """
                        CREATE TABLE adminDatas(
                            OPENAPIKEY VARCHAR(150),
                            OPENAPIURL VARCHAR(300),
                            NAVERREQURL VARCHAR(150),
                            NAVERID VARCHAR(150),
                            NAVERKEY VARCHAR(300),
                            HOSTERMAIL VARCHAR(100),
                            HOSTERMAILPW VARCHAR(100)
                        )DEFAULT CHARSET=utf8;
            """
    }

    kovidCurrentData = {
        "databasename": "CURRENTDATA",
        "sqlschema": "current",
        "tablename": "current",
        "current": """
                        CREATE TABLE current(
                            Date VARCHAR(150),
                            totaldecidedPatient VARCHAR(150),
                            todaydecidedPatient VARCHAR(150),
                            totalDeath VARCHAR(150),
                            increasedDeath VARCHAR(150)
                        )DEFAULT CHARSET=utf8;
            """
    }

    dbSchemaVariableList = [newsTag,kovidMailDB, adminDB, kovidCurrentData]
    @classmethod
    def clearConsole(cls) -> None:
        #Windows Clear command
        if platform.system() == 'Windows':
            os.system('cls')
        #Darwin type OS Clear Command(Linux / Mac OS)
        else:
            os.system('clear')

    @classmethod
    def pressKeyToContinue(cls) -> None:
        try:
            input("Press any key to continue...")
        except ValueError as e:
            pass
        except KeyboardInterrupt as e:
            pass

    @classmethod
    def globalErrorMSGHandler(cls,message):
        print(f"{textColor.FAIL}Error : {message}{textColor.ENDC}")

    # base64.b64encode / base64.b64decode document : https://docs.python.org/ko/3.7/library/base64.html
    # encrypt data : 사실 암호화가 아닌 유사 기능입니다
    def encrypt(self, value) -> base64:
        return base64.b64encode(value.encode("UTF-8"))

    # decrypt data
    def decrypt(self, value) -> Any:
        try:
            return base64.b64decode(value).decode('UTF-8')
        # Value가 None일 경우에 value를 그대로 return 한다.
        except AttributeError as e:
            self.errorMSGHandler(f"Some error occured while decrypting data : {e}")
            return value

    def connectionMSGHandelr(self,con,message):
        print(f"{con}{textColor.OKGREEN}{message}{textColor.ENDC}")

    def connectionOddMSGHandler(self,con,message):
        print(f"{con}{textColor.FAIL}{message}{textColor.ENDC}")

    def noticeMSGHandler(self,message):
        print(f"{textColor.OKBLUE}Software Notice : {message}{textColor.ENDC}")

    def warningMSGHandler(self,message):
        print(f"{textColor.WARNING}Warning : {message}{textColor.ENDC}")

    def errorMSGHandler(self,message,additionalMSG = None):
        print(f"{textColor.FAIL}Error : {message} / {additionalMSG}{textColor.ENDC}")

    #이 메소드 호출 후에는 해당 반환값을 저장하는 변수가 있어야함
    def readConfigYaml(self):
        try:
            # Read yaml and save as Python object
            with open(self.__configLocation) as f:
                res = yaml.load(f, Loader=yaml.FullLoader)
            return res
        except FileNotFoundError as e:
            self.errorMSGHandler(e, "Process terminate due to not existing file : Please check if config.yml exist.")


    #정상 입력이면 value를 비정상적인 입력이면 false를 반환
    def normalInput(self,msg) -> Any:
        loop = True
        try:
            while loop:
                value = input(msg)
                if value == "/back":
                    loop = False
                    return False
                else:
                    loop = False
                    return value
        except KeyboardInterrupt as e:
            return False

    # Return Encrypted value
    def hideInput(self,msg) -> Any:
        loop = True
        try:
            while loop:
                value = str(getpass.getpass(msg))
                if value == "/back":
                    loop = False
                    return False
                else:
                    loop = False
                    return self.encrypt(value)
        except KeyboardInterrupt as e:
            return False

    def onlyHiddenInput(self,msg) -> bool:
        loop = True
        try:
            while loop:
                value = str(getpass.getpass(msg))
                if value == "/back":
                    loop = False
                    return False
                else:
                    loop = False
                    return value
        except KeyboardInterrupt as e:
            return False

    def saveConfigYaml(self,yamlinstance) -> yaml:
        with open(self.__configLocation, 'w') as f:
            yaml.dump(yamlinstance,f)

    def returnSelectedOption(self, li,ymlIns = False) -> Any:
        opt = [[f'{i.value}. {i.name}',i.name] for i in li]
        loop = True
        while loop:
            print("=" * 20)
            for i in opt:
                if not ymlIns:
                    print(i[0])
                else:
                    #Args : ymlIns : Condition of if it's request related to yaml configuration
                    value = ymlIns[i[1]]
                    #  1번째 조건 : 암호화에 따른 출력 변화 2번째 조건 : value가 None일 경우를 대비하여 조건걸어놓음
                    if value['encrypt'] and value['value']:
                        print(f"{i[0]} : {self.decrypt(value['value'])}")
                    else:
                        print(f"{i[0]} : {value['value']}")
            print("=" * 20)
            try:
                select = input(">> ")
                # Command : /back : go back to previous page
                if select == "/back":
                    self.clearConsole()
                    return False
                else:
                    select = int(select)
                    if 1 <= select <= len(opt):
                        return li(select)
                    else:
                        self.clearConsole()
                        self.warningMSGHandler(self.wrongInpMSG)
            except ValueError as e:
                self.clearConsole()
                self.warningMSGHandler(self.wrongInpMSG)
                pass
            except KeyboardInterrupt as e:
                self.clearConsole()
                return False