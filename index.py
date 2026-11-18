import streamlit as st
import requests
import time
from services.supabase import supabase

st.markdown("""
<style>
    /* Hide Streamlit top header */
    header[data-testid="stHeader"] {
        display: none;
    }

    /* Hide Deploy button */
    .stDeployButton {
        display: none;
    }

    /* Hide top-right menu */
    #MainMenu {
        visibility: hidden;
    }

    /* Hide footer */
    footer {
        visibility: hidden;
    }

    .block-container {
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# Page configuration
# -----------------------------------
st.set_page_config(
    page_title="Plant Monitoring System",
    page_icon="🌱",
    layout="centered"
)

# -----------------------------------
# Environmental data
# -----------------------------------
temperature = 28.5
humidity = 65
light_intensity = 75
soil_moisture = 45

#-----------------------------------
# Plant assessment variables
#-----------------------------------
plant_type = None
leaf_condition = None

# -----------------------------------
# Live HTTP Polling Fragment
# -----------------------------------
@st.fragment(run_every="20s")
def live_environmental_updates():
    st.write("**Environmental Monitoring**")

    # Fetch live sensor data from your ESP32 / IoT HTTP endpoint
    try:
        with st.spinner("Fetching latest environmental data ...", show_time=True):
            response = (
                supabase.table("Environmental data")
                .select("*")
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )

        if not response.data:
            st.warning("No sensor data available.")
            return

        # Save latest readings to session_state so the inference engine can use them
        st.session_state.sensor_data = {
            "temperature": round(response.data[0]["temperature"], 2),
            "humidity": round(response.data[0]["humidity"], 2),
            "light_intensity": round(response.data[0]["light_intensity"], 2),
            "soil_moisture": round(response.data[0]["soil_moisture"], 2)
        }

    except requests.RequestException:
        st.caption("⚠️ Offline: Showing last known sensor readings.")

    sensors = st.session_state.sensor_data

    # First row of metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="🌡️ Temperature", value=f"{sensors['temperature']} °C")
    with col2:
        st.metric(label="💧 Humidity", value=f"{sensors['humidity']}%")

    # Second row of metrics
    col3, col4 = st.columns(2)
    with col3:
        st.metric(label="☀️ Light intensity", value=f"{sensors['light_intensity']}%")
    with col4:
        st.metric(label="🌱 Soil moisture", value=f"{sensors['soil_moisture']}%")

# -----------------------------------
# Main dashboard
# -----------------------------------
with st.container(border=True):
    st.subheader("🌱 Plant Monitoring System")
    st.divider()

    live_environmental_updates()

    st.divider()

    # -----------------------------------
    # Plant Assessment
    # -----------------------------------
    st.write("**Plant Assessment**")

    # User input for plant assessment
    # Plant type selection
    plant_type = st.selectbox(
        "**Plant type**",
        options=[
            "Rose",
            "Sunflower",
            "Tomato",
            "Chilli",
            "Mint",
            "Other"
        ],
        index=None,
        placeholder="Select plant"
    )

    # Leaf condition selection
    leaf_condition = st.radio(
        "**Leaf condition**",
        options=[
            "Healthy",
            "Wilting",
            "Yellowing",
            "Brown spots"
        ],
        index=0,
    )
      
    # -----------------------------------
    # Generate Recommendation
    # -----------------------------------
    generate = st.button(
        "Generate Recommendation",
        disabled=(plant_type is None or leaf_condition is None),
        use_container_width=True
    )

    if generate:

        st.divider()

        st.markdown("### Plant Assessment Result")

        st.write(f"**Plant:** {plant_type}")
        st.write(f"**Leaf condition:** {leaf_condition}")

        st.info(
            "Your expert system recommendation will appear here."
        )
