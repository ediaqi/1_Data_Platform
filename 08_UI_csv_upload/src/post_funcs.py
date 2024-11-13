# from constants import *
from frost_funcs import *
from utils import *
from request_DB import *


def post_thing():
    upload_file = st.file_uploader('Please upload *Thing* in .json format.')
    if upload_file:
        json_data = json.load(upload_file)
        with st.expander('View uploaded data', True):
        # if st.checkbox('View uploaded data'):
            st.write(json_data)
        if st.button('Upload Thing'):
            return_code = post_item(THINGS_URL, json_data, True)
            if return_code:
                st.write('Uploaded *Thing* successfully!')
            else:
                st.write('Error occurred. Please check the data again.')
    else:
        thing_json = './data/Thing.json'
        with st.expander('Sample File', True):
            with open(thing_json) as f:
                data = json.load(f)
                st.write(data)
            # download sample
            download_sample(thing_json)


def _upload_file_post(URL,
                      text='Property',
                      sample_file='./data/ObservedProperty.json',
                      access_token=None):
    upload_file = st.file_uploader(f'Please upload *{text}* in .json format.')
    if upload_file:
        json_data = json.load(upload_file)
        with st.expander('View uploaded data', True):
            st.write(json_data)
        if st.button(f'Upload {text}'):
            return_code = post_item(URL, json_data, True)
            if return_code:
                st.write(f'Uploaded *{text}* successfully!')
            else:
                st.write('Error occurred. Please check the data again.')
    
    else:        
        with st.expander('Sample File', True):
            with open(sample_file) as f:
                data = json.load(f)
                st.write(data)
            # download sample
            download_sample(sample_file)


def _get_things(access_token=None):
    # things = get_item(THINGS_URL)
    things = get_originkdp(THINGS_URL, access_token)
    if not things:
        st.write('There is not any *Thing* in the database. Please create one.')
        return None
    if things['@iot.count'] == 0: return
    things_dict = {}
    for thing in things['value']:
        # for k, v in thing.items():
        things_dict[f'{thing["@iot.id"]}'] = thing['description']
    thing_sel = st.sidebar.selectbox('Choose a current Thing',
                             things_dict.keys())
    st.sidebar.write(f'Description: *{things_dict[thing_sel]}*')
    thing_id = thing_sel.split(maxsplit=1)[0] # thing_id
    return thing_id


def post_location(access_token=None):
    json_text = {}
    thing_ids = None
    if st.sidebar.checkbox('Related to a *Thing*?', True):
        things = get_originkdp(THINGS_URL, access_token)
        if not things:
            st.write('There is not any *Thing* in the database. Please create one.')
            return None
        if things['@iot.count'] == 0: return
        things_dict = {}
        for thing in things['value']:
            things_dict[f'{thing["@iot.id"]}'] = thing['description']
        thing_ids = st.sidebar.multiselect('Choose a current Thing',
                                things_dict.keys())

    json_text['Things'] = []
    if thing_ids:
        json_text['Things'] = [{"@iot.id": thing_id} for thing_id in thing_ids]
    name = st.text_input('Name')
    if name:
        json_text['name'] = name
    desc = st.text_area('Description')
    if desc:
        json_text['description'] = desc

    encodingType = st.text_input('encodingType')
    if encodingType:
        json_text['encodingType'] = encodingType
    
    json_text['location'] = {}    
    with st.expander('location', True):
        location_type = st.text_input('type')
        if location_type:
            json_text['location']['type'] = location_type
        
        with st.container(border=True):
            st.write('coordinates')
            col1, col2 = st.columns(2)
            lat = col1.text_input('latitude')
            lon = col2.text_input('longitude')
            if lat and lon:
                json_text['location']['coordinates'] = [lat, lon]
    
    st.write('#### Review Your Input')
    st.json(json_text)
    if st.button('Create Location'):
        try:
            result = post_item(LOCATIONS_URL, json_text, json_data=True)
            if result:
                st.write('Uploaded successfully.')
            else:
                st.write('Upload Error. Please check the input.')
        except:
            st.write(f'Data is not valid. Please check the input.')

    return True


