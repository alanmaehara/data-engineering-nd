# Building Data Lake 
---

In this project, data modeling and ELT pipeline were built for the same company (Sparkify). This time, Amazon S3 was used for data storage, and Amazon EMR + Amazon Athena were used as the company's data lake. Python was used to build the data modeling and pipelines, and Spark was used to process the data.

---
## 1. Context

The company has grown their user base and song database even more and want to move their data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## 2. Goals and Deliverables

The main goal is to build an ELT pipeline that extracts their data from S3, processes them using Spark, and loads the data back into S3 as a set of dimensional tables. This will allow their analytics team to continue finding insights in what songs their users are listening to.

## 3. Database schema and ELT pipeline

Data was read from two main data sources (JSON files):
- `s3a://udacity-dend/song_data` - data containing information regarding songs/artists present in the app
- `s3a://udacity-dend/log_data` - data containing log events from the app

### 3.1. Fact Table

**Songplays**
|No|Column|Type|Description|
|---|---|---|---|
|1|`songplay_id`|INTEGER|Log identification|
|1|`start_time`|TIMESTAMP|Date and time that a song was played by the user|
|1|`user_id`|INTEGER|The user identification who played the song|
|1|`level`|STRING|Related to the user's subscription level|
|1|`song_id`|STRING|Song identification|
|1|`artist_id`|STRING|Artist identification|
|1|`session_id`|INTEGER|Session identification|
|1|`location`|STRING|Location where the song was played|
|1|`user_agent`|STRING|The user agent utilized when the song was played|

### 3.2. Dimension Tables

**Users**
|No|Column|Type|Description|
|---|---|---|---|
|1|`user_id`|INTEGER|User identification|
|1|`first_name`|STRING|User's first name|
|1|`last_name`|STRING|User's last name|
|1|`gender`|STRING|User's gender|
|1|`level`|STRING|Related to the user's subscription level|

**Songs**
|No|Column|Type|Description|
|---|---|---|---|
|1|`song_id`|STRING|Song identification|
|1|`title`|STRING|Song's title|
|1|`artist_id`|STRING|Artist identification|
|1|`year`|INTEGER|Song's release year|
|1|`duration`|DOUBLE|Song's duration|

**Artists**
|No|Column|Type|Description|
|---|---|---|---|
|1|`artist_id`|STRING|Artist identification|
|1|`name`|STRING|Artist's first name|
|1|`location`|STRING|Artist's location|
|1|`latitude`|INTEGER|Artist's latitude location|
|1|`longitude`|INTEGER|Artist's longitude location|

**Time**
|No|Column|Type|Description|
|---|---|---|---|
|1|`start_time`|TIMESTAMP|Date and time that a song was played by the user|
|1|`hour`|INTEGER|The hour in `start_time`|
|1|`day`|INTEGER|The day in `start_time`|
|1|`week`|INTEGER|The week in `start_time`|
|1|`month`|INTEGER|The month in `start_time`|
|1|`year`|INTEGER|The year in `start_time`|
|1|`weekday`|INTEGER|The weekday in `start_time`|

To generate the tables, one should run `python etl.py`. Be sure to have the `dl.cfg` file fulfilled with AWS credentials (I left them empty in this repository)