import streamlit as st

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
# Main dashboard
# -----------------------------------
with st.container(border=True):
        
    st.subheader("🌱 Plant Monitoring System")
    st.divider()

    # -----------------------------------
    # Environmental Monitoring
    # -----------------------------------
    st.write("**Environmental Monitoring**")

    # First row of metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="🌡️ Temperature",
            value=f"{temperature} °C"
        )
    
    with col2:
        st.metric(
            label="💧 Humidity",
            value=f"{humidity}%"
        )

    # Second row of metrics
    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            label="☀️ Light intensity",
            value=f"{light_intensity}%"
        )
    
    with col4:
        st.metric(
            label="🌱 Soil moisture",
            value=f"{soil_moisture}%"
        )

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

        # This is where you will call your
        # forward-chaining inference engine.
        st.success("Recommendation generated successfully!")

        st.info(
            "Your expert system recommendation will appear here."
        )
