'''
This application gives you an overview of all data available in the FROST server. With a logged-in account you can check for duplicates in your project.
'''

import requests
from utils import *
from styling import footer, display_header, sidebar_view

__author__ = "Han Tran"
__copyright__ = "EDIAQI Project"
__credits__ = ["Han Tran"]
__license__ = "EDIAQI Project"
__version__ = "1.0.0"
__maintainer__ = "Han Tran"
__email__ = "htran@know-center.at"


def _get_access_token(usr, pwd):
    payload = {
        'client_id': CLIENT_ID,
        'username': usr,
        'password': pwd,
        'grant_type': 'password',
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(FROST_KEYCLOAK_SERVER, data=payload)
    if response.status_code == 200:
        return response.json()['access_token']
    st.write('Username or Password is not correct. Please try again.')
    return None


def show_schema():
    st.sidebar.write('---------------------')
    if st.sidebar.checkbox('View Schema'):
        st.write('')
        _, col2, _ = st.columns((1, 2, 1))
        with col2:
            st.write('---------------------')
            st.subheader('Schema')
            st.write('[Reference](https://github.com/hylkevds/FROST-Server.Plugin.Projects/)')
            st.image('./images/Datamodel-SensorThingsApi-Projects.drawio.png')


def main():
    st.sidebar.write('### Login')
    usr = st.sidebar.text_input('Username')
    pwd = st.sidebar.text_input('Password', type='password')
    if usr and pwd:
        access_token = _get_access_token(usr, pwd)
        if access_token is None:
            return
        
        view = sidebar_view()
        match view:
            case 'Overall':
                view_all()
            case 'Ferrara':
                view_ferrara()
            case 'Seville':
                view_seville()
            case 'Estonia':
                view_estonia()
            case 'Zagreb':
                view_zagreb()
            case 'Vilnius':
                view_vilnius()
            case _:
                check_dups(access_token)
        show_schema()
    else:
        st.write('Please input username and password first.')
    return


if __name__ == '__main__':
    display_header()
    main()
    footer()
