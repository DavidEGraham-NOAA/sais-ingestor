create sequence sais_orbcomm_raw_data_pk_seq

CREATE TABLE public.sais_orbcomm_raw_data
(
  id integer NOT NULL DEFAULT nextval('sais_orbcomm_raw_data_pk_seq'::regclass),
  mmsi character varying(15),
  obsdate timestamp without time zone,
  latitude double precision,
  longitude double precision,
  status integer,
  turnrate double precision,
  heading double precision,
  sog double precision,
  cog double precision,
  pos_accuracy integer,
  raim integer,
  seconds integer,
  satid integer,
  obspoint point,
  reportedpoint geometry(Point,4326),
  obsdate_int integer,
  CONSTRAINT pk_sais_orbcomm_raw_data PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.sais_orbcomm_raw_data
  OWNER TO postgres;

COPY orbcomm_loader_tst (obsdate_int, mmsi, status, turnrate, sog, pos_accuracy, 
longitude, latitude, cog, heading)
FROM '/var/lib/pgsql/9.2/data/sep_2011_2.csv'
WITH csv

INSERT INTO sais_orbcomm_raw_data
            (mmsi, latitude, longitude, status, 
            turnrate, heading, sog, cog, pos_accuracy, obsdate_int)
select mmsi, latitude, longitude, status,
		turnrate, heading, sog, cog, pos_accuracy, obsdate_int
		FROM orbcomm_loader_tst
		
--sais_observations
--sais_derived_tracks
