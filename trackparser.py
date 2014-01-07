import sys
import psycopg2
import saisdb

#This is not the best idea, but it will get us through the big ones.
sys.setrecursionlimit(1600)

conn = psycopg2.connect("dbname=sais user=postgres password=4everYoung2$")
cur = conn.cursor()
mmsi = '366972620'
masterlist = []
lastcount = 0

def getsubs(vesselid, observationid):
  cur.execute("""SELECT ihs_obs_id, reportdate FROM ihs_observations 
                 WHERE reportdate BETWEEN (SELECT reportdate FROM ihs_observations WHERE ihs_obs_id = %(obid)s) 
                 AND (SELECT reportdate FROM ihs_observations WHERE ihs_obs_id = %(obid)s) + interval '3 days'
                 AND mmsi = %(mmsi)s;""",
                 {'mmsi':vesselid,'obid':observationid})
  morerows = cur.fetchall()
  conn.commit()
  if len(morerows) > 0:
      masterlist.extend(morerows)
      print str(len(masterlist))
      getsubs(vesselid, morerows[-1][0])
  else:
      return false
      
      
#Get the minimum observationid for our ship
cur.execute("""SELECT MIN(ihs_obs_id) FROM ihs_observations WHERE mmsi = '366972620';""")
startrow = cur.fetchall()
conn.commit()

for s in startrow:
  #get all rows within 3 days of this first observation
  cur.execute("""SELECT ihs_obs_id, reportdate FROM ihs_observations 
                 WHERE reportdate BETWEEN (SELECT reportdate FROM ihs_observations WHERE ihs_obs_id = %(obid)s) 
                 AND (SELECT reportdate FROM ihs_observations WHERE ihs_obs_id = %(obid)s) + interval '3 days'
                 AND mmsi = %(mmsi)s;""",
                 {'mmsi':mmsi,'obid':s[0]})
  subrows = cur.fetchall()
  conn.commit()
  
  if len(subrows) > 0:
      masterlist.extend(subrows)
      lastcount = len(masterlist)
      #we've been through once, now we need to recurse until we run out of rows
      hasmore = getsubs(mmsi, subrows[-1][0])
      if hasmore:
          print str(len(masterlist))
      else:
          print "pau"
    

