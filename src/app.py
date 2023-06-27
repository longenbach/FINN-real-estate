# streamlit_app.py

import pandas as pd
import streamlit as st
import json
import leafmap.foliumap as leafmap

st.set_page_config(layout='wide')
# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url, encoding='utf-8')


@st.cache_data(ttl=600)
def options_dict(df, option_keys: list, df_column_name="JSON"):
    option_dict = {key: [] for key in option_keys}
    for j_str in df[df_column_name]:
        j = json.loads(j_str)
        for key in option_keys:
            if key in j:
                option_i = j[key]
                if option_i not in option_dict[key]:
                    option_dict[key].append(option_i)
    return option_dict


@st.cache_data(ttl=600)
def format_map_df(df, keep_keys, df_column_name="JSON"):
    json_list = list()
    for j_str in df[df_column_name]:
        j = json.loads(j_str)
        # subset = {key: j[key] for key in keep_keys}
        subset = {key: j[key] for key in keep_keys if key in j}
        json_list.append(subset)
    df = pd.DataFrame(json_list)
    return df


ld_df = load_data(st.secrets["google_sheets"]["public_gsheets_url"])
# st.write(df)
k_keys = ['id', 'type', 'ad_id', 'coordinates.lon', 'coordinates.lat', 'location', 'ad_link', 'price']
map_df = format_map_df(df=ld_df, keep_keys=k_keys)# .head(1071)
map_df['location'] = map_df['location'].str.replace("`", "'")  # stupid backtick
map_df.rename(columns={'coordinates.lon': 'lon', 'coordinates.lat': 'lat'}, inplace=True)
st.write(map_df)
# st.map(map_df)
print(map_df.shape)
print(map_df.tail(3))
# https://github.com/opengeos/streamlit-geospatial/blob/master/pages/5_%F0%9F%93%8D_Marker_Cluster.py
m = leafmap.Map(center=[59.9, 10.8], zoom=11)
m.add_points_from_xy(
    map_df,
    x="lon",
    y="lat",
    #color_column='region',
    #icon_names=['gear', 'map', 'leaf', 'globe'],
    spin=True,
    add_legend=True,
)

m.to_streamlit(height=700)


st.write(options_dict(df=ld_df, option_keys=['type', 'local_area_name']))



options = ['Option 1', 'Option 2', 'Option 3']

selected_options = []

for option in options:
    if st.checkbox(option):
        selected_options.append(option)

st.write('You selected:', ', '.join(selected_options))
# Print results.
# for row in df.itertuples():
#    st.write(f"{row.name} has a :{row.pet}:")
