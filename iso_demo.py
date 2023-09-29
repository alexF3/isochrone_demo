import streamlit as st
import requests
import folium
from geopy.geocoders import MapBox
from folium.plugins import HeatMap
import folium
from streamlit_folium import st_folium
import geopandas as gpd

stations = gpd.read_file('data/Amtrak_Stations.geojson')
stations = stations[stations.StnType=='TRAIN']
stations['long'] =  stations.geometry.x
stations['lat'] = stations.geometry.y

# Mapbox API keys
MAPBOX_API_KEY = st.secrets[MAPBOX_API_KEY]
GEOCODING_API_KEY = st.secrets[GEOCODING_API_KEY]

# Mapbox Geocoding API
GEOCODING_API_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places/"

# Mapbox Isochrone API
ISOCHRONE_API_URL = "https://api.mapbox.com/isochrone/v1/mapbox/driving/"

# Initialize Mapbox geocoder
geolocator = MapBox(api_key=GEOCODING_API_KEY)

tab1, tab2 = st.tabs(["Demo", "About"])

with tab1:

    st.title("Where Are the Train Stations Near You?")
    st.image("data/train.jpg")


    # User input for ZIP code
    zip_code = st.text_input("Enter a City, Town, or ZIP Code:")

    if zip_code:

        # Geocode the ZIP code to get its centroid
        location = geolocator.geocode(f"{zip_code}, USA")


        coordinates = location.raw["center"]
        center = [float(coordinates[1]), float(coordinates[0])]

        # Make a request to Mapbox Isochrone API
        response = requests.get(
            f"{ISOCHRONE_API_URL}{center[1]},{center[0]}.json?contours_minutes=60&polygons=true&access_token={MAPBOX_API_KEY}"
        )

        # https://api.mapbox.com/isochrone/v1/mapbox/driving-traffic/-75.150282%2C40.740121?contours_minutes=10&polygons=true&denoise=1&access_token=pk.eyJ1IjoiYWxleG1hcHN0aGluZ3MiLCJhIjoiY2xuMW9ycXhnMDBvMDJ0bGxuM25jbnNsZCJ9.B4kD4ZNutPF2S2C4Ec5TfQ

        if response.status_code == 200:
            data = response.json()

            st.subheader("Amtrak Train Stations Within an Hour's Drive")

            # Create a Leaflet map
            m = folium.Map(location=center, zoom_start=8)

            # Add the isochrone polygons as GeoJSON to the map
            folium.GeoJson(data).add_to(m)
            iso = gpd.GeoDataFrame.from_features(data)[0:1].geometry.item()

            for row in stations.itertuples():
                if iso.contains(row.geometry):
                    city = row.City
                    folium.Marker([row.lat,row.long],popup= row.StationNam +'<br> <a href=https://www.amtrak.com/home.html target="_blank">buy tickets</a>').add_to(m)

        st_data = st_folium(m, width=725)

with tab2:
    st.title("This is how it all works")
    st.image("data/isochrone.jpg")

