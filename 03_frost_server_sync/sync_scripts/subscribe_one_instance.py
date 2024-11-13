import paho.mqtt.client as mqtt
import requests
import json
import threading
import signal
import sys

pilots = [("localhost", 1883), ("kcs-ediaqi-kdp.demo.know-center.at", 1883),("localhost", 1884)]
pilots2kdp_table = {}
url = "http://localhost:8080/FROST-Server/"

##
# TODO: hashmap IP, ID -> ID of KDP FROST
# save hashmap + counter to file everytime sth is updated
# FROST-Server PUSH Model: over authentification

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("v1.1/Things")

def on_message(client, userdata, msg):
    print("Received data from FROST-Server:")
    print(msg.topic)
    json_payload = json.loads(msg.payload.decode())
    pop_fields = []
    for field in json_payload.keys():
        if "Link" in field:
            pop_fields.append(field)
    for field in pop_fields:
        json_payload.pop(field)
    print(json_payload)
    """
    response = requests.post(url+msg.topic, json=json_payload)
    if response.status_code == 201:
        print("Forwarded to KDP successfully.")
    else:
        print(f"Failed to forward to KDP. Status code: {response.status_code}")
        print("Response content:", response.content)
    print("------")
    """


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(sys.argv[1], int(sys.argv[2]), 60)
    #client.connect("localhost", 1883, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()