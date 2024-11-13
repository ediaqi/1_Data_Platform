import paho.mqtt.client as mqtt
import requests
import json
import threading
import signal
import sys
import time
import os

# LIMITS

pilots = [("kcs-ediaqi-kdp.demo.know-center.at", 1883),("localhost", 1884)]
entities = ["Thing", "Location", "HistoricalLocation", "Datastream", "Sensor", "ObservedProperty", "Observation", "FeatureOfInterest"]
pilots2kdp_table = {}
clients = []
# KDP 
url = "http://localhost:8080/FROST-Server/"
# do a select http request on the frost-server to get max count
counter = 2000
##
# TODO: hashmap IP, ID -> ID of KDP FROST
# save hashmap + counter to file everytime sth is updated
# FROST-Server PUSH Model: over authentification

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("v1.1/Things")
    client.subscribe("v1.1/Locations")

def on_message(client, userdata, msg):
    print("Received data from FROST-Server:")
    print(msg.topic)
    json_payload = json.loads(msg.payload.decode())
    print(json_payload)
    pop_fields = []
    for field in json_payload.keys():
        if "Link" in field:
            pop_fields.append(field)
    for field in pop_fields:
        json_payload.pop(field)

    entity_id = json_payload["@iot.id"]
    for field in json_payload.keys():
        if (field in entities):
            kdp_key_id = userdata[0]+str(userdata[1])+":v1.1/"+field+"s"+str(loc_id["@iot.id"])
            json_payload[field] = {"@iot.id":pilots2kdp_table[kdp_key_id]}
        elif (field[:-1] in entities):
            list_ids = json_payload[field]
            kdp_ids = []
            for loc_id in list_ids:
                kdp_key_id = userdata[0]+str(userdata[1])+":v1.1/"+field+str(loc_id["@iot.id"])
                kdp_ids.append({"@iot.id":pilots2kdp_table[kdp_key_id]})
            json_payload[field] = kdp_ids
    print(json_payload)

    print(userdata)
    post_kdp(msg.topic, json_payload, userdata, entity_id)

def post_kdp(topic, payload, pilot, entity_id):
    global counter
    response = requests.post(url+topic, json=payload)
    if response.status_code == 201:
        print("Forwarded to KDP successfully.")
        pilot_id = pilot[0]+str(pilot[1])
        topic_id = topic+str(entity_id)
        counter += 1
        pilots2kdp_table[pilot_id+":"+topic_id] = counter
    else:
        print(f"Failed to forward to KDP. Status code: {response.status_code}")
        print("Response content:", response.content)
    print("------")

def write_table():
    with open("kdp_table.json", "w") as file:
        json.dump(pilots2kdp_table, file, indent=4)
    print("Data written to file.")


def write_thread_init():
    while True:
        time.sleep(5)
        write_table()

def load_table():
    global pilots2kdp_table
    global counter
    if os.path.exists("kdp_table.json"):
        with open("kdp_table.json", 'r') as file:
            pilots2kdp_table = json.load(file)
        counter = max(pilots2kdp_table.values())

def main():

    def initialize_mqtt(pilot, client_id):
        client = mqtt.Client("client_"+str(client_id), userdata=pilot)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(pilot[0], pilot[1], 60)
        clients.append(client)
        client.loop_forever()

    load_table()

    threads = []
    write_thread = threading.Thread(target=write_thread_init)
    write_thread.start()
    threads.append(write_thread)
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