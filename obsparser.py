import sys
import csv
import saisdb

#csv_file = '/media/Seagate Backup Plus Drive/GIS/sais_IHS/combinedhistorydata 2008.txt'
#csv_file = '/media/Seagate Backup Plus Drive/GIS/sais_IHS/combinedhistorydata 2009.txt'
#csv_file = '/media/Seagate Backup Plus Drive/GIS/sais_IHS/combinedhistorydata 2010.txt'
#csv_file = '/media/Seagate Backup Plus Drive/GIS/sais_IHS/combinedhistorydata 2011.txt'
#csv_file = '/media/Seagate Backup Plus Drive/GIS/sais_IHS/combinedhistorydata 2012.txt'
#csv_file = '/media/Seagate Backup Plus Drive/GIS/sais_IHS/combinedhistorydata 2013.txt'

# open csv file
with open(csv_file, 'rb') as csvfile:

    # get number of columns
    for line in csvfile.readlines():
        array = line.split(',')
        first_item = array[0]

    num_columns = len(array)
    csvfile.seek(0)

    reader = csv.reader(csvfile)
    #skip the header row
    reader.next()
    #LRIMOShipNo,Latitude,Longitude,AdditionalInfo,CallSign,Heading,MMSI,"MovementDateTime",MovementID,"ShipName","ShipType","Speed","Beam","Draught","Length","Destination","ETA","MoveStatus"
    included_cols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

    for row in reader:
        content = list(row[i] for i in included_cols)
        #print len(content)
        saisdb.SaveObservation(content[0], float(content[1]), float(content[2])*-1, content[3], content[4], content[5], content[6], content[7], content[8], content[9], content[10], content[11], content[12], content[13], content[14], content[15], content[16], content[17])
        #print content[0]
