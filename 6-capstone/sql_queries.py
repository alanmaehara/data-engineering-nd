import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

immigration_completed_drop = "DROP TABLE IF EXISTS immigration_completed"
temp_drop = "DROP TABLE IF EXISTS temp"
demo_drop = "DROP TABLE IF EXISTS demo"
airport_drop = "DROP TABLE IF EXISTS airport"

staging_immigration_drop = "DROP TABLE IF EXISTS staging_immigration"
staging_temp_drop = "DROP TABLE IF EXISTS staging_temp"
staging_demo_drop = "DROP TABLE IF EXISTS staging_demo"
staging_airport_drop = "DROP TABLE IF EXISTS staging_airport"


# CREATE TABLES


immigration_completed_table_create = ("""
    CREATE TABLE IF NOT EXISTS immigration_completed (
        cicid                   DOUBLE PRECISION NOT NULL SORTKEY,
        i94yr                   DOUBLE PRECISION,
        i94mon                  DOUBLE PRECISION,
        i94port                 VARCHAR,
        i94mode                 DOUBLE PRECISION,
        i94addr                 VARCHAR,
        i94bir                  DOUBLE PRECISION,
        i94visa                 DOUBLE PRECISION,
        biryear                 DOUBLE PRECISION,
        gender                  VARCHAR,
        visatype                VARCHAR,
        arrival_date            TIMESTAMP WITHOUT TIME ZONE,
        departure_date          TIMESTAMP WITHOUT TIME ZONE,
        airport_type            VARCHAR,
        airport_name            VARCHAR,
        iso_region              VARCHAR,
        local_code              VARCHAR DISTKEY,
        average_temp            DECIMAL,
        city                    VARCHAR,
        median_age              DECIMAL,
        male_pop                INTEGER,
        fem_pop                 INTEGER, 
        total_pop               INTEGER,
        foreign_born            INTEGER
    );
""")

temp_table_create = ("""
    CREATE TABLE IF NOT EXISTS temp (
        city                                VARCHAR NOT NULL DISTKEY,
        dt                                  TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        year                                INTEGER,
        month                               INTEGER,
        average_temp                        DECIMAL
        );
""")

demo_table_create = ("""
    CREATE TABLE IF NOT EXISTS demo (
        city                    VARCHAR NOT NULL DISTKEY,
        median_age              DECIMAL, 
        male_pop                INTEGER, 
        fem_pop                 INTEGER,
        total_pop               INTEGER, 
        foreign_born            INTEGER
    );
""")

airport_table_create = ("""
    CREATE TABLE IF NOT EXISTS airport (
        local_code      VARCHAR NOT NULL DISTKEY,
        airport_code    VARCHAR,
        airport_type    VARCHAR,
        airport_name    VARCHAR,
        iso_region      VARCHAR,
        municipality    VARCHAR,
        iata_code       VARCHAR,
        coordinates     VARCHAR 
    );
""")


staging_immigration_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_immigration (
        cicid           DOUBLE PRECISION NOT NULL SORTKEY,
        i94yr           DOUBLE PRECISION,
        i94mon          DOUBLE PRECISION,
        i94port         VARCHAR,
        i94mode         DOUBLE PRECISION,
        i94addr         VARCHAR,
        i94bir          DOUBLE PRECISION DISTKEY,
        i94visa         DOUBLE PRECISION,
        biryear         DOUBLE PRECISION,
        gender          VARCHAR,
        visatype        VARCHAR,
        arrival_date    TIMESTAMP WITHOUT TIME ZONE,
        departure_date  TIMESTAMP WITHOUT TIME ZONE
    );
""")

staging_temp_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_temp (
        dt                                  TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        AverageTemperature                  DECIMAL,
        AverageTemperatureUncertainty       DECIMAL,
        City                                VARCHAR NOT NULL DISTKEY,
        Country                             VARCHAR,
        Latitude                            VARCHAR,
        Longitude                           VARCHAR,
        year                                INTEGER,
        month                               INTEGER,
        day                                 INTEGER
    );
""")

staging_demo_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_demo (
        city                    VARCHAR NOT NULL DISTKEY,
        state                   VARCHAR, 
        median_age              DECIMAL, 
        male_population         INTEGER, 
        female_population       INTEGER,
        total_population        INTEGER, 
        number_of_veterans      INTEGER, 
        foreign_born            INTEGER, 
        average_household_size  DECIMAL, 
        state_code              VARCHAR, 
        race                    VARCHAR, 
        count                   INTEGER 
    );
""")

staging_airport_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_airport (
        ident           VARCHAR,
        type            VARCHAR,
        name            VARCHAR,
        elevation_ft    INTEGER,
        continent       VARCHAR,
        iso_country     VARCHAR,
        iso_region      VARCHAR,
        municipality    VARCHAR ,
        gps_code        VARCHAR,
        iata_code       VARCHAR,
        local_code      VARCHAR NOT NULL DISTKEY,
        coordinates     VARCHAR 

    );
""")



