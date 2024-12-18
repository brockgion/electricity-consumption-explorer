[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=17053334&assignment_repo_type=AssignmentRepo)
# CSCI 622 Project Overview - Brock

Hi! This project is called Electricity Consumption Explorer. The primary goal is to automatically ingest electricity meter data from my home, store it in Azure, process it using Databricks, and view the data analytics in PowerBI.

## Getting Started

- **Project Overview**:  
   - See [Project Brief](/SupplementaryInfo/ProjectFiles/Project%20Brief%20-%20Electricity%20Consumption%20Explorer%20-%20Brock%20Gion.pdf)
 for a simple, high-level document summarizing the project's goals, scope, and outcomes
    - See the [Project Presentation Slides](/SupplementaryInfo/ProjectFiles/FINAL-Project-Recap-CSCI-622-Electricity-Consumption-Explorer.pdf) that accompany the video for more detail

- **Project Demo Video**: 
The video below provides start-to-finish demo of how the system works (~9min video):
   
   <div>
   <a href="https://www.loom.com/share/ce671f234c8c4b1cafdf4efe7af01f7f">
   <img width="400" src="https://cdn.loom.com/sessions/thumbnails/ce671f234c8c4b1cafdf4efe7af01f7f-5042ff3909fbef90-full.jpg" target="_blank">
   </a>
   <p><a href="https://www.loom.com/share/ce671f234c8c4b1cafdf4efe7af01f7f" target="_blank"></a></p>
   </div>

## Data Engineering Lifecycle Used in Project

