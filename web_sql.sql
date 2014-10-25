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

CREATE OR REPLACE VIEW public.vw_track_details AS 
 SELECT DISTINCT v.fk_trackid,
    to_char(v.startdate, 'MM/DD/YYYY'::text) AS sdformatted,
    to_char(v.enddate, 'MM/DD/YYYY'::text) AS edformatted,
    vd.name,
    v.mmsi,
    v.features_intersected,
    v.atbas_intersected,
    v.pointcount,
    v.length,
    ta.invalid,
    ta.ta_id,
    v.startdate,
    v.enddate
   FROM mvw_track_details v
     LEFT JOIN vesseldetails vd ON vd.mmsi::text = v.mmsi::text
     LEFT JOIN track_analysis ta ON ta.fk_trackid = v.fk_trackid;

select * from vw_track_details

insert into vesseldetails (mmsi)  
(select o.mmsi AS mmsi
from ihs_observations o
left join vesseldetails v on o.mmsi = v.mmsi
where v.mmsi is null
group by o.mmsi) sq
