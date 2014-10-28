import datetime
import urllib2
import re
from bs4 import BeautifulSoup
import saisdb

'''Queries marinetraffic.com with mmsi/imo numbers to retrieve ship details'''
'''David Graham 11/11/2013'''

#Get the list of ships
ships = saisdb.GetIncompleteShips()
print ships
#ships = [('440272000',), ('357878000',)]
for s in ships:
    if (s[0] == None):
        continue
    #The url base should work for MMSI and IMO numbers
    #sometimes a minus sign is required to precede the number, haven't yet figured out exactly when that applies
    urlbase = 'http://shipais.co.uk/showship.php?map=Milfordhaven&mmsi='
    req = urllib2.Request(urlbase + s[0],
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'})

    try:
        response = urllib2.urlopen(req)
        the_page = response.read()
        #HTTPError
        #print the_page
        dt = datetime.datetime.now()
        soup = BeautifulSoup(the_page)
        maindiv = soup.find("div", {"class": "bg_color"})
        ship = {}
        #namediv = soup.find("h1", {"class": "details_header_vessel"})
        #ship['name'] = namediv.get_text().strip()
        #print maindiv
        #print "------------------------"
        detdiv = maindiv.findAll("table",{"class": "shiptable"})
        #print type(detdiv[0])
        flag = soup.find("acronym")
        flag = flag['title']
        ship['Flag'] = flag
        details1 = detdiv[0].get_text().strip()
        #print something
        details1_content = details1.splitlines()
        for i in details1_content:
            if ('Received' in i) or ('ETA' in i):
                continue
            if (i != ''):
                k,v = i.split(':')
                ship[k.strip().replace(" ", "")] = v.strip()
                #print i.strip()

        #ship now contains all our vessel details we can get
        if('Name' in ship):
            vname = ship['Name']
        else:
            ship['Name'] = None
            vname = None
        if ('Size' in ship):
            ship['Size'] = re.sub("m", "", ship['Size'])
            lb = ship['Size'].split("x")
            lb[0] = re.sub('\D', "", lb[0])
            lb[1] = re.sub('\D', "", lb[1])
        else:
            ship['Size'] = None
            lb = None
            lb = []
            lb.append(None)
            lb.append(None)
        if ('Tonnage' in ship):
            if(',' in ship['Tonnage']):
                tonnage = ship['Tonnage'].split(',')
                tonnage[0] = re.sub(" ", "", tonnage[0])
                tonnage[0] = re.sub("gt", "", tonnage[0])
                tonnage[1] = re.sub(" ", "", tonnage[1])
                tonnage[1] = re.sub("dwt", "", tonnage[1])
            elif ("gt" in ship['Tonnage']):
                tonnage[0] = re.sub(" ", "", tonnage[0])
                tonnage[0] = re.sub("gt", "", tonnage[0])
                tonnage[1] = None
            elif ("dwt" in ship['Tonnage']):
                tonnage[0] = None
                tonnage[1] = re.sub(" ", "", tonnage[1])
                tonnage[1] = re.sub("dwt", "", tonnage[1])
        else:
            tonnage = None
            tonnage = []
            tonnage.append(None)
            tonnage.append(None)
        ship['GrossTonnage'] = tonnage[0]
        ship['DeadWeight'] = tonnage[1]
        ship['LengthxBreadth'] = ship['Size']
        if('Built' not in ship):
            ship['Built'] = None
        else:
            if not(str(ship['Built']).isdigit()):
                year = ""
                for i in ship['Built']:
                    if i.isdigit():
                        year += i
                ship['Built'] = year
        if('IMO' not in ship):
            ship['IMO'] = None
        if('Callsign' not in ship):
            ship['Callsign'] = None
        if('Type' not in ship):
            ship['Type'] = None
        if('Status' not in ship):
            ship['Status'] = None

        print 'IMO: ' + str(ship['IMO'])
        print 'NAME: ' + str(ship['Name'])
        print 'CALLSIGN: ' + str(ship['Callsign'])
        print 'GROSS TON: ' + str(ship['GrossTonnage'])
        print 'DEAD: ' + str(ship['DeadWeight'])
        print 'FLAG: ' + ship['Flag']
        print 'YEAR: ' + str(ship['Built'])
        print 'TYPE: ' + str(ship['Type'])
        print 'STATUS: ' + str(ship['Status'])
        print 'LEN: ' + str(lb[0])
        print 'BEAM: ' + str(lb[1])
        print 'MMSI: ' + s[0]
        saisdb.UpdateVesselDetailsFromMmsi(ship['IMO'], ship['Name'], ship['Callsign'], ship['GrossTonnage'], ship['DeadWeight'], ship['Flag'], ship['Built'], ship['Type'], ship['Status'], 'shipais.co.uk', lb[0], lb[1], s[0])

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
