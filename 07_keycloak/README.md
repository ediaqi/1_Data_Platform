# Keycloak Setup with Docker Compose

This setup uses Docker Compose to deploy Keycloak along with a PostgreSQL database as its backend. Keycloak is configured to use an HTTPS URL, and it’s designed for secure access in production environments with hostname configurations and metrics enabled.

## Directory Structure

- `07_keycloak/`
  - `docker-compose.yaml`: Docker Compose file to define the Keycloak and PostgreSQL services.

## Prerequisites

- **Docker** and **Docker Compose** installed on your machine.
- **Valid SSL Certificates** (required for secure HTTPS connections in production).
- **Domain and DNS Configuration**: The Keycloak service URL (e.g., `https://kdp-ediaqi.know-center.at/keycloak`) should be mapped correctly in DNS.

## Setup and Installation

1. **Run Docker Compose**:
   ```bash
   docker-compose up
