import sys
import matplotlib.pyplot as plt

sys.path.append('..')
from KovidMail.Utility.globalutility import GlobalUtilities
from KovidMail.Datas.datarequest import requestData
from KovidMail.Utility.DButility import dbutility

class makegraph(GlobalUtilities):
    def __init__(self,dbmg : dbutility,rqd :requestData):
        self.dbc = dbmg
        self.rqd = rqd
        self.data = self.dbc.getCurrentData()

    # Get today patient y-axis maximum value
    def getY2Maximum(self,val):
        #add = int('1' + str((len(str(val)) - 1) * '0'))
        #return ((int(val) // add) * add) + add * 3
        return int(val * 1.05)

    #Get today patient y-axis minimum value
    def getY2Minimum(self,val):
        return int(val * 0.8) #int(str(limit_value)[0] + ((len(str(limit_value)) - 1) * '0'))

    #Get total patient y-axis maximum value
    def getY1Maximum(self,val):
        #add = int('1' + str((len(str(val)) - 1) * '0'))
        #return ((int(val) // add) * add) + add * 1.5
        return int(val * 1.1)

    #Get total patient y-axis minimum value : Minimum Value based on Maximum Value ( getMaximum())
    def getY1Minimum(self,val):
        return int(val * 0.8) #int(str(limit_value)[0] + ((len(str(limit_value)) - 1) * '0'))

    def buildGrarph(self):
        #Make Current Data if Data not exist
        if not self.dbc.getCurrentData():
            self.rqd.generateTestData()
        self.data = self.dbc.getCurrentData()
        self.noticeMSGHandler("Generating Graph...")
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (15,10)
        plt.rcParams['font.size'] = 15
        totalPatient = []
        date = []
        todayPatient = []
        for i in range(len(self.data)):
            totalPatient.append(int(self.data[i]['totaldecidedPatient']))
            date.append(self.data[i]['Date'])
            todayPatient.append(int(self.data[i]['todaydecidedPatient']))
        x = date
        y1 = totalPatient
        y2 = todayPatient

        ax1 = plt.subplot()
        ax1.plot(x,y2,'-o',color='blue',markersize=3,linewidth=5, alpha=0.7,label='Daily new patient')
        #Designate Graph Y - Range with Maximum Value
        ax1.set_ylim(self.getY2Minimum(int(min(y2))),self.getY2Maximum(int(max(y2))))
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Daily new patient')
        ax1.tick_params(axis='both',direction='in')

        ax2 = ax1.twinx()
        ax2.bar(x,y1,color='orange',label='Total Patient', alpha=0.7, width=0.7)
        #Designate Graph Y - Range with Maximum Value
        ax2.set_ylim(self.getY1Minimum(int(min(y1))), self.getY1Maximum(int(max(y1))))
        ax2.set_ylabel('Total Patient')
        ax2.tick_params(axis='y', direction='in')


        ax1.set_zorder(ax2.get_zorder() + 10)
        ax1.patch.set_visible(False)
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # add label to barplot and line plot
        for i,j in enumerate(x):
            ax2.text(j,y1[i], f"{format(y1[i],',')}",
                     fontsize=15,
                     color="black",
                     horizontalalignment='center',
                     verticalalignment='bottom')

        for i,j in enumerate(x):
            ax1.text(j,y2[i],f"{format(y2[i],',')}",
                     fontsize=18,
                     color="black",
                     horizontalalignment='center',
                     verticalalignment='bottom')
        plt.savefig(self.graphDirectory,bbox_inches='tight')
        plt.close("all")


