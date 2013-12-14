--selects basic observation data from postgis database with kml point info for inspection
SELECT ID, mmsi, reportdate, ST_AsKML(reportedpoint)
FROM sais_reports
WHERE ID IN (
--<ID LIST FROM R SCRIPT>
)


select '<Placemark id="' || testID || '"><description>' || mmsi || ' - ' || reportdate || '</description>' || ST_AsKML(reportedpoint) || '</Placemark>'
FROM sais_test
where testID in
