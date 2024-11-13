import requests
import os
import sys
import json
import threading
import paho.mqtt.client as mqtt
from urllib.parse import urlparse

KDP_URL = "http://localhost:8081/FROST-Server/v1.1/"
def post_kdp(topic, payload):
    response = requests.post(KDP_URL+topic, json=payload)
    if response.status_code == 201:
        print("Forwarded to KDP successfully.")
    else:
        print(f"Failed to forward to KDP. Status code: {response.status_code}")
        print("Response content:", response.content)
    print("------")

def get_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.hostname
    
    if domain is not None:
        return domain.split(':')[0]  # Remove port if present
    else:
        return None

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

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(userdata)

def on_message(client, userdata, msg):
    print("Received data from FROST-Server:")
    print(msg.topic)
    json_payload = json.loads(msg.payload.decode())
    print(json_payload)
    print("#####")
    

def initialize_mqtt(server_adress, topic, client_id):
    client = mqtt.Client("client_"+str(client_id), userdata=topic)
    client.username_pw_set("read", "read")
    client.on_connect = on_connect
    client.on_message = on_message
    print(f"Connected to: {server_adress} at port: 1883")
    client.connect(server_adress, 1883, 60)
    client.loop_forever()

def main():
    postman = {}
    postman["POST to"] = "v1.1/$batch"
    postman["Headers"] = "Content-Type: application/json"
    postman["requests"] = []

    dep = {"Locations": "Things", "Datastreams": ["Thing", "Sensor","ObservedProperty"]}
    plurals = {"Location":"Locations", "Thing": "Things", "Datastream": "Datastreams", 
    "Sensor":"Sensors", "ObservedProperty":"ObservedProperties", "FeatureOfInterest": "FeaturesOfInterest"}

    print(f"Start GET request to: {KDP_URL}")
    entity_values = get_origin(KDP_URL+"Datastreams")["value"]
    threads = []
    for client_id, v in enumerate(entity_values):
        url = v["properties"]["original@iot.navigationLink"]
        server_adress = get_domain(url)
        topic = "v1.1"+url.split("v1.1")[1]+"/Observations"
        print(topic)
        thread_init = threading.Thread(target=initialize_mqtt, args=(server_adress, topic, client_id,))
        thread_init.start()
        threads.append(thread_init)


    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()


if __name__ == "__main__":
    main()