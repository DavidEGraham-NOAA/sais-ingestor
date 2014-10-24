import datetime
import urllib2
import re
from bs4 import BeautifulSoup
import saisdb

'''Queries marinetraffic.com with mmsi/imo numbers to retrieve ship details'''
'''David Graham 11/11/2013'''
'''Completely rewritten 10/24/2014 to account for new version of marinetraffic.com'''

#Get the list of ships
ships = saisdb.GetIncompleteShips()
ships.pop(0)
ships = []
#ships.append('636016101')
#print ships

for s in ships:
    print "ship: " + str(s[0])
    #The url base should work for MMSI and IMO numbers
    #sometimes a minus sign is required to precede the number, haven't yet figured out exactly when that applies
    #MMSI = '440272000'
    urlbase = 'http://www.marinetraffic.com/ais/details/ships/370642000'
    req = urllib2.Request(urlbase,
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'})

    try:
        response = urllib2.urlopen(req)
        the_page = response.read()
        #HTTPError
        #print the_page
        dt = datetime.datetime.now()
        soup = BeautifulSoup(the_page)

        maindiv = soup.findAll("div", {"class": "col-xs-6"})
        shipvalues = []
        for row in maindiv:
            for b in row.findAll("b"):
                shipvalues.append(str(b).replace("<b>", "").replace("</b>", ""))
        print shipvalues
        ship = {}
        namediv = soup.find("h1", {"class": "font-200 no-margin"})
        #ship['name'] = namediv.get_text().strip()
        print ship['name']
        #print "------------------------"
        ship['IMO'] = shipvalues[0]
        ship['MMSI'] = shipvalues[1]
        ship['CallSign'] = shipvalues[2]
        ship['Flag'] = shipvalues[3]
        ship['Type'] = shipvalues[4]
        ship['LengthxBreadth'] = shipvalues[7].replace(" \xc3\x97 ", "x")
        lb = ship['LengthxBreadth'].split("x")
        if len(lb) == 2:
            if lb[0] == '-':
                lb[0] = None
            if lb[1] == '-':
                lb[1] = None
            lb[0] = lb[0].replace("m", "")
            lb[1] = lb[1].replace("m", "")

        else:
            lb = None
            lb = []
            lb.append(None)
            lb.append(None)

        ship['GrossTonnage'] = shipvalues[5]
        ship['DeadWeight'] = shipvalues[6].replace(" t", "")
        ship['YearBuilt'] = shipvalues[8]
        ship['Status'] = shipvalues[9]
        #print ship
        #print lb[0]
        #print lb[1]
        #print "here"
        #print type(detdiv[0])
        saisdb.UpdateVesselDetailsFromMmsi(ship['IMO'], ship['name'], ship['CallSign'], ship['GrossTonnage'], ship['DeadWeight'], ship['Flag'], ship['YearBuilt'], ship['Type'], ship['Status'], 'www.marinetraffic.com', lb[0], lb[1], ship['MMSI'])

    except urllib2.HTTPError as e:
        if e.code == 404:
            saisdb.UpdateNullVesselFromMmsi(s[0])
            pass
        else:
            #some other error, probably no network, just keep going
            pass

    except urllib2.URLError as e:
        print "URL Error"
        pass
        
    except Exception as e:
        #just keep going
        print str(repr(e))
        pass
        #print str(repr(e))