[![Drawio Detailed Ingestion Diagram](/SupplementaryInfo/screenshots/data-ingestion-process-local-and-cloud-process.png)](https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=data%20engineering%20lifecyle%20using%20in%20electricity%20consumption%20explorer.drawio#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1MaSfomZiAuxWsUCWuZGi7WtgyCweIivb%26export%3Ddownload)

<p><a href="https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=data%20engineering%20lifecyle%20using%20in%20electricity%20consumption%20explorer.drawio#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1MaSfomZiAuxWsUCWuZGi7WtgyCweIivb%26export%3Ddownload" target="_blank"><strong>SEE FULL-SIZE DIAGRAM: Data Engineering Lifecycle - Electricity Consumption Explorer</strong></a></p>



This diagram highlights the full lifecycle of data, showcasing how it is generated, ingested, transformed, and served. Power BI is the final step used for visualization, analysis, and exploration of the data.

# Project Motivation and Results

1. **Understand my electricity consumption patterns at home**
    - On average, over the last 4 years my monthly electric usage is ~745kwh/month
    - My monthly usage was the only metric I knew going into this project (by looking at my utility bill's since 2020)

2. **Reduce carbon footprint** 
    - Looking to become more efficient with my energy usage:
      - Key Question: Can I reduce my electricy consumption? If so, by how much? Possible to average ~600kwh/month? 
    - Interested in renewable energy sources (solar pv/battery)
      - Potential for data to help inform and accurately size a [solar pv rooftop system](https://en.wikipedia.org/wiki/Rooftop_solar_power)
 
----
**Key Project Takeaways**:
- Automated energy monitoring **reduced electricity usage by 7% over 3 months**
- Cloud-based ingestion via Azure Event Hub enables near real-time processing
- Results are visualized in Power BI for appliance-level insights and peak load patterns

**Next steps / Future Improvements**:
- Implement NILM (Non-Intrusive Load Monitoring) within the next phase to disaggregate appliance-level energy usage
- Refine visuals in Power BI to splice data into useful views (i.e. weekday vs. weekend patterns)
- Continue to integrate emporia sensor data (and other datasets) to understand relationships among different factors (i.e. weather affecting energy usage)
----

Reduced 3-month avg. from ~761kwh/mo to ~708kwh/mo (~7% reduction). Now I can begin to use more data to further refine and understand usage patterns of appliances.

![Reduce Electricity Usage](/SupplementaryInfo/screenshots/reduce-electricity-usage-comparing-3-month-avg.png)

Now able to view appliance level electricity usage, and know each appliance % of electrical consumption:

![Monitoring Appliance Electricity Usage](/SupplementaryInfo/screenshots/monitoring-appliance-electricity-usage.png)

Now able to use PowerBI to visualize and see metrics such as max peak load for any given day:

![Peakload PowerBI Dashboard](/SupplementaryInfo/screenshots/peakload-powerbi-dashboard.png)

## Project Steps

- Automated ingestion of Itronmeter and Emporia energy monitor data
- Data transformation for aggregation and time-based analytics
- Parquet-based storage for efficient querying and visualization
- Integration with tools like Power BI, Home Assistant, and Emporia's native app

## Methodology

Throughout the class we followed "The Fundamentals of Data Engineering Lifecycle" approach:

Main phases for this project:
1. Generation
2. Ingestion
3. Transformation / Serving / Storage
4. Analytics

![Monitoring Appliance Electricity Usage](/SupplementaryInfo/screenshots/data-engineer-lifecylcle-simplified-4-steps.png)

Source: https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/

## STEP 1: Data Generation
Data is generated in real-time using two primary sources: the Itron Electric Meter and the Emporia Home Energy Monitoring System. These devices provide granular energy usage data that forms the foundation of the entire data pipeline.

###  2 data sources
- *Itron Electric Meter* (installed on premise, at house)  
- *Emporia Home Circuit Monitoring System* (installed at breakerbox, at house)

###  All data from *itron* meter + *emporia* circuits integrated into Home Assistant
- Home Assistant requires 1 integration and 3-addons: 
  - Integration: [Azure Event Hub](https://www.home-assistant.io/integrations/azure_event_hub/?ref=kallemarjokorpi.fi)
  - [Xcel iTron MQTT](https://github.com/wingrunr21/hassio-xcel-itron-mqtt)  
  - [Mosquitto broker](https://github.com/home-assistant/addons/tree/master/mosquitto)  
  - [Advanced SSH & Web Terminal](https://github.com/hassio-addons/addon-ssh)


## STEP 2: Data Ingestion
The ingestion phase focuses on capturing and storing the raw data. Data is collected using Home Assistant, either through manual exports or automated workflows using Azure Event Hub and Azure Functions to ensure continuous and reliable data flow into Azure Storage.

![Drawio Detailed Ingestion Diagram](/SupplementaryInfo/screenshots/data-ingestion-generation-closeup.png)

2 Datasources used for ingestion:
- Itron Electric meter (installed on premise, at house)
- Emporia home circuit monitoring (installed in breakerbox, at house)

### Datasource descriptions:
- [Itron meter](https://na.itron.com/o/commerce-media/accounts/-1/attachments/3804170)
  - physical meter connected to the house
  - Polling rate 15 seconds (default). 1 second polling available
- [Emporia Home Energy Monitoring System](https://www.amazon.com/Smart-Home-Energy-Monitor-Vue/dp/B0C79PNK84) 
  - monitors 16-circuits total
  - Polling rate 1 minute

| 16circuits | Emporia Device Name | Home Assistant Name                     |
|------------|----------------------|-----------------------------------------|
| CT-1       | AC                   | sensor.ac_power_minute_average          |
| CT-2       | OFFICE               | sensor.office_power_minute_average      |
| CT-3       | DRYER                | sensor.dryer_power_minute_average       |
| CT-4       | DRYER                | sensor.dryer_power_minute_average_2     |
| CT-5       | WATER HEATER         | sensor.water_heater_power_minute_average|
| CT-6       | WATWR HEATER         | sensor.watwr_heater_power_minute_average|
| CT-7       | GARAGE FREEZER       | sensor.garage_freezer_power_minute_average |
| CT-8       | PELOTON ROOM         | sensor.peloton_power_minute_average     |
| CT-9       | WASHER               | sensor.washer_power_minute_average      |
| CT-10      | BOILER               | sensor.boiler_power_minute_average      |
| CT-11      | FRIDGE BASEMENT      | sensor.fridge_basement_power_minute_average |
| CT-12      | FRIDGE KITCHEN       | sensor.fridge_kitchen_power_minute_average |
| CT-13      | MICROWAVE            | sensor.microwave_power_minute_average   |
| CT-14      | DISHWASHER           | sensor.dishwasher_power_minute_average  |
| CT-15      | RANGE                | sensor.range_power_minute_average       |
| CT-16      | RANGE                | sensor.range_power_minute_average_2     |

### "Local" Data Ingestion Process

![Drawio Diagram Ingestion Overview](/SupplementaryInfo/screenshots/ingestion-overview.drawio.png)

All data is stored initially in Home Assistant, then uploaded to Azure Storage.

More specifically, all data captured in Home Assistant is initially raw values, but Home Assistant isn't persisent memory (i.e. it only stores meter data for the last 10 days). To achieve long-term storage of the meter data, it's crucial that all itron meter data is exported from Home Assistant and uploaded into Azure storage. 

### "Cloud" Data Ingestion

The project began with a local approach to process and batch-save meter data to Azure Data Lake Storage (ADLS Gen2). While reliable and easy to maintain, it required manual effort to run scripts weekly.

The cloud approach, using Azure Event Hubs and an Azure Function, automates this workflow. It eliminates manual intervention, providing a live stream of data into Azure Data Lake. This enables near real-time analysis in Power BI with a single-click refresh.

1. Data Generation: Electrical meter generates values 
2. Ingestion: Home Assistant captures data (~every 5 seconds)  
3. Event Hub: Home Assistant sends updates to Azure Event Hubs 
4. Azure Function: Triggers on Event Hub updates and saves raw data to:  
   `electric-meter-data / raw / itronmeter / parquet`  
5. Transformation: Use Azure Databricks to transform raw parquet data into Power BI-ready format  
6. Storage: Save transformed data to:  
   `electric-meter-data / transformed / itronmeter / cloud_ingest_itron_meter_data_1minute_interval.parquet`  
7. Visualization: Load transformed data into Power BI for analytics and reporting

### Comparison "Local" vs. "Cloud" Ingestion

| Aspect                    | Local Ingestion                          | Cloud Ingestion                            |
|---------------------------|------------------------------------------|-------------------------------------------|
| Effort                    | Manual script execution weekly          | Fully automated, no manual effort needed  |
| Ease of Troubleshooting   | Simple and straightforward             | Requires cloud configuration and monitoring |
| Data Availability         | Batch processed weekly                  | Near real-time data streaming             |
| Cost                      | Free                                    | ~$10/month for Azure Event Hubs           |

### Ingestion Preference: Cloud

At ~$10/mo and nearly fully automated, using the cloud approach offers a scalable and efficient option. As long as the system as a whole remains reliable, the goal is to use a cloud-first approach to data ingestion, while complimenting it with manual local when needed.

### Home Assistant Dashboard

All data is integrated with [Home Assistant](https://www.home-assistant.io/) and displayed in a dashboard view. Home Assistant was chosen because it integrates nicely with both the itron electric meter (1 device) and Emporia Energy load monitoring app (16 devices total). 

![Home Assistant Dashboard](/SupplementaryInfo/screenshots/home-assistant-custom-dashboard-electricity-consumption-explorer.png)

*Note: All steps explaind below require a basic understanding of Home Assistant. In short, there's a few key concepts important to know. In Home Assistant (HA) any "device" that is being displayed on the dashboard has underlying data that can be viewed. 

For a quick overview of Home Assistant (HA), skim this wiki summary:
> Home Assistant is free and open-source software used for home automation. It serves as an integration platform and smart home hub, allowing users to control smart home devices. Information from all devices and their attributes (entities) that the application sees can be used and controlled via automation or script
(source: https://en.wikipedia.org/wiki/Home_Assistant). 

### Understanding Devices and Entities in Home Assistant
To work effectively with Home Assistant (HA), it's important to understand the distinction between "devices" and "entities."

- *Device*: Represents the actual physical or sensor integrated into Home Assistant. For example, the itron meter and any emporia sensor is a "device."

- *Entity*: Represents specific attributes or functions of a device. Entities are what Home Assistant uses to interact with and control devices.

To access data in Home Assistant via the API, you need to know the device name (for identification) and the relevant entity name (to access specific data).

For example, to get power usage data from the itron meter the API call looks like:
- sensor.xcel_itron_5_instantaneous_demand_value

Likewise, to get data from emporia sensors, you follow the same pattern:
- sensor.fridge_basement_power_minute_average
- sensor.boiler_power_minute_average
- sensor.dishwasher_power_minute_average

### Additional Home Assistant Notes

* Home Assistant runs on a local Lenovo 540ti ThinkPad, always on and plugged in.  
* Any disruption to Home Assistant would interrupt the data flow. However, using Azure Event Hubs, such outages can be monitored and detected automatically.

### Methods to access raw data in Home Assistant: 
#### Method 1: Web UI Interface (Manual process)
- This functionalty is built into Home Assistant (HA) dashboards and is a native feature

Home Assistant can be accessed through a web browser as long as connected to the home network (can also be configured to be accessed remotely). Once HA is open in the web browser, find and click on device/entity, then choose the option to download/export the data. This is a straightforward approach, however, becomes cumbersome as the number of devices (and frequency of data exports) increases. 

#### Method 2: Windows Powershell Script (Manual, but less effort and can possibly be automated) 
The initial goal of this data ingestion process is to alleviate the need to export data through the HA interface and instead use a powershell script. Then once the data is retrieved it can be uploaded to Azure storage.

Two scripts are used to ingest data:
- get_itronmeter_data.ps1
- get_emporiacircuits_data.ps1

#### **Method 3: Home Assistant + Azure Event Hub Stream (Automated Cloud Workflow)**  
This method automates data ingestion by streaming raw data from Home Assistant to the cloud. Home Assistant captures real-time data from devices (e.g., Itron meter and Emporia circuits) **every 5 seconds and sends it directly to Azure Event Hub using its integration**. Event Hub acts as a pipeline, receiving the data and queuing it for processing.  

An Azure Function listens to Event Hub events, processes the incoming data (extracting fields like `sensor name`, `value`, and `timestamp`), and saves it into Azure Data Lake Storage (Gen2) in Parquet format. This enables efficient storage, querying, and long-term retention. For example, the cloud-ingested data is stored at:  


## STEP 3: Transformation
In this step, raw data is transformed into structured and optimized formats suitable for analysis. Using Azure Databricks, data is cleaned, aggregated (e.g., 1-minute intervals), and stored in Parquet format for efficient querying and downstream processing.

![Drawio Detailed Ingestion Diagram](/SupplementaryInfo/screenshots/data-transformation-serving-analytics-closeup.png)

The transformation phase processes raw electricity consumption data into structured formats optimized for analytics. Key steps include:

1. **Date Extraction**: 
   - Extracted the date (`YYYY-MM-DD`) from the `last_changed` timestamp to enable time-based aggregations and filtering

2. **Data Aggregation**:
   - **Itronmeter data**: Aggregated instantaneous demand values into one-minute intervals to reduce granularity while retaining detail
   - **Emporia sensors**: Consolidated data from 16 circuits into daily summaries for appliance-level and whole-home energy insights

3. **Format Conversion**: 
   - Transformed datasets are written to **Parquet format** to optimize storage and query performance. Parquet enables efficient integration with downstream tools like Power BI.

4. **Quality Validation**: 
   - Validated data during transformation to identify anomalies such as missing timestamps or outliers
   - No automated method (yet) to detect power outages
   - Manually annotating these event, expecting it doesn't occur often (i.e. ~2 known outages in last 2 months).
     - October 4th: 5:15am thru October 6th: 9:12am
       - Reason: Home Assistant server down. Wasn't monitoring, after a modem reboot it reassigned correct IP address.
     - November 7th: 11pm thru November 8th: 6:40pm 
       - Reason: Home Assistant update failed, needed to reinstall configuration settings.

Example of using PowerBI for visual inspection to notice outages:
![Outage Detection Visually Identifying Gaps in Data](/SupplementaryInfo/screenshots/outage-detection-gaps-in-data.png)

## STEP 4: Serving and Analytics
The transformed data is served through tools like Power BI to enable visualization and analysis. This step provides actionable insights, such as identifying peak loads and appliance-level usage trends, to help optimize energy consumption.

See ProjectFiles folder for [PowerBI dashboard file](/SupplementaryInfo/ProjectFiles/). The file has data loaded in and you can use it (as long as you have access to Power BI Desktop). It relies on a "testonly" Azure container setup for sample data only.

The serving layer utilizes multiple tools to support data insights (Home Assistant, Emporia App, PowerBI). PowerBI provided the best control and most interesting visuals. Example, added a "peak load" dimension and line graph to see pinpoint what time of day was the highest electrical load.

1. **Home Assistant**:
   - Integrated dashboards display near real-time data on energy consumption at the circuit and appliance levels
   - Features customizable visualizations for appliance-level trends (boiler, fridge, dishwasher, etc)

2. **Emporia Mobile App**:
   - Provides detailed energy consumption breakdowns
   - Great app to have on phone and can view anytime (not necessary to be connected to wifi home network)

3. **Power BI**:
   - Useful features:
     - Dynamic dashboard displaying usage day-by-day usage, and ability to see peak demand period during the day
     - Data is accessed via a coalesced Parquet file stored in Azure Blob Storage, ensuring seamless refreshes and efficient processing
     - Ability to add in calculated dimensions in PowerBI for enhanced analysis:
       - Max_Peak_Load
       - Time of Peak Load 
       - ![Time of Peak Load](/SupplementaryInfo/screenshots/time-of-peak-load.png)
      

4. **Machine Learning Readiness**:
   - The transformed data is structured to support future applications like **Non-Intrusive Load Monitoring (NILM)*
   - Idea is to enable appliance-level energy disaggregation without additional hardware sensors

5. **Scalability**:
   - The serving architecture supports scalability for incorporating additional sensors or higher-frequency data while maintaining performance
   - No orchestration scripts were automated yet
   - Using the powershell scipts - although manual, it allows for updating the data for daily and/or weekly batches


## Technologies Used
Emporia Home Energy Monitor
- https://www.emporiaenergy.com/energy-monitors/

Home Assistant
- https://www.home-assistant.io/
  - Core HA with 3 Add-ons Installed: 
    1. [Xcel iTron MQTT](https://github.com/wingrunr21/hassio-xcel-itron-mqtt)
    2. [Mosquitto broker](https://github.com/home-assistant/addons/tree/master/mosquitto)
    3. [Advanced SSH & Web Terminal (optional)](https://github.com/hassio-addons/addon-ssh)
   - 1 Integration Installed
     - [Azure Event Hub](https://www.home-assistant.io/integrations/azure_event_hub/?ref=kallemarjokorpi.fi)
   

Microsoft Services
- Azure Data Lake Storage Gen2 for data storage
- Azure Key Vault for secure access key management
- Azure Databricks + Pyspark for data processing and transformation
- Powershell Scripts
- PowerBI for analytics + dashboard
- Azure Events Hub
- Azure Function + Function App
