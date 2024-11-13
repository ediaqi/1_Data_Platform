# 1. Introduction 

This application serves as an alternative method for ingesting data into the FROST-Server, designed for users without prior knowledge of APIs or technical details. It provides a user-friendly interface (UI) that allows users to upload one or more CSV files simultaneously into the data platform.

```
|___images
|___src
|________\__init__.py
|________constants.py
|________frost_funcs.py
|________main.py
|________post_funcs.py
|________request_DB.py
|________styling.py
|___docker-compose.yml
|___Dockerfile
|___requirements.txt
```

# 2. Installation steps
## 2.1. Preparation

- Input the information of `keycloak` endpoint, client id and secret defined in `keycloak` for `FROST-server`
    - location: file `src/constants.py`
    - variable: 
        - `KEYCLOAK_ENDPOINT`
        - `KEYCLOAK_REALM`
        - `KEYCLOAK_CLIENTID`

## 2.2. Installation
- Run docker compose file
    ```
    docker compose up
    ```
- The service is available at port `8000`
    - To change the port, go to file `docker-compose.yml` and modify line 14 for port output
