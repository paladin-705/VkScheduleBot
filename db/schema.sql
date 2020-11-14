CREATE TABLE organizations
(
  id serial,
  organization character varying(80),
  faculty character varying(80),
  studgroup character varying(20),
  tag character(30) PRIMARY KEY
);

CREATE EXTENSION pg_trgm;
CREATE INDEX trgm_idx ON organizations USING GIN (lower(organization || ' ' || faculty || ' ' || studgroup) gin_trgm_ops);

CREATE TABLE schedule
(
  id serial,
  tag character(30),
  day character varying(10),
  "number" smallint,
  type smallint,
  "startTime" time without time zone,
  "endTime" time without time zone,
  title character varying(100),
  classroom character varying(50),
  lecturer character varying(50),
  PRIMARY KEY (tag, day, number, type),
  CONSTRAINT schedule_fkey FOREIGN KEY (tag)
	REFERENCES organizations (tag) MATCH SIMPLE
	ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE examinations
(
  tag character(30),
  title character varying(100),
  classroom character varying(50),
  lecturer character varying(50),
  day date,
  CONSTRAINT examinations_fkey FOREIGN KEY (tag)
	REFERENCES organizations (tag) MATCH SIMPLE
	ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE users
(
  type character(2),
  id integer,
  name character varying(30),
  username character varying(30),
  "scheduleTag" character(30),
  auto_posting_time time without time zone,
  is_today boolean,
  registration_timestamp timestamp with time zone DEFAULT now(),
  PRIMARY KEY (type, id)
);

CREATE VIEW users_vw AS 
 SELECT users.type,
    users.id,
    organizations.organization,
    organizations.faculty,
    organizations.studgroup,
    users.auto_posting_time,
    users.is_today,
    users.registration_timestamp
   FROM users
     JOIN organizations ON users."scheduleTag" = organizations.tag
 ORDER BY organizations.studgroup;

CREATE TABLE reports
(
  type character(2),
  report_id serial PRIMARY KEY,
  user_id integer,
  report text,
  date date
);

CREATE TABLE api_users
(
  id serial PRIMARY KEY,
  username character varying(50),
  pw_hash character(60)
)