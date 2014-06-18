import urllib2,csv,json,time,datetime,socket,traceback,sys
from bs4 import BeautifulSoup
from printmeta import Printmeta
from tarup import Tarup
from grabURL import GrabURL
from offset import Offset
import psycopg2,mechanize


startTime=time.time()

#GrabURL
url=GrabURL()
url.grabURL()

#set up browser
#Browser
br=mechanize.Browser()


#Cookie Jar
#cj=cookielib.LWPCookieJar()
#br.set_cookiejar(cj)

#Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(False)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

#Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),max_time=1)

#User-Agent
br.addheaders=[('User-agent','Firefox')]
#my user-agent:
#Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.73.11 (KHTML, like Gecko) Version/7.0.1 Safari/537.73.11

#Open a site
#response=br.open("http://www.fracfocusdata.org/DisclosureSearch/")
#html=response.read()

#Offset
offset=Offset()

#start...
count=0
urlcount=url.rowcount
#urlcount=1292
#row_id=0

#Start time
stime=long(time.strftime("%Y%m%d%H0000"))


#DB connection
conn=psycopg2.connect("dbname=XXX user=XXX host=XXX password=XXX")
cur=conn.cursor()


cur.execute("SELECT * FROM url;")
csvRows=cur.fetchall()
print str(len(csvRows))

#with open('url.csv','rb') as csvfile:
    #csvReader=csv.reader(csvfile,delimiter=',',quotechar='"')
    #try:
    #    monitorTB=open('hourlydata.csv','rb')
    #except:
    #    monitorTB=open('hourlydata.csv','wb')
    #    monitorTB.close()
    #    monitorTB=open('hourlydata.csv','rb')
    #monitorReader=csv.reader(monitorTB,delimiter=',',quotechar='"')
    #monitorList=list(monitorReader)
    #monitorcount=len(monitorList)
    #monitorTB.close()
    #with open('hourlydata.csv','wb') as hourlyfile:
        #hourlyrow=csv.writer(hourlyfile, delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL)
        #try:
        #    locationTB=open('location.csv','rb')
        #except:
        #    locationTB=open('location.csv','wb')
        #    locationTB.close()
        #    locationTB=open('location.csv','rb')
        #locationReader=csv.reader(locationTB,delimiter=',',quotechar='"')
        #locationList=list(locationReader)
        #locationcount=len(locationList)
        #locationTB.close()
        #with open('location.csv','ab') as locationTB:
            #locationrow=csv.writer(locationTB,delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL)

