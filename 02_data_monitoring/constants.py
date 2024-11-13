import streamlit as st
import pandas as pd
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px


FROST_KEYCLOAK_SERVER = "https://kdp-ediaqi.know-center.at/keycloak/realms/master/protocol/openid-connect/token"
DS_URL = 'https://kdp-ediaqi.know-center.at/FROST-Server/v1.1/Datastreams'

PRJ_CODES = ['FE', 'EE', 'SV', 'VL', 'ZG']

DS_ID_NAME_FILE = './data_input/datastreamID_name_all.csv'

SV_LIST = list(range(1157, 1215)) + list(range(1219, 1235)) \
            + list(range(5984, 5988))
FE_LIST = list(range(79, 443))
EE_LIST = list(range(1235, 1949))
VL_LIST = list(range(1949, 2369))
ZG_LIST = list(range(2369, 5984))

TIME_LIMIT = '4 hours'

# Keycloak Client for FROST-server
CLIENT_ID = 'frost'
CLIENT_SECRET = 'QAuIoOUTpBlKiD79J2iT9IRUZ10BS2ov'
