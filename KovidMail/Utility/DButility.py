import sys
from datetime import datetime
from enum import Enum
import pymysql as sql
import pymysql.err

from KovidMail.Utility.globalutility import GlobalUtilities
from KovidMail.Utility.configutility import ConfigurationWriter

class dbutility(GlobalUtilities):
    config = None
    dbfield = None
    sqlConnection = None
    __option = Enum('option', ["Initiate_Keys", "Edit_Key", "Reset_Database", "Add_Tag", "Delete_Tag", "exit"])

    def __init__(self,configutil : ConfigurationWriter):
        self.configutil = configutil
        self.readConfigAndGetConnection()
        self.essentialDatabaseInitiator()

    def reconnect(self):
        self.readConfigAndGetConnection()


    def readConfigAndGetConnection(self):
        def exceptionHandle(self):
            self.globalErrorMSGHandler("Service Locked. Can't connect to SQL due to wrong information.")
            self.globalErrorMSGHandler("Move to configuration writer.")
            self.pressKeyToContinue()
            self.configutil.writer()
            self.readConfigAndGetConnection()
        try:
            self.config = self.readConfigYaml()
            self.dbfield = self.config['sqlConnection']
            self.sqlConnection = sql.connect(
                user = self.decrypt(self.dbfield['user']['value']),
                port = int(self.dbfield['port']['value']),
                password= self.decrypt(self.dbfield['sqlpassword']['value']),
                host = self.dbfield['host']['value']
            )
            self.sqlCursor = self.sqlConnection.cursor(sql.cursors.DictCursor)
            self.noticeMSGHandler("Successfully connected to MySQL.")
        #SQL Connection 오류시 Config File 다시 작성 한 후, 다시 연결
        except sql.err.OperationalError as e:
            exceptionHandle(self)
        # 초기화 후 NoneType에 대해 decrypt에서 ASCII오류 발생시
        except TypeError as e:
            exceptionHandle(self)
        except ValueError as e:
            self.globalErrorMSGHandler("Some values of your configuration data make collision while connecting to SQL.")
            self.globalErrorMSGHandler("Please write SQL configuration information again.")
            self.configutil.writer()
            self.readConfigAndGetConnection()

    def returnConnectionStatus(self):
        if self.sqlConnection.open:
            return "Connected"
        else:
            return "Fail to connect."

    def getDatabaseList(self):
        state = "show databases;"
        self.sqlCursor.execute(state)
        lst = [i['Database'] for i in self.sqlCursor.fetchall()]
        return lst

    def getTableList(self,db):
        self.sqlCursor.execute(f"USE {db}")
        self.sqlCursor.execute("SHOW TABLES;")
        res = self.sqlCursor.fetchall()
        #List : Return Value
        ret = []
        for x in res:
            for q,w in x.items():
                ret.append(w)
        return ret

    def endConnection(self):
        self.sqlConnection.close()

    def checkDatabaseAndInitiateTable(self,databaseInfo):
        # get database name
        dbname = databaseInfo["databasename"]
        # get key name of sql schema
        sqlschema = databaseInfo[databaseInfo['sqlschema']]
        self.sqlCursor.execute(f"CREATE DATABASE {dbname}")
        self.noticeMSGHandler(f"Create database {dbname}")
        self.sqlCursor.execute(f"USE {dbname}")
        self.sqlCursor.execute(f"{sqlschema}")
        self.noticeMSGHandler(f"Create table : {databaseInfo['tablename']} at database {dbname}")

    def dropCurrentDataDataBaseIfExist(self):
        # This method is for Daemon initialization
        # Drop current database if exist
        state = "drop database CURRENTDATA;"
        try:
            self.sqlCursor.execute(state)
        except pymysql.err.OperationalError:
            pass

    def onlyInitiateTable(self,databaseInfo):
        dbname = databaseInfo["databasename"]
        self.sqlCursor.execute(f"USE {dbname}")
        sqlschema = databaseInfo[databaseInfo['sqlschema']]
        self.noticeMSGHandler(f"Create table : {databaseInfo['tablename']} at database {dbname}")
        self.sqlCursor.execute(f"{sqlschema}")

