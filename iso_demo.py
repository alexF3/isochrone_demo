import streamlit as st
import requests
import folium
from geopy.geocoders import MapBox
from folium.plugins import HeatMap
import folium
from streamlit_folium import st_folium
import geopandas as gpd

st.set_page_config(page_title="Isochrones: Human-Centered Geography with Streamlit")


stations = gpd.read_file('data/Amtrak_Stations.geojson')
stations = stations[stations.StnType=='TRAIN']
stations['long'] =  stations.geometry.x
stations['lat'] = stations.geometry.y

# Mapbox API keys
MAPBOX_API_KEY = st.secrets["MAPBOX_API_KEY"]
GEOCODING_API_KEY = st.secrets["GEOCODING_API_KEY"]

# Mapbox Geocoding API
GEOCODING_API_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places/"

# Mapbox Isochrone API
ISOCHRONE_API_URL = "https://api.mapbox.com/isochrone/v1/mapbox/driving/"

# Initialize Mapbox geocoder
geolocator = MapBox(api_key=GEOCODING_API_KEY)

tab1, tab2 = st.tabs(["Demo", "About"])


# style function
iso_style_function = lambda x: {
  'color' :  '#f79205'

}


with tab1:
    st.markdown("**Isochrones** are a great way to distill geospatial data down to the lived experience of a user.  With one simple API call, you can present someone with just the portion of your data that is within an hour's drive of where they are.  That can be a powerful for a number of behavioral science applications.")

    st.title("Where Are the Amtrak Stations Near You?")
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
            folium.GeoJson(data,style_function=iso_style_function).add_to(m)
            iso = gpd.GeoDataFrame.from_features(data)[0:1].geometry.item()

            for row in stations.itertuples():
                if iso.contains(row.geometry):
                    city = row.City
                    folium.Marker([row.lat,row.long],popup= row.StationNam +'<br> <a href=https://www.amtrak.com/home.html target="_blank">buy tickets</a>').add_to(m)

        st_data = st_folium(m, width=725)

with tab2:
    st.image("data/isochrone.jpg")
    st.markdown("""
    # Isochrone Streamlit Demo

This is a demo the use of isocrhones in an app.  An isochrone is the geographic polygon that can be reached from a given location in a certain about of time via a given means of transportation.  This lets you answer questions like "How many cofee shops are within a 20 minute walk of the apartment I'm looking at?."  In this case the app will show a user all the Amtrak stations within a one hour drive of location they input.


### To accomplish this the app uses:
 * The [MapBox Geocoding API](https://docs.mapbox.com/api/search/geocoding/) and the [MapBox Isochrone API ](https://docs.mapbox.com/api/navigation/isochrone/) to get coordinates for the input location and a 1-hour driving isocrhone around that point
 * [Geopandas](https://geopandas.org/en/stable/) and an open source file of Amtrak stations to filter to only the Amtrak train stations inside the isochrone
 * [Folium](https://pypi.org/project/folium/) to generate an interactive map of the isochrone and train stations
 * [Streamlit](https://streamlit.io/) to serve the application

## Key Takeaways:

* Isochrones are a great way to distill geography into human scale and match data to the patterns of a person's lived experiences
* MapBox APIs make it fast and easy to do geospatial work with Python (just make sure you DON'T POST YOUR API KEYS TO A PUBLIC REPO and read up on [protecting them on Streamlit](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management))
* This just scratches the surface of what can be done with open source tools and geospatial datasets


""")