def post_observedproperty(access_token=None):
    _upload_file_post(OBSERVEDPROPERTIES_URL, 'Property', 
                      './data/ObservedProperty.json', access_token)
    return


def post_sensor(access_token=None):
    _upload_file_post(SENSORS_URL, 'Sensor', 
                      './data/Sensor.json', access_token)
    return


def post_stream(multi=False, access_token=None):
    json_text = {}
    # get Thing
    thing_id = _get_things(access_token)
    if thing_id is None:
        return
    json_text['Thing'] = {"@iot.id": thing_id}

    # get Sensor
    ########################
    st.sidebar.write('-------------')
    sensors = get_originkdp(SENSORS_URL, access_token)
    if not sensors:
        st.write('There is no sensors in the database. Please *Create Sensor*.')
        return
    sensors_dict = {}
    for sensor in sensors['value']:
        sensors_dict[f'{sensor["@iot.id"]}'] = sensor['description']
    sensor_sel = st.sidebar.selectbox('Choose a current Sensor',
                                      sensors_dict.keys())
    if not sensors_dict:
        st.write('There is no Sensor in the database. Please create a new one.')
        return    
    st.sidebar.write(f'Description: *{sensors_dict[sensor_sel]}*')
    sensor_id = sensor_sel.split(maxsplit=1)[0] # sensor_id
    json_text['Sensor'] = {"@iot.id": sensor_id}

    #########################
    # input 
    name = st.text_input('Name')
    if name:
        json_text['name'] = name
    desc = st.text_area('Description')
    if desc:
        json_text['description'] = desc

    observationType = st.text_input('observationType')
    if observationType:
        json_text['observationType'] = observationType

    if multi:
        st.write('##### Input for each property')
        return post_multidatastream(json_text, access_token)
    return post_datastream(json_text, access_token)


def _post_unitOfMeasurement(text, i=0, cnt=3):
    json_text = {}
    with st.expander(f'unitOfMeasurement of *{text}*', True):
        mes_name = st.text_input('name', key=cnt*i+1)
        if mes_name:
            json_text['name'] = mes_name
        mes_symbol = st.text_input('symbol', key=cnt*i+2)
        if mes_symbol:
            json_text['symbol'] = mes_symbol
        definition = st.text_input('definition', key=cnt*i+3)
        if definition:
            json_text['definition'] = definition
    return json_text


def post_datastream(json_text, access_token=None):

    # get ObservedProperty
    ########################
    st.sidebar.write('-------------')
    properties = get_originkdp(OBSERVEDPROPERTIES_URL, access_token)
    if not properties:
        st.write('There is no property in the database. Please *Create ObservedProperty*')
        return
    prop_dict = {}
    for prop in properties['value']:
        prop_dict[f'{prop["@iot.id"]}. {prop["name"]}'] = prop['description']        
    prop_sel = st.sidebar.selectbox('Choose a current Property',
                                    prop_dict.keys())
    st.sidebar.write(f'Description: {prop_dict[prop_sel]}')
    prop_id = prop_sel.split('.', maxsplit=1)[0]
    json_text['ObservedProperty'] = {"@iot.id": int(prop_id)}
    
    
    json_text['unitOfMeasurement'] = {}
    unitOfMeasurement = _post_unitOfMeasurement(prop_sel)
    if unitOfMeasurement:
        json_text['unitOfMeasurement'] = unitOfMeasurement
    st.write('#### Review Your Input')
    st.json(json_text)
    with open('json_text.json', 'w') as f:
        json.dump(json_text, f, indent=4)
    if st.button('Create Datastream'):
        try:
            result = post_item(DATASTREAMS_URL, json_text, json_data=True)
            if result:
                st.write('Uploaded successfully.')
            else:
                st.write('Upload Error. Please check the input.')
        except:
            st.write(f'Data is not valid. Please check the input.')

    st.sidebar.write('-------------')
    return


