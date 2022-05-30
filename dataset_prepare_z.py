import glob
import pandas as pd
import streamlit as st

def labels_in_map(df):
    st.title("Landmarks in map")
    st.subheader("Google Landmark Dataset v2 landmarks for countries: **Greece, France, Spain, Italy, Poland, Slovenia**")
    img_loc_count = 0
    for id in list(df.dropna()['images']):
        images = id.split(' ')
        img_loc_count += len(images)

    st.map(df)
    st.write('Landmark IDs with location: **' + str(df.dropna().shape[0]) + '**')
    st.write('Total images with location: **' + str(img_loc_count) + '**')
    st.write("*Note: Outliers exist due to either a) incorrect coordinates from commons.wikimedia source url or b) landmark was misplaced in one of countries' json files.*")

root = './files'

df_train_clean = pd.read_csv(root + '/train_clean.csv') # columns: [ 'landmark_id', 'images' ] -- 81313 ids
df_labelmap_loc_gld = pd.read_csv(root + '/train_label_to_category_loc.csv')
df_merged = df_labelmap_loc_gld.merge(df_train_clean, on='landmark_id') #keep only labels for cleaned train-set
df_merged['lon'] = df_merged['lon'].apply( lambda x: None if(x=='None') else float(x))
df_merged['lat'] = df_merged['lat'].apply( lambda x: float(x) if(x!='None') else None)

country_json_paths = glob.glob(root + '/*.json')
df_country = []
for country in country_json_paths:
    df_country.append(pd.read_json(country))
    
df_countries = pd.concat(df_country, ignore_index=True).rename(columns={'id': 'landmark_id'})
df_final = df_countries.merge(df_merged, on='landmark_id')

labels_in_map(df_final.dropna())