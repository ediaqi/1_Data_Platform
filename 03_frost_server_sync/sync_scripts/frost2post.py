import requests
import os
import sys
import json

KDP_URL = "http://localhost:8080/FROST-Server/v1.1/"
def post_kdp(topic, payload):
    response = requests.post(KDP_URL+topic, json=payload)
    if response.status_code == 201:
        print("Forwarded to KDP successfully.")
    else:
        print(f"Failed to forward to KDP. Status code: {response.status_code}")
        print("Response content:", response.content)
    print("------")

def get_origin(url_to_request):

    response = requests.get(url_to_request, auth=AUTH)
    if response.status_code == 200:
        # The request was successful
        data = response.json()  # Assuming the response is in JSON format
        #print("Response data:", data)
        return data
    else:
        # There was an error with the request
        print(f"Error {response.status_code}: {response.text}")
        print("------")
        return 0

def main():
    postman = {}
    postman["POST to"] = "v1.1/$batch"
    postman["Headers"] = "Content-Type: application/json"
    postman["requests"] = []

    dep = {"Locations": "Things", "Datastreams": ["Thing", "Sensor","ObservedProperty"]}
    plurals = {"Location":"Locations", "Thing": "Things", "Datastream": "Datastreams", 
    "Sensor":"Sensors", "ObservedProperty":"ObservedProperties", "FeatureOfInterest": "FeaturesOfInterest"}

    print(f"Start GET request to: {KDP_URL}")
    list_entities = ["Things", "Locations", "Sensors", "ObservedProperties", "FeaturesOfInterest", "Datastreams"]
    for entity in list_entities:
        entity_values = get_origin(KDP_URL+entity)["value"]
        if entity == "Observations" or entity == "HistoricalLocations":
            continue
        for v in entity_values:
            vjson = {}
            vjson["id"] = entity+str(v["@iot.id"])
            vjson["atomicityGroup"] = "group1"
            vjson["method"] = "post"
            vjson["url"] = entity
            vjson["body"] = {}
            for f in v:
                if "navigationLink" in f:
                    l = f.split("@")[0]
                    if entity in dep and l in dep[entity]:
                        rs = get_origin(v[f])
                        if l[-1] == "s":
                            vjson["body"][l] = []
                            for r in rs["value"]:
                                vjson["body"][l].append({"@iot.id" : "$"+l+str(r["@iot.id"])})
                        else:
                            vjson["body"][l] = {"@iot.id" : "$"+plurals[l]+str(rs["@iot.id"])}
  
                if not "Link" in f:
                    vjson["body"][f] = v[f]
                    
            if entity == "Datastreams":
                if not "properties" in vjson["body"]:
                    vjson["body"]["properties"] = {}
                vjson["body"]["properties"]["original@iot.navigationLink"] = v["@iot.selfLink"]
            postman["requests"].append(vjson)

    #print(json.dumps(postman))
    with open("postman.json", "w") as json_file:
        json.dump(postman, json_file)


if __name__ == "__main__":
    main()