# STAGING TABLES

staging_immigration_copy = ("""
    COPY staging_immigration FROM {}
    credentials 'aws_iam_role={}'
    format as parquet;
""").format(config.get('S3', 'IMMIGRATION_DATA'), config.get('IAM_ROLE', 'ARN'))

staging_temp_copy = ("""
    COPY staging_temp FROM {}
    credentials 'aws_iam_role={}'
    CSV
    dateformat 'auto'
    timeformat 'auto'
    IGNOREHEADER 1
    region 'us-east-1';
""").format(config.get('S3', 'TEMP_DATA'), config.get('IAM_ROLE', 'ARN'))

staging_demo_copy = ("""
    COPY staging_demo FROM {}
    credentials 'aws_iam_role={}'
    CSV
    dateformat 'auto'
    timeformat 'auto'
    IGNOREHEADER 1
    region 'us-east-1';
""").format(config.get('S3', 'DEMO_DATA'), config.get('IAM_ROLE', 'ARN'))

staging_airport_copy = ("""
    COPY staging_airport FROM {}
    credentials 'aws_iam_role={}'
    CSV
    dateformat 'auto'
    timeformat 'auto'
    IGNOREHEADER 1
    region 'us-east-1';
""").format(config.get('S3', 'AIRPORT_DATA'), config.get('IAM_ROLE', 'ARN'))

# CLEANED TABLES

temp_table_insert = ("""
    INSERT INTO temp (city, dt, year, month, average_temp)
    SELECT   
    LOWER(City) as city,
    dt,
    year,
    month,
    AverageTemperature as average_temp
    FROM staging_temp
""")

demo_table_insert = ("""
    INSERT INTO demo (city, median_age, male_pop, fem_pop, total_pop,foreign_born)
    SELECT 
    LOWER(city) as city,
    median_age,
    male_population as male_pop,
    female_population as fem_pop,
    total_population as total_pop,
    foreign_born
    FROM staging_demo
    
""")

airport_table_insert = ("""
    INSERT INTO airport (local_code, airport_code, airport_type, airport_name, iso_region, municipality, iata_code, coordinates)
    SELECT local_code,
    ident as airport_code,
    type as airport_type,
    name as airport_name,
    iso_region,
    LOWER(municipality) as municipality,
    iata_code,
    coordinates
    FROM staging_airport
    WHERE local_code IS NOT NULL
""")

# FINAL TABLE


immigration_completed_table = ("""
    INSERT INTO immigration_completed (cicid, i94yr, i94mon, i94port, i94mode, i94addr, i94bir, i94visa, biryear, gender, visatype, arrival_date, departure_date, airport_type, airport_name, iso_region, local_code, average_temp, city, median_age, male_pop, fem_pop, total_pop, foreign_born)
    SELECT  i.cicid as cicid, 
            i.i94yr as i94yr, 
            i.i94mon as i94mon, 
            i.i94port as i94port, 
            i.i94mode as i94mode, 
            i.i94addr as i94addr, 
            i.i94bir as i94bir, 
            i.i94visa as i94visa,
            i.biryear as biryear, 
            i.gender as gender, 
            i.visatype as visatype, 
            i.arrival_date as arrival_date, 
            i.departure_date as departure_date, 
            a.airport_type as airport_type, 
            a.airport_name as airport_name, 
            a.iso_region as iso_region, 
            a.local_code as local_code, 
            t.average_temp as average_temp, 
            t.city as city, 
            d.median_age as median_age,  
            d.male_pop as male_pop, 
            d.fem_pop as fem_pop, 
            d.total_pop as total_pop,
            d.foreign_born as foreign_born
        FROM staging_immigration i
        LEFT JOIN airport a ON (i.i94port = a.local_code)
        LEFT JOIN temp t ON (a.municipality = t.city AND i.i94mon = t.month)
        LEFT JOIN demo d ON (a.municipality = d.city)
""")

# QUERY LISTS

drop_table_queries = [immigration_completed_drop, staging_immigration_drop, temp_drop, staging_temp_drop, demo_drop, staging_demo_drop, airport_drop, staging_airport_drop] 

create_table_queries = [immigration_completed_table_create, staging_immigration_table_create, staging_temp_table_create, staging_demo_table_create, staging_airport_table_create, temp_table_create, demo_table_create, airport_table_create]

copy_table_queries = [staging_immigration_copy, staging_demo_copy, staging_temp_copy, staging_airport_copy]

insert_table_queries = [temp_table_insert, demo_table_insert, airport_table_insert, immigration_completed_table]
