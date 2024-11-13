import requests
import os
import sys
import json
import threading
import paho.mqtt.client as mqtt
from urllib.parse import urlparse
import tqdm
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3 import disable_warnings

# Disable only the specific warning
disable_warnings(InsecureRequestWarning)

KDP_URL = "https://kdp-ediaqi.know-center.at/FROST-Server/v1.1/"
FROM_URL = "https://frost.labservice.it/FROST-Server/v1.1/"
FOIS_OFFSET = 0

def get_access_token():

    response = requests.post("https://kdp-ediaqi.know-center.at/keycloak/realms/master/protocol/openid-connect/token", data=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors
    token_response = response.json()
    return token_response['access_token']

def post_kdp(url, payload, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers, verify=False)
    if response.status_code == 201:
        pass
        #print("Forwarded to KDP successfully.")
    else:
        print(f"Failed to forward to KDP. Status code: {response.status_code}")
        print("Response content:", response.content)

def get_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.hostname
    
    if domain is not None:
        return domain.split(':')[0]  # Remove port if present
    else:
        return None

def get_origin(url_to_request, a):
    while True:
        try:
            response = requests.get(url_to_request, auth=a, verify=False)
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
        except requests.exceptions.ConnectionError:
            print("Getting ConnectionError")
            time.sleep(600)

def get_originkdp(url_to_request, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url_to_request, headers=headers, verify=False)
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
    print(f"Start GET request from: {FROM_URL}")
    access_token = get_access_token()
    entity_values = get_origin(FROM_URL+"Datastreams", AUTH)
    while True:
        for i in range(40, len(entity_values["value"])):
            d = entity_values["value"][i]
            identifier = d["properties"]["identifier"]
            kdp_id = get_originkdp(KDP_URL+"Datastreams?$filter=properties/identifier eq '"+identifier+"'", access_token)
            obs_link = kdp_id["value"][0]["Observations@iot.navigationLink"]
            obskdp = get_originkdp(obs_link, access_token)
            obsdict = []
            while True:
                if obskdp["@iot.count"] == 0:
                    break
                obsdict.extend(obskdp["value"])

                if "@iot.nextLink" not in obskdp:
                    break
                  
                obskdp = get_originkdp(obskdp["@iot.nextLink"], access_token)
            
            obs_link_og = d["Observations@iot.navigationLink"]
            obskdpog = get_origin(obs_link_og+"?$expand=FeatureOfInterest($select=@iot.id)", AUTH)
            obsdictog = []
            while True:
                if obskdpog["@iot.count"] == 0:
                    break
                obsdictog.extend(obskdpog["value"])
                if "@iot.nextLink" not in obskdpog:
                    break
                obskdpog = get_origin(obskdpog["@iot.nextLink"], AUTH)
            set_A = {(d["phenomenonTime"], d["result"]) for d in obsdictog}
            set_B = {(d["phenomenonTime"], d["result"]) for d in obsdict}
            unique_in_A = set_A - set_B
            dat_array = [[d["result"], d["phenomenonTime"], d["resultTime"], d["FeatureOfInterest"]["@iot.id"]+FOIS_OFFSET] for d in obsdictog if (d["phenomenonTime"], d["result"]) in unique_in_A]
            create_obs = [{"Datastream":{ "@iot.id": kdp_id["value"][0]["@iot.id"]},
                "components": ["result", "phenomenonTime", "resultTime", "FeatureOfInterest/id"]}]
            create_obs[0]["dataArray"] = dat_array
            post_kdp(KDP_URL+"CreateObservations", create_obs, access_token)
            print(f"Done with Datastream: {identifier}")
        if "@iot.nextLink" not in entity_values:
            entity_values = get_origin(FROM_URL+"Datastreams", AUTH)
            continue

        entity_values = get_origin(entity_values["@iot.nextLink"], AUTH)

if __name__ == "__main__":
    main()