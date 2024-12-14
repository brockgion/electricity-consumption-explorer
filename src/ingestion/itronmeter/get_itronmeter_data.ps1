# PowerShell script to extract itron smart meter data from Home Assistant for a range of dates

$authToken = Get-Content -Path "AccountKeyHomeAssistant.config" -Raw
$authToken = $authToken.Trim()

$headers = @{
    "Authorization" = "Bearer $authToken"
    "Content-Type" = "application/json"
}

$sensor_id = "sensor.xcel_itron_5_instantaneous_demand_value"

$saveDirectory = "itronmeter\rawdata"

if (!(Test-Path -Path $saveDirectory)) {
    New-Item -ItemType Directory -Path $saveDirectory | Out-Null
}

# Define the start and end dates for the range
$startDate = [datetime]::Parse("2024-12-11")
$endDate = [datetime]::Parse("2024-12-11")

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

    $formattedData

    $fileName = "$saveDirectory\$dateString" + "_$sensor_id.csv"
    $formattedData | Export-Csv -Path $fileName -NoTypeInformation -Encoding UTF8

    $currentDate = $currentDate.AddDays(1)

}

python "..\ingestion\main_ingest.py" $fileName