def post_multidatastream(json_text, access_token=None):

    # get ObservedProperty
    ########################
    st.sidebar.write('-------------')
    properties = get_originkdp(OBSERVEDPROPERTIES_URL, access_token)
    if not properties:
        st.write('There is no property in the database. Please *Create ObservedProperty*')
        return
    prop_dict = {}
    for prop in properties['value']:
        prop_dict[f'{prop["@iot.id"]}. {prop["name"]}'] = prop['description']        
    prop_sel = st.sidebar.multiselect('Choose from the current Properties',
                                    prop_dict.keys())
    if len(prop_sel) < 2:
        st.write('Please select more than one property.')
        st.sidebar.write('-------------')
        return
    prop_ids = [int(i.split('.', maxsplit=1)[0]) for i in prop_sel]
    json_text['ObservedProperties'] =[{"@iot.id": i} for i in prop_ids]
    json_text['unitOfMeasurements'] = []
    json_text['multiObservationDataTypes'] = []
    for i in range(len(prop_ids)):
        pro_name = prop_sel[i]
        st.write(f'###### {pro_name}')
        multiObservationDataTypes = st.text_input(f'multiObservationDataType for {pro_name}',
                                                  key=i*4)
        if multiObservationDataTypes:
            json_text['multiObservationDataTypes'].append(multiObservationDataTypes)
        result = _post_unitOfMeasurement(pro_name, i, cnt=4)
        if result:
            json_text['unitOfMeasurements'].append(result)

    st.write('#### Review Your Input')
    st.json(json_text)
    if st.button('Create Multidatastream'):
        try:
            result = post_item(MULTIDATASTREAMS_URL, json_text, json_data=True)
            if result:
                st.write('Uploaded successfully.')
            else:
                st.write('Upload Error. Please check the input.')
        except:
            st.write(f'Data is not valid. Please check the input.')

    st.sidebar.write('-------------')


def post_observations(access_token=None):
    # get Things
    ########################
    things = get_originkdp(THINGS_URL, access_token)
    if not things: return
    if things['@iot.count'] == 0: return

    things_dict = {}
    for thing in things['value']:
        things_dict[f'{thing["@iot.id"]}'] = thing['description']
    thing_sel = st.sidebar.selectbox('Choose a current Thing',
                             things_dict.keys())
    st.sidebar.write(f'Description: *{things_dict[thing_sel]}*')
    thing_id = thing_sel.split(maxsplit=1)[0]

    # # get Datastreams
    # ########################
    observation_stream(thing_id, access_token)
    return


def check_uploaded_observations(access_token=None):
    if not access_token:
        return
    # get Things
    ########################
    things = get_originkdp(THINGS_URL, access_token)
    if not things: return
    if things['@iot.count'] == 0: return

    things_dict = {}
    for thing in things['value']:
        things_dict[f'{thing["@iot.id"]}'] = thing['description']
    thing_sel = st.sidebar.selectbox('Choose a current Thing',
                             things_dict.keys())
    thing_id = thing_sel.split(maxsplit=1)[0]
    filtered_ds = _get_thing_stream_rel(thing_id, access_token)
    filtered_ds_ids_names = {i['name']:i['@iot.id'] for i in filtered_ds}
    selected_ds = st.sidebar.multiselect('Select one or more Datastreams', filtered_ds_ids_names.keys())
    if not selected_ds:
        st.write('Please select one ore more Datastreams to display.')
        return
    selected_ds_ids_names = {j:i for i, j in filtered_ds_ids_names.items() if i in selected_ds}
    
    st.write('#### Recent Data uploaded')
    df_show = pd.DataFrame()
    col1, _ = st.columns([1, 2])
    ntop = col1.selectbox('How many latest values would you like to view?', [1, 10, 50, 100, 200, 500], 2)
    id_list = list(selected_ds_ids_names.keys())
    for ds_id in id_list:
        query = f'''
            SELECT "PHENOMENON_TIME_START", "RESULT_NUMBER" 
                FROM public."OBSERVATIONS" 
                WHERE "DATASTREAM_ID"={ds_id}
                ORDER BY "PHENOMENON_TIME_START" DESC 
                LIMIT {ntop};
        '''
        data = retrieve_data(query)
        if not data:
            st.write(f'There is no data retrieved for {selected_ds_ids_names[ds_id]}.')
            continue
        data = pd.DataFrame(data)
        data.columns = ['TimeStamp', selected_ds_ids_names[ds_id]]
        data['TimeStamp'] = pd.to_datetime(data['TimeStamp'])
        data['TimeStamp'] = data['TimeStamp'].dt.tz_convert('Europe/Vienna')
        if df_show.empty:
            df_show = data
        else:
            df_show = df_show.merge(data, how='outer')
    if not df_show.empty:
        if df_show.drop_duplicates().shape[0] < df_show.shape[0]:
            st.write('__There are duplicates!__')
        # df_show = df_show.set_index('TimeStamp')
        df_show = df_show.sort_values('TimeStamp', ascending=False)
        st.write(df_show.reset_index(drop=True))

    st.sidebar.write('-------------------')


