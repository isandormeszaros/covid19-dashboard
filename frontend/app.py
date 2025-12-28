import streamlit as st
import pandas as pd
import requests
import altair as alt
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("BACKEND_URL")

st.set_page_config(layout="wide", page_title="COVID19 Dashboard")

st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #264653; color: white; }
    h1 { color: #264653; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_countries_list():
    if not API_URL: return {}
    base_url = API_URL.replace('/api/dashboard', '')
    try:
        resp = requests.get(f"{base_url}/api/countries")
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return {"HUN": "Hungary", "USA": "United States"}

# Navbar 
with st.sidebar:
    st.title("COVID19 Dashboard")
    
    # Legördülő
    countries_map = get_countries_list()
    options = [f"{code} - {name}" for code, name in countries_map.items()]
    
    selected_option = st.selectbox("Válassz országot:", options, index=0)
    country_input = selected_option.split(" - ")[0]
    
    st.write("---")
    st.button("Frissítés")

# Site
st.title(f"Dashboard - {countries_map.get(country_input, country_input)}")

try:
    response = requests.get(f"{API_URL}/{country_input}")
    
    if response.status_code == 404:
        st.error(f"**Nincs adat ehhez az országhoz: {country_input}**")
        st.stop()
    elif response.status_code != 200:
        st.error("Szerver hiba.")
        st.stop()
        
    data = response.json()
    metrics = data["metrics"]
    charts = data["charts"]

    # KPI
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ország", data["country"])
    c2.metric("Várható élettartam", f"{metrics['life_expectancy']} év")
    c3.metric("Munkanélküliség", metrics["unemployment"])
    c4.metric("Öngyilkossági ráta", metrics["suicide_rate"])

    st.markdown("---")

    # Grafikonok
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("GDP Trend (USD/capita)")
        if charts["gdp"]:
            df_gdp = pd.DataFrame(charts["gdp"])
            chart = alt.Chart(df_gdp).mark_line(color='#ff7f7f', point=True).encode(
                x=alt.X('year:O', axis=alt.Axis(format='d', title='Év')), 
                y=alt.Y('value:Q', title='GDP'),
                tooltip=['year', 'value']
            ).interactive()
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Nincs elérhető GDP adat.")

    with col2:
        st.subheader("Várható élettartam (Év)")
        if charts["life_exp"]:
            df_life = pd.DataFrame(charts["life_exp"])
            chart_life = alt.Chart(df_life).mark_line(color='#90ee90', point=True).encode(
                x=alt.X('year:O', axis=alt.Axis(format='d', title='Év')),
                y=alt.Y('value:Q', scale=alt.Scale(zero=False), title='Életkor'),
                tooltip=['year', 'value']
            ).interactive()
            st.altair_chart(chart_life, use_container_width=True)
        else:
            st.info("Nincs elérhető élettartam adat.")

except Exception as e:
    st.error(f"Nem érhető el a Backend! ({e})")