import os

class Tarup:
    def __init__(self,filename):
        self.filename=filename
        
    def tarup(self):
        csvdir="/home/airchina/tempcsv"
        tarCall="tar -C "+csvdir+" -czf "+self.filename+".tar "+"./"
        os.system(tarCall)
        #moveing
        archivedir="/home/airchina/archive"
        mvCall="mv "+self.filename+".tar "+" "+ archivedir
        os.system(mvCall)
        