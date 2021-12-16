import sys
import matplotlib.pyplot as plt

sys.path.append('..')
from KovidMail.Utility.globalutility import GlobalUtilities

class makegraph(GlobalUtilities):
    def __init__(self,dbmg,rqd):
        self.dbc = dbmg
        self.rqd = rqd
        self.data = self.dbc.getCurrentData()

    # Get today patient y-axis maximum value
    def getY2Maximum(self,val):
        add = int('1' + str((len(str(val)) - 1) * '0'))
        return ((int(val) // add) * add) + add * 3

    #Get total patient y-axis maximum value
    def getY1Maximum(self,val):
        add = int('1' + str((len(str(val)) - 1) * '0'))
        return ((int(val) // add) * add) + add * 1.5

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
        ax1.set_ylim(0,self.getY2Maximum(int(max(y2))))
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Daily new patient')
        ax1.tick_params(axis='both',direction='in')

        ax2 = ax1.twinx()
        ax2.bar(x,y1,color='orange',label='Total Patient', alpha=0.7, width=0.7)
        ax2.set_ylim(0, self.getY1Maximum(int(max(y1))))
        ax2.set_ylabel('Total Patient')
        ax2.tick_params(axis='y', direction='in')


        ax1.set_zorder(ax2.get_zorder() + 10)
        ax1.patch.set_visible(False)
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # add label to barplot and line plot
        for i,j in enumerate(x):
            ax2.text(j,y1[i], f"{y1[i]}",
                     fontsize=12,
                     color="black",
                     horizontalalignment='center',
                     verticalalignment='bottom')

        for i,j in enumerate(x):
            ax1.text(j,y2[i],f"{y2[i]}",
                     fontsize=12,
                     color="black",
                     horizontalalignment='center',
                     verticalalignment='bottom')
        plt.savefig(self.graphDirectory,bbox_inches='tight')
        plt.close()


