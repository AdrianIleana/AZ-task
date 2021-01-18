# AZ-task
Dynatrace task repo

## Overview
This is a Python3 CLI-application that can be used to configure, in Dynatrace, Management-Zones via the API in a configuration-as-code approach.

## Requirements:
- Python 3.9.0 Runtime
- Install Requests Package: `pip install requests`
- Install PyYAML Package: `pip install PyYAML`
- Dynatrace Tenant with `WriteConfig` and `ReadConfig` permissions assigned to your [API token](https://www.dynatrace.com/support/help/dynatrace-api/basics/dynatrace-api-authentication/)
- API Token needs to be Base64 encoded and placed in the text file: `encoded_token.txt` (UTF-8 character set)
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
 1. First of all double check if you have all the prerequisites required.  
   
 2. Clone the repo locally
 
 3. Provide your own token and configuration input by updating the files accordingly (`input.yml` and `encoded_token.txt`).
 
 4. Execute the app by simply running the `main.py` script from the Command-Line:  
    ```
    C:\Users\adria\PycharmProjects\AZ-task>py main.py
    
    ``` 
    Be aware that **each execution** will iterate through the `teams` specified in the YAML file and:
     - if team does not exists already : 
       - **create a new management zone** with the team's title
     - if team exists :
       - **update it with the current configuration** (any previous rule will be removed).
 
  *NOTE: There is no need for parameters as by design the app will look for the config file `input.yml` and the token `encoded_token.txt` in the same directory where the script resides.*
 
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
