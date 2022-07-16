import datetime
import os
from pathlib import Path

'''
Log file writer
'''

class Logger:
    __logBucket = []
    __logDirectory = str(Path(os.getcwd()).parent)

    @classmethod
    def Log(cls,msg:str):
        print(msg, end="\n")
        cls.__logBucket.append(msg)

    @classmethod
    def ExtractLogFile(cls):
        # Now String Format
        now = datetime.datetime.now().strftime("%Y_%m_%d %H:%M:%S")

        # Check log directory exist
        # Make directory if not exist
        if not os.path.isdir(cls.__logDirectory):
            os.mkdir(cls.__logDirectory)

        logFileDirectory = cls.__logDirectory + "/" + now + ".txt"
        with open(logFileDirectory, 'w') as t:
            t.write('\n'.join(cls.__logBucket))
        print(f"Log file saved to {logFileDirectory}")




if __name__ =="__main__":
    Logger.ExtractLogFile()