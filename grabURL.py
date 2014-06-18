import urllib2
from bs4 import BeautifulSoup
import psycopg2

class GrabURL:
    
    def __init__(self):
        self.response=urllib2.urlopen('http://aqicn.org/city/all/')
        self.rowcount=0
        self.conn=psycopg2.connect("dbname=XXX user=XXX host=XXX password=XXX")
        self.cur=self.conn.cursor()
        
        self.cur.execute("TRUNCATE TABLE url;")
        
        
    def grabURL(self):
        print 'starting...\n'
        html=self.response.read()
        
        soup=BeautifulSoup(html)
        
        body=soup.find("h1",text="China").findNext("div","whitebody")
        city=body.find_all('div',style="width:80%")
        
        i=0  
        for station in city:
            for each in station.find_all('a'):
                s=each.text.split(' (')[0].encode('utf8')
                u=s.decode('utf8')
                try:
                    cStationName=repr(u).split("'")[1]
                    cCNName=each.text.split('(')[1].encode('utf8').split(')')[0]
                    cURL=each.get('href')
                    self.cur.execute("INSERT INTO url VALUES (%s,%s,%s);",(cStationName,cCNName,cURL,))
                    i+=1
                except:
                    pass
                #try:
                #    self.cur.execute("INSERT INTO url VALUES (%s,%s,%s)",(repr(u).split("'")[1],each.text.split('(')[1].encode('utf8').split(')')[0],each.get('href')))
                #except:
                #    pass
        self.rowcount=i
        self.conn.commit()
        
        self.cur.close()
        self.conn.close()
        
        print 'URLs have been grabbed into url table\n'







