import streamlit as st
import requests
from utils import api_helpers

def main():

    if "response" not in st.session_state:

        url = f"https://api.nasa.gov/planetary/apod?api_key={api_helpers.get_api()}"
        response = requests.get(url)
        data = response.json()
        st.write(response)
        # dict_keys(['copyright', 'date', 'explanation', 'hdurl', 'media_type', 'service_version', 'title', 'url'])
        print(data.keys())




if __name__ == '__main__':

    main()