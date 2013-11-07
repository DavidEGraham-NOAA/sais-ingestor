SELECT ID, mmsi, reportdate, ST_AsKML(reportedpoint)
FROM sais_reports
where ID in (<ID LIST FROM R SCRIPT)
