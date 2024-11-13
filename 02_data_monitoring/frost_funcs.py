import requests
from constants import DS_URL
import streamlit as st


def get_ds(access_token):
    headers = { 'Authorization': f'Bearer {access_token}'}
    response = requests.get(DS_URL, headers=headers)    
    data = None
    if response.status_code == 200:
        # The request was successful        
        data = response.json()
        # # Assuming the response is in JSON format
    else:        # There was an error with the request        
        st.write(f"Error {response.status_code}: {response.text}")        
        # st.write("-------------------")
    return data
