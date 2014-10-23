--Track info screen

--track details
SELECT trackid, min(reportdate), max(reportdate) 
FROM ihs_observations INNER JOIN ihs_derived_tracks_dev
ON ihs_obs_id = fk_ihs_obs_id
GROUP BY trackid
