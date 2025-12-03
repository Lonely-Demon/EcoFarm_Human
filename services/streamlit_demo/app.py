import streamlit as st
import requests

st.title('EcoFarm Backend Demo')

BASE_URL = st.text_input('Base API URL', 'http://localhost:8001')

st.header('Weather')
lat = st.number_input('Latitude', value=12.9)
lon = st.number_input('Longitude', value=80.2)
provider = st.selectbox('Provider', options=['auto', 'open-meteo', 'nasa-power'])
if st.button('Get Weather'):
    try:
        r = requests.get(f"{BASE_URL}/weather?lat={lat}&lon={lon}&provider={provider}")
        if r.status_code == 200:
            st.json(r.json())
        else:
            st.error(f"Error: {r.status_code} - {r.text}")
    except Exception as e:
        st.error(str(e))

st.header('Farm Endpoints')
if st.button('Check Farms service'):
    try:
        r = requests.get('http://localhost:8002/')
        st.json(r.json())
    except Exception as e:
        st.error(str(e))

if st.button('Check Auth service'):
    try:
        r = requests.get('http://localhost:8000/')
        st.json(r.json())
    except Exception as e:
        st.error(str(e))

st.header('AI Recommendations')
if st.button('Get Recs for Tamil Nadu sample location'):
    try:
        rec = requests.post('http://localhost:8003/ai/rec/', json={"lat":12.9, "lon":80.2, "preferred_crops": ["tomato"]})
        if rec.status_code == 200:
            st.json(rec.json())
        else:
            st.error(f"Error: {rec.status_code} - {rec.text}")
    except Exception as e:
        st.error(str(e))

if st.button('Check AI service'):
    try:
        r = requests.get('http://localhost:8003/')
        st.json(r.json())
    except Exception as e:
        st.error(str(e))
