import paho.mqtt.client as mqtt
import requests
import json
import threading
import sys
import time
import os
import copy

clients = []
pilots = [("localhost", 1883)]
entities = {"Thing":"Things", "Location":"Locations", "Datastream":"Datastreams", "Sensor":"Sensors", "ObservedProperty":"ObservedProperties", "Observation":"Observations", "FeatureOfInterest":"FeaturesOfInterest"}
# KDP 
KDP_URL = "http://localhost:8080/FROST-Server/"
# TODO check for other entities

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for entity in entities.keys():
        client.subscribe("v1.1/"+entities[entity])

def on_message(client, userdata, msg):
    print("Received data from FROST-Server:")
    print(msg.topic)
    json_payload = json.loads(msg.payload.decode())
    print(json_payload)
    print("#####")
    iterate_payload = copy.deepcopy(json_payload)
    for field in iterate_payload.keys():
        
        if "@iot.navigationLink" in field:
            field_type = field.split("@")[0]
            if field_type == "HistoricalLocations":
                continue
            get_data = get_origin(json_payload[field])
            if ("@iot.count" in get_data) and (get_data["@iot.count"] > 0):
                kdp_ids = []
                for value in get_data["value"]:
                    value_link = value["@iot.selfLink"]
                    kdp_request = KDP_URL + "v1.1/" + field_type + "?$filter=properties/original@iot.navigationLink eq '"+value_link+"'"
                    kdp_data = get_origin(kdp_request)
                    kdp_id = kdp_data["value"][0]["@iot.id"]
                    # search in KDP
                    kdp_ids.append({"@iot.id":kdp_id})
                json_payload[field_type] = kdp_ids
            if ("@iot.selfLink" in get_data):
                value_link = get_data["@iot.selfLink"]
                field_type_plural = entities[field_type]
                kdp_request = KDP_URL + "v1.1/" + field_type_plural + "?$filter=properties/original@iot.navigationLink eq '"+value_link+"'"
                kdp_data = get_origin(kdp_request)
                kdp_id = kdp_data["value"][0]["@iot.id"]
                # search in KDP
                json_payload[field_type] = {"@iot.id":kdp_id}

    # add to properties the local id
    if not "result" in json_payload:
        if not "properties" in json_payload:
            json_payload["properties"] = {}
        json_payload["properties"]["original@iot.navigationLink"] = json_payload["@iot.selfLink"]
        

    # remove Link field
    pop_fields = []
    for field in json_payload.keys():
        if "@" in field:
            pop_fields.append(field)
    for field in pop_fields:
        json_payload.pop(field)

    print(json_payload)

    post_kdp(msg.topic, json_payload)

def post_kdp(topic, payload):
    response = requests.post(KDP_URL+topic, json=payload)
    if response.status_code == 201:
        print("Forwarded to KDP successfully.")
    else:
        print(f"Failed to forward to KDP. Status code: {response.status_code}")
        print("Response content:", response.content)
    print("------")

def get_origin(url_to_request):

    response = requests.get(url_to_request)
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

    def initialize_mqtt(pilot, client_id):
        client = mqtt.Client("client_"+str(client_id), userdata=pilot)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(pilot[0], pilot[1], 60)
        clients.append(client)
        client.loop_forever()

    threads = []
    # Create threads for initializing clients and running tasks
    for client_id, pilot in enumerate(pilots):
        thread_init = threading.Thread(target=initialize_mqtt, args=(pilot, client_id,))
        thread_init.start()
        threads.append(thread_init)


    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()

    print("All threads have finished.")



if __name__ == "__main__":
    main()