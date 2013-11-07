--selects basic observation data from postgis database with kml point info for inspection
SELECT ID, mmsi, reportdate, ST_AsKML(reportedpoint)
FROM sais_reports
WHERE ID IN (
--<ID LIST FROM R SCRIPT>
)
