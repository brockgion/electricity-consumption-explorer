## Overview
This readme contains raw notes collected as going through the process to integrate Home Assistant with Azure Events Hub. Essentially, you need to do these two things:
- Create Azure Events Hub
- Setup Shared Access Signature

## Key details for Powershell Script to created Shared Access Key
- EventHub namespace: cloud-ingest
- EventHub name: cloud-ingest-eventhub
- $Access_Policy_Name="RootManageSharedAccessKey"
- $Access_Policy_Key="Tx...."

## Steps involved for process to integrate Home Assistant with Azure Events Hubs:

### TUTORIAL #1 ~15 MINUTES
==Create Azure Events Hub
Follow instructions here: 
- Quickstart: Create an event hub using Azure portal https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-create

High level, doing three primary things: creating a resource group, an Event Hubs namespace, and an event hub

- create resource group in Azure Portal (named it "cloud-ingest")
- create an event hubs namespace (named it "cloud-ingest")
- pricing tier, choose basic (~$11/mo) *only select minimum 1 Throughput Unit
- create event hub, within the namespace you just deployed (named it "cloud-ingest-eventhub")
- leave defaults (partition count 1 and retention 1 hour) 

### TUTORIAL #2 ~10 MINUTES
==Setup Shared Access Signature (SAS) to Event Hubs resources
Follow instructions here:
- Authenticate access to Event Hubs resources using shared access signatures (SAS) https://learn.microsoft.com/en-us/azure/event-hubs/authenticate-shared-access-signature

High level, you are creating a Shared Access Policy for the Event Hub with ‘Send’ claims (this can be done with RootManageAccessKey from your namespace, although this key has additional claims which probably aren't needed)

- Generate a Shared Access Signature token
- You generate an access token for Event Hubs using a shared actions policy
- Generating a signature(token) from a policy
- Using provided PowerShell Script (open in cloud shell)
- If needed, verify cloudshell enabled and registered to your Azure subscription (https://learn.microsoft.com/en-us/azure/cloud-shell/get-started/classic?tabs=azurecli)

```
[Reflection.Assembly]::LoadWithPartialName("System.Web")| out-null
$URI="cloud-ingest.servicebus.windows.net/cloud-ingest-eventhub/"
$Access_Policy_Name="RootManageSharedAccessKey"
$Access_Policy_Key="TMa....."
# Token expires now+300
$Expires=([DateTimeOffset]::Now.ToUnixTimeSeconds())+300
$SignatureString=[System.Web.HttpUtility]::UrlEncode($URI)+ "`n" + [string]$Expires
$HMAC = New-Object System.Security.Cryptography.HMACSHA256
$HMAC.key = [Text.Encoding]::ASCII.GetBytes($Access_Policy_Key)
$Signature = $HMAC.ComputeHash([Text.Encoding]::ASCII.GetBytes($SignatureString))
$Signature = [Convert]::ToBase64String($Signature)
$SASToken = "SharedAccessSignature sr=" + [System.Web.HttpUtility]::UrlEncode($URI) + "&sig=" + [System.Web.HttpUtility]::UrlEncode($Signature) + "&se=" + $Expires + "&skn=" + $Access_Policy_Name
$SASToken
```

- If successful, the output of this script will generate a SAS token (a long string), that's all you need to do
- Now you're ready to connect Home Assistant to Azure Event Hub using an "integration", see next tutorial #3

### TUTORIAL #3 ~20 MINUTES
==First time setup Home ASsistant to Azure Events Hub
https://www.home-assistant.io/integrations/azure_event_hub/?ref=kallemarjokorpi.fi

- setup Azure details (done in the 2 previous tutorials above, expect it to take ~30 minutes)
- need to "add the integration" to home assitant
- after enabling, follow the prompts and fill out the following details (specific to your Azure workspace)
- Final prompt requires eventhub name, namespace, and access policy key
  - Event Hub Namespace: in my case, "cloud-ingest-eventhub"
  - Event Hub SAS Policy I used "RootManageSharedAccessKey" (once this integration is working I can secure this better by creating a non-root custom policy just for "send" claims only)
  - Event Hub SAS Key: "Txr41...." (you can find this string in the Azure portal under Event Hub > Shared access policies > click on the policy, and view Primary Key)
- If everything entered correctly, SUCCESS! Integration is enabled
- Note: Event Hubs have a retention time of at most 7 days, if you do not capture or use the events they are deleted automatically from the Event Hub, the default retention is 1 day.
- By default, no entities are excluded, so make sure to configure this right away
- In Home Assitant, need to adjust configuration.yaml file (instructions: https://www.home-assistant.io/docs/configuration/)
- To begin, only interested in ONE entity (my electrical meter) being exposed to Azure Events Hub
- Entity name: sensor.xcel_itron_5_instantaneous_demand_value

```
azure_event_hub:
  filter:
    include_entities:
      - sensor.xcel_itron_5_instantaneous_demand_value
```

FINAL STEPS
==Verifying Home Assistant > Settings > Azure Event Hub
- Make sure the devices/entities you expect to appear show here, if not add them
- Choose inernval between sending batches to the hub (default 5 seconds)

POTENTIAL HTTP ISSUE:
- If Home Assistant is running on HTTP, it could lead to certificate issues when connecting to secure Azure services, which require SSL/TLS. This mismatch might trigger the warnings during the Azure Event Hub connection.

TROUBLESHOOTING STEPS:
- Right after enabling the integration, check Home Assistant logs for any warnings. One indiciation of this problem is Home Assistant might "lock up" and become unavailable. In my case, the logs traced back to a https:// protocol

POTENTIAL SOLUTIONS for HTTPS: 
- Use "nginx Proxy Manager" add-on: https://github.com/hassio-addons/addon-nginx-proxy-manager
- Register a free domainname on duckdns.org (configured setup as https://hcoreassist.duckdns.org/)
- Otherwise, could setup "Let's Encrypt" add-on to automatically configure HTTPS (requires update to configuration.yaml file)
- Using "nabu casa" service (paid solution $6.50/mo, testing). Allows cloud access to Home Assistant, auto configure SSL (https://www.nabucasa.com/)

## Home Assistant Notes, Updates

12/13/24 - Home Assistant Core Update 
- Update HA Core from 2024.9.3 to 2024.12.2 (~10 minutes)
- Updated HA Operating System from 13.1 to 14.0 (~20 minutes)

SECURING HOME ASSISTANT:
- Once SSL is setup, access Home Assistant using https://
- In Home Assistant, modify configuration.yaml file to enforce ip limit and login attempts

```
http:
  ip_ban_enabled: true
  login_attempts_threshold: 5
```

## Reference
Misc links related to topic of home assistant and Azure:
- https://www.sgdigital.ee/post/sending-home-assistant-history-to-azure