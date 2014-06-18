Air Quality Index data Scraper

Author: Zhenyang Hua

---------------------------------------
V1.0

Python version: 2.6+
required module: BeautifulSoup4, lxml, libxml2

Run the 'grabjson.py', and it will update the URL first,
and then grab the data from URL and store all the locations in 'location.csv',
and all the air quality index in 'hourlydata.csv'.

METADATA
location.csv table structure:
Column1: LocationID
Column2: Latitude
Column3: Longitude
Column4: StationName
Column5: ParentCity
Column6: SourceURL

hourlydata.csv table structure:
Column1: LocationID
Column2: StationName
Column3: ChineseName
Column4: Latitude
Column5: Longitude
Column6: PM2.5
Column7: PM10
Column8: O3
Column9: NO2
Column10: SO2
Column11: CO
Column12: Temperature
Column13: DewPoint
Column14: Pressure
Column15: Humidity
Column16: Wind
Column17: EST_time
Column18: Unix_time
