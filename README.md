# AZ-task
Dynatrace task repo

## Overview
Python3 CLI-application that can be used to configure, in Dynatrace, Management-Zones via the API in a configuration-as-code approach.

## Requirements:
- Python 3.9.0 Runtime
- Install Requests Package: `pip install requests`
- Install PyYAML Package: `pip install PyYAML`
- Dynatrace Tenant with `WriteConfig` and `ReadConfig` permissions assigned to your [API token](https://www.dynatrace.com/support/help/dynatrace-api/basics/dynatrace-api-authentication/)
- A file `input.yml` in the style of the provided example:
```yaml
environment_id: xhs-3452uu124
tenant_id: anu85007
teams:
    global-pcf-a:
        cost-center: ct-4291
        entity: ab-3
        host-group-prefixes:
            - global-pcf-a-Z
            - global-pcf-a-Y
    global-pcf-b:
        cost-center: ct-4291
        entity: ab-3
```
## Instruction on how to use the app:
 First of all double check if you have all the prerequisites required.  
   
 Once you got the repo locally cloned you can run the app by simply executing the `main.py` script.  
   
 There is no need for parameters as by design the app will look for the config file `input.yml` in the same directory where the script resides.  

 **Examples:**
 ```cmd
C:\Users\adria\PycharmProjects\AZ-task>py main.py

GET request status code is: 200
GET retrieved 0 existing zones.
POST request ran with response code: 201
POST request successfully created new management zone: global-pcf-a

GET request status code is: 200
GET retrieved 1 existing zones.
POST request ran with response code: 201
POST request successfully created new management zone: global-pcf-b

C:\Users\adria\PycharmProjects\AZ-task>
 ```
