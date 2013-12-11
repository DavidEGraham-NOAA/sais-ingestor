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


select * from seq_tracks

SELECT mmsi, reportdate, id 
FROM sais_reports
WHERE mmsi NOT IN ('0','1')
ORDER BY reportdate
LIMIT 50

CREATE OR REPLACE FUNCTION get_vessel_tracks() RETURNS integer AS $$
DECLARE
  vessel RECORD;
  report RECORD;
  trackmember RECORD;
  seqnum INT;
BEGIN
  FOR vessel IN SELECT mmsi FROM vesseldetails GROUP BY mmsi LOOP
    FOR report IN SELECT mmsi, min(reportdate) AS rptdate FROM sais_reports WHERE MMSI = vessel.mmsi GROUP BY mmsi LOOP
      seqnum := nextval('seq_tracks');
      FOR trackmember IN SELECT id, mmsi, reportdate FROM sais_reports WHERE mmsi = report.mmsi AND reportdate BETWEEN report.rptdate AND report.rptdate + interval '3 days' LOOP
        --for each one of these we also need to do the 3 day lookahead
        --insert here
        RAISE NOTICE 'TRACK is %, %, % with trackid %', trackmember.id, quote_ident(trackmember.mmsi), trackmember.reportdate, seqnum;
      END LOOP;
      RAISE NOTICE '----------------------END TRACK-----------------------';
    END LOOP;
    --RAISE NOTICE 'MMSI is %', quote_ident(vessel.mmsi);
  END LOOP;
  RAISE NOTICE 'Pau';
  RETURN 1;
END;
$$ LANGUAGE plpgsql;

select * from get_vessel_tracks();

select * from sais_reports where mmsi = '247184200' AND reportdate BETWEEN '2009-01-20 07:25:53'::timestamp AND '2009-01-20 07:25:53'::timestamp + interval '3 days'

select * from seq_tracks;

alter sequence seq_tracks restart with 1;
