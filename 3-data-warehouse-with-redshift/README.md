# Building ETL pipeline for Sparkify with Amazon S3 & Redshift
---

In this project, data modeling and ETL pipeline were built for the same company (Sparkify). This time, Amazon S3 was used for data storage, and Amazon Redshift as the company's data warehouse. Python was used to build the data modeling and pipelines.

---
## 1. Context

The company has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## 2. Goals and Deliverables

The main goal is to build an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. 