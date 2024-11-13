import requests
obs_response = requests.get("https://frost.labservice.it/FROST-Server/v1.1/Datastreams(1)/Observations", auth=("read", "read-Quieta-Sm\\si")).json()
print("@iot.count:"+str(obs_response["@iot.count"]))
obs = []
while True:
    #print(len(obs_response["value"]))
    obs.extend(obs_response["value"])
    if "@iot.nextLink" not in obs_response:
        break
    obs_response = requests.get(obs_response["@iot.nextLink"], auth=("read", "read-Quieta-Sm\\si")).json()
print(f"Actual amount of Observations: {len(obs)}")