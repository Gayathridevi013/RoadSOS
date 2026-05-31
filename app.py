import streamlit as st
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

# ----------------------------
# PAGE CONFIG
# ----------------------------

st.set_page_config(
    page_title="RoadSoS",
    page_icon="🚑",
    layout="wide"
)

# ----------------------------
# HOSPITAL DATABASE
# ----------------------------

hospitals = [
    {"name": "Apollo Trauma Centre", "lat": 13.0827, "lon": 80.2707},
    {"name": "Government General Hospital", "lat": 13.0878, "lon": 80.2785},
    {"name": "MIOT Hospital", "lat": 13.0215, "lon": 80.1859},
    {"name": "SRM Medical Centre", "lat": 12.8230, "lon": 80.0450},
]

# ----------------------------
# DISTANCE FUNCTION
# ----------------------------

def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


# ----------------------------
# FIND NEAREST HOSPITAL
# ----------------------------

def find_nearest_hospital(user_lat, user_lon):

    nearest = None
    min_distance = float("inf")

    for hospital in hospitals:

        dist = calculate_distance(
            user_lat,
            user_lon,
            hospital["lat"],
            hospital["lon"]
        )

        if dist < min_distance:
            min_distance = dist
            nearest = hospital

    return nearest, round(min_distance, 2)


# ----------------------------
# SEVERITY PREDICTION
# ----------------------------

def predict_severity(speed_drop, impact):

    score = speed_drop + (impact * 30)

    if score < 30:
        return "Minor"

    elif score < 60:
        return "Moderate"

    elif score < 90:
        return "Severe"

    else:
        return "Critical"


# ----------------------------
# FIRST AID GUIDANCE
# ----------------------------

def get_first_aid(severity):

    if severity == "Minor":
        return """
        • Move to a safe area.
        • Check for small injuries.
        • Monitor symptoms.
        """

    elif severity == "Moderate":
        return """
        • Stay calm.
        • Check for bleeding.
        • Contact emergency services.
        """

    elif severity == "Severe":
        return """
        • Keep victim still.
        • Control bleeding.
        • Do not move injured body parts.
        • Call ambulance immediately.
        """

    else:
        return """
        • CRITICAL EMERGENCY
        • Call ambulance immediately.
        • Check breathing.
        • Start CPR if required.
        • Keep airway clear.
        """


# ----------------------------
# HEADER
# ----------------------------

st.title("🚑 RoadSoS")
st.subheader("AI Powered Emergency Response Assistant")

st.markdown("---")

# ----------------------------
# USER INPUT
# ----------------------------

col1, col2 = st.columns(2)

with col1:

    st.header("📍 Location")

    user_lat = st.number_input(
        "Latitude",
        value=13.0827
    )

    user_lon = st.number_input(
        "Longitude",
        value=80.2707
    )

with col2:

    st.header("🚗 Accident Details")

    speed_drop = st.slider(
        "Speed Drop",
        0,
        100,
        50
    )

    impact = st.selectbox(
        "Impact Detected?",
        [0, 1]
    )

# ----------------------------
# SOS BUTTON
# ----------------------------

st.markdown("---")

if st.button("🚨 ACTIVATE SOS", use_container_width=True):

    severity = predict_severity(
        speed_drop,
        impact
    )

    hospital, distance = find_nearest_hospital(
        user_lat,
        user_lon
    )

    st.success("Emergency Request Activated")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Severity",
            severity
        )

    with col2:
        st.metric(
            "Nearest Hospital",
            hospital["name"]
        )

    with col3:
        st.metric(
            "Distance",
            f"{distance} km"
        )

    st.markdown("---")

    st.subheader("🏥 Recommended Hospital")

    st.write(
        f"**{hospital['name']}**"
    )

    st.write(
        f"Location: ({hospital['lat']}, {hospital['lon']})"
    )

    st.markdown("---")

    st.subheader("🩺 AI Golden Hour Assistant")

    st.info(
        get_first_aid(severity)
    )

    st.markdown("---")

    st.subheader("📞 Emergency Contacts")

    st.write("Ambulance: 108")
    st.write("Police: 100")
    st.write("Road Assistance: 1033")

    st.warning(
        "SOS Alert sent to nearby emergency services (Simulation)"
    )

# ----------------------------
# FOOTER
# ----------------------------

st.markdown("---")

st.caption(
    "RoadSoS | National Road Safety Hackathon 2026"
)