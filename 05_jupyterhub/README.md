# JupyterHub with Keycloak Authentication and iRODS Integration

This project sets up a JupyterHub environment with Keycloak-based OAuth2 authentication and uses notebooks to store files to iRODS. It provides a multi-user environment with both Python and R notebooks, allowing users to securely access and work with data.

## Features

- **Keycloak Authentication**: Users log in via Keycloak OAuth2 for secure access.
- **Python and R Support**: JupyterHub supports both Python and R, with IRkernel pre-installed for R notebooks.
- **Resource Limits**: Each user is limited to 1 CPU and 2GB of memory to prevent resource overuse.
- **Persistent Storage**: Uses Docker volumes to store user data persistently.
- **Automatic Notebook Copying**: Copies example notebooks to each user’s home directory upon login.

## Directory Structure

- `jupyterhub/`
  - `Dockerfile`: Defines the JupyterHub environment, including installations for Python, R, and OAuth2 authentication.
  - `jupyterhub_config.py`: Configuration file for JupyterHub, setting up Keycloak authentication, user limits, and a hook for copying notebooks.
- `notebooks/`
  - `demo_frost_read.ipynb`, `demo_irods_read.ipynb`: Example Python notebooks for reading data from FROST and iRODS.
  - `R_demo_frost.ipynb`, `R_demo_irods.ipynb`: Example R notebooks for reading data from FROST and iRODS.
- `docker-compose.yml`: Docker Compose file to set up the JupyterHub service and manage the Docker volume for persistent storage.
- `README.md`: Documentation for setting up and running this project.

## Prerequisites

- Docker and Docker Compose installed
- Access to a Keycloak server
- iRODS installed locally

## Installation
1. **Run Docker**:
   ```bash
    docker-compose up -d
