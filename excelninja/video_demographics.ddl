CREATE TABLE video_demographics (
  measure varchar(50) NOT NULL,
  id bigint(20) NOT NULL,
  country_code varchar(10) DEFAULT NULL,
  country varchar(50) DEFAULT NULL,
  gender varchar(10) DEFAULT NULL,
  age_min int(11) DEFAULT NULL,
  age_max int(11) DEFAULT NULL,
  reach bigint(20) DEFAULT NULL,
  KEY ms_country (country),
  KEY ms_measure (measure),
  KEY ms_age_min (age_min),
  KEY ms_age_max (age_max),
  KEY ms_gender (gender)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;