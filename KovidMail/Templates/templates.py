import random
from datetime import datetime, timedelta
from pytz import timezone

class template:
    '''

    Deprecated : templates.py will be replaced with Python Django Base template ( from Official Release 1.0 )

    Template1 : Will be used in official version release. This HTML layout is not for mobile user, but for smart watch users.

    Template2 : For mobile mail application users
    '''
    def __init__(self):
        self.easteregg = "https://github.com/J-hoplin1/KovidMail"
        #How many days will data contain
        self.graphRange = 7

    def Template1(self,databox):
        covidData = databox["data"]
        executed = (datetime.now(timezone('Asia/Seoul')) + timedelta(days=0)).strftime("%Y년 %m월 %d일")
        # Without Topic News
        __htmltemplate1 = f"""
            <!DOCTYPE html>
                <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Document</title>
                        <style>@import url('https://fonts.googleapis.com/css2?family=Readex+Pro:wght@200&display=swap');</style>
                        <style>
                            * {{
                                font-family: 'Readex Pro', sans-serif;
                            }}

                            body{{
                                margin: 0px;
                                padding: 0px;
                            }}
                            div.main-layout{{
                                height: 90%;
                                width: 100%;
                                padding: 0px;
                            }}

                            div.main-title{{
                                margin: 15px 0px;
                            }}

                            h1{{
                                font-size: 32px;
                                border-bottom: 2px solid #8D94BA;
                            }}
                            /*div.float-container{{
                                display: flex;  
                                justify-content: space-around;
                                height: 40%;
                            }}*/
                            div.basic-information{{
                                text-align: center;
                                padding: 15px 15px;
                                font-size: 20px;
                                width: 30%;
                                height: 100px;
                            }}
                            div.img-container{{
                                width:600px;
                                padding: 10px 0px;
                            }}
                            img.graph{{
                                width: 600px;
                                height: 400px;
                            }}
                            p {{
                                line-height: 1.5;
                                font-size: 19px;
                                width: 100%;
                            }}

                            h3{{
                                margin: 0;
                                text-align: left;
                            }}
                            a{{
                                text-decoration: none;
                            }}
                            a:link{{
                                color: brown;
                                text-decoration: none;
                            }}
                            a:visited{{
                                color: brown;
                                text-decoration: none;
                            }}
                            li{{
                                line-height: 1.5;
                                font-size: 19px;
                                width: 100%;
                                margin: 19px;
                                list-style-type : circle;
                            }}
                            li.source{{
                                font-size: 15px;
                                line-height: 1.5;
                            }}
                        </style>
                    </head>
                    <body style="font-family: 'Readex Pro', sans-serif;margin: 0px;padding: 0px;">
                        <div class="main-layout" style="height: 90%;width: 100%;padding: 0px;">
                            <h1 style="font-size: 32px;border-bottom: 2px solid #8D94BA;">{executed}<br>코로나 바이러스 브리핑</h1>
                            <h2>< 금일 신규 확진자 및 사망자 정보 ></h2>
                            <p style="line-height: 1.5;font-size: 19px;width: 100%;">전체 확진자 수 : {format(int(covidData['totalDecidedPatient']),',')}명</p>
                            <p style="line-height: 1.5;font-size: 19px;width: 100%;">전체 사망자 수: {format(int(covidData['totalDeath']),',')}명</p>
                            <p style="line-height: 1.5;font-size: 19px;width: 100%;">일일 신규 확진자 수 : {format(int(covidData['todayDecidedPatient']),',')}명</p>
                            <p style="line-height: 1.5;font-size: 19px;width: 100%;">일일 사망자 수 : {format(int(covidData['increasedDeath']),',')}명</p>
                            <div class="img-container" style="padding: 10px 0px;width:600px;">
                                <h3 class="plot-title" style="margin: 0; text-align: center;">지난 {self.graphRange}일간 확진자수 추이 그래프</h3>
                                <img style="width: 600px;height: 400px;" src="cid:graph" class="graph">
                            </div>
                            <br>
                            <br>
                            <p style="line-height: 1.5;font-size: 19px;width: 100%;">< 데이터 출처 ></p>
                            <ul>
                                <li style="font-size: 16px;line-height: 1.5;" class="source"><a href="https://www.data.go.kr/">공공데이터 포털</a> </li>
                                <li style="font-size: 16px;line-height: 1.5;" class="source"><a href="https://developers.naver.com/docs/serviceapi/search/news/news.md#%EB%89%B4%EC%8A%A4">Naver News Search API</a></li>
                            </ul>
                            <p style="line-height: 1.5;font-size: 19px;width: 100%;">대한민국 중앙방역대책본부 코로나바이러스 감염증 현황 <a href="http://ncov.mohw.go.kr/">바로가기</a></p>
                            <p style="line-height: 1.5;font-size: 19px;width: 100%;">제작 : Hoplin / Source Code Opened at <a href="https://github.com/J-hoplin1/Kovid-Mail">Github</a></p>
                        </div>
                    </body>
            </html>
                """

        return __htmltemplate1

    def Template2(self,databox):
        covidData = databox["data"]
        topicNews = databox["news"]

        executed = (datetime.now(timezone('Asia/Seoul')) + timedelta(days=0)).strftime("%Y년 %m월 %d일")
        #Select Random Topics from Topics
        topicKeys = random.sample(list(topicNews.keys()),3)
        #Topic1
        newsCovid1 = list(range(len(topicNews[topicKeys[0]])))
        newsCovid1 = [topicNews[topicKeys[0]][i] for i in random.sample(newsCovid1,3)]
        inlinetemplate1 = ""
        for i in range(len(newsCovid1)):
            inlinetemplate1 += f"<li style=\"line-height: 1.5;font-size: 19px;width: 100%;margin: 19px;\">Topic {i + 1} | <a href=\"{newsCovid1[i]['originallink']}\">{newsCovid1[i]['title']}</a></li>"
        #Topic2
        newsCovid2 = list(range(len(topicNews[topicKeys[1]])))
        newsCovid2 = [topicNews[topicKeys[1]][i] for i in random.sample(newsCovid2,3)]
        inlinetemplate2 = ""
        for i in range(len(newsCovid2)):
            inlinetemplate2 += f"<li style=\"line-height: 1.5;font-size: 19px;width: 100%;margin: 19px;\">Topic {i + 1} | <a href=\"{newsCovid2[i]['originallink']}\">{newsCovid2[i]['title']}</a></li>"
        #Topic3
        newsCovid3 = list(range(len(topicNews[topicKeys[2]])))
        newsCovid3 = [topicNews[topicKeys[2]][i] for i in random.sample(newsCovid3,3)]
        inlinetemplate3 = ""
        for i in range(len(newsCovid3)):
            inlinetemplate3 += f"<li style=\"line-height: 1.5;font-size: 19px;width: 100%;margin: 19px;\">Topic {i + 1} | <a href=\"{newsCovid3[i]['originallink']}\">{newsCovid3[i]['title']}</a></li>"

        __htmltemplate2 = f"""
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
                <style>@import url('https://fonts.googleapis.com/css2?family=Readex+Pro:wght@200&display=swap');</style>
                <style>
                    * {{
                        font-family: 'Readex Pro', sans-serif;
                    }}

                    body{{
                        margin: 0px;
                        padding: 0px;
                    }}
                    div.main-layout{{
                        height: 90%;
                        width: 100%;
                        padding: 0px;
                    }}

                    div.main-title{{
                        margin: 15px 0px;
                    }}

                    h1{{
                        font-size: 32px;
                        border-bottom: 2px solid #8D94BA;
                    }}
                    /*div.float-container{{
                        display: flex;  
                        justify-content: space-around;
                        height: 40%;
                    }}*/
                    div.basic-information{{
                        text-align: center;
                        padding: 15px 15px;
                        font-size: 20px;
                        width: 30%;
                        height: 100px;
                    }}
                    div.img-container{{
                        width:600px;
                        padding: 10px 0px;
                    }}
                    img.graph{{
                        width: 600px;
                        height: 400px;
                    }}
                    p {{
                        line-height: 1.5;
                        font-size: 19px;
                        width: 100%;
                    }}

                    h3{{
                        margin: 0;
                        text-align: left;
                    }}
                    a{{
                        text-decoration: none;
                    }}
                    a:link{{
                        color: brown;
                        text-decoration: none;
                    }}
                    a:visited{{
                        color: brown;
                        text-decoration: none;
                    }}
                    li{{
                        line-height: 1.5;
                        font-size: 19px;
                        width: 100%;
                        margin: 19px;
                        list-style-type : circle;
                    }}
                    li.source{{
                        font-size: 15px;
                        line-height: 1.5;
                    }}
                </style>
            </head>
            <body style="font-family: 'Readex Pro', sans-serif;margin: 0px;padding: 0px;">
                <div class="main-layout" style="height: 90%;width: 100%;padding: 0px;">
                    <h1 style="font-size: 32px;border-bottom: 2px solid #8D94BA;">{executed}<br>코로나19 바이러스 일일 브리핑</h1>
                    <h2>< 금일 신규 확진자 및 사망자 정보 ></h2>
                    <p style="line-height: 1.5;font-size: 19px;width: 100%;">전체 확진자 수 : {format(int(covidData['totalDecidedPatient']),',')}명</p>
                    <p style="line-height: 1.5;font-size: 19px;width: 100%;">전체 사망자 수: {format(int(covidData['totalDeath']),',')}명</p>
                    <p style="line-height: 1.5;font-size: 19px;width: 100%;">일일 신규 확진자 수 : {format(int(covidData['todayDecidedPatient']),',')}명</p>
                    <p style="line-height: 1.5;font-size: 19px;width: 100%;">일일 사망자 수 : {format(int(covidData['increasedDeath']),',')}명</p>
                    <div class="img-container" style="padding: 10px 0px;width:600px;">
                        <h3 class="plot-title" style="margin: 0; text-align: center;">지난 {self.graphRange}일간 확진자수 추이 그래프</h3>
                        <img style="width: 600px;height: 400px;border-radius: 6px;" src="cid:graph" class="graph">
                    </div>
                    <h2>< 주요 토픽 뉴스 ></h2>
                    <h3>#{topicKeys[0]}</h3>
                    <ul>
                        {inlinetemplate1}
                    </ul>
                    <h3>#{topicKeys[1]}</h3>
                    <ul>
                        {inlinetemplate2}
                    </ul>
                    <h3>#{topicKeys[2]}</h3>
                    <ul>
                        {inlinetemplate3}
                    </ul>
                    <br>
                    <br>
                    <p style="line-height: 1.5;font-size: 19px;width: 100%;">< 데이터 출처 ></p>
                    <ul>
                        <li style="font-size: 16px;line-height: 1.5;" class="source"><a href="https://www.data.go.kr/">공공데이터 포털</a> </li>
                        <li style="font-size: 16px;line-height: 1.5;" class="source"><a href="https://developers.naver.com/docs/serviceapi/search/news/news.md#%EB%89%B4%EC%8A%A4">Naver News Search API</a></li>
                    </ul>
                    <p style="line-height: 1.5;font-size: 19px;width: 100%;">대한민국 중앙방역대책본부 코로나바이러스 감염증 현황 <a href="http://ncov.mohw.go.kr/">바로가기</a></p>
                    <p style="line-height: 1.5;font-size: 19px;width: 100%;">제작 : Hoplin / Source Code Opened at <a href="{self.easteregg}">Github</a></p>
                </div>
            </body>
        </html>
        """
        return __htmltemplate2