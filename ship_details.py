import datetime
import urllib2
from bs4 import BeautifulSoup

'''Queries marinetraffic.com with mmsi/imo numbers to retrieve ship details'''
'''David Graham 11/11/2013'''

#The url base should work for MMSI and IMO numbers
#sometimes a minus sign is required to precede the number, haven't yet figured out exactly when that applies
#We also have to spoof the user-agent header or we'll be redirected to a junk page
#urlbase = 'http://www.marinetraffic.con/en/ais/details/ships/'
urlbase = 'http://new.marinetraffic.com/en/ais/details/ships/'
req = urllib2.Request(urlbase + '372359000',
  headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'})
response = urllib2.urlopen(req)
the_page = response.read()
#HTTPError
print the_page
dt = datetime.datetime.now()
soup = BeautifulSoup(the_page)

maindiv = soup.find("div", {"class": "details_under_1"})
ship = {}
namediv = soup.find("h1", {"class": "details_header_vessel"})
ship['name'] = namediv.get_text().strip()
print maindiv
print "------------------------"
detdiv = maindiv.findAll("div",{"class": "details_under_1_div"})
#print detdiv[0]
#print type(detdiv[0])
details1 = detdiv[0].get_text().strip()
#print something

details1_content = details1.splitlines()
for i in details1_content:
    if (i != ''):
        k,v = i.split(':')
        ship[k.strip().replace(" ", "")] = v.strip()
        #print i.strip()

details2 = detdiv[1].get_text().strip()
details2_content = details2.splitlines()
#print details2_content
for i in details2_content:
    if (i != ''):
        k,v = i.split(':')
        ship[k.strip().replace(" ", "")] = v.strip()

#ship now contains all our vessel details we can get
print ship
#<h1 class="details_header_vessel">MSC POH LIN</h1>


#bob = iter(detdiv[0])
#print str(len(detdiv[0]))
#for i in something:
#    #print str(i)
#    dastring = str(i).strip()
#    print dastring
#    print "========"
