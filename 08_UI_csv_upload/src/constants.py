import csv
import json
import time
import os
import numpy as np
import pandas as pd
import requests
import streamlit as st
import pytz
from datetime import datetime, timedelta
import psycopg2


from streamlit_date_picker import date_range_picker, PickerType
import plotly.express as px

local_tz = pytz.timezone('Europe/Vienna')


FROST_SERVER = 'https://kdp-ediaqi.know-center.at/FROST-Server/'
VERSION = 'v1.1'

FROST_KEYCLOAK_SERVER = "https://kdp-ediaqi.know-center.at/keycloak/realms/master/protocol/openid-connect/token"

THINGS_URL = f'{FROST_SERVER}/{VERSION}/Things'
LOCATIONS_URL = f'{FROST_SERVER}/{VERSION}/Locations'
OBSERVEDPROPERTIES_URL = f'{FROST_SERVER}/{VERSION}/ObservedProperties'
SENSORS_URL = f'{FROST_SERVER}/{VERSION}/Sensors'
DATASTREAMS_URL = f'{FROST_SERVER}/{VERSION}/Datastreams'
MULTIDATASTREAMS_URL = f'{FROST_SERVER}/{VERSION}/MultiDatastreams'
OBSERVATIONS_URL = f'{FROST_SERVER}/{VERSION}/Observations'
CREATE_OBSERVATIONS_URL = f'{FROST_SERVER}/{VERSION}/CreateObservations'

BATCH_UPLOAD_URL = f'{FROST_SERVER}/{VERSION}/$batch'

TIME_COL = 'phenomenonTime'
RESULT_COL = 'result'
CSV_FILE_TMP = 'csv_file_tmp.csv'

KEYCLOAK_ENDPOINT = os.environ['KEYCLOAK_ENDPOINT']
KEYCLOAK_REALM = os.environ['KEYCLOAK_REALM']
KEYCLOAK_CLIENTID= os.environ['KEYCLOAK_CLIENTID']


COLUMN_MAPPING = {
    'pm25': 'PM2.5',
    'temp': 'T',
    'humid': 'RH',
    'voc': 'TVOC',
    'co2': 'CO2',
    'ch2o': 'CH2O',
    'no2': 'NO2',
    'o3': 'O3',
    'noise': 'noise',
    'pres': 'P'
}

DATE_HOUR_COLS = [['Date', 'Hour'], 
                  ['Fecha', 'Hora'],
                  ['Date', 'Time']]

TOP_VIEW = 100