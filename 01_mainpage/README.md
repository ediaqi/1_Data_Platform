```
|___images
|___constants.py
|___docker-compose.yml
|___Dockerfile
|___README.md
|___requirements.txt
```

- This is the landing page for the data platform. There are 8 separated websites.
    1. Data Platform
    2. JupyterHub
    3. Publish FROST to Data Platform
    4. CSV Upload UI
    5. Data Monitoring
    6. Keycloak
    7. FROST-Server
    8. Airflow

- To deploy this application, simply run
    ```
    docker compose up
    ```
- To modify the URI of the websites, replace contant values in file `constants.py`
    1. Data Platform: `METALNX`
    2. JupyterHub: `JHUB`
    3. Publish FROST to Data Platform: `PUBLISH`
    4. CSV Upload UI: `CSV_UPLOAD`
    5. Data Monitoring: `MONITORING`
    6. Keycloak: `KEYLOAK`
    7. FROST-Server: `FROST_SERVER`
    8. Airflow: `AIRFLOW`

**Notes:** Make sure docker and docker compose have already been installed.