# Basic Database initiator and Checker. Not as Option
    def essentialDatabaseInitiator(self):
        def returnNotExistMSG(msg):
            return f"Database '{msg}' not exist. Initiate database {msg}"
        def returnExistMSG(msg):
            return f"Database '{msg}' exist."
        # Get Existing Database lists
        # if 'userlist' database not exist in database
        for i in self.dbSchemaVariableList:
            getDBList = self.getDatabaseList()
            # If database not Exist
            # add (databasename).lower() : For windows and mysql 8.0 lowerversion compatibility
            if i['databasename'] not in getDBList and i['databasename'].lower() not in getDBList:
                self.checkDatabaseAndInitiateTable(i)
            # If database Exist
            else:
                self.noticeMSGHandler(returnExistMSG(i['databasename']))
                getTableList = self.getTableList(i['databasename'])
                if i['tablename'] not in getTableList and i['tablename'].lower() not in getTableList:
                    self.onlyInitiateTable(i)
                else:
                    pass

    def initiateKeys(self):
        print("=" * 60)
        print("Service Key Initiator. Pre existing Datas will be delete.")
        print("=" * 60)
        dbkey = self.adminDB["dbKeys"]
        keys = list(self.adminDB["dbKeys"].keys())
        dbName = self.adminDB["databasename"]
        tableName = self.adminDB["tablename"]
        self.sqlCursor.execute(f"USE {dbName}")
        self.sqlCursor.execute(f"DELETE FROM  {tableName}")
        keyBox = []

        for i in range(len(keys)):
            loop = True
            while loop:
                res = None
                try:
                    if not dbkey[keys[i]]:
                        res = self.normalInput("Save Key : %13s >> " % keys[i])
                    else:
                        # 암호화 된 byte string값에 대해 string 변환 후 넣어준다.
                        res = self.hideInput("Save Key : %13s >> " % keys[i])
                        res = res.decode('utf-8')
                except ValueError as e:
                    pass
                except AttributeError as e:
                    pass
                if not res:
                    self.warningMSGHandler("Type again")
                else:
                    keyBox.append(f"\'{res}\'")
                    loop = False
        sqlState = f"""
            INSERT INTO adminDatas ({','.join(keys)})
            VALUES ({','.join(keyBox)});
        """
        try:
            self.sqlCursor.execute(sqlState)
            self.sqlConnection.commit()
        except sql.err.DataError as e:
            # Exception : In condition of too long value
            self.warningMSGHandler("Value out of range re-process this process")
            self.pressKeyToContinue()
            self.initiateKeys()
        # Programming Error : For not supported save type value
        except sql.err.ProgrammingError as e:
            self.clearConsole()
            self.globalErrorMSGHandler("You may type unsupported type value. Please try again.")
            self.pressKeyToContinue()
            self.initiateKeys()

    def addTag(self):
        self.clearConsole()
        db = self.newsTag
        newtag = self.normalInput("새로 추가할 태그 입력하기 >> ")
        if not newtag:
            self.warningMSGHandler("잘못된 입력형태입니다. 추가가 불가능합니다.")
            self.pressKeyToContinue()
        else:
            if newtag in self.getNewsTag():
                self.noticeMSGHandler("이미 존재하는 태그입니다. 추가가 불가능합니다.")
                self.pressKeyToContinue()
            else:
                self.sqlCursor.execute(f"USE {db['databasename']}")
                sqlState = f"INSERT INTO {db['tablename']}(tag) VALUES(\'{newtag}\')"
                self.sqlCursor.execute(sqlState)
                self.sqlConnection.commit()
                self.noticeMSGHandler("태그 추가가 완료되었습니다.")
                self.pressKeyToContinue()

    def addTagWithValue(self, value):
        db = self.newsTag
        self.sqlCursor.execute(f"USE {db['databasename']}")
        sqlState = f"INSERT INTO {db['tablename']}(tag) VALUES(\'{value}\')"
        self.sqlCursor.execute(sqlState)
        self.sqlConnection.commit()

    def getNewsTag(self):
        db = self.newsTag
        self.sqlCursor.execute(f"USE {db['databasename']}")
        sqlState = f"SELECT * FROM {db['tablename']}"
        self.sqlCursor.execute(sqlState)
        datas = self.sqlCursor.fetchall()
        return [i['tag'] for i in datas]


    def deleteTag(self):
        self.clearConsole()
        newtag = self.getNewsTag()
        opt = Enum('options', newtag)
        db = self.newsTag
        loop = True
        if not newtag:
            self.noticeMSGHandler("삭제할 태그가 존재하지 않습니다.")
            self.pressKeyToContinue()
            return
        while loop:
            res = self.returnSelectedOption(opt)
            if not res:
                loop = False
            else:
                res = str(res.name)
                self.sqlCursor.execute(f"USE {db['databasename']}")
                sqlState = f"DELETE FROM {db['tablename']} WHERE tag=\'{res}\'"
                self.sqlCursor.execute(sqlState)
                self.sqlConnection.commit()
                loop = False
        print(f"Left Tags : {','.join(self.getNewsTag())}")
        self.pressKeyToContinue()

    def deleteDatabase(self):
        loop = True
        while loop:
            self.warningMSGHandler("데이터 베이스가 삭제되면 입력된 모든 값 또한 삭제되게 됩니다. 삭제하시겠습니까?")
            opt = None
            try:
                opt = self.normalInput("Yes 혹은 No를 입력하여 승인 혹은 보류하기 >> ")
            except ValueError as e:
                self.warningMSGHandler("잘못된 값이 입력되었습니다.")
            if not opt:
                loop = False
            else:
                getDBList = self.getDatabaseList()
                if opt.lower() == "yes":
                    for i in self.dbSchemaVariableList:
                        getDBList = self.getDatabaseList()
                        if i["databasename"] in getDBList or i["databasename"].lower() in getDBList:
                            self.noticeMSGHandler(f"Database deleted permanantly : {i['databasename']}")
                            self.sqlCursor.execute(f"DROP DATABASE {i['databasename']}")
                        else:
                            pass
                    self.noticeMSGHandler("데이터 베이스 삭제 작업이 완료되었습니다.")
                    loop = False
                elif opt.lower() == "no":
                    self.clearConsole()
                    loop = False
                else:
                    self.clearConsole()
                    self.warningMSGHandler("잘못된 값이 입력되었습니다. 'Yes' 혹은 'No'만 입력해주세요.")

    #Combined method with datarequest.generateTestData
    def testData(self, res):
        item = res.findAll('item')
        self.sqlCursor.execute(f"USE CURRENTDATA")
        for p in range(len(item) - 2, -1, -1):
            i = item[p]
            li = []
            # date
            li.append(f"\'{datetime.strptime(i.find('stateDt').text, '%Y%m%d').date().strftime('%Y-%m-%d')}\'")
            # total decided patient
            li.append(f"\'{i.find('decideCnt').text}\'")
            # today decided patient
            li.append(f"\'{str(int(i.find('decideCnt').text) - int(item[p + 1].find('decideCnt').text))}\'")
            # total death
            li.append(f"\'{i.find('deathCnt').text}\'")
            # increased Death
            li.append(f"\'{str(int(i.find('deathCnt').text) - int(item[p + 1].find('deathCnt').text))}\'")
            self.sqlCursor.execute(
                f"INSERT INTO current(Date,totaldecidedPatient,todaydecidedPatient,totalDeath,increasedDeath) VALUES({','.join(li)})")
            self.sqlConnection.commit()

    def getServiceDatas(self):
        db = self.adminDB
        self.sqlCursor.execute(f"USE {db['databasename']}")
        sqlState = f"SELECT * FROM {db['tablename']}"
        self.sqlCursor.execute(sqlState)
        return self.sqlCursor.fetchall()

    def getCurrentData(self):
        db = self.kovidCurrentData
        self.sqlCursor.execute(f"USE {db['databasename']}")
        sqlState = f"SELECT * FROM {db['tablename']}"
        self.sqlCursor.execute(sqlState)
        datas = self.sqlCursor.fetchall()
        return datas[-7:] # Return Recent 7 datas

    def getCurrentDataOnlyRecentDate(self):
        '''
        This method will be deprecated soon
        '''
        base = self.getCurrentData()
        renew = list()
        if not base:
            return False
        else:
            return [base[-1]['Date'],len(base)]

    def setCurrentData(self, state):
        db = self.kovidCurrentData
        self.sqlCursor.execute(f"USE {db['databasename']}")
        self.sqlCursor.execute(
            f"INSERT INTO current(Date,totaldecidedPatient,todaydecidedPatient,totalDeath,increasedDeath) VALUES({state})")
        self.sqlConnection.commit()

    # Return Subscriber List
    def getSubscriberList(self):
        db = self.kovidMailDB
        self.sqlCursor.execute(f"USE {db['databasename']}")
        sqlState = f"SELECT * FROM {db['tablename']}"
        self.sqlCursor.execute(sqlState)
        datas = self.sqlCursor.fetchall()
        return [i['email'] for i in datas]

    # Return Mail data for SMTP
    def returnMailInfo(self):
        db = self.adminDB
        self.sqlCursor.execute(f"USE {db['databasename']}")
        sqlState = f"SELECT HOSTERMAIL,HOSTERMAILPW FROM {db['tablename']}"
        self.sqlCursor.execute(sqlState)
        return self.sqlCursor.fetchall()

        # Add new Subscriber
    def addNewSubscriber(self, mail):
        db = self.kovidMailDB
        self.sqlCursor.execute(f"USE {db['databasename']}")
        sqlState = f"INSERT INTO {db['tablename']}(email) VALUES(\'{mail}\')"
        self.sqlCursor.execute(sqlState)
        self.sqlConnection.commit()

    # Delete new Subscriber
    def deleteSub(self, mail):
        db = self.kovidMailDB
        self.sqlCursor.execute(f"USE {db['databasename']}")
        sqlState = f"DELETE FROM {db['tablename']} WHERE email=\'{mail}\'"
        self.sqlCursor.execute(sqlState)
        self.sqlConnection.commit()

    def editIndividualKey(self):
        li = list(self.adminDB["dbKeys"].keys())
        opt = Enum('opt', li)
        loop = True
        while loop:
            self.clearConsole()
            res = self.returnSelectedOption(opt)
            if not res:
                loop = False
            else:
                self.sqlCursor.execute(f"USE {self.adminDB['databasename']}")
                changeValue = str(res.name)
                self.clearConsole()
                value = None
                print(f"Selected Option : {changeValue}")
                try:
                    if self.adminDB["dbKeys"][changeValue]:
                        value = self.hideInput(f"Enter data you want to change / Field : {changeValue} >> ").decode('utf-8')
                        if not value:
                            self.warningMSGHandler(self.wrongInpMSG)
                        else:
                            self.sqlCursor.execute(f"UPDATE {self.adminDB['tablename']} SET {changeValue}=\'{value}\'")
                            self.sqlConnection.commit()
                            loop = False
                    else:
                        value = self.normalInput(f"Enter data you want to change / Field : {changeValue} >> ")
                        if not value:
                            self.warningMSGHandler(self.wrongInpMSG)
                        else:
                            self.sqlCursor.execute(f"UPDATE {self.adminDB['tablename']} SET {changeValue}=\'{value}\'")
                            self.sqlConnection.commit()
                            loop = False
                # Wrong Types of Input
                except sql.err.ProgrammingError as e:
                    self.globalErrorMSGHandler(f"Typed Value : {value} | This value is unable to be saved.")
                    self.pressKeyToContinue()
                    self.editIndividualKey()

    def selectOption(self):
        mainFunctionMapper = {
            "Initiate_Keys": self.initiateKeys,
            "Edit_Key": self.editIndividualKey,
            "Reset_Database": self.deleteDatabase,
            "Add_Tag": self.addTag,
            "Delete_Tag": self.deleteTag,
        }
        self.clearConsole()
        loop = True
        while loop:
            self.essentialDatabaseInitiator()
            res = self.returnSelectedOption(self.__option)
            if not res:
                loop = False
            else:
                res = str(res.name)
                self.clearConsole()
                if res == "exit":
                    loop = False
                else:
                    mainFunctionMapper[res]()
            self.clearConsole()