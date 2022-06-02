import glob
import imp
# import json
import pandas as pd
import streamlit as st
# from shapely.geometry import Point
# from shapely.geometry.polygon import Polygon


def labels_in_map(df):
    img_loc_count = 0
    for id in list(df.dropna()['images']):
        images = id.split(' ')
        img_loc_count += len(images)

    st.map(df)
    st.write('Landmark IDs: **' + str(df.dropna().shape[0]) + '**')
    st.write('Total images: **' + str(img_loc_count) + '**')

def polygon_country_check(row):
    polygon_country_check.counter +=1
    print(polygon_country_check.counter) 
    if(row['country']=='FR'):
        k=0
    point = Point(row['lon'], row['lat'])
    polygons_paths = glob.glob(root+ '/polygons/*.json')
    for country in polygons_paths:
        c = country.split('.json')[0].split('/')[-1]
        country_polygons = json.load(open(country))
        for feat in country_polygons['features']:
            coords = feat['geometry']['coordinates']
            for crd in coords:
                polygon_points = [tuple(x) for x in crd]
                polygon = Polygon(polygon_points)
                if polygon.contains(point):
                    return c
    polygon_country_check.outliers += 1
    return None

root = './files'

df_train_clean = pd.read_csv(root + '/train_clean.csv') # columns: [ 'landmark_id', 'images' ] -- 81313 ids
df_labelmap_loc_gld = pd.read_csv(root + '/train_label_to_category_loc.csv')

df_labelmap_loc_gld = df_labelmap_loc_gld.merge(df_train_clean, on='landmark_id') #keep only labels for cleaned train-set
df_labelmap_loc_gld['lon'] = df_labelmap_loc_gld['lon'].apply( lambda x: None if(x=='None') else float(x))
df_labelmap_loc_gld['lat'] = df_labelmap_loc_gld['lat'].apply( lambda x: float(x) if(x!='None') else None)

country_json_paths = glob.glob(root + '/landmarks_per_country/*.json')
df_country = []
for country in country_json_paths:
    df_country_temp = pd.read_json(country)
    df_country_temp['country'] = country.split('/')[-1][:2]
    df_country.append(df_country_temp)
    
df_countries = pd.concat(df_country, ignore_index=True).rename(columns={'id': 'landmark_id'})
df_final = df_countries.merge(df_labelmap_loc_gld, on='landmark_id')

# country cleaning using polygons
# df_final_2 = df_final
# polygon_country_check.outliers = 0
# polygon_country_check.counter = 0
# df_final_2['country2']=df_final.apply(polygon_country_check, axis=1)
# print('Outliers detected: ', polygon_country_check.outliers)
# df_final_2.to_csv('df_final.csv', index=False)
df_final_2 = pd.read_csv(root + '/df_final.csv')

st.title("Landmarks in map")
filter = st.selectbox("Landmarks' filter", ('A. Cleaned GLDv2', 'B. Countries of interest', 'C. Countries of interest - cleaned'))
if 'A. ' in filter:
    st.subheader("Google Landmark Dataset v2 (cleaned) landmarks ")
    labels_in_map(df_labelmap_loc_gld.dropna())
elif 'B. ' in filter:
    st.subheader("Google Landmark Dataset v2 (cleaned) landmarks for countries: **Greece, France, Spain, Italy, Poland, Slovenia**")
    labels_in_map(df_final.dropna())
elif 'C. ' in filter:
    st.subheader("Google Landmark Dataset v2 (cleaned) landmarks for countries: **Greece, France, Spain, Italy, Poland, Slovenia** - Outliers cleaned")
    labels_in_map(df_final_2.dropna())