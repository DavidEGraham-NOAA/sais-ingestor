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
