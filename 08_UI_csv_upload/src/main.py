import os
from urllib.parse import urlencode

from streamlit.runtime import Runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx

from streamlit_keycloak import login


from frost_funcs import *
from styling import footer, display_header, show_schema
from utils import *
from post_funcs import *


def _get_access_token(usr, pwd):
    payload = {
        'client_id': "frost",
        'username': usr,
        'password': pwd,
        'grant_type': 'password',
        'client_secret': ''
    }

    response = requests.post(FROST_KEYCLOAK_SERVER, data=payload)
    if response.status_code == 200:
        return response.json()['access_token']
    st.write('Username or Password is not correct. Please try again.')
    return None


def _call_func(access_token):
    show_schema()

    imp = st.sidebar.radio('Select', 
                           [
                            'Create Observations',
                            'View Uploaded Observations',
                            'View missing Data'], 
                        #    6
                           )
    match imp:
        case 'Create Observations':
            post_observations(access_token=access_token)
        case 'View Uploaded Observations':
            check_uploaded_observations(access_token=access_token)
        case _:
            view_missing_data(access_token=access_token)


def main():
    st.sidebar.write('### Login')
    usr = st.sidebar.text_input('Username')
    pwd = st.sidebar.text_input('Password', type='password')
    if usr and pwd:
        access_token = _get_access_token(usr, pwd)
        if access_token is None:
            return
        _call_func(access_token)


if __name__ == "__main__":
    display_header()
    main()
    footer()
