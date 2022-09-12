from io import BytesIO
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import window
from pyspark.sql.types import *
from reasoning_functions import *


if __name__ == "__main__":
    path = "/home/kautuk/Desktop/Reasoning-work/streaming_reasoning/" # this is the path on the local system
    # path = "/tmp/pycharm_project_459/streaming_reasoning/" # this is the path on the server
    datafiles_path = path + "10_instances/" # change this to the folder we want to perform reasoning on

    # tbox = get_ontology(path + "tbox.owl").load()

    spark = SparkSession \
        .builder \
        .appName("My Application") \
        .config("spark.some.config.option", "some-value") \
        .config("spark.executor.cores", "12") \
        .getOrCreate()
        # set the number of cores here

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
        .trigger(processingTime='0.5 second') \
        .option("truncate", "true") \
        .start()
    #      .option("numRows", 200) \
    #    .trigger(processingTime='1 second') \ this can be altered
    # outputMode can be changed as per our requirements

    print("Type of stream_df = ", type(stream_df))
    print("Type of stream_df_query = ", type(stream_df_query))


    def process_row(x):
        byteArray = x[2]
        # print("Type of byteArray = ", type(byteArray))
        onto_string = byteArray.decode()
        # print("Type of onto_string = ", type(onto_string))
        # print("onto_string = ", onto_string)
        onto_fileobj = BytesIO(str.encode(onto_string))
        # print("Type of onto_fileobj = ", type(onto_fileobj))
        owl_file = x[1][x[1].rindex('/') + 1:]
        # print("owl_file name = ", owl_file)

        initiate_reasoning(owl_file, onto_fileobj)


    forEach_df = stream_df \
        .writeStream \
        .trigger(processingTime='1 second') \
        .foreach(process_row) \
        .start()
    # outputMode can be changed per our requirement

    forEach_df.awaitTermination()

