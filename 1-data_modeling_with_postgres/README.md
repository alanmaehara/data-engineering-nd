# Building ETL pipeline for Sparkify
---

In this project, data modeling and ETL pipeline were built for a major music streaming company. Postgres and python were used to build the data modeling and pipelines.

---
## 1. Context

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## 2. Goals and Deliverables

The goal is to create a Postgres database with tables designed to optimize queries on song play analysis. In this project, the deliverables were: **(1) create a database (star schema structure)** to receive the JSON logs in an adequate setting; **(2) build a reliable ETL pipeline** to afford the usage of queries of interest by the analytics team.

## 3. Dataset Description & Database Schema

Two main sources were given for this project. One is a subset of the [Million Song Dataset](https://labrosa.ee.columbia.edu/millionsong/), which contains a list of artists and songs. The other is a dataset with activity logs from Sparkify's users.

In this project, one fact and four dimension tables on a star schema layout were defined, and ETL pipeline was built to transfer local files into tables in Postgres using Python and SQL.

### 3.1. Fact Table

**Songplays**
|No|Column|Type|Description|
|---|---|---|---|
|1|`songplay_id`|SERIAL PRIMARY KEY|Log identification|
|1|`start_time`|TIMESTAMP NOT NULL|Date and time that a song was played by the user|
|1|`user_id`|INT NOT NULL|The user identification who played the song|
|1|`level`|VARCHAR|Related to the user's subscription level|
|1|`song_id`|VARCHAR|Song identification|
|1|`artist_id`|VARCHAR|Artist identification|
|1|`session_id`|INT NOT NULL|Session identification|
|1|`location`|VARCHAR|Location where the song was played|
|1|`user_agent`|VARCHAR|The user agent utilized when the song was played|

### 3.2. Dimension Tables

**Users**
|No|Column|Type|Description|
|---|---|---|---|
|1|`user_id`|INT PRIMARY KEY|User identification|
|1|`first_name`|VARCHAR NOT NULL|User's first name|
|1|`last_name`|VARCHAR NOT NULL|User's last name|
|1|`gender`|CHAR(1)|User's gender|
|1|`level`|VARCHAR NOT NULL|Related to the user's subscription level|

**Songs**
|No|Column|Type|Description|
|---|---|---|---|
|1|`song_id`|VARCHAR PRIMARY KEY|Song identification|
|1|`title`|VARCHAR NOT NULL|Song's title|
|1|`artist_id`|VARCHAR NOT NULL|Artist identification|
|1|`year`|INT|Song's release year|
|1|`duration`|NUMERIC (15,5) NOT NULL|Song's duration|

**Artists**
|No|Column|Type|Description|
|---|---|---|---|
|1|`artist_id`|VARCHAR PRIMARY KEY|Artist identification|
|1|`name`|VARCHAR NOT NULL|Artist's first name|
|1|`location`|VARCHAR|Artist's location|
|1|`latitude`|NUMERIC|Artist's latitude location|
|1|`longitude`|NUMERIC|Artist's longitude location|

**Time**
|No|Column|Type|Description|
|---|---|---|---|
|1|`start_time`|TIMESTAMP PRIMARY KEY|Date and time that a song was played by the user|
|1|`hour`|NUMERIC NOT NULL|The hour in `start_time`|
|1|`day`|NUMERIC NOT NULL|The day in `start_time`|
|1|`week`|NUMERIC NOT NULL|The week in `start_time`|
|1|`month`|NUMERIC NOT NULL|The month in `start_time`|
|1|`year`|NUMERIC NOT NULL|The year in `start_time`|
|1|`weekday`|NUMERIC NOT NULL|The weekday in `start_time`|

To generate the tables, two files were created:

1. `sql_queries.py` : it contains all queries to create, insert, update, and delete tables;
2. `create_tables.py`: calls `sql_queries.py` to create and drop tables (if necessary).

## 4. ETL Pipeline

The ETL pipeline is fully described in the `etl.ipynb` file, and it mocks the ETL process contained in the `etl.py` with some data samples.  

Once the `etl.ipynb` ran without issues, the `etl.py` was built and ran with the entire dataset. In order to visualize the final result, the `test.ipynb` file was created to display the generated tables and entries.

In summary, once the ETL pipeline was built, the following scripts were ran from the terminal (in order) so that the tables would become available for Sparkify's team:
1. `python create_tables.py`
2. `python etl.py`