for row in csvRows:
    urlresponse=False
    httpcounter=0
    while urlresponse==False:
        try:
            if count >=urlcount:
                break
            
            print 'loading url '+str(count+1)+' of '+str(urlcount)+'...'
            
            #time out tolerence
            timeout = 10
            socket.setdefaulttimeout(timeout)
            #wait for 3 seconds
            time.sleep(3)
            #response=urllib2.urlopen(row[2])
            response=br.open(row[2])
            html=response.read()
            
            urlresponse=True
            
            soup=BeautifulSoup(html)
            
            #time in epoch format
            unix_time=int(time.time()-int(time.ctime()[14:-8])*60-int(time.ctime()[17:-5]))
            #time in iso-8601 format
            #cur_time=datetime.datetime.utcfromtimestamp(cur_time).isoformat()
            #time in YYYYMMDDHHMMSS format
            cur_time=time.strftime("%Y%m%d%H0000")
            
            cur_pm25=cur_pm10=cur_o3=cur_no2=cur_so2=cur_co=cur_t=cur_d=cur_p=cur_h=cur_w='Null'
            
            try:
                cur_pm25=soup.find(id='cur_pm25').text
            except:
                pass
            try:
                cur_pm10=soup.find(id='cur_pm10').text
            except:
                pass
            try:
                cur_o3=soup.find(id='cur_o3').text
            except:
                pass
            try:
                cur_no2=soup.find(id='cur_no2').text
            except:
                pass
            try:
                cur_so2=soup.find(id='cur_so2').text
            except:
                pass
            try:
                cur_co=soup.find(id='cur_co').text
            except:
                pass
            try:    
                cur_t=soup.find(id='cur_t').text
            except:
                pass
            try:
                cur_d=soup.find(id='cur_d').text
            except:
                pass
            try:
                cur_p=soup.find(id='cur_p').text
            except:
                pass
            try:
                cur_h=soup.find(id='cur_h').text
            except:
                pass
            try:
                cur_w=soup.find(id='cur_w').text
            except:
                pass
            
            body=soup.findAll("script",type="text/javascript")[-1].text.split(';')[0][20:][:-3]+'}'            
            
            count+=1
            
            childcount=0
                            
            
            #if row_id==monitorcount:row_id+=1
            #else: row_id=monitorcount+1
            #monitorcount+=1    
                
            jdata=json.loads(body)
            #print jdata
            for value in jdata.values():
                for child in value:
                    for k,v in child.items(): 
                        if k=='city' and v.split(' (')[0]==row[0]:
                            childcount+=1
                            cn=row[1]
                            city=child.get('city').split(' (')[0]
                            #print city
                            #print child.get('g')
                            lat_0=float(child.get('g')[0])
                            lon_0=float(child.get('g')[1])
                            offset.transform(lat_0,lon_0)
                            lat=round(offset.lat,6)
                            lon=round(offset.lon,6)
                            
                            #check if lat lon falls in China bounding box
                            try:
                                if (lat>53.559712 or lat<15.781945) or (lon<73.560763 or lon>134.770467):
                                    continue
                            except:
                                pass
                            
                            #check if the location of new records are already in the csv file,
                            #If not exists, add a new location to the location csv file.
                            cur.execute("SELECT * FROM location;")
                            conn.commit()
                            locationList=cur.fetchall()
                            #print locationList
                            
                            checkSameLocation=0
                            #tempcount=0
                            for each in locationList:
                                #tempcount+=1
                                if lat==each[1] and lon==each[2]:
                                    checkSameLocation+=1
                                    #object_id=tempcount
                                    print 'Location already exists...'
                            
                            if checkSameLocation==0:
                                print 'New Location...'
                                #object_id=locationcount+1
                                parent_city=row[2].split('/')[4]
                                #locationrow.writerow([str(object_id),lat,lon,city,parent_city,row[2]])
                                cur.execute("INSERT INTO location(latitude,longitude,stationname,parentcity,sourceurl) VALUES (%s,%s,%s,%s,%s);"
                                            ,(lat,lon,city,parent_city,row[2],))
                                conn.commit()
                                #locationcount+=1
                            cur.execute("SELECT locationid FROM location WHERE sourceurl=%s",(row[2],))
                            location_id=cur.fetchone()[0]
                            #hourlyrow.writerow([str(row_id),str(object_id),city,cn,lat,lon,cur_pm25,cur_pm10,cur_o3,cur_no2,
                            #                    cur_so2,cur_co,cur_t,cur_d,cur_p,cur_h,cur_w,cur_time,unix_time])
                            #cur.execute("INSERT INTO hourlydata(locationid,stationname,chinesename,latitude,longitude,pm25,pm10,o3,no2,so2,co,temperature,dewpoint,pressure,humidity,wind,est_time,unix_time) VALUES (,
                            #Handle Null
                            nullDict={'location_id':location_id,'city':city,'cn':cn,'lat':lat,'lon':lon,'cur_pm25':cur_pm25,'cur_pm10':cur_pm10,
                                      'cur_o3':cur_o3,'cur_no2':cur_no2,'cur_so2':cur_so2,'cur_co':cur_co,'cur_t':cur_t,
                                      'cur_d':cur_d,'cur_p':cur_p,'cur_h':cur_h,'cur_w':cur_w,'cur_time':cur_time,'unix_time':unix_time}
                            for k,v in nullDict.items():
                                if v == 'Null':
                                    nullDict[k] = None  
                            cur.execute("""INSERT INTO hourlydata(locationid,stationname,chinesename,latitude,longitude,pm25,pm10,o3,no2,so2,co,temperature,dewpoint,pressure,humidity,wind,est_time,unix_time)
                                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
                                        ,(nullDict['location_id'],nullDict['city'],nullDict['cn'],nullDict['lat'],nullDict['lon'],
                                          nullDict['cur_pm25'],nullDict['cur_pm10'],nullDict['cur_o3'],nullDict['cur_no2'],
                                            nullDict['cur_so2'],nullDict['cur_co'],nullDict['cur_t'],nullDict['cur_d'],
                                            nullDict['cur_p'],nullDict['cur_h'],nullDict['cur_w'],nullDict['cur_time'],nullDict['unix_time'],))
                            conn.commit()
                if childcount>=1: break
        except ValueError:
            urlresponse=True
            pass
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "*** print_exception:"
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2, file=sys.stdout)
            time.sleep(8)
            httpcounter+=1
            if httpcounter>3:urlresponse=True
            pass



#End time
etime=long(time.strftime("%Y%m%d%H%M%S"))

#copy Test
cur.execute("""COPY (SELECT locationid,stationname,chinesename,latitude,longitude,pm25,pm10,o3,no2,so2,co,temperature,dewpoint,pressure,humidity,wind,est_time
            FROM hourlydata WHERE est_time >= %s AND est_time<= %s)
            TO '/home/airchina/tempcsv/aqi.csv' DELIMITER ',' CSV HEADER;""",(stime,etime,))
print str(stime)+'.csv has been created.'
cur.execute("COPY location TO '/home/airchina/tempcsv/location.csv' DELIMITER ',' CSV HEADER;")
print 'location.csv has been created.'


conn.commit()
cur.close()
conn.close()

#Readme
readme=Printmeta('/home/airchina/tempcsv/README.txt')
readme.printmeta()
print 'README.txt has been created.'
print str(stime)+'.csv has been created.'

#Tar up results
tar=Tarup(str(stime))
tar.tarup()
print str(stime)+'.tar has been saved in archive.'
print 'finishing...'

endTime=time.time()

print 'Total Time: '+str((endTime-startTime)/60)+' secs'