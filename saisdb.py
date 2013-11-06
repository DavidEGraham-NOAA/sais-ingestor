

def SaveObservation(LRIMOShipNo,Latitude,Longitude,AdditionalInfo,CallSign,Heading,MMSI,MovementDateTime,MovementID,ShipName,ShipType,Speed,Beam,Draught,Length,Destination,ETA,MoveStatus):
    #print str(Latitude) + " " + str(Longitude) + " " + str(MMSI) + " " + str(MovementDateTime)
    bob = """INSERT INTO saisobservations (imonumber, reportedpoint, latitude, longitude, additionalinfo, callsign, heading, mmsi, reportdate, movementid, shipname, shiptype, speed, beam, draught, length, destination, eta, movestatus) 
              SELECT %(imo)s, ST_GeomFromText('POINT(%(lon)s %(lat)s)', 4326), %(lat)s, %(lon)s, %(addinfo)s, %(call)s, %(head)s,%(mmsi)s,
              to_timestamp(%(movedt)s, 'YYYY-MM-DD HH24:MI:SS:MS'), %(moveid)s,%(ship)s,%(type)s,%(spd)s,%(beam)s,%(draught)s,%(length)s,%(dest)s,%(eta)s,%(move)s;
              """, {'imo': LRIMOShipNo,'lat': Latitude,'lon': Longitude,'addinfo':AdditionalInfo,'call':CallSign.strip(),'head':Heading.strip(),'mmsi':MMSI.strip(),'movedt':MovementDateTime,
              'moveid':MovementID,'ship':ShipName.strip(),'type':ShipType.strip(),'spd':Speed,'beam':Beam,'draught':Draught,'length':Length,'dest':Destination.strip(),'eta':ETA,'move':MoveStatus.strip()}
    print bob
