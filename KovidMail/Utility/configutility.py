'''
Code written by Hoplin

Last written : 2021.12.01
'''

import sys
from enum import Enum
from KovidMail.Utility.globalutility import GlobalUtilities


class ConfigurationWriter(GlobalUtilities):
    '''
    Class Document
    ConfigurationWriter : 서비스 설정파일인 config.yml에 대한 수정,입력,저장 인터페이스를 제공하는 클래스입니다

    <변수>
    __options : 기본적인 이 클래스에서 제공하는 옵션들을 저장하고있는 Enum 타입의 객체입니다
    __editOptions : 필드를 수정/재정의 하기 위해서 필드를 저장하게 되는 Enum타입의 객체입니다
    __yamlInstance : yaml을 python 객체로 변환한 값을 저장합니다.
    __configLocation : config.yml의 경로를 저장합니다.
    __clearYaml : Yaml값을 초기화하기 위한 기본적인 포맷입니다.
    '''
    __options = Enum('options', ['Write_config_field', 'Edit_field', 'Clear_field','Chang_config_pw','exit'])
    __editOptions = None
    __yamlInstance = None
    __clearYaml = {
        'sqlConnection':
                       {
                        'host':
                            {
                                'encrypt': False,
                                'value': None
                            },
                        'sqlpassword':
                            {
                                'encrypt': True,
                                'value': None
                            },
                        'user':
                            {
                                'encrypt': True,
                                'value': None
                            }

                        },
        'configData': {
            'configpw':
                {
                    'encrypt': True,
                    'value': None
                }
        }
    }

    def __init__(self):
        #Call Configuration file
        self.__yamlInstance = self.readConfigYaml()
        #초기 비밀번호 없을시 admin으로 디폴트 초기화
        self.initiatePW(False)
        self.__editOptions = Enum('editopt',list(self.__yamlInstance['sqlConnection'].keys()))

    def initiatePW(self,forceChange : False):
        if not forceChange:
            if not self.__yamlInstance['configData']['configpw']['value']:
                self.__yamlInstance['configData']['configpw']['value'] = self.encrypt('admin')
                self.saveConfigYaml(self.__yamlInstance)
                self.__yamlInstance = self.readConfigYaml()
        else:
            self.__yamlInstance['configData']['configpw']['value'] = self.encrypt('admin')
            self.saveConfigYaml(self.__yamlInstance)
            self.__yamlInstance = self.readConfigYaml()

    def changeConfigPW(self):
        print("변경할 설정파일 root 비밀번호 입력하기")
        inpValue = self.onlyHiddenInput(">> ")
        print("비밀번호를 다시입력해 확인하기")
        reValue = self.onlyHiddenInput(">> ")
        if inpValue == reValue:
            self.__yamlInstance['configData']['configpw']['value'] = self.encrypt(reValue)
            self.saveConfigYaml(self.__yamlInstance)
            self.__yamlInstance = self.readConfigYaml()
            #보안을 위해 기존 변수 비우기
            inpValue = reValue = None
            print("비밀번호 변경이 완료되었습니다.")
            self.pressKeyToContinue()
            self.clearConsole()
        else:
            self.errorMSGHandler("비밀번호 변경에 실패하였습니다","두 비밀번호가 일치하지 않습니다.")
            self.pressKeyToContinue()
            self.clearConsole()

    def editor(self):
        inpValue = None
        loop = True
        while loop:
            res = self.returnSelectedOption(self.__editOptions,self.__yamlInstance['sqlConnection'])
            if not res:
                loop = False
            else:
                selectedField = res.name
                field = self.__yamlInstance['sqlConnection'][selectedField]
                print(f"선택 된 필드 : {selectedField} 값 변경하기. 변경할 값을 입력해주세요.")
                try:
                    if field['encrypt']:
                        inpValue = self.hideInput(">> ")
                        loop = False
                    else:
                        inpValue = self.normalInput(">> ")
                        loop = False
                    field['value'] = inpValue
                    self.saveConfigYaml(self.__yamlInstance)
                    self.clearConsole()
                except ValueError as e:
                    self.clearConsole()
                    self.warningMSGHandler(self.__wrongInpMSG)
                    pass


    def writer(self):
        writingSector = self.__yamlInstance['sqlConnection']
        features = list(writingSector.keys())
        for i in features:
            forceBreak = False
            loop = True
            while loop:
                try:
                    value = " "
                    if writingSector[i]['encrypt']:
                        value = self.hideInput("Save information %8s >> " % i)
                    else:
                        value = self.normalInput("Save information %8s >> " % i)
                    if not value:
                        self.warningMSGHandler("Writer stopped due to abnormal Input")
                        forceBreak = True
                        loop = False
                        self.pressKeyToContinue()
                    else:
                        loop = False
                        writingSector[i]['value'] = value
                        loop = False
                except TypeError as e:
                    self.clearConsole()
                    self.warningMSGHandler(self.__wrongInpMSG)
            if forceBreak:
                break

        if forceBreak:
            self.clearConsole()
        else:
            self.saveConfigYaml(self.__yamlInstance)
            # Reload after change
            self.__yamlInstance = self.readConfigYaml()
            self.clearConsole()

    def passwordChecker(self):
        print("설정값 변경/조회 권한을 얻기 위해 비밀번호 입력하기")
        val = self.hideInput(">> ")
        if not val:
            self.clearConsole()
            pass
        else:
            if self.__yamlInstance['configData']['configpw']['value'] == val:
                self.clearConsole()
                return True
            else:
                self.warningMSGHandler("잘못된 패스워드가 입력되었습니다.")
                self.pressKeyToContinue()
                self.clearConsole()
                return False


    def clearYaml(self):
        #clear yaml file
        self.__yamlInstance = self.__clearYaml
        self.initiatePW(True)

    def checkPWAndExecute(self,method):
        ck = self.passwordChecker()
        if ck:
            method()
        else:
            pass

    def optionSelector(self):
        self.clearConsole()
        loop = True
        while loop:
            res = self.returnSelectedOption(self.__options,False)
            if not res:
                loop = False
            else:
                ot = self.__options
                # 'Write_config_field', 'Edit_field', 'Clear_field'
                self.clearConsole()
                if res == ot.Write_config_field:
                    self.checkPWAndExecute(self.writer)
                elif res == ot.Edit_field:
                    self.checkPWAndExecute(self.editor)
                elif res == ot.Chang_config_pw:
                    self.checkPWAndExecute(self.changeConfigPW)
                elif res == ot.Clear_field:
                    self.checkPWAndExecute(self.clearYaml)
                    #self.clearYaml()
                elif res == ot.exit:
                    loop = False