from elasticsearch import Elasticsearch
import pandas as pd

class KnowAIDEClient:
    def __init__(self, es_host="http://localhost:9200", index_name="knowaide-fusion-index"):
        self.es = Elasticsearch(es_host)
        self.index_name = index_name

    def get_data(self, time_window=None, **kwargs):
        """
        Retrieves fused multi-modal datasets using semantic criteria.
        
        Args:
            time_window (tuple): (start_iso_str, end_iso_str) for phenomenonTime.
            **kwargs: Dynamic filters using Django-style syntax (e.g., Location__name).
        
        Returns:
            dict: The raw Elasticsearch response (hits).
        """
        # Base query structure
        query_body = {
            "query": {
                "bool": {
                    "must": []
                }
            }
        }
        must_clauses = query_body["query"]["bool"]["must"]

        # 1. Handle Time Window (Nested Query on Observations)
        if time_window:
            start_time, end_time = time_window
            must_clauses.append({
                "nested": {
                    "path": "Observations",
                    "query": {
                        "range": {
                            "Observations.phenomenonTime": {
                                "gte": start_time,
                                "lte": end_time
                            }
                        }
                    },
                    "inner_hits": {} # Retrieve only matching observations
                }
            })

        # 2. Handle Dynamic Semantic Filters
        for key, value in kwargs.items():
            # Translate 'Location__name' -> 'Location.name'
            # Translate 'occupant_feedback__thermal_comfort' -> 'occupant_feedback.thermal_comfort'
            es_field = key.replace("__", ".")
            
            # Check if we need a nested query (for Observations) or standard match
            if es_field.startswith("occupant_feedback"):
                # Based on Notebook Cell 27 logic
                must_clauses.append({
                    "match": {
                         es_field: value
                    }
                })
            elif es_field.startswith("ObservedProperty") or es_field.startswith("Location"):
                # Exact match for keyword fields (URIs, Names)
                # Use .keyword for exact matching if it's a text field
                if "definition" in es_field or "name" in es_field:
                    search_field = f"{es_field}.keyword" if "definition" not in es_field else es_field
                    must_clauses.append({"term": {search_field: value}})
                else:
                    must_clauses.append({"match": {es_field: value}})
            else:
                 must_clauses.append({"match": {es_field: value}})

        # Execute Query
        print(f"Executing Query: {query_body}") # Debug
        response = self.es.search(index=self.index_name, body=query_body, size=100)
        
        return self._process_response(response)

    def _process_response(self, response):
        """
        Formats the Elasticsearch response into a user-friendly structure.
        """
        hits = response['hits']['hits']
        results = []
        for hit in hits:
            source = hit['_source']
            # If inner_hits exists (from time window), use those observations
            if 'inner_hits' in hit:
                observations = [h['_source'] for h in hit['inner_hits']['Observations']['hits']['hits']]
            else:
                observations = source.get('Observations', [])
            
            # Flatten context for the result
            item = {
                "DatastreamID": source.get("@iot.id"),
                "Location": source.get("Location", {}).get("name"),
                "Property": source.get("ObservedProperty", {}).get("name"),
                "OccupantFeedback": source.get("occupant_feedback", {}),
                "Observations": observations
            }
            results.append(item)
        return results

# Singleton instance for easy import
# Usage: from knowaide import knowaide
knowaide = KnowAIDEClient()