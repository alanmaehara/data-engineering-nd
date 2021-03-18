# Capstone
---

In this project, data modeling and ETL pipeline were built for a major travel agency company in the US. For data storage, Amazon S3 was utilized. For data warehouse, Amazon Redshift was the chosen solution, and ETL process was conducted in python to build the data modeling and pipelines.

---
## 1. Context

The travel agency company is currently struggling to promote its services, and a change in the business strategy is expected in the short-term. The company is considering to target foreigners living in the US or temporary workers/travellers, as it has never focused on marketing strategies for foreigners.

The data analytics & engineering department received the task to build databases and answer the following business questions:
1. What are the common US destinations for immigrants per month?
2. What are the demographics (median age, population size, average household size) for the cities with highest number of immigrants?

## 2. Goals and Deliverables

Build an ETL process that enable company's stakeholders to access the data according to their needs. In this project, data modeling and pipelines were done with Python, while Amazon S3 and Redshift were the main cloud-solution to deliver ready-to-use data for users.

## 3. Dataset Description & Database Schema

The following data sources were utilized in this project:

- **Immigration Table**: This data comes from the [US National Tourism and Trade Office](https://travel.trade.gov/research/reports/i94/historical/2016.html), and contains historical data from immigrants who entered in the US in 2016. A data dictionary is included in the repository. 
- **Airport Table**: This is a simple table of airport codes and corresponding cities. It comes from [Datahub](https://datahub.io/core/airport-codes#data).
- **Temperature Table**: This data comes from [Kaggle's World Temperature Data](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data). Data from the most recent and usable year was utilized in this project (2012).
- **Demographic Table**: This data comes from the [US Census Bureau's 2015 American Community Survey](https://public.opendatasoft.com/explore/dataset/us-cities-demographics/information/?dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6InVzLWNpdGllcy1kZW1vZ3JhcGhpY3MiLCJvcHRpb25zIjp7fX0sImNoYXJ0cyI6W3siYWxpZ25Nb250aCI6dHJ1ZSwidHlwZSI6ImNvbHVtbiIsImZ1bmMiOiJBVkciLCJ5QXhpcyI6Im1lZGlhbl9hZ2UiLCJzY2llbnRpZmljRGlzcGxheSI6dHJ1ZSwiY29sb3IiOiIjRkY1MTVBIn1dLCJ4QXhpcyI6ImNpdHkiLCJtYXhwb2ludHMiOjUwLCJzb3J0IjoiIn1dLCJ0aW1lc2NhbGUiOiIiLCJkaXNwbGF5TGVnZW5kIjp0cnVlLCJhbGlnbk1vbnRoIjp0cnVlfQ%3D%3D). It contains demographic data in the US.

### 3.1. Fact Table

**Immigration - 3,096,313 entries**
|No|Column|Type|Description|
|---|---|---|---|
|1|`cicid`|DOUBLE PRECISION|ID|
|2|`i94yr`|DOUBLE PRECISION|Arrival year|
|3|`i94mon`|DOUBLE PRECISION|Arrival month|
|4|`i94port`|VARCHAR|Port where immigrant disembarked (three-character code|
|5|`i94mode`|DOUBLE PRECISION|Transportation mode to the US|
|6|`i94addr`|VARCHAR(2)|State where immigrant is located|
|7|`i94bir`|DOUBLE PRECISION|Age|
|8|`i94visa`|DOUBLE PRECISION|Reason of stay|
|9|`biryear`|DOUBLE PRECISION|Year of birth|
|10|`gender`|VARCHAR|Gender|
|11|`visatype`|VARCHAR|Visa Type|
|12|`arrival_date`|TIMESTAMP WITHOUT TIME ZONE|Date of arrival in the US|
|13|`departure_date`|TIMESTAMP WITHOUT TIME ZONE|Date of departure in the US|

### 3.2. Dimension Table

**Airport - 52,998 entries**
|No|Column|Type|Description|
|---|---|---|---|
|1|`airport_code`|VARCHAR(4)|Airport code. It may refer to either IATA airport code (a three-letter code which is used in passenger reservation, ticketing and baggage-handling systems) or the ICAO airport code (a four letter code used by ATC systems and for airports that do not have an IATA airport code)|
|2|`airport_type`|VARCHAR|Airport type|
|3|`airport_name`|VARCHAR|Airport name|
|4|`iso_region`|VARCHAR|Country region where airport is located|
|5|`municipality`|VARCHAR|Airport city name|
|6|`iata_code`|VARCHAR|IATA airport code. If airport doesn't have a IATA code, NaN is displayed|
|7|`local_code`|VARCHAR|local airport code. Foreign Key to Immigration data Table, column `i94port`|
|8|`coordinates`|VARCHAR|Geolocation coordinates of the airport|

**Temperature - 3,448 entries**
|No|Column|Type|Description|
|---|---|---|---|
|1|`dt`|TIMESTAMP|timestamp with year, month, and day|
|2|`AverageTemperature`|DECIMAL|Average temperature in Celsius|
|3|`city`|VARCHAR|City where temperature measurements were taken|
|3|`year`|VARCHAR|City where temperature measurements were taken|
|3|`month`|VARCHAR|City where temperature measurements were taken|

**Demographic - 567 entries**
|No|Column|Type|Description|
|---|---|---|---|
|1|`city`|VARCHAR|City|
|2|`median_age`|INTEGER|City's median age|
|3|`male_pop`|INTEGER|Number of male population|
|4|`fem_pop`|INTEGER|Number of female population|
|5|`total_pop`|INTEGER|Total population|
|6|`foreign_born`|INTEGER|Number of foreign-born people living in the city|

All of them were stored in Amazon S3 for further ETL.

## 4. ETL Pipeline

The ETL step is pretty straight-forward given the size and nature of the sources. Extraction was done on each particular data source location, and storage was done in Amazon S3. This raw data would be leveraged by Amazon Redshift, in which we will carry on the transformation step. We could use cloud-machines like Amazon EC2 or more robust solutions such as the Amazon EMR to leverage the use of Apache Spark, but since this project is simple and won't require updates in the data source, ETL was triggered locally.

A cheaper option would be to use an on-premise solution, based in a single local machine. Since Amazon credits were available for learners in this particular nanodegree course, we will make use of these credits by using cloud solutions.

The entire process is as follows:

1. S3 as data lake: ingest raw data in Amazon S3;
2. Create clusters in Amazon Redshift and generate final tables to receive cleaned data;
3. Copy raw data to Redshift, perform data cleaning and transformations, and ingest cleaned data to Redshift tables. 

### 4.1 Data Cleaning, Data Quality Checks, and Data Transformation

Data cleaning and transformation were done in the `data_quality.ipynb` file. The following tasks were performed:
- In the immigration table, SAS-formatted dates `arrdate` and `depdate` were transformed to proper dates in 'YY-MM-DD' format. Null values in the `i94port` column were removed, and duplicates in the `cicid` column were removed (if any).
- In the airport table, null values and duplicates in the `local_code` columns were removed.
- Using the immigration table (fact) as a base table, perform a left join with table airport on `i94port` and `local_code`.
- In the temperature table, transform `dt` variable into timestamp, and split it to columns `year`, `month`. Filter temperature table to Year 2012. Remove duplicates from column `City`.
- In the demographics table, remove duplicates on column `City`.
- Set `municipality` (from airport table), `City` (temperature table), and `City` (demographic table) to lowercase.
- With the remnant table, perform a left join with temperature table on `municipality` = `city`, and `i94mon` = `month`. Use the immigration table as the main table.
- Left join the immigration table with demographic table on `municipality` = `City`.

To generate the tables, two files were created:

1. `create_cluster.ipynb`: used to programmaticaly create AWS Redshift clusters for this project.
2. `sql_queries.py` : it contains all queries to create, insert, update, and delete tables;
3. `create_tables.py`: calls `sql_queries.py` to create and drop tables (if necessary).

In summary, once the ETL pipeline was built, the following scripts were ran from the terminal (in order) so that the tables would become available for the company:
1. `python create_tables.py`
2. `python etl.py`

### 4.2. Data Dictionary

The final table contains the following columns:

**immigration_completed - 3,096,313 entries**
|No|Column|Type|
|---|---|---|
|1|cicid               |DOUBLE PRECISION
|2|i94yr               |DOUBLE PRECISION
|3|i94mon              |DOUBLE PRECISION
|4|i94port             |VARCHAR
|5|i94mode             |DOUBLE PRECISION
|6|i94addr             |VARCHAR
|7|i94bir              |DOUBLE PRECISION
|8|i94visa             |DOUBLE PRECISION
|9|biryear             |DOUBLE PRECISION
|10|gender               |VARCHAR
|11|visatype           |VARCHAR
|12|arrival_date        |TIMESTAMP WITHOUT TIME ZONE
|13|departure_date       |TIMESTAMP WITHOUT TIME ZONE
|14|airport_type          |VARCHAR
|15|airport_name           |VARCHAR
|16|iso_region              |VARCHAR
|17|local_code              |VARCHAR
|18|average_temp            |DECIMAL
|19|city                    |VARCHAR
|20|median_age              |DECIMAL
|21|male_pop                |INTEGER
|22|fem_pop                 |INTEGER
|23|total_pop               |INTEGER
|24|foreign_born            |INTEGER




# 5. Addressing Other Scenarios

This project could have been dealt differently in some other scenarios:

**SCENARIO 1 - The data was increased by 100x.**
In this scenario, we would make use of Amazon EMR and leverage data transfer and transformations with Spark. Raw data would be put in S3 buckets (as we did) but the whole operation would be done with Spark.

**SCENARIO 2 - The pipelines would be run on a daily basis by 7 am every day.**
In this case, data pipeline orchestrators scuh as Apache Airflow would be used. For this project, we didn't have the real need for an orchestrator, since the company needs updated data from year to year.

**SCENARIO 3 - The database needed to be accessed by 100+ people.**
Very difficult scenario, since we would first map the needs of these users and how they would access the data. Choice of tools could also vary accordingly.