#store data for use in future backtests
import csv
import datetime
import platform
import os
import shutil
import time

class Recorder(object):

    def __init__(self):
        self.date=datetime.datetime.now(datetime.timezone.utc)

        if platform.system() == 'Linux':
            self.data_path = r"/home/pi/mnt/gdrive/hydrogen/"
        elif platform.system() == 'Windows':
            self.data_path = r"E:\Data\\Records\\"

    def fopen(self):
        with open(self.data_path + str(self.date)+'_data.csv', 'a+', newline='') as self.csvfile:
            self.recwriter = csv.writer(self.csvfile)

    def record(self, event):
        self.recwriter.writerow()

    def fclose(self):
        self.csvfile.close()

    def retrieve(self):
        #get recorded files from netword drive if any        
        if platform.system() == 'Windows':
            today=datetime.datetime.now() #datetime.timezone.utc
            #C:\Users\rritt\Google Drive\hydrogen
            src_dir =os.path.join('C:\\','Users','rritt','Google Drive','hydrogen')
            #E:\Data\Records
            dest_dir =os.path.join('E:\\','Data','Records')
            #print(src_dir)
            #print(dest_dir)
            files=os.listdir(src_dir)
            #print(files)
            for f in files:
                f=os.path.join(src_dir,f)
                fmodtime=datetime.datetime.strptime(time.ctime(os.path.getmtime(f)), "%a %b %d %H:%M:%S %Y")
                fmodday=fmodtime.day
                if fmodday<today.day:
                    shutil.move(f,dest_dir) #copy the file to destination dir
            

        

#specialized class for tick data
class PriceRecorder(Recorder):
    def record(self,tickevent):
        self.date=datetime.datetime.strptime(tickevent.data['time'][:-2], '%Y-%m-%d %H:%M:%S.%f')
        #print(self.date)
        with open(self.data_path + str(tickevent.pair.replace('_', '')) +'-'+self.date.strftime("%Y-%m-%d")+'.csv', 'a+', newline='') as self.csvfile: #self.data_path + 
            #print('writing row')
            self.recwriter = csv.writer(self.csvfile)
            self.recwriter.writerow([str(tickevent.pair.replace('_', '')),str(tickevent.data['time']),str(tickevent.data['bid']),str(tickevent.data['bid'])])
        #print('event recorded')
        #self.db.append()

#secialized class for general data like e.g. news
class DataRecorder(Recorder):
    def record(self):
        self.recwriter.writerow()

if __name__=='__main__':
    pass

#Record:
#EUR/USD,20190101 22:06:11.699,1.14587,1.14727