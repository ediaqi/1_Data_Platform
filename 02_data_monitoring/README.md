# 1. Introduction
This application gives you an overview of all data available in the FROST server. With a logged-in account you can check for duplicates in your project.

```
|__data_input
|______datastreamID_name_all.csv
|__images
|__constants.py
|__docker-compose.yml
|__Dockerfile
|__frost_funcs.py
|__main.py
|__README.md
|__request_DB.py
|__requirements.txt
|__styling.py
|__utils.py
```

# 2. Installation steps
## 2.1. Preparation
- Extract Datastream ID and names from the database
    - Refer the format in `data_input/datastreamID_name_all.csv`
    - Reference SQL command
        ``` sql
        SELECT "NAME", "THING_ID", "ID"
        FROM public."DATASTREAMS";
        ```

- Modify DATASTREAM_ID list for all projects if needed
    - location: file `constants.py`
    - values
        - Seville: `SV_LIST`
        - Ferrara: `FE_LIST`
        - Vilnius: `VL_LIST`
        - Estonia: `EE_LIST`
        - Zagreb: `ZG_LIST`

- Modify `Keycloak` server if necessary
    - location: file `constants.py`
    - variable: `FROST_KEYCLOAK_SERVER`

- Modify datastream URL from frost server
    - location: file `constants.py`
    - variable: `DS_URL`

- Input the client id and secret defined in `keycloak` for `FROST-server`
    - location: file `constants.py`
    - variable: 
        - `CLIENT_ID`
        - `CLIENT_SECRET`

- Input the environment variables
    - location: file `_.env`
    - input the database info
    - change file name `_.env` to `.env`

## 2.2. Installation
- Run docker compose file
    ```
    docker compose up
    ```
- The service is available at port `8503`
    - To change the port, go to file `docker-compose.yml` and modify line 14 for port output
