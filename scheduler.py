import schedule,time,sys
import pymysql,logging
from KovidMail.Utility.configutility import ConfigurationWriter
from KovidMail.Utility.DButility import dbutility
from KovidMail.Datas.datarequest import requestData
from KovidMail.Utility.patternchecker import patternChecker
from KovidMail.Datas.graph import makegraph
from KovidMail.SMTP.smtp import SendMail
from KovidMail.Utility.globalutility import GlobalUtilities

class scheduler(GlobalUtilities):
    def __init__(self,logger):
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
        # Logger
        self.logger = logger

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
            self.noticeMSGHandler("Basic condition check complete! Scheduler is now running!")

    def closeSession(self):
        self.clearConsole()
        self.logLevelInfo("Please wait while close connection with SQL Server...")
        self.dbmg.endConnection()
        self.logLevelInfo("Completed! Bye Bye")
        self.pressKeyToContinue()

    def logLevelInfo(self,msg):
        self.logger.info(msg)

    def logLevelWarning(self,msg):
        self.logger.warning(msg)

    def main(self):
        self.logLevelInfo("Start stream!")
        mainloop = True
        while mainloop:
            subs = self.dbmg.getSubscriberList()
            result = self.dataRequest.reProcessXML(self.dataRequest.buildRequests())
            if not result:
                self.logLevelWarning("The three reasons why you can't send an email.\n1. API hasn't been updated(High possibility at time of 00 : 00 ~ 10 : 00)\n2. Your api keys might be wrong\n3. Request address might be wrong")
                time.sleep(5)
            else:
                self.graphGen.buildGrarph()
                # sendres : variable for checking send or fail
                sendres = True
                for i in subs:
                    sendres = self.smtpMod.buildMimeAndSendMail(i)
                    if not sendres:
                        loop = False
                        self.logLevelWarning(f"Fail to send mail to {i} due to wrong email format")
                        self.pressKeyToContinue()
                        return
                    print(f"Complete to send mail to : {i}")
                print()
                print("Complete to send mail")
                mainloop = False
                self.logLevelInfo("End Stream!")


def start():
    p.main()

if __name__ == "__main__":
    #Default time is 10:00
    scheduledtime = "10:00"
    GlobalUtilities.clearConsole()
    argss = sys.argv
    try:
        #If schedule time exist as arguments, change time
        scheduledtime = argss[1]
    except IndexError as e:
        pass
    # Logger
    logger = logging.getLogger("Kovid-Mail-Scheduler")
    logger.setLevel(logging.DEBUG)
    # Create console handler and set level to debug
    consolechannel = logging.StreamHandler()
    consolechannel.setLevel(logging.DEBUG)
    # Log Format
    format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    consolechannel.setFormatter(format)
    # add
    logger.addHandler(consolechannel)
    # Scheduler Instance
    p = scheduler(logger)
    # Schedule
    try:
        schedule.every().day.at(scheduledtime).do(start)
    #If wron type of time format : Close
    except schedule.ScheduleValueError as e:
        GlobalUtilities.globalErrorMSGHandler("Wrong types of time format. Scheduler close")
        sys.exit()
    loop = True
    logger.info(f"Schedule time has been set : {scheduledtime}")
    logger.info(f"Scheduler now executed! Listening until {scheduledtime}!")
    while loop:
        try:
            # 예약작업 실행 : scheduler.main()
            schedule.run_pending()
            logger.info("Listening... | Press Ctrl + C to exit")
            time.sleep(3)
        except KeyboardInterrupt as e:
            p.closeSession()
            loop = False
