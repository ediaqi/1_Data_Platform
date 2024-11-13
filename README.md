```
|___01_mainpage
|___02_data_monitoring
|___03_frost_server_sync
|___04_frost_server_publish_irods
|___05_jupyterhub
|___06_data_platform
|___07_keycloak
|___08_UI_csv_upload
```

# 01. Mainpage
This is the landing page where one can find all the links to other applications or websites within the project.

# 02. Data Monitoring
This gives you an overview of all data available in the FROST server. With a logged-in account you can check for duplicates in your project.

# 03. FROST-Server
FROST-Server implements the OCG SensorThings API data model and API. It is designed to store, manage and share sensor data efficiently and supports querying and publishing observations and measurements collected by various IoT devices.

# 04. Publish FROST to Data Platform
Here you can user-friendly query the FROST-Server for observations and upload a .csv dump to the data management platform. Each extracted dump will get a DOI.

# 05. Jupyterhub
At Jupyterhub you can perform data analysis using jupyter notebook. Both Python and R are supported. Data/Metadata can be directly uploaded or retrieved from iRODS.

# 06. Data Platform
iRODS data platform with MetaLNX UI to exchange data in EDIAQI and publish data sets to the outside of EDIAQI.

# 07. Keycloak
This is the user account management section for the rest of the applications, except iRODS.

# 08. CSV UI Upload
This application serves as an alternative method for ingesting data into the FROST-Server, designed for users without prior knowledge of APIs or technical details. It provides a user-friendly interface (UI) that allows users to upload one or more CSV files simultaneously into the data platform.
