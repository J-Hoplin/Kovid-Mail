import sys,json
from KovidMail.Templates.templates import template
sys.path.append('..')
from KovidMail.Utility.globalutility import GlobalUtilities

class htmlwriter(GlobalUtilities):

    def __init__(self):
        self.tmp = template()

    def openJSON(self):
        with open(self.dataJSONDirectory) as jn:
            self.json_data = json.load(jn)

    # Template : Without News
    def returnTemplate1(self):
        self.openJSON()
        htmltemplate = self.tmp.Template1(self.json_data)
        return htmltemplate

    #Template : With Topic News
    def returnTemplate2(self):
        self.openJSON()
        htmltemplate = self.tmp.Template2(self.json_data)
        return htmltemplate