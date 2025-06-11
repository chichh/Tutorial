
#COMMENT FOR TUTORIAL
import pandas as pd
import matplotlib.pyplot as plt
import folium
import webbrowser
from mapbox import Geocoder
import geopandas as gpd
from shapely.geometry import Point
import os
MAPBOX_TOKEN = "pk.eyJ1IjoibXNraG91ZWlyeSIsImEiOiJjbWJrdGIzYmQwdzBkMnJweTIzcnliaGtiIn0.KPXgJ_4WTDtAAWH7iXwecQ"
geocoder=Geocoder(access_token=MAPBOX_TOKEN)
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
        xlsx_file=pd.ExcelFile(xlsx_file)
        #df_raw_xlsx=pd.read_excel(file_path)
        df_raw_xlsx=pd.concat([xlsx_file.parse(sheet_name) for sheet_name in xlsx_file.sheet_names],axis=1)
        PHcountsall=df_raw_xlsx.iloc[12:16,1:17].sum()
        PHcountsmicro=df_raw_xlsx.iloc[12:16,35:51].sum()
        df_raw_xlsx.loc[len(df_raw_xlsx)]=PHcountsall
        df_raw_xlsx.loc[len(df_raw_xlsx)]=PHcountsmicro
        xlsx_dataframes[xlsx_file]=df_raw_xlsx
        print(f"Loaded {xlsx_file} in raw dataframe")

#CSV MAPPING
df1 = pd.DataFrame(columns=['Street 1', 'Street 2', 'Address', 'Int_ID', 'Collection_Date','Latitude','Longitude','PH NB Left Volume', 'PH NB Through Volume', 'PH NB Right Volume','PH SB Left Volume', 'PH SB Through Volume', 'PH SB Right Volume','PH EB Left Volume', 'PH EB Through Volume', 'PH EB Right Volume','PH WB Left Volume', 'PH WB Through Volume', 'PH WB Right Volume', 'PH S Pedestrians','PH N Pedestrians','PH W Pedestrians','PH E Pedestrians','PH NB Left Micromobility', 'PH NB Through Micromobility', 'PH NB Right Micromobility','PH SB Left Micromobility', 'PH SB Through Micromobility', 'PH SB Right Micromobility','PH EB Left Micromobility', 'PH EB Through Micromobility', 'PH EB Right Micromobility','PH WB Left Micromobility', 'PH WB Through Micromobility', 'PH WB Right Micromobility'])
df1.loc[0,'Street 1']=df_raw_csv.iloc[2,1]
df1.loc[0,'Street 2']=df_raw_csv.iloc[2,2]
df1.loc[0,'Address']= df1.loc[0,'Street 1'].split('-')[1] + " and "+df1.loc[0,'Street 2']+", Washington DC"
df1.loc[0,'Int_ID']='N/A'
df1.loc[0,'Collection_Date']=df_raw_xlsx.iloc[0,2]
df1.loc[0,'Latitude']=df_raw_csv.iloc[8,1]
df1.loc[0,'Longitude']=df_raw_csv.iloc[8,2]
df1.iloc[0,7:19]=df_raw_csv.iloc[17,1:13]
df1.iloc[0,19:23]=df_raw_csv.iloc[26,1:5]
df1.iloc[0,23:35]=df_raw_csv.iloc[30,1:13]


df2 = pd.DataFrame(columns=['Street 1', 'Street 2','Address', 'Int_ID', 'Collection_Date','Latitude','Longitude','PH NB Left Volume', 'PH NB Through Volume', 'PH NB Right Volume','PH SB Left Volume', 'PH SB Through Volume', 'PH SB Right Volume','PH EB Left Volume', 'PH EB Through Volume', 'PH EB Right Volume','PH WB Left Volume', 'PH WB Through Volume', 'PH WB Right Volume', 'PH S Pedestrians','PH N Pedestrians','PH W Pedestrians','PH E Pedestrians','PH NB Left Micromobility', 'PH NB Through Micromobility', 'PH NB Right Micromobility','PH SB Left Micromobility', 'PH SB Through Micromobility', 'PH SB Right Micromobility','PH EB Left Micromobility', 'PH EB Through Micromobility', 'PH EB Right Micromobility','PH WB Left Micromobility', 'PH WB Through Micromobility', 'PH WB Right Micromobility'])
df2.loc[0,'Street 1']=df_raw_xlsx.iloc[7,1]
df2.loc[0,'Street 2']=df_raw_xlsx.iloc[7,5]
df2.loc[0,'Int_ID']=df_raw_csv.iloc[4,1]
df2.loc[0,'Collection_Date']=df_raw_csv.iloc[6,1]
df2.loc[0, 'Address']=df2.loc[0,'Street 1'].split('\n')[0]+' and '+df2.loc[0,'Street 2'].split('\n')[0]+', Washington DC'
#APPLY PREV LOGIC
response=geocoder.forward(df2.loc[0, 'Address'],limit=1,country=['us'])
result=response.geojson()
features=result['features']
coords=features[0]['geometry']['coordinates']
df2.loc[0,'Longitude']=coords[0]
df2.loc[0,'Latitude']=coords[1]
#df2.loc[0,'Latitude']=df_raw_csv.iloc[8,1]
#df2.loc[0,'Longitude']=df_raw_csv.iloc[8,2]
df2.iloc[0,7:10]=df_raw_xlsx.iloc[33,9:12]
df2.iloc[0,10:13]=df_raw_xlsx.iloc[33,1:4]
df2.iloc[0,13:16]=df_raw_xlsx.iloc[33,13:16]
df2.iloc[0,16:19]=df_raw_xlsx.iloc[33,5:8]
df2.iloc[0,19]=df_raw_xlsx.iloc[33,12]
df2.iloc[0,20]=df_raw_xlsx.iloc[33,4]
df2.iloc[0,21]=df_raw_xlsx.iloc[33,16]
df2.iloc[0,22]=df_raw_xlsx.iloc[33,8]
df2.iloc[0,23:26]=df_raw_xlsx.iloc[34,9:12]
df2.iloc[0,26:29]=df_raw_xlsx.iloc[34,1:4]
df2.iloc[0,29:32]=df_raw_xlsx.iloc[34,13:16]
df2.iloc[0,32:35]=df_raw_xlsx.iloc[34,5:8]

df=pd.concat([df1,df2],ignore_index=True)

#trialdata={'Longitude': [-77.027508], 'Latitude': [38.928703], 'EB':[56], 'ID':[123]}
#df_valid= pd.DataFrame(data=trialdata)
geometry=[Point(xy) for xy in zip(df['Longitude'],df['Latitude'])]
gdf=gpd.GeoDataFrame(df,geometry=geometry)
gdf.set_crs(epsg=4326,inplace=True)
gdf.to_file("trialpointsfromdf.shp")