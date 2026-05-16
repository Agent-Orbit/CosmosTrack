import streamlit as st
import requests
from utils import api_helpers
import datetime
import plotly.graph_objects as go
import math
import random
import pandas as pd

def main():

    st.title("Asteroid Tracker")
    st.divider()

    if "Data_NeoWs" not in st.session_state:

        API_KEY = api_helpers.get_api()

        today = datetime.date.today()
        week_later = today + datetime.timedelta(days=7)

        url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&end_date={week_later}&api_key={API_KEY}"

        response = requests.get(url)

        if response.status_code == 200:

            st.session_state.Data_NeoWs = response.json()

        else:

            st.error("Failed to fetch NASA data")
            st.stop()

    NeoWsData = st.session_state.Data_NeoWs

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers+text",
            marker=dict(size=30, color="blue"),
            text=["Earth"],
            name="Earth"
        )
    )

    hazardous_ast = 0
    lowest_magnitude = float("inf")

    hazardous_asteroids = []
    miss_distance = []
    magnitude = []
    name = []
    approach_date = []
    neo_id = []
    url_list = []

    for key, asteroid_list in NeoWsData["near_earth_objects"].items():

        for asteroid in asteroid_list:

            if not asteroid["close_approach_data"]:

                continue

            approach = asteroid["close_approach_data"][0]

            distance = float(approach["miss_distance"]["kilometers"])
            distance_scaled = distance / 1000000

            hazardous = asteroid["is_potentially_hazardous_asteroid"]

            if hazardous:

                hazardous_ast += 1

            asteroid_size = 30 - asteroid["absolute_magnitude_h"]
            asteroid_size = max(5, min(asteroid_size, 25))

            if asteroid["absolute_magnitude_h"] < lowest_magnitude:

                lowest_magnitude = asteroid["absolute_magnitude_h"]

            date = approach["close_approach_date"]

            random.seed(date + asteroid["name"])

            angle = random.uniform(0, 360)
            angle_rad = math.radians(angle)

            x = distance_scaled * math.cos(angle_rad)
            y = distance_scaled * math.sin(angle_rad)

            fig.add_trace(
                go.Scatter(
                    x=[x],
                    y=[y],
                    mode="markers",
                    marker=dict(
                        size=asteroid_size,
                        color="red" if hazardous else "green"
                    ),
                    text=f"Name: {asteroid['name']}",
                    name=asteroid["name"]
                )
            )

            hazardous_asteroids.append(hazardous)
            miss_distance.append(distance)
            magnitude.append(asteroid["absolute_magnitude_h"])
            name.append(asteroid["name"])
            approach_date.append(date)
            neo_id.append(asteroid["neo_reference_id"])
            url_list.append(asteroid["nasa_jpl_url"])

    df = pd.DataFrame({
        "neo_id": neo_id,
        "name": name,
        "approach_date": approach_date,
        "url": url_list,
        "magnitude": magnitude,
        "miss_distance_km": miss_distance,
        "is_hazardous": hazardous_asteroids
    })

    fig.update_layout(
        xaxis_title="Distance (million km)",
        yaxis_title="Distance (million km)",
        showlegend=False
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total asteroids tracked this week",
            value=int(NeoWsData["element_count"])
        )

    with col2:

        st.metric(
            "Hazardous asteroids",
            value=hazardous_ast
        )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Largest Asteroid (Lowest Magnitude)",
            value=round(lowest_magnitude, 2)
        )

    with col2:

        closest_distance = min(miss_distance) if miss_distance else 0

        st.metric(
            "Closest Approach (km)",
            value=f"{closest_distance:,.0f}"
        )

    st.divider()

    st.markdown("# Asteroids Plot:")

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("# Data:")

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        data=csv,
        file_name="NASA_Asteroids.csv",
        mime="text/csv"
    )

if __name__ == "__main__":

    main()