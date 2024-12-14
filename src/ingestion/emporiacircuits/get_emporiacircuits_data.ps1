# PowerShell script to extract data from multiple sensors in Home Assistant for a range of dates

$authToken = Get-Content -Path "AccountKeyHomeAssistant.config" -Raw
$authToken = $authToken.Trim()

$headers = @{
    "Authorization" = "Bearer $authToken"
    "Content-Type" = "application/json"
}

# List of all 16 sensors to fetch data from
$sensors = @(
    "sensor.ac_power_minute_average",
    "sensor.boiler_power_minute_average",
    "sensor.dishwasher_power_minute_average",
    "sensor.dryer_power_minute_average",
    "sensor.dryer_power_minute_average_2",
    "sensor.fridge_basement_power_minute_average",
    "sensor.fridge_kitchen_power_minute_average",
    "sensor.garage_freezer_power_minute_average",
    "sensor.microwave_power_minute_average",
    "sensor.office_power_minute_average",
    "sensor.peloton_power_minute_average",
    "sensor.range_power_minute_average",
    "sensor.range_power_minute_average_2",
    "sensor.washer_power_minute_average",
    "sensor.water_heater_power_minute_average",
    "sensor.watwr_heater_power_minute_average"
)

$saveDirectory = "emporiacircuits\rawdata"

if (!(Test-Path -Path $saveDirectory)) {
    New-Item -ItemType Directory -Path $saveDirectory | Out-Null
}

# Define the start and end dates for the range
$startDate = [datetime]::Parse("2024-12-01")
$endDate = [datetime]::Parse("2024-12-12")

foreach ($sensor_id in $sensors) {

    $currentDate = $startDate
    while ($currentDate -le $endDate) {

        $dateString = $currentDate.ToString("yyyy-MM-dd")
        $start_date = "$dateString`T00:00:00Z"

        $url = "http://homeassistant.local:8123/api/history/period/$($start_date)?filter_entity_id=$sensor_id"

        $response = Invoke-WebRequest -Uri $url -Method GET -Headers $headers

        $data = $response.Content | ConvertFrom-Json

        $formattedData = $data | ForEach-Object {
            $_ | ForEach-Object {
                [PSCustomObject]@{
                    entity_id    = $_.entity_id
                    state        = $_.state
                    last_changed = $_.last_changed
                }
            }
        }

        $fileName = "$saveDirectory\$dateString" + "_$($sensor_id -replace 'sensor.', '').csv"
        $formattedData | Export-Csv -Path $fileName -NoTypeInformation -Encoding UTF8

        if (Test-Path -Path $fileName) {
            Write-Output "File saved successfully: $fileName"

            python "..\ingestion\main_ingest.py" $fileName
            if ($LASTEXITCODE -ne 0) {
                Write-Output "Error: File $fileName was not saved correctly."
            }
        } else {
            Write-Output "Error: File $fileName does not exist after saving."
        }

        $currentDate = $currentDate.AddDays(1)
    }
}