#import psycopg2
#
#conn=psycopg2.connect("dbname=XXX user=XXX host=XXX password=XXX")
#cur=conn.cursor()
#cur.execute("""DROP TABLE films;""")
#conn.commit()
#cur.close()
#conn.close()

from grabURL import GrabURL

url=GrabURL()
url.grabURL()
print 'row count: '+ str(url.rowcount)