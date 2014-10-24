--Track info screen

--track details
SELECT trackid, min(reportdate), max(reportdate) 
FROM ihs_observations INNER JOIN ihs_derived_tracks_dev
ON ihs_obs_id = fk_ihs_obs_id
GROUP BY trackid


--start and end dates
update mvw_track_details set startdate = sq.startdate, enddate = sq.enddate 
from (SELECT trackid, min(reportdate) as startdate, max(reportdate) as enddate
FROM ihs_observations INNER JOIN ihs_derived_tracks_dev
ON ihs_obs_id = fk_ihs_obs_id
GROUP BY trackid) AS sq
where trackid = sq.trackid


update mvw_track_details set startdate = sq.startdate, 
enddate = sq.enddate, mmsi = sq.mmsi
from (SELECT trackid, min(reportdate) as startdate, max(reportdate) as enddate,
min(mmsi) AS mmsi
FROM ihs_observations INNER JOIN ihs_derived_tracks_dev
ON ihs_obs_id = fk_ihs_obs_id
GROUP BY trackid) AS sq
where fk_trackid = sq.trackid

select * from mvw_track_details

drop view vw_track_details

CREATE OR REPLACE VIEW vw_track_details AS
SELECT DISTINCT v.fk_trackid, 
	to_char(startdate, 'MM/DD/YYYY') AS sdformatted, 
	to_char(enddate, 'MM/DD/YYYY') AS edformatted, 
	vd.name,
	vd.mmsi,
	features_intersected, 
	atbas_intersected, 
	pointcount, 
	v.length,
	ta.invalid,
	startdate,
	enddate
FROM mvw_track_details v
	LEFT OUTER JOIN vesseldetails vd on vd.mmsi = v.mmsi
	LEFT OUTER JOIN track_analysis ta on ta.fk_trackid = v.fk_trackid

select * from vw_track_details

insert into vesseldetails (mmsi)  
(select o.mmsi AS mmsi
from ihs_observations o
left join vesseldetails v on o.mmsi = v.mmsi
where v.mmsi is null
group by o.mmsi) sq
