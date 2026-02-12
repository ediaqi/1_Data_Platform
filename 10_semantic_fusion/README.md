# Semantic Fusion Layer

This directory contains the Python modules required to interact with the **KnowAIDE Semantic Fusion Index**. This layer resolves the impedance mismatch between the OGC SensorThings API and iRODS by providing a unified, pre-materialized query engine.

## Directory Structure

- `indexer.py`: Handles index initialization (mapping creation) and data ingestion/appending.
- `knowaide.py`: The client wrapper exposing the high-level `get_data` API for researchers.

## Prerequisites

- Python 3.10+
- Elasticsearch instance running (see `../08_elasticsearch`)
- Python dependencies:
  ```bash
  pip install elasticsearch pandas