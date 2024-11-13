# FROST Server Publish to iRODS Application

This project is a Streamlit-based web application designed to interact with the Know-Center's FROST server and publish data to an iRODS-based data platform. It allows users to authenticate, select data from specific sensors and datastreams, preview the data, and publish it to the Know Data Platform in CSV format.

## Features

- **Authentication**: Uses Keycloak for user authentication.
- **Data Retrieval**: Connects to the Know-Center FROST server to retrieve sensor and observation data.
- **Data Filtering**: Allows users to filter data by project, sensor, and thing.
- **Preview Data**: Displays a preview of the selected data before publishing.
- **Publish to iRODS**: Exports the data as a CSV file and uploads it to a specified path in the iRODS system.

## Directory Structure

- `app/`
  - `EDIAQI_logo.jpg`, `knowcenter.jpg`: Image assets used in the application.
  - `frost2irods.py`: The main Python script for the Streamlit app, handling data retrieval, filtering, and publishing.
- `resources/`
  - `instructions.md`: Instructions for users on how to use the application.
  - `requirements.txt`: Python dependencies required for the application.
- `README.md`: Documentation for setting up and running the application.

## Prerequisites

- Python 3.8 or later
- iRODS iCommands installed locally
- Keycloak

## Installation

1. **Install the required dependencies**:
   ```bash
    pip install -r requirements.txt
2. **Run the Streamlit App**:
   ```bash
    streamlit run app/frost2irods.py
