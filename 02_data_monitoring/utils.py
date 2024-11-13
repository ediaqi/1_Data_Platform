from constants import *
from request_DB import retrieve_data
from frost_funcs import get_ds

import plotly.express as px


def view_all():
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:

        query = '''
        SELECT "ID", "NAME"
            FROM public."PROJECTS";
        '''
        data = retrieve_data(query)
        if data:
            data = pd.DataFrame(data)
            data.columns = ['#', 'Name']
            st.subheader('Projects')
            st.write(f'### {data.shape[0]}')
            data.set_index('#', inplace=True)
            data['Code'] = PRJ_CODES
            st.table(data)
        else:
            st.write('There is something wrong. Please check the DB connection.')
    
    with col2:
        st.subheader('Things')
        query = '''
        SELECT "NAME", "ID"
	        FROM public."THINGS";
        '''
        data = retrieve_data(query)
        if data:
            data = pd.DataFrame(data)
            data.columns = ['Name', 'ID']
            st.write(f'### {data.shape[0]}')
            data['Project'] = data['ID'].str.split('.').str[1]
            df = data['Project'].value_counts().sort_values().reset_index()

            fig = px.pie(df, values='count', names='Project', hole=0.5)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update(layout_showlegend=False)
            fig.update_layout(

                title={'text': '#Things in each Project',
                'y':0.95,
                'x':0.45,
                'xanchor': 'center',
                'yanchor': 'top' })
            st.plotly_chart(fig)
        else:
            st.write('There is something wrong. Please check the DB connection.')
    
    with col3:
        st.subheader('Locations')
        query = '''
            SELECT "NAME", "ID"
                FROM public."LOCATIONS";'''
        data = retrieve_data(query)
        if data:
            data = pd.DataFrame(data)
            data.columns = ['Name', 'ID']
            st.write(f'### {data.shape[0]}')
            data['Project'] = data['ID'].str.split('.').str[1]
            df = data['Project'].value_counts().sort_values().reset_index()

            fig = px.pie(df, values='count', names='Project', hole=0.5,
                        #  title='#Locations in each Project'
                         )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update(layout_showlegend=False)
            fig.update_layout(
                title={
                    'text': '#Locations in each Project',
                'y':0.95,
                'x':0.45,
                'xanchor': 'center',
                'yanchor': 'top' })
            st.plotly_chart(fig)
    
    with col4:
        st.subheader('Sensors')
        query = '''
            SELECT COUNT (*)
                FROM public."SENSORS";
            '''
        data = retrieve_data(query)
        if data:
            st.write(f'### {data[0][0]}')
    
    st.write('------------------------------')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Datastreams')
        query = '''
            SELECT "NAME","SENSOR_ID", "THING_ID"
                FROM public."DATASTREAMS";'''
        data = retrieve_data(query)
        if data:
            data = pd.DataFrame(data)
            data.columns = ['Name', 'Sensor_ID', 'Thing_ID']
            st.subheader(data.shape[0])
            data['Project'] = data['Thing_ID'].str.split('.').str[1]
            df = data['Project'].value_counts().sort_values()#.reset_index()
            fig = px.bar(df, orientation='h', title='#Datastream in each Project',
                        text_auto=True, height=350)
            fig.update(layout_showlegend=False)

            st.plotly_chart(fig)
            
        else:
            st.write('There is something wrong. Please check the DB connection.')

    with col2:
        df = data[['Project', 'Sensor_ID']].value_counts().sort_values().reset_index()

        fig = px.bar(df, x='count', y='Sensor_ID', orientation='h', 
                     title='#Datastream in each Project and Sensor',
                    text_auto=True, color='Project', height=600)
        st.plotly_chart(fig)

    #####################################
    st.write('------------------------------')
    st.subheader('ObservedProperties and unitOfMeasurement')
    col1, col2 = st.columns([1, 3])
    with col1:
        query = f'''
            SELECT COUNT (*)
                FROM public."OBS_PROPERTIES"
        '''
        data = retrieve_data(query)
        if data:
            st.write(f'#### #ObservedProperties: {data[0][0]}')
        ## get #OBS_PROPERTIES each project
        query = '''
            SELECT "OBS_PROPERTY_ID", "THING_ID", "UNIT_NAME", "UNIT_SYMBOL"
                FROM public."DATASTREAMS"
            '''
        data = retrieve_data(query)
        if data:
            data = pd.DataFrame(data)
            data.columns = ["OBS_PROPERTY_ID", "THING_ID", "UNIT_NAME", "UNIT_SYMBOL"]
            data['Project'] = data['THING_ID'].str.split('.').str[1]
            data.drop('THING_ID', axis=1, inplace=True)
            data = data.drop_duplicates()
            df = data.groupby('Project')['OBS_PROPERTY_ID'].count().sort_values()
            fig = px.bar(df, orientation='h', title='#ObservedProperties in each Project',
                            text_auto=True, height=350)
            fig.update(layout_showlegend=False)
            st.plotly_chart(fig)

    ## JOIN OBS_PROPERTIES with DATASTREAMS
    with col2:
        st.subheader('Details')
        query = '''
            SELECT "NAME", "DEFINITION", "DESCRIPTION", "ID"
            FROM public."OBS_PROPERTIES";
        '''
        props = retrieve_data(query)
        if props:
            props = pd.DataFrame(props)
            props.columns = ["NAME", "DEFINITION", "DESCRIPTION", "OBS_PROPERTY_ID"]
            df = data.merge(props, how='right')#.drop('Project', axis=1)
            # st.write(df)
            df = df[['OBS_PROPERTY_ID', 'NAME', 'Project', 'DESCRIPTION', 'UNIT_NAME', 'UNIT_SYMBOL', 'DEFINITION']
                    ].drop_duplicates(subset=['OBS_PROPERTY_ID', 'NAME', 'DESCRIPTION', 'UNIT_NAME', 'UNIT_SYMBOL', 'DEFINITION']).sort_values(
                        ['OBS_PROPERTY_ID', 'Project']).reset_index(drop=True)
            st.write(df)


