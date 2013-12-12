CREATE TABLE public.sais_derived_tracks
(
  fk_reportid integer NOT NULL, -- Foreign key to sais_reports.id identifying the observation to which this track element applies.
  trackid integer NOT NULL, -- Identifies a distinct track. Derived from seq_tracks.
  CONSTRAINT sais_derived_tracks_pkey PRIMARY KEY (fk_reportid, trackid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.sais_derived_tracks
  OWNER TO postgres;
COMMENT ON TABLE public.sais_derived_tracks
  IS 'Table to group observations into synthesized tracks. See get_vessel_tracks() function for insertion logic.';
COMMENT ON COLUMN public.sais_derived_tracks.fk_reportid IS 'Foreign key to sais_reports.id identifying the observation to which this track element applies.';
COMMENT ON COLUMN public.sais_derived_tracks.trackid IS 'Identifies a distinct track. Derived from seq_tracks. ';


CREATE TABLE public.vesseldetails
(
  "ID" integer NOT NULL DEFAULT nextval('"vesseldetails_ID_seq"'::regclass), -- Unique identifier for vessel records.
  mmsi character varying(10),
  imo character varying(10), -- The vessel's IMO number.
  name character varying(50), -- The vessel's name.
  callsign character varying(10), -- The vessel's callsign.
  flag character varying(50), -- The vessel's flag.
  length integer, -- The vessel's length in meters.
  beam integer, -- The vessel's beam in meters.
  tonnage integer, -- The vessel's gross tonnage.
  deadweight integer, -- The vessel's deadweight.
  status character varying(100), -- The vessel's status, e.g. "lost at sea".
  type character varying(50), -- The type of vessel, e.g. "Fishing Vessel".
  yearbuilt integer, -- The year the vessel was built.
  updatedate timestamp without time zone, -- The date the record was last updated.
  createdate timestamp without time zone NOT NULL DEFAULT now(), -- The date the record was created.
  propulsion character varying(50),
  datasource character varying(100), -- The data source for this record, normally a url from which the information came.
  CONSTRAINT pk_vessels PRIMARY KEY ("ID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.vesseldetails
  OWNER TO postgres;
COMMENT ON TABLE public.vesseldetails
  IS 'Table containing vessel details such as name, imo, mmsi, size, etc';
COMMENT ON COLUMN public.vesseldetails."ID" IS 'Unique identifier for vessel records.';
COMMENT ON COLUMN public.vesseldetails.imo IS 'The vessel''s IMO number.';
COMMENT ON COLUMN public.vesseldetails.name IS 'The vessel''s name.';
COMMENT ON COLUMN public.vesseldetails.callsign IS 'The vessel''s callsign.';
COMMENT ON COLUMN public.vesseldetails.flag IS 'The vessel''s flag.';
COMMENT ON COLUMN public.vesseldetails.length IS 'The vessel''s length in meters.';
COMMENT ON COLUMN public.vesseldetails.beam IS 'The vessel''s beam in meters.';
COMMENT ON COLUMN public.vesseldetails.tonnage IS 'The vessel''s gross tonnage.';
COMMENT ON COLUMN public.vesseldetails.deadweight IS 'The vessel''s deadweight.';
COMMENT ON COLUMN public.vesseldetails.status IS 'The vessel''s status, e.g. "lost at sea".';
COMMENT ON COLUMN public.vesseldetails.type IS 'The type of vessel, e.g. "Fishing Vessel".';
COMMENT ON COLUMN public.vesseldetails.yearbuilt IS 'The year the vessel was built.';
COMMENT ON COLUMN public.vesseldetails.updatedate IS 'The date the record was last updated.';
COMMENT ON COLUMN public.vesseldetails.createdate IS 'The date the record was created.';
COMMENT ON COLUMN public.vesseldetails.datasource IS 'The data source for this record, normally a url from which the information came.';

