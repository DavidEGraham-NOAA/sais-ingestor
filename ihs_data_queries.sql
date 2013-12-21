--insert ihs_observations from ihs_raw_data
INSERT INTO ihs_observations (fk_ihs_raw_id, mmsi, heading, speed, draught, reportedpoint, reportdate) 
SELECT ihs_raw_id, mmsi, heading::numeric AS head, speed::numeric, draught::numeric, 
ST_GeomFromText('Point('||longitude||' '||latitude||')''',4326),
reportdate FROM ihs_raw_data

