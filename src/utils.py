import pandas as pd
import json


def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    pd.read_csv(csv_url)
    return pd.read_csv(csv_url)


def get_json_list(df, df_column_name="JSON"):
    json_list = list()
    for j_str in df[df_column_name]:
        j = json.loads(j_str)
        json_list.append(j)
    return json_list


def format_map_df(df, keep_keys, df_column_name="JSON"):
    json_list = list()
    for j_str in df[df_column_name]:
        j = json.loads(j_str)
        subset = {key: j[key] for key in keep_keys}
        json_list.append(subset)
    df = pd.DataFrame(json_list)
    return df


if __name__ == "__main__":
    public_gsheets_url = 'https://docs.google.com/spreadsheets/d/1Cbz3zpCBgIcmrnfPTnCukQRy5UFCHuykJiiOq4IcBHs/edit#gid=0'
    ld = load_data(sheets_url=public_gsheets_url)
    #jl = get_json_list(df=ld, df_column_name="JSON")
    map_df = format_map_df(df=ld, keep_keys=['id', 'type', 'ad_id', 'coordinates.lon', 'coordinates.lat', 'location'], df_column_name="JSON")
    print(9)


