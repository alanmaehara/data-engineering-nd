import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, to_date
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format, dayofweek, \
    monotonically_increasing_id
from pyspark.sql.types import StructType as S, StructField as Stfld, DoubleType as Db, StringType as Sty, IntegerType as Int, DateType, TimestampType

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    Process the song data file from S3, creates song and artist tables and load them back to S3
    
    """
    # set schema for song data
    schema_song = S([
        Stfld("artist_id",Sty()),
        Stfld("artist_latitude",Db()),
        Stfld("artist_location",Sty()),
        Stfld("artist_longitude",Db()),
        Stfld("artist_name",Sty()),
        Stfld("duration",Db()),
        Stfld("num_songs",Int()),
        Stfld("title",Sty()),
        Stfld("year",Int())
    ])
    
    # get filepath to song data file
    song_data = input_data + 'song_data/*/*/*/*.json'
    
    # read song data file
    df = spark.read.json(song_data, schema = schema_song)
    df.createOrReplaceTempView("song_data_table")

    # extract columns to create songs table
    songs_table = df.select(col("song_id"), col("title"), col("artist_id"), col("year"), col("duration")).distinct()
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy("year", "artist_id").parquet("{}songs/songs_table.parquet".format(output_data))
    
    # extract columns to create artists table
    artists_table = df.select(col("artist_id"), col("artist_name"), col("artist_location"),\
                              col("artist_latitude"), col("artist_longitude")).distinct()    
    # write artists table to parquet files
    artists_table.write.parquet(output_data + 'artists/')    
    
def process_log_data(spark, input_data, output_data):
    """
    Process the log data file from S3, creates song and artist tables and load them back to S3
    
    """
    # get filepath to log data file
    log_data = input_data + 'log_data/*/*/*.json'

    # read log data file
    df = spark.read.json(log_data) 
    
    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong')

    # extract columns for users table    
    user_table = df.select(col("userId"), col("firstName"), col("lastName"), col("gender"), col("level")).distinct()
    
    # write users table to parquet files
    user_table.write.parquet("{}users/users_table.parquet".format(output_data))
    
    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: datetime.fromtimestamp(x / 1000), TimestampType())
    df = df.withColumn("timestamp", get_timestamp(col("ts")))
    
    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: to_date(x), TimestampType())
    df = df.withColumn("start_time", get_timestamp(col("ts")))
    
    # extract columns to create time table
    df = df.withColumn("hour", hour("timestamp"))
    df = df.withColumn("day", dayofmonth("timestamp"))
    df = df.withColumn("month", month("timestamp"))
    df = df.withColumn("year", year("timestamp"))
    df = df.withColumn("week", weekofyear("timestamp"))
    df = df.withColumn("weekday", dayofweek("timestamp"))
    
    time_table = df.select(col("start_time"), col("hour"), col("day"), col("week"), \
                           col("month"), col("year"), col("weekday")).distinct()
    
    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy("year", "month").parquet("{}time/time_table.parquet".format(output_data))

    # read in song data to use for songplays table
    song_df = spark.sql("SELECT DISTINCT song_id, artist_id, artist_name FROM song_data_table")

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = df.join(song_df, song_df.artist_name == df.artist, "inner") \
        .distinct() \
        .select(col("start_time"), col("userId"), col("level"), col("sessionId"), \
                col("location"), col("userAgent"), col("song_id"), col("artist_id")) \
        .withColumn("songplay_id", monotonically_increasing_id())

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy("year", "month").parquet(output_data + 'songplays/')
    
def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://sparkify-dend/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