def _get_count_item(table, item):
    query = f'''
            SELECT COUNT(*)
                FROM public."{table}"
                WHERE "ID" LIKE '%{item}%'
            '''
    data = retrieve_data(query)
    if data:
        st.write(f'### {data[0][0]}')
    else:
        st.write('Please check the connection.')


def _view_heatmap_obs(query1, query2, height=900):

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('1. Observations per Day')
    ds_names = retrieve_data(query2)
    if ds_names:
        ds_names = pd.DataFrame(ds_names)
        ds_names.columns = ['Name', 'ID']
        ds_names['ID'] = ds_names['ID'].astype(str)
        ds_names = ds_names.set_index('ID')
        ds_names = ds_names['Name'].to_dict()

    obs = retrieve_data(query1)
    if obs:
        
        obs = pd.DataFrame(obs)
        obs.columns = ['Date', 'Datastream_ID', 'Count']
        df = obs.set_index(['Date', 'Datastream_ID']).unstack()
        df.columns = df.columns.droplevel()        
        df = df.T
        df.index = df.index.astype(str)
        df = df.reset_index()
        df['Datastream_ID'] = df['Datastream_ID'].apply(lambda x: ds_names[x])
        df = df.set_index('Datastream_ID')
        with col2:
            st.write(f'### #Datastream has Observations: {obs["Datastream_ID"].nunique()}')

        fig = px.imshow(df, x=df.columns, y=df.index, height=height)
        fig.update_xaxes(side="top")
        st.plotly_chart(fig)
    else:
        st.write('No data found in the Database.')
    return obs


