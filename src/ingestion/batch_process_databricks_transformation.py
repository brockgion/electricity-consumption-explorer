# Databricks notebook source
# MAGIC %md
# MAGIC ## Connect to Azure Storage

# COMMAND ----------

import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pyspark.sql.functions import sum, desc, isnull, col, avg, count, when, from_json, to_timestamp, window
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

storage_account_name = "azdbrickstorage"
my_scope = "azdbrick-scope" 
my_key = "electricSecret" 

# Configure Spark to use the storage account key from your secret scope
spark.conf.set(
    f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net",
    dbutils.secrets.get(scope=my_scope, key=my_key)
)

# Define the URI for accessing the data
uri = f"abfss://electric-meter-data@{storage_account_name}.dfs.core.windows.net/"

# itron - single day
# itron_df = spark.read.csv(uri+"raw/itronmeter/2024-11-30_sensor.xcel_itron_5_instantaneous_demand_value.csv", header=True)

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

# Generate a list of dates within the range
start_date = datetime.strptime("2024-10-01", "%Y-%m-%d")
end_date = datetime.strptime("2024-11-30", "%Y-%m-%d")

date_range = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") 
              for i in range((end_date - start_date).days + 1)]

combined_itron_df = None

for date in date_range:
    file_path = f"{uri}raw/itronmeter/{date}_sensor.xcel_itron_5_instantaneous_demand_value.csv"
    try:
        daily_df = spark.read.csv(file_path, header=True)
        daily_df = daily_df.withColumn("date", col("last_changed").substr(1, 10))  # Add 'date' column
        
        if combined_itron_df is None:
            combined_itron_df = daily_df
        else:
            combined_itron_df = combined_itron_df.unionAll(daily_df)
    except Exception as e:
        print(f"File not found or error reading data for {date}: {e}")

display(combined_itron_df)
itron_df = combined_itron_df

for sensor in sensors:
    df_name = sensor.replace("_power_minute_average", "") + "_df"
    file_path = f"{uri}raw/emporiacircuits/{date}_{sensor}.csv"
    dataframes[df_name] = spark.read.csv(file_path, header=True)
    print(f"DataFrame '{df_name}' created from file: {file_path}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## itron (meter data)
# MAGIC
# MAGIC Add "date" field

# COMMAND ----------

itron_df = itron_df.withColumn("date", col("last_changed").substr(1, 10))
display(itron_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Show as line graph, aggregate to defined intervals (e.g. 1 second, 1 minute, 15min, 1 hour, etc.)

# COMMAND ----------

from pyspark.sql.functions import avg, col, to_timestamp, expr, round, lit, date_format

# Define the specific date range for display
STARTDATE = "2024-11-30"
ENDDATE = "2024-11-30"

start_date = f"{STARTDATE} 00:00:00"
end_date = f"{ENDDATE} 23:59:59"

itron_df = itron_df.withColumn("last_changed", to_timestamp("last_changed"))

itron_df = itron_df.withColumn(
    "rounded_timestamp", 
    # expr("timestamp((unix_timestamp(last_changed) DIV 1) * 1)")  # Round to the nearest second
    expr("timestamp((unix_timestamp(last_changed) DIV 60) * 60)")  # Round to the nearest minute
    # expr("timestamp((unix_timestamp(last_changed) + 450) DIV 900 * 900)")  # round to 15 minutes
    # expr("timestamp((unix_timestamp(last_changed) + 1800) DIV 3600 * 3600)")  # Round to nearest hour
)

aggregated_data = (
    itron_df.groupBy("rounded_timestamp")
            .agg(round(avg("state"), 2).alias("average_state"))
            .withColumnRenamed("rounded_timestamp", "window_start")
)

# Add derived 'date' field
aggregated_data = aggregated_data.withColumn("date", date_format(col("window_start"), "yyyy-MM-dd"))

filtered_data = aggregated_data.filter(
    (col("window_start") >= to_timestamp(lit(start_date))) &
    (col("window_start") <= to_timestamp(lit(end_date)))
)

# Display the filtered data
display(filtered_data.orderBy("window_start"))


# COMMAND ----------

# MAGIC %md
# MAGIC ### Save transformed data in Azure blob storage as "parquet" format

# COMMAND ----------

directory_path = "transformed/itronmeter"  # Define the specific directory path

output_path = f"{uri}{directory_path}/"

aggregated_data.coalesce(1).write.format("parquet").mode("overwrite").save(output_path)

# COMMAND ----------

# MAGIC %md
# MAGIC ## emporia sensors
# MAGIC
# MAGIC add "date" field

# COMMAND ----------

def aggregate_and_display(sensor_df, sensor_name):
    # Ensure the column names are correct
    if "last_changed" in sensor_df.columns and "state" in sensor_df.columns:
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
    else:
        print(f"Columns 'last_changed' or 'state' not found in DataFrame for {sensor_name}")

for sensor_name, sensor_df in dataframes.items():
    aggregate_and_display(sensor_df, sensor_name)