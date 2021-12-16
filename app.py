import sys,pymysql,platform,datetime
from KovidMail.Utility.configutility import ConfigurationWriter
from KovidMail.Utility.DButility import dbutility
from enum import Enum
from KovidMail.Datas.datarequest import requestData
from KovidMail.Utility.patternchecker import patternChecker
from KovidMail.Datas.graph import makegraph
from KovidMail.SMTP.smtp import SendMail
from KovidMail.Utility.globalutility import GlobalUtilities


option = Enum('opt',["Service_Test","Add_Subscriber","Delete_User","View_Subscriber_List","Broadcast","Configuration_Writer","Database_Manager","About_This_Software","End"])

class application(GlobalUtilities):
    '''
    app.py : Tool for admin
        - Test Service passively
        - Register / Unregister / View Subscriber
        - Broadcasting Notice
        - Move to Configuration Writer
        - Move to Databse Manager

    Share one Database Manager instance's Address to manage SQL Cursor with thread safe and collision safe
    So basically not all modules doesn't have independent in inner instance
    but have independent relation between modules
    '''

    def __init__(self):
        # Due to sharing instance address, it requires order of declaration
        # If you want to edit my source code, i recommend to at least follow this order of instnce declaration.
        self.configwt = ConfigurationWriter()
        self.dbmg = dbutility(self.configwt)
        self.checkServiceKeyExist()
        self.dataRequest = requestData(self.dbmg)  # Need to close sql session
        self.graphGen = makegraph(self.dbmg,self.dataRequest)  # Need to close sql session
        self.smtpMod = SendMail(self.dbmg)  # Need to close sql session
        self.ptck = patternChecker()
        self.clearConsole()
        self.checkBasicConditionForService()

    def checkServiceKeyExist(self):
        testkey = " "
        try:
            testkey = self.dbmg.getServiceDatas()
        #Exception occured when database not found
        except pymysql.err.OperationalError as e:
            self.dbmg.essentialDatabaseInitiator()
        #if service key not exist, initiate key.
        if not testkey:
            self.clearConsole()
            self.globalErrorMSGHandler("Service Locked. You need to Initiate Keys to run service.")
            self.dbmg.initiateKeys()
            self.clearConsole()

    def checkBasicConditionForService(self):
        exist = True
        dblt = self.dbmg.getDatabaseList()
        for i in self.dbSchemaVariableList:
            if i["databasename"] in dblt or i["datbasename"].lower() in dblt:
                pass
            else:
                exist = False
                break
        if not exist:
            self.errorMSGHandler("Some necessary database not setted yet! Will move to database setting page.")
            self.pressKeyToContinue()
            self.dbmg.selectOption()
        else:
            self.noticeMSGHandler("Basic condition check complete! Move to main.")

    def serviceTester(self):
        subs = self.dbmg.getSubscriberList()
        result = self.dataRequest.reProcessXML(self.dataRequest.buildRequests())
        if not result:
            self.warningMSGHandler("The three reasons why you can't send an email.\n1. API hasn't been updated(High possibility at time of 00 : 00 ~ 10 : 00)\n2. Your api keys might be wrong\n3. Request address might be wrong")
            self.pressKeyToContinue()
            loop = False
        else:
            self.graphGen.buildGrarph()
            # sendres : variable for checking send or fail
            sendres = True
            for i in subs:
                sendres = self.smtpMod.buildMimeAndSendMail(i)
                if not sendres:
                    loop = False
                    self.pressKeyToContinue()
                    return
                print(f"Complete to send mail to : {i}")
            print()
            print("Complete to send mail")
            self.pressKeyToContinue()
            loop = False


    def addSubsciber(self):
        subs = self.dbmg.getSubscriberList()
        newEmail = self.normalInput("New E-Mail to Register >> ")
        #Check email form
        try:
            if not self.ptck.checkEmailPattern(newEmail):
                self.warningMSGHandler("Wrong types of E-Mail. Please Check Again")
                self.pressKeyToContinue()
            else:
                if newEmail in subs:
                    self.warningMSGHandler(f"Fail to register.E-Mail {newEmail} already exist at database")
                    self.pressKeyToContinue()
                else:
                    self.dbmg.addNewSubscriber(newEmail)
                    self.noticeMSGHandler("Register Completed!")
                    self.pressKeyToContinue()
        except TypeError as e:
            self.warningMSGHandler("Wrong types of E-Mail. Please Check Again")
            self.pressKeyToContinue()

    def DeleteUser(self):
        subs = self.dbmg.getSubscriberList()
        if not subs:
            self.warningMSGHandler("Subscriber not exist!")
            self.pressKeyToContinue()
        else:
            deleteMail = self.normalInput("E-Mail to unregister >> ")
            # Check email form
            if not self.ptck.checkEmailPattern(deleteMail):
                self.warningMSGHandler("Wrong types of E-Mail. Please Check Again")
                self.pressKeyToContinue()
            else:
                if deleteMail not in subs:
                    self.warningMSGHandler(f"E-Mail : {deleteMail} not exist. Please check agian")
                    self.pressKeyToContinue()
                else:
                    self.dbmg.deleteSub(deleteMail)
                    self.noticeMSGHandler("Unregister Completed!")
                    self.pressKeyToContinue()

    def ViewSubscriber(self):
        subs = self.dbmg.getSubscriberList()
        if not subs:
            self.warningMSGHandler("Subscriber not exist!")
            self.pressKeyToContinue()
        else:
            for i, j in enumerate(subs, start=1):
                print(f"{i}. {j}")
            print()
            self.pressKeyToContinue()

    def broadcast(self):
        subs = self.dbmg.getSubscriberList()
        title = self.normalInput("Broadcasting Title >> ")
        if not title:
            return
        broadcastmsg = self.normalInput("Message to broadcast >> ")
        if not title:
            return
        for i in subs:
            self.smtpMod.buildMimeAndSendMail(i, True, title, broadcastmsg)
            print(f"Complete to send mail : {i}")
        print()
        print("Complete to send broadcast mail")
        self.pressKeyToContinue()

    def moveToConfig(self):
        self.configwt.optionSelector()
        self.dbmg.readConfigAndGetConnection()
        self.dbmg.essentialDatabaseInitiator()

    def reconnect(self):
        self.dbmg.reconnect()

    def closeSession(self):
        self.clearConsole()
        self.noticeMSGHandler("Please wait while close connection with SQL Server...")
        self.dbmg.endConnection()
        self.noticeMSGHandler("Completed! Bye Bye")
        self.pressKeyToContinue()

    def toDBMG(self):
        self.dbmg.selectOption()
        self.checkServiceKeyExist()

    def aboutThisSoftware(self):
        state = """
        < Kovid Mail Service > 
        
        1. What is this software for? : This sofware is for Korea Covid 19 Information Mail Service. This software is manage tool for service
        
        2. Optimized OS : Linux / Mac OS.
        
        3. Made by : Hoplin
        
        4. This software is Open source, you can see source code at Github
        
            - Github : https://github.com/J-hoplin1/KovidMail
            
            - License : MIT License
        """
        print(state)
        self.pressKeyToContinue()

    def main(self):
        __optionMapper = {
            "Service_Test" : self.serviceTester,
            "Add_Subscriber" : self.addSubsciber,
            "Delete_User" : self.DeleteUser,
            "View_Subscriber_List" : self.ViewSubscriber,
            "Broadcast" : self.broadcast,
            "Configuration_Writer" : self.moveToConfig,
            "Database_Manager" : self.toDBMG,
            "About_This_Software" : self.aboutThisSoftware
        }
        loop = True
        executedTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        while loop:
            print("< Kovid Mail Service Manage Tool >")
            print()
            if self.dbmg.returnConnectionStatus():
                self.connectionMSGHandelr("My-SQL connetion Status : ", self.dbmg.returnConnectionStatus())
            else:
                self.connectionOddMSGHandler("My-SQL connetion Status : ", self.dbmg.returnConnectionStatus())
            print(f"System Info : {platform.platform()}")
            print(f"Executed Time : {executedTime}")
            res = self.returnSelectedOption(option)
            if not res:
                self.closeSession()
                loop = False
            else:
                res = res.name
                if res != "End":
                    self.clearConsole()
                    __optionMapper[res]()
                else:
                    self.closeSession()
                    loop = False
                self.clearConsole()

if __name__ == "__main__":
    GlobalUtilities.clearConsole()
    p = application()
    p.main()
