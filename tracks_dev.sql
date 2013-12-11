CREATE OR REPLACE FUNCTION get_vessel_details() RETURNS integer AS $$
DECLARE
  vessel RECORD;
BEGIN
  FOR vessel IN SELECT mmsi FROM vesseldetails GROUP BY mmsi LIMIT 50 LOOP
    RAISE NOTICE 'MMSI is %', quote_ident(vessel.mmsi);
  END LOOP;
  RAISE NOTICE 'Pau';
  RETURN 1;
END;
$$ LANGUAGE plpgsql;

select * from get_vessel_details();

SELECT mmsi, reportdate, id 
FROM sais_reports
WHERE mmsi NOT IN ('0','1')
ORDER BY reportdate
LIMIT 50

select * from seq_tracks
