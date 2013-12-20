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
  internaltrack RECORD;
  seqnum INT;
BEGIN
  FOR vessel IN SELECT mmsi FROM vesseldetails GROUP BY mmsi LOOP
    FOR report IN SELECT mmsi, min(reportdate) AS rptdate FROM sais_reports WHERE MMSI = vessel.mmsi GROUP BY mmsi LOOP
      seqnum := nextval('seq_tracks');
      FOR trackmember IN SELECT id, mmsi, reportdate FROM sais_reports WHERE mmsi = report.mmsi AND reportdate BETWEEN report.rptdate AND report.rptdate + interval '3 days' LOOP
        --for each one of these we also need to do the 3 day lookahead
        --insert here
        --RAISE NOTICE 'TRACK is %, %, % with trackid %', trackmember.id, quote_ident(trackmember.mmsi), trackmember.reportdate, seqnum;
          FOR internaltrack IN SELECT id, mmsi, reportdate FROM sais_reports WHERE mmsi = trackmember.mmsi AND reportdate BETWEEN trackmember.reportdate AND trackmember.reportdate + interval '3 days' LOOP
            INSERT INTO sais_derived_tracks (fk_reportid, trackid) SELECT internaltrack.id, seqnum WHERE NOT EXISTS (SELECT * FROM sais_derived_tracks WHERE fk_reportid =  internaltrack.id);
            RAISE NOTICE 'INTERNAL TRACK is %, %, % with trackid %', internaltrack.id, quote_ident(internaltrack.mmsi), internaltrack.reportdate, seqnum;
          END LOOP;
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

alter sequence seq_tracks restart with 1;

select * from sais_derived_tracks

select count(fk_reportid), trackid from sais_derived_tracks group by trackid order by count desc

select * from sais_derived_tracks where trackid = 14304

select * from sais_reports where id = 181054

select * from sais_reports where mmsi = '477144240'

SELECT * FROM vesseldetails WHERE updatedate IS NULL LIMIT 50;


CREATE OR REPLACE FUNCTION public.ihs_get_vessel_tracks()
  RETURNS integer AS
$BODY$
DECLARE
  vessel RECORD;
  report RECORD;
  trackmember RECORD;
  internaltrack RECORD;
  seqnum INT;
BEGIN
  FOR vessel IN SELECT mmsi FROM ihs_observations GROUP BY mmsi LOOP
    FOR report IN SELECT mmsi, min(reportdate) AS rptdate FROM sais_reports WHERE MMSI = vessel.mmsi GROUP BY mmsi LOOP
      seqnum := nextval('seq_tracks');
      FOR trackmember IN SELECT id, mmsi, reportdate FROM sais_reports WHERE mmsi = report.mmsi AND reportdate BETWEEN report.rptdate AND report.rptdate + interval '3 days' LOOP
        --for each one of these we also need to do the 3 day lookahead
        --insert here
        --RAISE NOTICE 'TRACK is %, %, % with trackid %', trackmember.id, quote_ident(trackmember.mmsi), trackmember.reportdate, seqnum;
          FOR internaltrack IN SELECT id, mmsi, reportdate FROM sais_reports WHERE mmsi = trackmember.mmsi AND reportdate BETWEEN trackmember.reportdate AND trackmember.reportdate + interval '3 days' LOOP
            INSERT INTO sais_derived_tracks (fk_reportid, trackid) SELECT internaltrack.id, seqnum WHERE NOT EXISTS (SELECT * FROM sais_derived_tracks WHERE fk_reportid =  internaltrack.id);
            RAISE NOTICE 'INTERNAL TRACK is %, %, % with trackid %', internaltrack.id, quote_ident(internaltrack.mmsi), internaltrack.reportdate, seqnum;
          END LOOP;
      END LOOP;
      RAISE NOTICE '----------------------END TRACK-----------------------';
    END LOOP;
    --RAISE NOTICE 'MMSI is %', quote_ident(vessel.mmsi);
  END LOOP;
  RAISE NOTICE 'Pau';
  RETURN 1;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.get_vessel_tracks()
  OWNER TO postgres;

