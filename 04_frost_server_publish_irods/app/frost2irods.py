import streamlit as st
import os
import signal
import subprocess
import json
from platform import system
import requests
import pandas as pd
from streamlit_keycloak import login
from dataclasses import asdict
from datetime import datetime

FROST_NAME = "https://kdp-ediaqi.know-center.at/FROST-Server/"
AUTH = ('', '')
session_irods = {"irods_host":"localhost",
                 "irods_port": 1247,
                 "irods_zone_name": "ediaqi"}
#test

def stop_app_info(info_msg: str) -> None:
    """
    stops the app and displays an info message

    :param info_msg: string to be displayed by the app
    :return:
    """
    st.info(info_msg)
    st.stop()


def stop_app_error(info_msg: str) -> None:
    """
    stops the app and displays an error message

    :param info_msg: string to be displayed by the app
    :return:
    """
    st.error(info_msg)
    st.stop()

def test_irods_connection(username, password):
    try:
        session_irods["irods_user_name"] = username
        with open("/home/ldirry/.irods/irods_environment.json", "w") as json_file:
            json.dump(session_irods, json_file)
        # only create another process if there is not another one running
        cmd = ["iinit"]
        process = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid, stdin=subprocess.PIPE, encoding='utf8')
        process.stdin.write(password+"\n")
        process.stdin.flush()
        process.wait(timeout=3)
        if process.returncode != 0:
            raise Exception("iCommands exited")
    except Exception as e:
        print(e)
        stop_app_error("There was a problem with the login to the platform!")


def publishirods(username, password, path_irods, df):
    """
    starts and stops the mlflow platform on port
    opens subprocess in background
    stops by killing tracked subprocess
    in a streamlit session there can only be one open mlflow
    possibly leak -> client leaves/reload page without stopping mlflow

    :param port: port on which the mlflow platform should start on
    :return:
    """

    try:
        session_irods["irods_user_name"] = username
        with open("/home/ldirry/.irods/irods_environment.json", "w") as json_file:
            json.dump(session_irods, json_file)
        # only create another process if there is not another one running
        cmd = ["iinit"]
        process = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid, stdin=subprocess.PIPE, encoding='utf8')
        process.stdin.write(password+"\n")
        process.stdin.flush()
        process.wait(timeout=3)
        if process.returncode != 0:
            raise Exception("iCommands exited")
        #data = get_origin(FROST_NAME+frost_url)
        #if data == 0:
        #    stop_app_info(f"Invalid FROST-Server path")
        df.to_csv("dump.csv", index=False)
        #with open("dump.csv", "w") as json_file:
        #    json.dump(data, json_file)
        cmd2 = [f"iput -f dump.csv /ediaqi/home/{username}/{path_irods}"]
        process2 = subprocess.Popen(cmd2, shell=True, preexec_fn=os.setsid)
        process2.wait(timeout=3)
        if process2.returncode != 0:
            raise Exception("Problem with upload of file")
        st.success("Successfully uploaded the dump to the platform!")
    except Exception as e:
        print(e)
        stop_app_error("The path is not valid, make sure the folder exists within the home directory and the filename doesn't contain any whitespaces!")
    
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

def get_originkdp(url_to_request, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url_to_request, headers=headers)
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

