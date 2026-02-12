from elasticsearch import Elasticsearch
from datetime import datetime

class FusionIndexer:
    def __init__(self, es_host="http://localhost:9200", index_name="knowaide-fusion-index"):
        self.es = Elasticsearch(es_host)
        self.index_name = index_name

    def create_mapping(self):
        """
        Initializes the index with the pre-materialized nested structure.
        Source: elasticsearch.ipynb (Cell 5)
        """
        mapping = {
            "mappings": {
                "properties": {
                    "@iot.id": {"type": "long"},
                    "name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                    "description": {"type": "text"},
                    "unitOfMeasurement": {"type": "object"},
                    "ObservedProperty": {
                        "properties": {
                            "name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "definition": {"type": "keyword"},
                            "description": {"type": "text"}
                        }
                    },
                    "Sensor": {
                        "properties": {
                            "name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "metadata": {"type": "keyword"},
                            "properties": {"type": "object"}
                        }
                    },
                    "Thing": {
                        "properties": {
                            "name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "description": {"type": "text"},
                            "properties": {"type": "object"}
                        }
                    },
                    "Location": {
                        "properties": {
                            "name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "description": {"type": "text"},
                            "location": {"type": "geo_shape"}
                        }
                    },
                    # Nested objects for independent querying of time-series data
                    "Observations": {
                        "type": "nested",
                        "properties": {
                            "@iot.id": {"type": "long"},
                            "phenomenonTime": {"type": "date"},
                            "result": {"type": "double"}
                        }
                    },
                    "occupant_feedback": {
                        "properties": {
                            "perceived_iaq": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "thermal_comfort": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                            "path": {"type": "keyword"}
                        }
                    }
                }
            }
        }
        
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name, body=mapping)
            print(f"Index '{self.index_name}' created successfully.")
        else:
            print(f"Index '{self.index_name}' already exists.")

    def index_datastream(self, doc_id, document_body):
        """
        Indexes a complete fused document (Datastream + Metadata + Observations).
        Source: elasticsearch.ipynb (Cell 17)
        """
        resp = self.es.index(index=self.index_name, id=doc_id, document=document_body)
        print(f"Document {doc_id} indexed. Result: {resp['result']}")

    def append_observation(self, doc_id, observation_data):
        """
        Appends a new observation to the nested 'Observations' list.
        This enables the 'Integration Tax' workflow described in the paper.
        """
        script = {
            "source": "ctx._source.Observations.add(params.obs)",
            "lang": "painless",
            "params": {
                "obs": observation_data
            }
        }
        self.es.update(index=self.index_name, id=doc_id, body={"script": script})
        print(f"Observation appended to Datastream {doc_id}.")

# Example usage pattern if run as script
if __name__ == "__main__":
    indexer = FusionIndexer()
    indexer.create_mapping()