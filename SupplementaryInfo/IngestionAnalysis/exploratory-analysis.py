# Databricks notebook source
# MAGIC %md
# MAGIC ## Connect to Azure Storage

# COMMAND ----------

# Add imports, read in data to analyze
import json
import matplotlib.pyplot as plt
from pyspark.sql.functions import sum, desc, isnull, col, avg, count, when, from_json, to_timestamp, window
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

storage_account_name = "azdbrickstorage"  # Your storage account name
my_scope = "azdbrick-scope"  # The secret scope you created
my_key = "electricSecret"  # The secret key name in your vault

# Configure Spark to use the storage account key from your secret scope
spark.conf.set(
    f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net",
    dbutils.secrets.get(scope=my_scope, key=my_key)
)

# Define the URI for accessing the data
uri = f"abfss://electric-meter-data@{storage_account_name}.dfs.core.windows.net/"

# itron
itron_df = spark.read.csv(uri+"raw-input/xcel_itron_5_instantaneous_demand_value-2024-11-13.csv", header=True)

# emporia sensors
sensors = [
    "ac_power_minute_average",
    "office_power_minute_average",
    "dryer_power_minute_average",
    "dryer_power_minute_average_2",
    "water_heater_power_minute_average",
    "watwr_heater_power_minute_average",
    "garage_freezer_power_minute_average",
    "peloton_power_minute_average",
    "washer_power_minute_average",
    "boiler_power_minute_average",
    "fridge_basement_power_minute_average",
    "fridge_kitchen_power_minute_average",
    "microwave_power_minute_average",
    "dishwasher_power_minute_average",
    "range_power_minute_average",
    "range_power_minute_average_2"
]

dataframes = {}

date = "2024-11-13"

for sensor in sensors:
    df_name = sensor.replace("_power_minute_average", "") + "_df"
    file_path = f"{uri}raw-input/{sensor}-{date}.csv"
    dataframes[df_name] = spark.read.csv(file_path, header=True)
    print(f"DataFrame '{df_name}' created from file: {file_path}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## exploratory - itron (meter data)

# COMMAND ----------

display(itron_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Show as line graph, aggregate to 1 hour intervals

# COMMAND ----------

df = itron_df   
df = df.withColumn("last_changed", to_timestamp("last_changed"))

data_to_plot = df.select("last_changed", "state")

# Aggregate data to 1 minute intervals and extract the start of each window
aggregated_data = (
    data_to_plot
    .groupBy(window("last_changed", "1 minute"))
    .agg(avg("state").alias("average_state"))
    .withColumn("window_start", col("window.start"))
    .select("window_start", "average_state")
)

display(aggregated_data)

# COMMAND ----------

# MAGIC %md
# MAGIC ## exploratory - emporia sensors

# COMMAND ----------

def aggregate_and_display(sensor_df, sensor_name):
    sensor_df = sensor_df.withColumn("last_changed", to_timestamp("last_changed"))

    data_to_plot = sensor_df.select("last_changed", "state")

    aggregated_data = (
        data_to_plot
        .groupBy(window("last_changed", "1 minute"))
        .agg(avg("state").alias("average_state"))
        .withColumn("window_start", col("window.start"))
        .select("window_start", "average_state")
    )

    print(f"Displaying data for {sensor_name}")
    display(aggregated_data)

for sensor_name, sensor_df in dataframes.items():
    aggregate_and_display(sensor_df, sensor_name)