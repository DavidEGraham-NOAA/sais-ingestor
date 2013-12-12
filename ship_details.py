import datetime
import urllib2
from bs4 import BeautifulSoup
import saisdb

'''Queries marinetraffic.com with mmsi/imo numbers to retrieve ship details'''
'''David Graham 11/11/2013'''

#Get the list of ships
ships = saisdb.GetIncompleteShips()
#print ships

for s in ships:
    #The url base should work for MMSI and IMO numbers
    #sometimes a minus sign is required to precede the number, haven't yet figured out exactly when that applies
    #MMSI = '440272000'
    urlbase = 'http://new.marinetraffic.com/en/ais/details/ships/'
    req = urllib2.Request(urlbase + s[0],
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'})

    try:
        response = urllib2.urlopen(req)
        the_page = response.read()
        #HTTPError
        #print the_page
        dt = datetime.datetime.now()
        soup = BeautifulSoup(the_page)

        maindiv = soup.find("div", {"class": "details_under_1"})
        ship = {}
        namediv = soup.find("h1", {"class": "details_header_vessel"})
        ship['name'] = namediv.get_text().strip()
        #print maindiv
        #print "------------------------"
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

        vname = namediv.get_text().strip()
        print vname
        #print ship
        lb = ship['LengthxBreadth'].split("x")
        '''print 'IMO: ' +ship['IMO']
        print 'NAME: ' + ship['name']
        print 'CALLSIGN: ' + ship['CallSign']
        print 'GROSS TON: ' + ship['GrossTonnage']
        print 'DEAD: ' + ship['DeadWeight']
        print 'FLAG: ' + ship['Flag']
        print 'YEAR: ' + ship['YearBuilt']
        print 'TYPE: ' + ship['Type']
        print 'STATUS: ' + ship['Status']
        print 'LEN: ' + lb[0].replace("m","")
        print 'BEAM: ' + lb[1].replace("m","")
        print 'MMSI: ' + ship[0]'''
        saisdb.UpdateVesselDetailsFromMmsi(ship['IMO'], ship['name'], ship['CallSign'], ship['GrossTonnage'], ship['DeadWeight'], ship['Flag'], ship['YearBuilt'], ship['Type'], ship['Status'], 'new.marinetraffic.com', lb[0].replace("m",""), lb[1].replace("m",""), s[0])

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
