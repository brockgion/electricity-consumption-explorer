# Initial databricks code for exploratory analysis

# visualizing different intervals for meter data, decided on 1 minute best balance for graphing

from pyspark.sql.functions import avg, col, to_timestamp, date_trunc, expr, round

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

display(aggregated_data.orderBy("window_start"))