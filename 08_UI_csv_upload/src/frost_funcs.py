from constants import *


def get_originkdp(url_to_request, access_token):    
    headers = { 'Authorization': f'Bearer {access_token}'}
    response = requests.get(url_to_request, headers=headers)    
    data = None
    if response.status_code == 200:
        # The request was successful        
        data = response.json()
        # # Assuming the response is in JSON format
    else:        # There was an error with the request        
        st.write(f"Error {response.status_code}: {response.text}")        
        # st.write("-------------------")
    return data


def post_item(url, json_file, json_data=False, access_token=None):

    headers = { 'Authorization': f'Bearer {access_token}'}
    try:
        if json_data: # stream, not file
            r = requests.post(url, 
                        json=json_file, headers=headers, 
                        )
        else:
            r = requests.post(url, 
                            data=open(json_file, 'rb'), headers=headers, 
                            )        
        st.write(f'Return code: {r.status_code}')
        if r.status_code == 201:
            st.write(f'upload successfully')
        elif r.status_code == 502:
            st.write('Data is digesting. Please wait about 30 minutes to check the imported data.')
        else:
            st.write(f'**Upload failed.**')
            st.write(r.json()['message'])
            return False
        
            
        return True
    except:
        st.write('Can not make the connection to FROST-Server. Please check.')
        return False
