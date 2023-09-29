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





## License

[MIT](https://choosealicense.com/licenses/mit/)