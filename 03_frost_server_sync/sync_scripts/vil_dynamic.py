import requests
import os
import sys
import json
import threading
import paho.mqtt.client as mqtt
from urllib.parse import urlparse
import tqdm
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3 import disable_warnings

# Disable only the specific warning
disable_warnings(InsecureRequestWarning)

KDP_URL = "https://kdp-ediaqi.know-center.at/FROST-Server/v1.1/"
FROM_URL = "https://airwings-sensorthings.wings-ict-solutions.eu/v1.1/"
AUTH = ("", "")
AUTH2 = ("", "")
lookup_FOIS = {}

def get_access_token():
    payload = {
        'client_id': "frost",
        'username': "",
        'password': "",
        'grant_type': 'password',
        'client_secret': ''
    }

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
        for d in entity_values["value"]:
            identifier = d["properties"]["identifier"]
            #print(identifier)
            #kdp_id = get_origin(KDP_URL+"Datastreams?$filter=properties/identifier eq '"+identifier+"'", AUTH2)
            #print(kdp_id)
            kdp_id = get_originkdp(KDP_URL+"Datastreams?$filter=properties/identifier eq '"+identifier+"'", access_token)
            obs_link = kdp_id["value"][0]["Observations@iot.navigationLink"]
            latest_link = obs_link+"?$orderby=phenomenonTime desc&$top=1"
            latest = get_originkdp(latest_link, access_token)
            # get everything
            if latest["@iot.count"] == 0:
                from_obs_link = get_origin(d["Observations@iot.navigationLink"]+"?$expand=FeatureOfInterest($select=@iot.id)", AUTH)
                """
                while True:
                    if from_obs_link["@iot.count"] == 0:
                        break
                    for obs_entry in tqdm.tqdm(from_obs_link["value"]):
                        #fois_id = get_origin(obs_entry["FeatureOfInterest@iot.navigationLink"], AUTH)["@iot.id"]
                        fois_id = obs_entry["FeatureOfInterest"]["@iot.id"]
                        filtered_data = {key: value for key, value in obs_entry.items() if "@" not in key}
                        filtered_data["FeatureOfInterest"] = { "@iot.id": fois_id + FOIS_OFFSET}
                        post_kdp(obs_link, filtered_data, access_token)
                    if "@iot.nextLink" not in from_obs_link:
                        break
                        
                    from_obs_link = get_origin(from_obs_link["@iot.nextLink"], AUTH)
                """
            else:
                pe = latest["value"][0]["phenomenonTime"]
                from_obs_link = get_origin(d["Observations@iot.navigationLink"]+"?$filter=phenomenonTime gt "+pe+"&$expand=FeatureOfInterest($select=@iot.id)", AUTH)
            while True:
                if from_obs_link["@iot.count"] == 0:
                    break
                create_obs = [{"Datastream":{ "@iot.id": kdp_id["value"][0]["@iot.id"]},
                "components": ["result", "phenomenonTime", "resultTime", "FeatureOfInterest/id"]}]
                dat_array = []
                for obs_entry in tqdm.tqdm(from_obs_link["value"]):
                    x = []
                    x.append(obs_entry["result"])
                    x.append(obs_entry["phenomenonTime"])
                    x.append(obs_entry["resultTime"])

                    if obs_entry["FeatureOfInterest"]["@iot.id"] in lookup_FOIS:
                        x.append(lookup_FOIS[obs_entry["FeatureOfInterest"]["@iot.id"]])
                    else:
                        identifer2 = get_origin(FROM_URL+"FeaturesOfInterest("+str(obs_entry["FeatureOfInterest"]["@iot.id"])+")", AUTH)["properties"]["identifier"]
                        lookup_FOIS[obs_entry["FeatureOfInterest"]["@iot.id"]] = get_originkdp(KDP_URL+"FeaturesOfInterest?$filter=properties/identifier eq '"+identifer2+"'", access_token)["value"][0]["@iot.id"]
                        x.append(lookup_FOIS[obs_entry["FeatureOfInterest"]["@iot.id"]])
                    dat_array.append(x)
                    #fois_id = get_origin(obs_entry["FeatureOfInterest@iot.navigationLink"], AUTH)["@iot.id"]
                    #fois_id = obs_entry["FeatureOfInterest"]["@iot.id"]
                    #filtered_data = {key: value for key, value in obs_entry.items() if "@" not in key}
                    #filtered_data["FeatureOfInterest"] = { "@iot.id": fois_id + FOIS_OFFSET}
                create_obs[0]["dataArray"] = dat_array
                
                post_kdp(KDP_URL+"CreateObservations", create_obs, access_token)
                if "@iot.nextLink" not in from_obs_link:
                    break
                    
                from_obs_link = get_origin(from_obs_link["@iot.nextLink"], AUTH)
            print(f"Done with Datastream: {identifier}")
        if "@iot.nextLink" not in entity_values:
            entity_values = get_origin(FROM_URL+"Datastreams", AUTH)
            continue

        entity_values = get_origin(entity_values["@iot.nextLink"], AUTH)

if __name__ == "__main__":
    main()