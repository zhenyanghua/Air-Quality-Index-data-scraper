class Printmeta:
    def __init__(self,filename):
        self.file=open(filename,'w')
    
    def printmeta(self):
        self.file.write("Python version: 2.6+\n"+
                        "required module: BeautifulSoup4, lxml, libxml2\n"+
                        "\n"
                        "Run the 'grabjson.py', and it will update the URL first,\n"+
                        "and then grab the data from URL and store all the locations in 'location.csv',\n"+
                        "and all the air quality index in 'aqi.csv'.\n"+
                        "\n"+
                        "METADATA\n"
                        "location.csv table structure:\n"
                        "Column1: LocationID\n"
                        "Column2: Latitude\n"
                        "Column3: Longitude\n"
                        "Column4: StationName\n"
                        "Column5: ParentCity\n"
                        "Column6: SourceURL\n"
                        "\n"
                        "hourlydata.csv table structure:\n"
                        "Column1: LocationID\n"
                        "Column2: StationName\n"
                        "Column3: ChineseName\n"
                        "Column4: Latitude\n"
                        "Column5: Longitude\n"
                        "Column6: PM2.5\n"
                        "Column7: PM10\n"
                        "Column8: O3\n"
                        "Column9: NO2\n"
                        "Column10: SO2\n"
                        "Column11: CO\n"
                        "Column12: Temperature\n"
                        "Column13: DewPoint\n"
                        "Column14: Pressure\n"
                        "Column15: Humidity\n"
                        "Column16: Wind\n"
                        "Column17: EST_time\n"
                        "Column18: Unix_time\n")
        self.file.close()