def view_missing_data(access_token=None):
    if not access_token:
        return
    # get Things
    ########################
    things = get_originkdp(THINGS_URL, access_token)
    if not things: return
    if things['@iot.count'] == 0: return

    things_dict = {}
    for thing in things['value']:
        things_dict[f'{thing["@iot.id"]}'] = thing['description']
    thing_sel = st.sidebar.selectbox('Choose a current Thing',
                             things_dict.keys())
    thing_id = thing_sel.split(maxsplit=1)[0]
    filtered_ds = _get_thing_stream_rel(thing_id, access_token)
    filtered_ds_ids_names = {i['name']:i['@iot.id'] for i in filtered_ds}
    selected_ds = st.sidebar.multiselect('Select one or more Datastreams', filtered_ds_ids_names.keys())
    selected_ds_ids_names = {j:i for i, j in filtered_ds_ids_names.items() if i in selected_ds}
    if selected_ds_ids_names:
        st.write('#### Selected Datastreams')
    else:
        st.write('**Please select one or more Datastreams.**')
    for idx, ds_id in enumerate(selected_ds_ids_names.keys()):
        st.write(f'##### {idx+1}. {selected_ds_ids_names[ds_id]}')
        min_date = retrieve_data(f'''
            SELECT MIN("PHENOMENON_TIME_START")
                FROM public."OBSERVATIONS"
                WHERE "DATASTREAM_ID" = {ds_id};''')
        if min_date:
            min_date = min_date[0][0]
        max_date = retrieve_data(f'''
            SELECT MAX("PHENOMENON_TIME_START")
                FROM public."OBSERVATIONS"
                WHERE "DATASTREAM_ID" = {ds_id}; ''')
        if max_date:
            max_date = max_date[0][0]
        
        if not min_date or not max_date:
            st.write('**This Datastream does not have data yet.**')
            continue
        date_range_string = date_range_picker(picker_type=PickerType.time,
                                            start=min_date, end=max_date,
                                            key=selected_ds_ids_names[ds_id]
                                                            )
        if date_range_string:
            start_time, end_time = date_range_string
            start_time = local_tz.localize(datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
            end_time = local_tz.localize(datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S'))
        
            if st.checkbox(f'View #Observations per day ({selected_ds_ids_names[ds_id]})',
                           key=f'{ds_id}_view_obs'):
                query = f'''
                SELECT DATE("PHENOMENON_TIME_START") AS "Date", COUNT(*) AS "Count"
                    FROM public."OBSERVATIONS"
                    WHERE "DATASTREAM_ID" = {ds_id}
                    AND "PHENOMENON_TIME_START" >= '{start_time}'
                    AND "PHENOMENON_TIME_START" <= '{end_time}'
                    GROUP BY DATE("PHENOMENON_TIME_START")
                    ORDER BY DATE("PHENOMENON_TIME_START") DESC;
                    '''
                data = retrieve_data(query)
                if data:
                    data = pd.DataFrame(data)
                    data.columns = ['TimeStamp', 'Count']
                    data.set_index('TimeStamp', inplace=True)
                    _, col2 = st.columns([1, 15])
                    with col2:
                        if st.checkbox('View Plot of #Observations per day', True, 
                                    key=f'{ds_id}_plot_cnt'):
                            fig = px.scatter(data)
                            fig.layout.showlegend = False
                            fig.update_layout(yaxis_title= "Count")
                            st.plotly_chart(fig)
                        if st.checkbox('View data in table', key=f'{ds_id}_view_cnt'):

                            st.write(data)

            # view values with time
            if st.checkbox(f'View values in the selected period of {selected_ds_ids_names[ds_id]}'):
                query = f'''
                SELECT "PHENOMENON_TIME_START" AS "Date", "RESULT_NUMBER" AS "Value"
                    FROM public."OBSERVATIONS"
                    WHERE "DATASTREAM_ID" = {ds_id}
                    AND "PHENOMENON_TIME_START" >= '{start_time}'
                    AND "PHENOMENON_TIME_START" <= '{end_time}'
                    ORDER BY "PHENOMENON_TIME_START";
                    '''
                data = retrieve_data(query)
                if data:
                    data = pd.DataFrame(data)
                    data.columns = ['TimeStamp', 'Value']                    
                    data['TimeStamp'] = data['TimeStamp'].apply(lambda x: x.astimezone(local_tz))
                    _, col2 = st.columns([1, 15])
                    with col2:
                        data = data.drop_duplicates()
                        if st.checkbox('View Plot (already deduplicated if any)', True, key=f'{ds_id}_plot_value'):
                            data_dup = data.copy()
                            data_dup = data_dup.drop_duplicates()
                            data_dup.set_index('TimeStamp', inplace=True)
                            fig = px.line(data_dup)
                            fig.layout.showlegend = False
                            st.plotly_chart(fig)
                        if st.checkbox('View data in table', key=f'{ds_id}_view_value'):
                            data.set_index('TimeStamp', inplace=True)
                            st.write(data)


@st.cache_data
def _get_thing_stream_rel(thing_id, access_token=None):
    r = get_originkdp(DATASTREAMS_URL, access_token)
    if r:
        datastreams = r['value']
        filtered_ds = [i for i in datastreams if thing_id in i['name']
                       and (SEVILLE_CODE in i['name'])]
        return filtered_ds
    return None


def _exract_timestamp(df) -> pd.DataFrame:
    cols = []
    timestamp_cols = []
    has_timestamp = None
    for date_col, hour_col in DATE_HOUR_COLS:
        cols = [i for i in df.columns 
                        if (i.lower().strip() in [date_col.lower(), hour_col.lower()])]
        if len(cols) == 2:
            has_timestamp = st.checkbox('Data has Timestamp', True)
            col1, col2, _ = st.columns([1, 1, 4])
            with col1:
                timestamp_cols.append(st.selectbox('Date', [''] + list(df.columns), 
                                                   ([''] + list(df.columns)).index(cols[0])))
            with col2:
                rest_cols = [''] + [i for i in df.columns if i!=timestamp_cols[0]]
                timestamp_cols.append(st.selectbox('Hour', rest_cols, 
                                                   rest_cols.index(cols[1])))
            break
    timestamp_cols = [i for i in timestamp_cols if i.strip()]
    if len(timestamp_cols) == 2:
        if has_timestamp:            
            time_disp = st.checkbox('Hide Display')
            col1, col2, col3, _ = st.columns([2, 1.5, 4, 2])
            if not time_disp:
                with col1:
                    st.write('Columns contain Timestamps')
                    st.write(df[timestamp_cols])
            try:
                date_col, hour_col = timestamp_cols
                df['Timestamp'] = df[date_col].astype(str) + ' ' + df[hour_col].astype(str)
                df['Timestamp'] = pd.to_datetime(df['Timestamp']).astype(str)
                df['Timestamp'] = df['Timestamp'].apply(\
                    lambda x: utc_to_local(datetime.fromisoformat(x)).isoformat(timespec='seconds'))
                timestamp_cols.append('Timestamp')
                if not time_disp:
                    col2.write('==> convert to Timestamp ==>')
                    with col3:
                        st.write('Combined Date and Hour')
                        st.write(df[['Timestamp']])
            except:
                st.write('**!!!Can not read date time or timestamp as given**')
        else:
            cols = []
    else: # only timestamp column?
        cols = [i for i in df.columns if ('timestamp' in i.lower().strip())]
        if len(cols) == 1: # found
            has_timestamp = st.checkbox('Data has Timestamp', True)
            try:
                if has_timestamp:
                    col1, _ = st.columns([1, 4])
                    timestamp_cols.append(col1.selectbox('Timestamp', df.columns, 
                                                    list(df.columns).index(cols[0])))
                    df[cols[0]] = pd.to_datetime(df[cols[0]]).astype(str)
                    df = df.rename(columns={cols[0]: 'Timestamp'})
                    df['Timestamp'] = df['Timestamp'].apply(\
                            lambda x: utc_to_local(datetime.fromisoformat(x)).isoformat(timespec='seconds'))
                    timestamp_cols[-1] = 'Timestamp'
                    st.write(df['Timestamp'])
            except:
                st.write(f'Can not parse timestamp column "{cols[0]}"')
        else:
            st.write('There is no timestamps in the uploaded data.')

    return df, timestamp_cols


def _search_column(v, name, all_cols):
    default_index = None
    if isinstance(name, str):
        map_val = [i for i in all_cols if name in i.lower()]
    else:
        map_val = [i for j in name for i in all_cols if j in i.lower()]

    if len(map_val) >= 1:
        if len(map_val) > 1:
            st.write(f'There are more than one match for {name}: {map_val}')
        default_index = all_cols.index(map_val[0])
    else:
        st.write(f'**Could not find a match for {v}. Please select from the list.**')

    return default_index


def _column_mapping(v, name, all_cols):

    match name:
        case 'T': # temperature
            return _search_column(v, 'temp', all_cols)
        ################################
        # 2. P
        case 'P':
            return _search_column(v, 'pres', all_cols)
        ################################
        # 3. PM2.5
        case 'PM2.5':
            return _search_column(v, 'pm2', all_cols)
        ################################
        # 4. RH
        case 'RH':
            # default_index = _search_column(v, 'humid', all_cols)
            # if default_index:
            #     return default_index
            return _search_column(v, ['humid', 'hr'], all_cols)
        ################################
        # 5. O3
        case 'O3':
            return _search_column(v, 'o3', all_cols)
        ################################
        # 6. TVOC
        case 'TVOC':
            return _search_column(v, 'voc', all_cols)
        ################################
        # 7. NO2
        case 'NO2':
            return _search_column(v, 'no2', all_cols)
        ################################
        # 8. CH2O
        case 'CH20':
            return _search_column(v, 'cho2', all_cols)
        ################################
        # 9. CO2
        case 'CO2':
            return _search_column(v, 'co2', all_cols)
        ################################
        # 10. noise
        case 'noise':
            return _search_column(v, 'noise', all_cols)
        case _:
            return None


def observation_stream(thing_id, access_token=None):
    filtered_ds = _get_thing_stream_rel(thing_id, access_token)
    datastreams_values = [i['name'] for i in filtered_ds]
    with st.sidebar:
        if datastreams_values:
            st.write('__Datastreams in this Thing__')
            st.write(datastreams_values)
        else:
            st.write('__There is no Datastream in this Thing__')
            return
        
    if st.sidebar.checkbox('View Datastream details'):
        st.write('##### Datastream details')
        st.write(filtered_ds)
    col1, col2, _ = st.columns([4, 1, 5])
    file_uploadeds = col1.file_uploader('Upload file(s)', accept_multiple_files=True)
    sep = col2.text_input('Delimiter', ',')
    json_text = {}
    mapping = {}
    if file_uploadeds:
        df = pd.DataFrame()
        for file_uploaded in file_uploadeds:
            if file_uploaded.name.lower().endswith('.csv'):
                tmp = pd.read_csv(file_uploaded, sep=sep)
                df = pd.concat([df, tmp], ignore_index=True)
            elif file_uploaded.name.lower().endswith('.xlsx'):
                tmp = pd.read_excel(file_uploaded)
                df = pd.concat([df, tmp], ignore_index=True)
            else:
                st.write(f'Only .csv and .xlsx accepted. Your file: {file_uploaded.name}')
        if not df.empty:
            if st.sidebar.checkbox('View uploaded data', True):
                st.write('##### Uploaded Data')
                st.write(df)
            if st.sidebar.checkbox('View data type of each column'):
                st.sidebar.write(df.dtypes)
            
            # check duplicates
            #############################
            if df.shape[0] > df.drop_duplicates().shape[0]:
                st.write('##### >>> Duplicates detected! Duplicates will be automatically removed before uploaded into Database.<<<')
                st.write(df[df.duplicated()])
                st.write('##### >>> Data after dropped duplicates:')
                st.write(df[df.duplicated(keep=False)])
                df = df.drop_duplicates()
            st.subheader('Data Parsed:')

            ################################
            # extract Timestamp
            df, timestamp_cols = _exract_timestamp(df)
            timestamp_map = [i for i in timestamp_cols if 'timestamp' in i.lower()]
            if len(timestamp_map) == 1:
                mapping['Timestamp'] = timestamp_map[0]
                
            
            ################################
            st.write('##### Mapping value columns with Datastreams')
            all_cols = [i for i in df.columns if i not in timestamp_cols]
            col1, _ = st.columns([1, 1.5])

            with col1:
                for v in datastreams_values:
                    default_index = 0
                    name = v.split('@')[0].strip() # example "PM2.5@THI.SV.001" -> PM2.5
                    default_index = _column_mapping(v, name, all_cols)
                    if default_index is not None:
                        mapping[v] = st.selectbox(v, all_cols, default_index)
                        if len([i for i in mapping[v] if i]) > 0: # column selected
                            all_cols = [i for i in all_cols if i not in mapping.values()]
                    else:
                        mapping[v] = st.selectbox(v, [None]+all_cols, default_index)

            ################################
            # convert temp to Celcius if nescessary
            temp = [[i, j] for i, j in mapping.items() if j and 'temp' in j.strip().lower()]
            if len(temp) == 1:
                temp_id, temp_name = temp[0]
                if len(temp_name.split('(')) > 1:
                    if 'f' in temp_name.split('(')[1].strip().lower():
                        filtered_temp = [i for i in filtered_ds if i['name']==temp_id][0]
                        if 'celsius' in filtered_temp["unitOfMeasurement"]['name'].lower():                            
                            st.write('###### >>> Temperature in the file is in Fahrenheit. Datastream is in Celsius.')
                            if st.checkbox('Convert?', True):
                                col1, col2, col3, _ = st.columns([1, 1, 1, 3])
                                col1.write(df[temp_name])
                                col2.write('==> Converted ==>')
                                new_col = 'Temperature (C)'
                                df[new_col] = ((df[temp_name].astype(float) - 32)*5/9).round(1)
                                col3.write(df[new_col])
                                mapping[temp_id] = new_col
            ################################
            # create json to send request
            df_tmp = pd.DataFrame.from_dict(mapping, orient='index').reset_index()
            df_tmp.columns = ['Datastream', 'Column Name']
            if st.checkbox('###### Review Final Mapping', True):
                
                st.write(df_tmp)


            #############################################
            ## check duplicates in DB
            st.write('----------------------')
            mapping = {i: j for i, j in mapping.items() if j}
            st.write('#### Check data in FROST-Server and Duplicates') # Han modified 20240918
            ds_name_ids = {i['name']:i['@iot.id'] for i in filtered_ds}
            df_dup = df.drop_duplicates(subset='Timestamp', keep='first')
            # st.write(df.shape)
            if df.shape[0] > df_dup.shape[0]:
                df_dedup = df[df.duplicated(subset='Timestamp', keep=False)]
                st.write(f'Timestamp has duplicates: {df.shape[0] - df_dup.shape[0]} rows')
                st.write(df_dedup[mapping.values()])
                st.write('**>>>Duplicates will be removed. First values have been kept.**')
                df = df.drop_duplicates(subset='Timestamp', keep='first')

            st.write('-----------')
            df_new, data = None, None
            for ds_name, ds_id in ds_name_ids.items():
                if ds_name not in mapping: continue
                st.write(f'**{ds_name}**') 
                # if not mapping[ds_name]: continue
                # st.write(f'**{ds_name}**')                
                ds_series = df[df[mapping[ds_name]].notna()][['Timestamp', mapping[ds_name]]].drop_duplicates()
                if ds_series.empty:
                    continue
                start_time = ds_series['Timestamp'].min()
                end_time = ds_series['Timestamp'].max()
                st.write(f'Start time: **{start_time}**')
                st.write(f'End time: **{end_time}**')
                query = f'''
                    SELECT "PHENOMENON_TIME_START", "RESULT_NUMBER"
                        FROM public."OBSERVATIONS"
                        WHERE "DATASTREAM_ID" = {ds_id}
                        AND "PHENOMENON_TIME_START" >= '{start_time}'
                        AND "PHENOMENON_TIME_START" <= '{end_time}'
                    ORDER BY DATE("PHENOMENON_TIME_START") DESC;'''

                data = retrieve_data(query)
                if data:
                    if df_new is None: df_new = pd.DataFrame()
                    ds_series['Timestamp'] = pd.to_datetime(ds_series['Timestamp']).apply(lambda x: x.astimezone(local_tz))
                    st.write(f'\t\tFound data in DB: **{len(data)}** rows')
                    data = pd.DataFrame(data)
                    data.columns = ['Timestamp', ds_name]
                    data['Timestamp'] = data['Timestamp'].apply(lambda x: x.astimezone(local_tz))
                    data = data.sort_values('Timestamp').reset_index(drop=True)
                    if st.checkbox(f'View {ds_name} in DB'):
                        st.write(ds_series[ds_series['Timestamp'].isin(data['Timestamp'])])
                    st.write(f'--> Drop these data of **{ds_name}** from uploaded data below before import')
                    ds_series = ds_series[~ds_series['Timestamp'].isin(data['Timestamp'])]
                    # st.write(ds_series)
                    if not ds_series.empty:
                        if df_new.empty: df_new = ds_series
                        else:
                            df_new = df_new.merge(ds_series, on='Timestamp')
                        if st.checkbox(f'View new {ds_name} to import'):
                            st.write(ds_series)
                    else:
                        st.write(f'There is no new data from **{ds_name}** to import')

                else:
                    st.write(f'**{ds_name}**: not found')
                st.write('----------------------')

            if isinstance(df_new,pd.DataFrame) and (df_new.empty):
                st.write('**>>>There is no new data to upload.**')
                return
            
            if df_new is not None:
                df_new['Timestamp'] = df_new['Timestamp'].apply(lambda x: x.isoformat(timespec='seconds'))
                df = df[df['Timestamp'].isin(df_new['Timestamp'])]
            df = df.dropna(how='all', axis=1)
            if st.checkbox(f'View the final data will be imported', True):
                st.write(f'Size: {df.shape[0]} rows')
                st.write(df)
            #################################
            if st.button('Upload data'):
                start_time = time.time()
                tz = pytz.timezone('Europe/Berlin')
                berlin_now = datetime.now(tz).replace(microsecond=0).isoformat(timespec='seconds')
                df['resultTime'] = berlin_now

                if 'Timestamp' in mapping:
                    for ds_name, col in mapping.items():
                        if col is None:
                            st.write(f'>>> {ds_name} does not have a match -> Skip {ds_name}')
                        if ds_name == 'Timestamp': continue
                        df_remove_na = df[df[col].notna()]
                        if df_remove_na.empty:
                            st.write(f'No data to upload from {ds_name}')
                            continue

                        ds_id = [i['@iot.id'] for i in filtered_ds if i['name']==ds_name][0]
                        d = dict()
                        d["Datastream"] =  { "@iot.id": ds_id}
                        d["components"] = ["result", "phenomenonTime", "resultTime"]
                        
                        d["dataArray"] = df_remove_na[[col, 'Timestamp', 'resultTime']].values.tolist()

                        try:
                            st.write(f'Uploading {ds_name}. Please wait and do not close the window. Do not refresh the page...')
                            if post_item(CREATE_OBSERVATIONS_URL, [d], json_data=True, 
                                        access_token=access_token):
                                st.write(f'Done uploading {col}')
                        except:
                            st.write(f'{d} is not valid. Skipped.')
                else:
                    st.write('There is no Timestamp in the data. Please check.')
                st.write(f'Upload Time: {round((time.time()-start_time)/60, 1)} mins')
    st.sidebar.write('-----------')
    return
