import smtplib,sys
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from pytz import timezone
from KovidMail.Templates.htmlwriter import htmlwriter
sys.path.append('..')
from KovidMail.Utility.globalutility import GlobalUtilities

class SendMail(GlobalUtilities):

    def __init__(self,dbmg):
        self.dbc = dbmg # Database manager address from hub application
        self.writer = htmlwriter()
        #Initiate Template

    def buildMimeAndSendMail(self,to,broadcast=False,title=None,broadcastmsg=None):
        '''

        :param to: Address of recieving mail
        '''
        sendres = True
        self.__data = self.dbc.returnMailInfo()
        htmlTemplate = str(self.writer.returnTemplate2())
        #Declare Multi Mime
        multimime = MIMEMultipart()
        _from = self.__data[0]['HOSTERMAIL']
        _to = to
        executed = (datetime.now(timezone('Asia/Seoul')) + timedelta(days=0)).strftime("%Y년 %m월 %d일")
        multimime['From'] = _from
        multimime['To'] = _to

        #If it's broadcasting mode
        if broadcast:
            multimime['Subject'] = f"[Broadcasting] {title}"
            message = MIMEText(_text = broadcastmsg, _charset = "utf-8")
        #If it's normal mode
        else:
            multimime['Subject'] = f"{executed} 코로나19 바이러스 일일 브리핑"
            message = MIMEText(htmlTemplate, 'html')
            # Image Mime
            with open(self.graphDirectory, 'rb') as f:
                image = MIMEImage(f.read(), Name="CurrentCovidGraph.png")
                image.add_header('Content-ID', '<graph>')
                multimime.attach(image)
        multimime.attach(message)
        smtp = smtplib.SMTP('smtp.naver.com',587)
        smtp.starttls()
        try:
            smtp.login(_from,self.decrypt(self.__data[0]['HOSTERMAILPW']))
        except smtplib.SMTPAuthenticationError as e:
            self.globalErrorMSGHandler("While login to your account, authentication error occured. Please check your E-mail or PW")
            sendres = False
            return sendres
        smtp.sendmail(_from,_to,multimime.as_string())
        return sendres

    def closeConnection(self):
        self.dbc.endConnection()