def run_the_app() -> None:
    """
    form and showcase of the pycaret and mlflow tools

    :return:
    """
    # SELECT DATA SET
    _, t, _, _, _ = st.sidebar.columns(5)
    with t:
        st.image("knowcenter.jpg", width=150)
    st.sidebar.header("Know-Center Platform Login")
    sb_username = st.sidebar.text_input(label="Username")
    sb_password = st.sidebar.text_input(label="Password", type="password")

    x, y = st.columns([1, 3])
    with x:
        st.text('')
        st.text('')
        st.text('')
        st.text('')
        st.text('')
        st.image("EDIAQI_logo.jpg", width=150)
    with y:
        st.title(f"Obtain SensorThings Observations from Know-Center FROST-Server")

    lprojects = []#[d["name"] for d in get_originkdp(FROST_NAME+"v1.1/Projects", keycloak.access_token)["value"]]
    idprojects = []
    for d in get_originkdp(FROST_NAME+"v1.1/Projects", keycloak.access_token)["value"]:
        lprojects.append(d["name"])
        idprojects.append(d["@iot.id"])

    st.subheader("Select datastream by filtering")
    optionsproject = st.selectbox(
        "Select Pilot or Campaign",
        lprojects)
    chosen_id = idprojects[lprojects.index(optionsproject)]
    a, b = st.columns(2)
    with b:
        lsensors = [d["@iot.id"] for d in get_originkdp(FROST_NAME+"v1.1/Projects("+str(chosen_id)+")/Sensors", keycloak.access_token)["value"]]
        #lsensors.insert(0, "Any")
        option = st.multiselect(
        "Select Sensor(s)",
        lsensors)
    with a:
        lthings = [d["@iot.id"] for d in get_originkdp(FROST_NAME+"v1.1/Projects("+str(chosen_id)+")/Things", keycloak.access_token)["value"]]
        #idthings = [d["@iot.id"] for d in get_originkdp(FROST_NAME+"v1.1/Projects("+str(chosen_id)+")/Things", keycloak.access_token)["value"]]
        option2 = st.multiselect(
        "Select Thing(s)",
        lthings)
        if option2 is None:
            st.write("No Things are in this Project")
            st.stop()
    query = "v1.1/Datastreams?$expand=Sensor,Thing &$filter="
    for idx, o in enumerate(option):
        if idx==0:
            query+="(Sensor/id eq '"+o+"'"
        else:
            query+=" or Sensor/id eq '"+o+"'"
        if idx==len(option)-1:
            query+=")"
    for idx, o in enumerate(option2):
        if len(option) > 0 and idx==0:
            query+=" and "
        if idx==0:
            query+="(Thing/id eq '"+o+"'"
        else:
            query+=" or Thing/id eq '"+o+"'"
        if idx==len(option2)-1:
            query+=")"

    if len(option) == 0 and len(option2) == 0:
        st.write("Select at least one Thing or Sensor.")
        st.stop()
    ldatastreams = []
    lobs = []
    lids = []
    for d in get_originkdp(FROST_NAME+query, keycloak.access_token)["value"]:
        ldatastreams.append(d["name"])
        lids.append(d["@iot.id"])
    
    #ldatastreams2 = []
    #lobs2 = []
    #for d in get_originkdp(FROST_NAME+"v1.1/Projects("+str(chosen_id)+")/Things('"+chosen_id2+"')/Datastreams", keycloak.access_token)["value"]:
    #    ldatastreams.append(d["name"])
    #    lobs.append(d["Observations@iot.navigationLink"])
    #for d in get_originkdp(FROST_NAME+"v1.1/Projects("+str(chosen_id)+")/Sensors('"+option+"')/Datastreams", keycloak.access_token)["value"]:
    #    ldatastreams2.append(d["name"])
    #    lobs2.append(d["Observations@iot.navigationLink"])

    #indices = [i for i, item in enumerate(ldatastreams) if item in ldatastreams2]
    #ldatastreams = [ldatastreams[i] for i in indices]
    #lobs = [lobs[i] for i in indices]
    if ldatastreams == []:
        st.write("There are no datastreams that belong to this Thing and Sensor combination.")
        st.stop()
    option3 = st.multiselect(
    "Select Datastream(s)",
    ldatastreams)
    if len(option3) == 0:
        st.write("Select at least one Datastream.")
        st.stop()

    
    selected_indices = [ldatastreams.index(item) for item in option3]

    lchosenids = [lids[i] for i in selected_indices]

    query = "v1.1/Observations?$expand=Datastream($select=id, name) &$filter="
    for idx, o in enumerate(lchosenids):
        if idx==0:
            query+="(Datastream/id eq '"+str(o)+"'"
        else:
            query+=" or Datastream/id eq '"+str(o)+"'"
        if idx == (len(lchosenids))-1:
            query+=")"

    today = get_originkdp(FROST_NAME+query+"&$orderby=phenomenonTime desc&$top=1", keycloak.access_token)
    if today["@iot.count"] == 0:
        st.write("There are no observation in the chosen datastream.")
        st.stop()
    today = today["value"][0]["phenomenonTime"]
    five_months_ago = get_originkdp(FROST_NAME+query+"&$orderby=phenomenonTime asc&$top=1", keycloak.access_token)["value"][0]["phenomenonTime"]
    #today = datetime.date.today()
    #five_months_ago = today - datetime.timedelta(days=5*30)  # Approximate 5 months as 150 days
    today = datetime.strptime(today.split("T")[0], "%Y-%m-%d")
    five_months_ago = datetime.strptime(five_months_ago.split("T")[0], "%Y-%m-%d")
    # Create a date slider
    selected_date = st.slider(
        "Select a date",
        min_value=five_months_ago,
        max_value=today,
        value=(five_months_ago, today),
        format="YYYY-MM-DD"
    )
    def extract_name(json_str):
        return json_str['name']
    checked = st.checkbox("Show Preview")
    empt = False
    if checked:
        with st.spinner("Loading preview..."):
            dataobs = get_originkdp(FROST_NAME+query+"and phenomenonTime ge "+str(selected_date[0]).split(" ")[0]+"T00:00:00%2B00:00 and phenomenonTime le "+str(selected_date[1]).split(" ")[0]+"T00:00:00%2B00:00", keycloak.access_token)
            if dataobs["@iot.count"] == 0:
                empt = True
                st.write("There are no observation in the chosen datastream.")
            else:
                df = pd.DataFrame(dataobs["value"])
                df = df[["@iot.id", "Datastream", "result", "phenomenonTime"]]
                df.columns = ["id", "Datastream", "result", "phenomenonTime"]

                df['Datastream'] = df['Datastream'].apply(extract_name)
                df[['phenomenonTimeStart', 'phenomenonTimeEnd']] = df['phenomenonTime'].str.split('/', expand=True)
                del df['phenomenonTime']
                st.dataframe(df.head(100))
    if empt:
        st.stop()
    
    # TODO multiple pages
        

        #with st.container(height=200):
        
    
    #st.subheader("Or specify a direct query for the FROST-Server")
    #frost_url = st.text_input(label="URL", value="v1.1/Things")
    #if st.button('Only Request & Display'):
    #    data = get_origin(FROST_NAME+frost_url)
    #    if data == 0:
    #        stop_app_info(f"Invalid FROST-Server path")
    #    with st.container(height=300):
    #        st.json(data)
    t, z = st.columns(2)
    default_name = option3[0].replace("@", "_").replace(".", "_") + ".csv"

    with t:
        path_irods = st.text_input(label="Know Data platform home user path", value=default_name)
    with z:
        st.write('')
        st.write('')
        pub = st.button('Publish .csv file to Know Data Platform')
    if pub:
        alldata = []
        test_irods_connection(sb_username, sb_password)
        progress_bar = st.progress(0)
        dataobs = get_originkdp(FROST_NAME+query+"and phenomenonTime ge "+str(selected_date[0]).split(" ")[0]+"T00:00:00%2B00:00 and phenomenonTime le "+str(selected_date[1]).split(" ")[0]+"T00:00:00%2B00:00&$top=10000", keycloak.access_token)
        if dataobs["@iot.count"] == 0:
            st.write("There are no observation in the chosen datastream.")
            st.stop()

        while True:
            if dataobs["@iot.count"] == 0:
                break
            alldata.extend(dataobs["value"])
            progress_bar.progress(len(alldata)/dataobs["@iot.count"], text="Preparing dump")
           
            if "@iot.nextLink" not in dataobs:
                break
            dataobs = get_originkdp(dataobs["@iot.nextLink"], keycloak.access_token)
        

        df = pd.DataFrame(alldata)
        df = df[["@iot.id", "Datastream", "result", "phenomenonTime"]]
        df.columns = ["id", "Datastream", "result", "phenomenonTime"]

        df['Datastream'] = df['Datastream'].apply(extract_name)
        df[['phenomenonTimeStart', 'phenomenonTimeEnd']] = df['phenomenonTime'].str.split('/', expand=True)
        del df['phenomenonTime']

        publishirods(sb_username, sb_password, path_irods, df)

    #if not chosen_models:
    #    stop_app_info(f"Need to select least one model!")
    



def main() -> None:
    """
    displays an instruction page on how to use this app
    forward option for running the app
    :return:
    """
    # opens the instruction markdown documentation file and displays it
    app_instructions_path = os.path.join("..", "resources", "instructions.md")
    app_content = (open(app_instructions_path, 'r')).read()
    readme_text = st.markdown(app_content)

    # option to switch to the run application page
    option_instructions = "Show instructions"
    option_start_app = "Run app"
    start_options = st.sidebar.selectbox(label="App start options",
                                         options=[option_instructions,
                                                  option_start_app]
                                         )
    if start_options == option_instructions:
        st.sidebar.success('To continue choose: ' + option_start_app)
    elif start_options == option_start_app:
        readme_text.empty()
        run_the_app()

keycloak = login(
    url="https://kdp-ediaqi.know-center.at/keycloak",
    realm="master",
    client_id="publishgui",
)
if keycloak.authenticated:
    main()
else:
    st.title("Publish to Know data platform Login")