def _view_datastreams_count(CODE, height=700):
    st.subheader('2. Datastreams')
    query1 = f'''
        SELECT COUNT (*)
            FROM public."DATASTREAMS"
            WHERE "THING_ID" LIKE '%{CODE}%'
    '''
    data = retrieve_data(query1)
    if data:
        st.write(f'#### Total: {data[0][0]}')
    ###########
    query2 = f'''
        SELECT d."NAME" AS datastream_name, d."THING_ID", d."SENSOR_ID", s."NAME" AS sensor_name
            FROM public."DATASTREAMS" d
            JOIN public."SENSORS" s ON d."SENSOR_ID" = s."ID"
            WHERE d."THING_ID" LIKE '%{CODE}%'
        '''
    data = retrieve_data(query2)
    if data:
        data = pd.DataFrame(data)
        data.columns = ['Name', 'Thing_ID', 'Sensor_ID', 'Sensor_Name']
        data['ID_Name'] = data['Sensor_ID'] + ' - ' + data['Sensor_Name']
        data.drop(['Sensor_ID', 'Sensor_Name'], axis=1, inplace=True)
        df = data.groupby(['Thing_ID', 'ID_Name']).count().reset_index()
        df = df.rename(columns={'Name': 'Count'})
        df = df.sort_values(['Thing_ID'], ascending=False)
        df = df.rename(columns={'ID_Name': 'Name'})
        fig = px.bar(df, x='Count', y='Thing_ID', orientation='h', 
                        title='#Datastream in each Thing and Sensor',
                text_auto=True, color='Name', height=height)
        st.plotly_chart(fig)


def view_ferrara():

    col1, col2, _ = st.columns([1, 1, 3])
    CODE = 'FE'
    with col1:
        st.subheader('Things')
        _get_count_item('THINGS', CODE)
            
    with col2:
        st.subheader('Locations')
        _get_count_item('LOCATIONS', CODE)

    query1 = f'''
        SELECT DATE("PHENOMENON_TIME_START"), "DATASTREAM_ID", COUNT (*)
        FROM 
            public."OBSERVATIONS"
        WHERE "DATASTREAM_ID" IN {tuple(FE_LIST)}
        GROUP BY DATE("PHENOMENON_TIME_START"), "DATASTREAM_ID"
        '''
    query2 = f'''
        SELECT "NAME","ID"
            FROM public."DATASTREAMS"
            WHERE "ID" IN {tuple(FE_LIST)}
        '''
    obs = _view_heatmap_obs(query1, query2)

    #######################
    st.write('---------------')
    col1, _ = st.columns(2)
    with col1:
        _view_datastreams_count(CODE)



def view_seville():

    CODE = 'SV'
    col1, col2, _ = st.columns([1, 1, 3])
    with col1:
        st.subheader('Things')
        _get_count_item('THINGS', 'SV')
            
    with col2:
        st.subheader('Locations')
        _get_count_item('LOCATIONS', 'SV')

    query1 = f'''
        SELECT DATE("PHENOMENON_TIME_START"), "DATASTREAM_ID", COUNT (*)
        FROM 
            public."OBSERVATIONS"
        WHERE "DATASTREAM_ID" IN {tuple(SV_LIST)}
        GROUP BY DATE("PHENOMENON_TIME_START"), "DATASTREAM_ID"
        '''
    query2 = f'''
        SELECT "NAME","ID"
        FROM public."DATASTREAMS"
        WHERE "ID" IN {tuple(SV_LIST)}
        '''
    obs = _view_heatmap_obs(query1, query2, 700)

    ############
    # DATASTREAMS
    st.write('---------------')
    col1, _ = st.columns(2)
    with col1:
        _view_datastreams_count(CODE, height=550)


def view_estonia():

    CODE = 'EE'
    col1, col2, _ = st.columns([1, 1, 3])
    with col1:
        st.subheader('Things')
        _get_count_item('THINGS', 'EE')
            
    with col2:
        st.subheader('Locations')
        _get_count_item('LOCATIONS', 'EE')

    query1 = f'''
        SELECT DATE("PHENOMENON_TIME_START"), "DATASTREAM_ID", COUNT (*)
        FROM 
            public."OBSERVATIONS"
        WHERE "DATASTREAM_ID" IN {tuple(EE_LIST)}
        GROUP BY DATE("PHENOMENON_TIME_START"), "DATASTREAM_ID"
        '''
    query2 = f'''
        SELECT "NAME","ID"
        FROM public."DATASTREAMS"
        WHERE "ID" IN {tuple(EE_LIST)}
        '''
    obs = _view_heatmap_obs(query1, query2, 700)

    st.write('---------------')
    col1, _ = st.columns(2)
    with col1:
        _view_datastreams_count(CODE, height=1100)


