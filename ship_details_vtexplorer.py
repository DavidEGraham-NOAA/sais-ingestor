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
    #MMSI = '440272000'
    urlbase = 'http://vessels.vtexplorer.com/vessels/list?search_text='
    req = urllib2.Request(urlbase + s[0],
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'})

    try:
        response = urllib2.urlopen(req)
        the_page = response.read()
        #HTTPError
        #print the_page
        dt = datetime.datetime.now()
        soup = BeautifulSoup(the_page)

        tbody = soup.find("tbody")
        ship = {}
        #namediv = soup.find("h1", {"class": "details_header_vessel"})
        #ship['name'] = namediv.get_text().strip()
        #print maindiv
        #print "------------------------"
        link1 = tbody.find("a")
        href1 = 'http://vessels.vtexplorer.com'+link1.get('href')
        #print detdiv[0]
        #print type(detdiv[0])
        req2 = urllib2.Request(href1,
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'})
        try:
            response2 = urllib2.urlopen(req2)
            the_page2 = response2.read()
            soup2 = BeautifulSoup(the_page2)
            mainp = soup2.find("p", style="font-size:1.2em;")
            link2 = mainp.find("a")
            href2 = link2.get('href')
            req = urllib2.Request(href2,
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'})
            try:
                response = urllib2.urlopen(req)
                the_page = response.read()
                soup = BeautifulSoup(the_page)
                div = soup.findAll("div", {"class": "col-xs-6 col-sm-6 col-md-6 ais-data first"})
                details1 = div[0].get_text().strip()
                details1_content = details1.splitlines()
                details2 = div[1].get_text().strip()
                details2_content = details2.splitlines()
                vname = soup.find("h1").get_text().strip()
                ship['Name'] = vname
                div2 = soup.findAll("div", {"class": "col-xs-6 col-sm-6 col-md-6 ais-data last first"})
                details3 = div2[0].get_text().strip()
                details3_content = details3.splitlines()
                key = None
                value = None
                for i in details1_content:
                    if(i != ''):
                        if(key == None):
                            key = i
                            key.strip().replace("\t", "")
                        else:
                            value = i
                            value.strip().replace("\t", "")
                            ship[key.replace(" ", "")] = value.strip()
                            key = None
                            value = None
                for i in details2_content:
                    if(i != ''):
                        if(key == None):
                            key = i
                        else:
                            value = i
                            ship[key.strip().replace("\t", "")] = value.strip()
                            key = None
                            value = None
                for i in details3_content:
                    if(i != ''):
                        if(key == None):
                            key = i
                        else:
                            value = i
                            ship[key.strip().replace("\t", "")] = value.strip()
                            key = None
                            value = None

                #ship now contains all our vessel details we can get
                
                if('Name' in ship):
                    pass
                else:
                    ship['Name'] = None
                    vname = None
                if ('Size' in ship):
                    ship['Size'] = re.sub("m", "", ship['Size'])
                    ship['Size'] = re.sub(" ", "", ship['Size'])
                    lb = ship['Size'].split("x")
                    lb[0] = re.sub('\D', "", lb[0])
                    lb[1] = re.sub('\D', "", lb[1])
                else:
                    ship['Size'] = None
                    lb = None
                    lb = []
                    lb.append(None)
                    lb.append(None)
                if ('GT' in ship):
                    ship['GT'] = re.sub("t", "", ship['GT'])
                    ship['GT'] = re.sub('\D', "", ship['GT'])
                    if(ship['GT'] == ""):
                        ship['GT'] = None
                else:
                    ship['GT'] = None
                if ('DWT' in ship):
                    ship['DWT'] = re.sub("t", "", ship['DWT'])
                    ship['DWT'] = re.sub('\D', "", ship['DWT'])
                    if (ship['DWT'] == ""):
                        ship['DWT'] = None
                else:
                    ship['DWT'] = None
                ship['LengthxBreadth'] = ship['Size']
                if('Built' not in ship):
                    ship['Built'] = None
                else:
                    ship['Built'] = re.sub('\D', "", ship["Built"])
                    if(ship['Built'] == ""):
                        ship['Built'] = None
                if('IMO' not in ship):
                    ship['IMO'] = None
                if('Callsign' not in ship):
                    ship['Callsign'] = None
                if('Shiptype' not in ship):
                    ship['Shiptype'] = None

                print 'IMO: ' + str(ship['IMO'])
                print 'NAME: ' + str(ship['Name'])
                print 'CALLSIGN: ' + str(ship['Callsign'])
                print 'GROSS TON: ' + str(ship['GT'])
                print 'DEAD: ' + str(ship['DWT'])
                print 'FLAG: ' + ship['Flag']
                print 'YEAR: ' + str(ship['Built'])
                print 'TYPE: ' + str(ship['Shiptype'])
                print 'LEN: ' + lb[0]
                print 'BEAM: ' + lb[1]
                print 'MMSI: ' + s[0]
                saisdb.UpdateVesselDetailsFromMmsi(ship['IMO'], ship['Name'], ship['Callsign'], ship['GT'], ship['DWT'], ship['Flag'], ship['Built'], ship['Shiptype'], None, 'vessels.vtexplorer.com', lb[0], lb[1], s[0])

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
