# Elasticsearch Setup with Docker Compose

This setup deploys **Elasticsearch 8.12.0**, serving as the **Semantic Fusion Layer** for the KnowAIDE platform. It acts as a denormalized query engine that pre-materializes links between quantitative sensor streams (FROST-Server) and qualitative file assets (iRODS), enabling the high-efficiency retrieval demonstrated in the EDIAQI benchmarks.

## Directory Structure

- `08_elasticsearch/`
  - `docker-compose.yaml`: Docker Compose file defining the single-node Elasticsearch service optimized for the Semantic Fusion Index.

## Prerequisites

- **Docker** and **Docker Compose** installed on your machine.
- **System Resources**: Ensure sufficient RAM is allocated to Docker (Minimum 4GB recommended, as the container is configured with 2GB heap).
- **Network**: Port `9200` must be available.

## Configuration Highlights

- **Version**: `8.12.0` (Strictly pinned to match the KnowAIDE benchmarking environment).
- **Cluster Mode**: `single-node` (Suitable for the Fusion Index architecture where data is pre-materialized).
- **Persistence**: Data is persisted in the `es_data` Docker volume.

## Setup and Installation

1. **Run Docker Compose**:
   ```bash
   docker-compose up -d