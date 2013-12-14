'ship_name','ship_callsign','ship_flag','ship_imo','ship_length','ship_tonnage','ship_type','mmsi'

CREATE TABLE shipmetadataloader (ship_name varchar(50), callsign varchar(20), flag varchar(50),
imo varchar(20), length numeric, tonnage numeric, ship_type varchar(50), mmsi varchar(20))

COPY shipmetadataloader FROM '/var/lib/pgsql/ShipMetadata.txt' DELIMITER ',' CSV;

select * from shipmetadataloader