def view_zagreb():
    CODE = 'ZG'

    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        st.subheader('Things')
        _get_count_item('THINGS', CODE)
            
    with col2:
        st.subheader('Locations')
        _get_count_item('LOCATIONS', CODE)

    query1 = f'''
        SELECT DATE("PHENOMENON_TIME_START"), "DATASTREAM_ID", COUNT (*)
        FROM 
            public."OBSERVATIONS"
        WHERE "DATASTREAM_ID" IN {tuple(ZG_LIST)}
        GROUP BY DATE("PHENOMENON_TIME_START"), "DATASTREAM_ID"
        '''
    query2 = f'''
        SELECT "NAME","ID"
        FROM public."DATASTREAMS"
        WHERE "ID" IN {tuple(ZG_LIST)}
        '''
    obs = _view_heatmap_obs(query1, query2, 700)
    #############################
    st.write('---------------')
    col1, _ = st.columns(2)    
    with col1:
        _view_datastreams_count(CODE, height=1200)


def view_vilnius():
    CODE = 'VL'
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        st.subheader('Things')
        _get_count_item('THINGS', CODE)
            
    with col2:
        st.subheader('Locations')
        _get_count_item('LOCATIONS', CODE)

    query1 = f'''
        SELECT DATE("PHENOMENON_TIME_START"), "DATASTREAM_ID", COUNT (*)
        FROM 
            public."OBSERVATIONS"
        WHERE "DATASTREAM_ID" IN {tuple(VL_LIST)}
        GROUP BY DATE("PHENOMENON_TIME_START"), "DATASTREAM_ID"
        '''
    query2 = f'''
        SELECT "NAME","ID"
        FROM public."DATASTREAMS"
        WHERE "ID" IN {tuple(VL_LIST)}
        '''
    obs = _view_heatmap_obs(query1, query2, 700)
    #############################
    st.write('---------------')
    col1, _ = st.columns(2)
    with col1:
        _view_datastreams_count(CODE, height=650)


def check_dups(access_token=None):
    st.write('Retrieving data... This takes up to a minute (or more). Please wait....')
    ds = get_ds(access_token)
    ds_ids = []
    if ds:
        ds_ids = [i['@iot.id'] for i in ds['value']]
        ds_names = [i['name'] for i in ds['value']]
        df_names = pd.DataFrame(ds_names)
        df_names.columns = ['NAME']
        df_names['value'] = 0
        df_names.set_index('NAME', inplace=True)
    
    query = f'''
        SELECT "DATASTREAM_ID", COUNT (*)
        FROM public."OBSERVATIONS"
        WHERE "DATASTREAM_ID" IN {tuple(ds_ids)}
        GROUP BY "DATASTREAM_ID"
'''
    data = retrieve_data(query)
    if data:
        data = pd.DataFrame(data)
        data.columns = ['Datastream_ID', '#Total']
        data = data.set_index('Datastream_ID')

    
    query = f'''
    SELECT "DATASTREAM_ID", COUNT(DISTINCT "PHENOMENON_TIME_START")
    FROM public."OBSERVATIONS"
    WHERE "DATASTREAM_ID" IN {tuple(ds_ids)}
    GROUP BY "DATASTREAM_ID"
'''
    data2 = retrieve_data(query)

    if data2:
        data2 = pd.DataFrame(data2)
        data2.columns = ['Datastream_ID', '#Deduplicated']
        data2 = data2.set_index('Datastream_ID')
        if data is not None:
            df = data.join(data2)
            
            ds_id_name = pd.read_csv(DS_ID_NAME_FILE).set_index('ID')
            df = df.join(ds_id_name[['NAME']], how='left')
            df = df.set_index('NAME', drop=True)
            df = df.join(df_names, how='right').drop('value', axis=1)
            df = df.fillna(0)
            df_display = df.copy()
            df_display['Diff'] = df['#Total'] - df['#Deduplicated']
            st.write(df_display)
            # warning
            df_diff = df_display[df_display['#Total']!=df_display['#Deduplicated']]
            if not df_diff.empty:
                st.write(f'#### Duplicates detected')
                st.write(df_diff)
            else:
                st.write(f'#### No Duplicates detected')
            fig = px.bar(df, #orientation='h',
                         title='#Observation in Database',
                        text_auto=True, height=850
                        )

            fig.update_layout(barmode='group')
            st.plotly_chart(fig)
