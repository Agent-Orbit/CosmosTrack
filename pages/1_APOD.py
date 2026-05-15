import streamlit as st
import requests
from utils import api_helpers
import datetime

def main():
    st.title("NASA Astronomy Picture of the Day Gallery")
    st.divider()

    if "data_today" not in st.session_state:
        API_KEY = api_helpers.get_api()
        url_today = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"
        response_today = requests.get(url_today)
        st.session_state.data_today = response_today.json()
    
    if "favorites" not in st.session_state:
        st.session_state.favorites = []

    data = st.session_state.data_today
    
    st.markdown("### Today's APOD:")
    make_PicCard(data['hdurl'], data['title'], APODtype=data['media_type'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Add to favourites", key="fav_today", use_container_width=True):
            if data not in st.session_state.favorites:
                st.session_state.favorites.append(data)
                st.success("Added to favorites!")
            else:
                st.info("Already in favorites")
        
    with col2:
        if st.button("Details", key="details_today", use_container_width=True):
            st.session_state.selected_apod = data
    
    st.divider()

    if "randomAPODs" not in st.session_state:
        API_KEY = api_helpers.get_api()
        random_count = 6
        url_random = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&count={random_count}"
        response_random = requests.get(url_random)
        st.session_state.randomAPODs = response_random.json()
    
    randomAPODs = st.session_state.randomAPODs
    mid = len(randomAPODs) // 2
    first_half_APODs = randomAPODs[:mid]
    second_half_APODs = randomAPODs[mid:]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Some APOD's")
    
    with col2:
        if st.button("Refresh", key="refresh_random", use_container_width=True):
            del st.session_state.randomAPODs
            st.rerun()

    st.write("")
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        for item in first_half_APODs:
            make_PicCard(item['hdurl'], item['title'], APODtype=item['media_type'])
            
            col_l, col_r = st.columns(2)
            
            with col_l:
                if st.button("Add to favourites", key=f"{item['date']}_fav_left", use_container_width=True):
                    if item not in st.session_state.favorites:
                        st.session_state.favorites.append(item)
                        st.success("Added!")
                    else:
                        st.info("Already in favorites")
                
            with col_r:
                if st.button("Details", key=f"{item['date']}_details_left", use_container_width=True):
                    st.session_state.selected_apod = item
    
    with col2:
        for item in second_half_APODs:
            make_PicCard(item['hdurl'], item['title'], APODtype=item['media_type'])
            
            col_l, col_r = st.columns(2)
            
            with col_l:
                if st.button("Add to favourites", key=f"{item['date']}_fav_right", use_container_width=True):
                    if item not in st.session_state.favorites:
                        st.session_state.favorites.append(item)
                        st.success("Added!")
                    else:
                        st.info("Already in favorites")
                
            with col_r:
                if st.button("Details", key=f"{item['date']}_details_right", use_container_width=True):
                    st.session_state.selected_apod = item

    st.divider()

    today = datetime.date.today()
    apod_start = datetime.date(1995, 6, 16)

    st.markdown("### Select a Date")

    selected_date = st.date_input(
        "Select APOD Date",
        value=today,
        min_value=apod_start,
        max_value=today,
        format="YYYY-MM-DD"
    )

    if "selectedAPOD" not in st.session_state:
        st.session_state.selectedAPOD = None
        st.session_state.last_date = None

    if st.session_state.last_date != selected_date:
        API_KEY = api_helpers.get_api()
        url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&date={selected_date}"
        response = requests.get(url)
        
        if response.status_code == 200:
            st.session_state.selectedAPOD = response.json()
            st.session_state.last_date = selected_date
        else:
            st.error("Failed to fetch APOD")

    if st.session_state.selectedAPOD:
        selectedAPOD = st.session_state.selectedAPOD
        
        st.markdown("### Your APOD:")
        make_PicCard(selectedAPOD['hdurl'], selectedAPOD["title"], APODtype=selectedAPOD["media_type"])

        col_l, col_r = st.columns(2)

        with col_l:
            if st.button("Add to favourites", key=f"{selectedAPOD['date']}_fav_selected", use_container_width=True):
                if selectedAPOD not in st.session_state.favorites:
                    st.session_state.favorites.append(selectedAPOD)
                    st.success("Added to favorites!")
                else:
                    st.info("Already in favorites")

        with col_r:
            if st.button("Details", key=f"{selectedAPOD['date']}_details_selected", use_container_width=True):
                st.session_state.selected_apod = selectedAPOD

    st.divider()

def make_PicCard(data, title, APODtype):
    
    if APODtype == "image":
        st.image(data, caption=f"Title: {title}")
    else:
        st.video(data)

if __name__ == '__main__':
    main()