import streamlit as st
import requests
from utils import api_helpers
import datetime

def main():

    if "Data_NeoWs" not in st.session_state:

        API_KEY = api_helpers.get_api()
        today = datetime.date.today()
        week_later = today + datetime.timedelta(days=7)

        url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&end_date={week_later}&api_key={API_KEY}"
        response = requests.get(url)
        data = response.json()
        st.session_state.Data_NeoWs = data

        
    
    NeoWsData = st.session_state.Data_NeoWs
    st.title("Asteroids")
    st.divider()
    
    for key,data in NeoWsData["near_earth_objects"].items():

        st.write(key)
        st.write(data[0]["name"])

if __name__ == "__main__":

    main()