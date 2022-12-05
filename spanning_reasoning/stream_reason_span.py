from io import BytesIO
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import window
from pyspark.sql.types import *

if __name__ == "__main__":
    print("Hello!!")
    # path = "/home/kautuk/Desktop/Reasoning-work/streaming_reasoning/"
    path = "/home/kautuk/Desktop/Reasoning-work/spanning_reasoning/"
    num_instances = 10  # hard-coded for now
    # datafiles_path = path + "datafiles/" + str(num_instances) + "_instances/"
    datafiles_path = "/home/kautuk/Desktop/Reasoning-work/spanning_reasoning/datafiles/10_instances/"

    spark = SparkSession \
        .builder \
        .appName("My Application") \
        .config("spark.some.config.option", "some-value") \
        .config("spark.executor.cores", "24") \
        .getOrCreate()

    # https://stackoverflow.com/questions/45798332/spark-streaming-whole-text-files
    # https://spark.apache.org/docs/3.0.0-preview/sql-data-sources-binaryFile.html
    schema = StructType([
        StructField("path", StringType(), False),
        StructField("modificationTime", TimestampType(), False),
        StructField("length", LongType(), False),
        StructField("content", BinaryType(), True)
    ])

    stream_df = spark \
        .readStream \
        .format("binaryFile") \
        .option("pathGlobFilter", "*.owl") \
        .schema(schema) \
        .load(path=datafiles_path)

    stream_df = stream_df.drop("modificationTime", "length")
    stream_df = stream_df.withColumn('proc_ts', F.current_timestamp())
    stream_df = stream_df.select("proc_ts", "path", "content")

    stream_df.printSchema()

    stream_df_query = stream_df \
        .writeStream \
        .format("console") \
        .option("truncate", "true") \
        .start()
    #      .option("numRows", 200) \
    #    .trigger(processingTime='1 second') \
    # outputMode can be changed as per our requirements

    print("Type of stream_df = ", type(stream_df))
    print("Type of stream_df_query = ", type(stream_df_query))
