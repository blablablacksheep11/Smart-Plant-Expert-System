import streamlit as st
import requests
from services.supabase import supabase
from infer import derive_init_facts, infer
from knowledge import rules

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

if "sensor_data" not in st.session_state:
    st.session_state.sensor_data = {
        "temperature": 0,
        "humidity": 0,
        "light_intensity": 0,
        "soil_moisture": 0
    }

if "previous_facts" not in st.session_state:
    st.session_state.previous_facts = None

recommendation_messages = {
    "recommend_plant_conditions_healthy": {
        "message": "Your plant conditions are healthy. Continue maintaining the current environmental conditions.",
        "status": "success"
    },

    "recommend_fertilization": {
        "message": "Your plant may require additional nutrients. Consider applying suitable fertilizer.",
        "status": "warning"
    },

    "recommend_environment_adjustment": {
        "message": "Your plant is experiencing environmental stress. Adjust the surrounding temperature and monitor soil moisture.",
        "status": "warning"
    },

    "recommend_improve_ventilation_and_pest_control": {
        "message": "Improve air circulation around your plant and inspect it for possible fungal infections or pests.",
        "status": "warning"
    },

    "recommend_watering_and_shade": {
        "message": "Your plant may need additional water. Move it to a partially shaded area to reduce excessive sunlight and heat.",
        "status": "warning"
    }
}

# -----------------------------------
# Live HTTP Polling Fragment
# -----------------------------------
@st.fragment(run_every="20s")
def live_environmental_updates():
    column1, column2 = st.columns([8, 2])
    with column1:
        st.write("**Environmental Monitoring**")
    with column2:
        st.button("Refresh", type="tertiary", key="refresh_environmental_data")

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
            "Chilli",
            "Cactus",
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
        st.subheader("📋 Plant Assessment Result")

        # Derive initial facts based on sensor readings and previous facts 
        facts = derive_init_facts(
            soil_moisture=st.session_state.sensor_data["soil_moisture"],
            temperature=st.session_state.sensor_data["temperature"],
            humidity=st.session_state.sensor_data["humidity"],
            light_intensity=st.session_state.sensor_data["light_intensity"],
            previous_facts=st.session_state.previous_facts
        )

        st.session_state.previous_facts = facts

        facts.add(f"plant_type_{plant_type.lower()}")
        facts.add(f"leaf_condition_{leaf_condition.lower()}")     

        st.write("**Recommendation:**")

        recommendations, fired_rules = infer(rules, facts)
        if recommendations:
            for recommendation in sorted(recommendations):
                details = recommendation_messages.get(
                    recommendation,
                    "No recommendation available."
                )

                message = details["message"]
                status = details["status"]

                if status == "success":
                    st.success(message)

                elif status == "warning":
                    st.warning(message)

        else:
            st.write("No specific recommendations at this time.")
        
        
        st.write("**Rules fired:**")
        with st.popover("View reasoning"):
            for rule in fired_rules:
                st.write(rule["name"])

        