import sys,requests,json
from pytz import timezone
from typing import MutableSequence
from bs4 import BeautifulSoup
from urllib.parse import urlencode, quote_plus
from datetime import datetime, timedelta

sys.path.append("..")
from KovidMail.Utility.globalutility import GlobalUtilities


class requestData(GlobalUtilities):

    def __init__(self,dbmg):
        #Set variable access : Private
        self.__datapack = dict()
        self.dbmg = dbmg # Database manager address from hub application
        self.getServiceData()

    def getServiceData(self):
        serviceData = self.dbmg.getServiceDatas()
        # If data is not exist it will move to key initiating page
        if not serviceData:
            self.warningMSGHandler("You need to Initiate Keys to run service.")
            self.dbmg.initiateKeys()
            serviceData = self.dbmg.getServiceDatas()
        keyvalue = list(serviceData[0].keys())
        for i in keyvalue:
            if self.dbmg.adminDB['dbKeys'][i]:
                self.__datapack[i] = self.decrypt(serviceData[0][i])
            else:
                self.__datapack[i] = serviceData[0][i]

    # end date : + 1 start date : -1
    def buildRequests(self,end = 1,exec = -1) -> BeautifulSoup:
        self.getServiceData()
        # 코드 실행한 시점
        executedPoint = datetime.now(timezone('Asia/Seoul'))
        endDate = executedPoint + timedelta(days=end)  # 하루뒤의 시간을 의미한다.
        executedPoint = executedPoint + timedelta(days=exec)
        # 시작범위 : Datetime
        searchStart = executedPoint.strftime("%Y%m%d")  # strftime으로 포맷을 맞추어준다."%Y%m%d" : YYYYMMDD형태로 출력
        # 끝범위 : Datetime
        searchEnd = endDate.strftime("%Y%m%d")  # 끝범위를 다음날로 해줘야 오늘 날짜에 대한 값만 나온다.
        # Request Query를 만든다.
        queryParameter = '?' + urlencode({
            quote_plus('serviceKey'): self.__datapack['OPENAPIKEY'],
            quote_plus('pageNo'): 1,
            quote_plus('numOfRows'): 10,
            quote_plus('startCreateDt'): searchStart,
            quote_plus('endCreateDt'): searchEnd
        })
        try:
            response = requests.get(self.__datapack['OPENAPIURL'] + queryParameter).text.encode('utf-8')  # 기본적으로 requests를 인코딩한 반환값은 Byte String이 나오게 된다.
        except requests.exceptions.MissingSchema as e:
            self.globalErrorMSGHandler("Fail while sending request.\nPlease check request url.")
            return False
        except requests.exceptions.InvalidURL as e:
            self.globalErrorMSGHandler("Fail while sending request.\nPlease check request url.")
            return False
        response = response.decode('utf-8')  # bytestring to Normal String
        res = BeautifulSoup(response, 'lxml-xml')
        return res

    def addNews(self) -> MutableSequence:
        basicTags = ["코로나 바이러스", "코로나 백신", "변이 바이러스"]
        # If tag not exist in database initiate database with basic Tags
        tagsinDB = self.dbmg.getNewsTag()
        for i in basicTags:
            if i not in tagsinDB:
                self.dbmg.addTagWithValue(i)
            else:
                pass
        keywords = self.dbmg.getNewsTag()
        headers = {
            'X-Naver-Client-Id' : self.__datapack['NAVERID'],
            'X-Naver-Client-Secret' : self.__datapack['NAVERKEY']
        }
        reqURL = self.__datapack['NAVERREQURL']
        reqURL = [[f"{reqURL}?query={quote_plus(j)}",i] for i,j in enumerate(keywords)]
        newsdict = dict()
        for j in reqURL:
            try:
                try:
                    newsdict[keywords[j[1]]] = requests.get(j[0],headers=headers).json()['items']
                except KeyError as e:
                    self.globalErrorMSGHandler("Fail while sending request to Naver News API.\nPlease check api key or request url.")
                    return False
                except requests.exceptions.MissingSchema as e:
                    self.globalErrorMSGHandler("Fail while sending request.\nPlease check request url.")
                    return False
            except requests.exceptions.MissingSchema as e:
                print(f"Wrong URL : {j[0]} Fail to request")
                return False
        return newsdict

    def reProcessXML(self, BSXML: BeautifulSoup) -> bool:
        #If BSXML is False : it means fail to make request
        if not BSXML:
            return
        res = BSXML
        item = res.findAll('item')
        if len(item) < 2:
            return False
            #Test statement
            #res = self.buildRequests(1,-2)
            #item = res.findAll('item')
        else:
            self.noticeMSGHandler("New data has been updated successfully. Continue process...")
        # Pre process API Request Result
        self.noticeMSGHandler("Pre processing datas...")
        dayBefore = item[1]
        today = item[0]
        dataDate = datetime.strptime(today.find('stateDt').text, "%Y%m%d").date().strftime("%Y-%m-%d")
        totalDecidedPatient = today.find('decideCnt').text
        todayDecidedPatient = str(int(today.find('decideCnt').text) - int(dayBefore.find('decideCnt').text))
        totalDeath = today.find('deathCnt').text
        increasedDeath = str(int(today.find('deathCnt').text) - int(dayBefore.find('deathCnt').text))

        # Graph Data
        # Return : [latest data's date field, length of current date]
        self.noticeMSGHandler("Checking data for graph...")
        getCurrentData = self.dbmg.getCurrentDataOnlyRecentDate()
        # If empty set
        if not getCurrentData:
            self.generateTestData()
        # If have at least one data
        else:
            latestDataDate = getCurrentData[0]
            #today's date as string
            now = (datetime.now(timezone('Asia/Seoul')) + timedelta(days=0)).strftime("%Y-%m-%d")
            #Pass if recent data's date field is same with today
            if now == latestDataDate:
                pass
            #Generate data if it's not
            else:
                self.dbmg.setCurrentData(f"\'{dataDate}\',\'{totalDecidedPatient}\',\'{todayDecidedPatient}\',\'{totalDeath}\',\'{increasedDeath}\'")

        res = self.addNews()
        if not res:
            return False

        dataDictionary = {
            'dataDate': dataDate,
            'data': {
                'totalDecidedPatient': totalDecidedPatient,
                'todayDecidedPatient': todayDecidedPatient,
                'totalDeath': totalDeath,
                'increasedDeath': increasedDeath,
            },
            'news': res
        }
        self.dumpToJSON(dataDictionary)
        return True

    def generateTestData(self):
        datas = self.dbmg.getServiceDatas()
        key = self.decrypt(datas[0]['OPENAPIKEY'])
        url = datas[0]['OPENAPIURL']
        #Call data for 7days
        end = 1
        exec = -7
        executedPoint = datetime.now(timezone('Asia/Seoul'))
        endDate = executedPoint + timedelta(days=end)  # 하루뒤의 시간을 의미한다.
        executedPoint = executedPoint + timedelta(days=exec)
        # 시작범위 : Datetime
        searchStart = executedPoint.strftime("%Y%m%d")  # strftime으로 포맷을 맞추어준다."%Y%m%d" : YYYYMMDD형태로 출력
        # 끝범위 : Datetime
        searchEnd = endDate.strftime("%Y%m%d")  # 끝범위를 다음날로 해줘야 오늘 날짜에 대한 값만 나온다.
        # Request Query를 만든다.
        queryParameter = '?' + urlencode({
            quote_plus('serviceKey'): key,
            quote_plus('pageNo'): 1,
            quote_plus('numOfRows'): 10,
            quote_plus('startCreateDt'): searchStart,
            quote_plus('endCreateDt'): searchEnd
        })
        response = requests.get(url + queryParameter).text.encode(
            'utf-8')  # 기본적으로 requests를 인코딩한 반환값은 Byte String이 나오게 된다.
        response = response.decode('utf-8')  # bytestring to Normal String
        res = BeautifulSoup(response, 'lxml-xml')
        self.dbmg.testData(res)

    def dumpToJSON(self, dicInstance: MutableSequence) -> None:
        with open(self.dataJSONDirectory, 'w') as f:
            json.dump(dicInstance, f, ensure_ascii=False, indent=4)