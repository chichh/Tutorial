
#COMMENT FOR TUTORIAL
import pandas as pd
import matplotlib.pyplot as plt
import folium
import webbrowser
from mapbox import Geocoder
import geopandas as gpd
from shapely.geometry import Point
import os

cd=os.getcwd()
print("Scanning Directory")
all_files=os.listdir(cd)
csv_files=[f for f in all_files if f.endswith('.csv')]
xlsx_files=[f for f in all_files if f.endswith('.xlsx')]
csv_dataframes={}
xlsx_dataframes={}
if csv_files:
    print("Found CSV")
    for csv_file in csv_files:
        file_path=os.path.join(cd,csv_file)
        df_raw_csv=pd.read_csv(file_path, encoding='cp1252')
        csv_dataframes[csv_file]=df_raw_csv
        print(f"Loaded {csv_file} in raw dataframe")
        
if xlsx_files:
    print("Found XLSX")
    for xlsx_file in xlsx_files:
        file_path=os.path.join(cd,xlsx_file)
        df_raw_xlsx=pd.read_excel(file_path)
        xlsx_dataframes[xlsx_file]=df_raw_xlsx
        print(f"Loaded {xlsx_file} in raw dataframe") 

df = pd.DataFrame(columns=['Int_Name','Int_ID', 'Collection_Date','Latitude','Longitude','Approach','PH_Volume','PH_Vehicle','PH_Micromobility','PH_HeavyVehicle'])

#IF CSV SET ELEMENTS
# IF XLSX SET ELEMENTS




trialdata={'Longitude': [-77.027508], 'Latitude': [38.928703], 'EB':[56], 'ID':[123]}
df_valid= pd.DataFrame(data=trialdata)
geometry=[Point(xy) for xy in zip(df_valid['Longitude'],df_valid['Latitude'])]
gdf=gpd.GeoDataFrame(df_valid,geometry=geometry)
gdf.set_crs(epsg=4326,inplace=True)
#gdf.to_file("trialpointsfromexcel.shp")

'''

df=pd.read_csv('AddressIntersection.csv')
df['Latitude'] = None
df['Longitude'] = None
MAPBOX_TOKEN = "pk.eyJ1IjoibXNraG91ZWlyeSIsImEiOiJjbWJrdGIzYmQwdzBkMnJweTIzcnliaGtiIn0.KPXgJ_4WTDtAAWH7iXwecQ"
geocoder=Geocoder(access_token=MAPBOX_TOKEN)

def get_lat_lon(address):
    location=geocode(address)
    return(pd.Series([location.latitude,location.longitude]))

for idx, row in df.iterrows():
    address=row['Address']
    response=geocoder.forward(address,limit=1,country=['us'])
    result=response.geojson()
    features=result['features']
    if features:
        coords=features[0]['geometry']['coordinates']
        df.at[idx,'Longitude']=coords[0]
        df.at[idx,'Latitude']=coords[1]
    else:
        df.at[idx,'Latitude']='error'
        df.at[idx,'Longitude']='error'
    if result:
       print("Intersection") 
    else:
        df.at[idx,'Latitude']='error'
        df.at[idx,'Longitude']='error'        
#df[['Latitude','Longitude']]=df['Address'].apply(get_lat_lon)
print(df)

df_valid=df[(df['Latitude']!='error') & (df['Longitude']!='error') & (df['Latitude'].notnull()) & (df['Longitude'].notnull())]
m=folium.Map(location=[df_valid['Latitude'].mean(),df_valid['Longitude'].mean()])
for i, row in df_valid.iterrows():
    folium.Marker(location=[row['Latitude'], row['Longitude']], popup=row['Address'],).add_to(m)
m.save("map2.html")
webbrowser.open("map2.html")

geometry=[Point(xy) for xy in zip(df_valid['Longitude'],df_valid['Latitude'])]
gdf=gpd.GeoDataFrame(df_valid,geometry=geometry)
gdf.set_crs(epsg=4326,inplace=True)
gdf.to_file("trialpoints.shp")

'''