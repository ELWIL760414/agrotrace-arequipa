import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="AgroTrace - Arequipa", layout="wide")
st.title("🚜 AgroTrace: Control de Trazabilidad y Saldos")
st.subheader("Región: Arequipa (Piloto: Uva y Granada)")

data_parcelas = {
    "CLP": "CLP-040501-2024-0187",
    "Productor": "Agroexportaciones Valle de Majes S.A.C.",
    "Fundo": "Fundo Santa Isabel — Sector El Pedregal",
    "Cultivo": "Uva",
    "Variedad": "Sweet Globe (uva de mesa)",
    "MTD": "0.012 (Habilitado por SENASA)",
    "Vigencia": "2026-08-01 al 2027-07-31",
    "Capacidad Total (KG)": 125000,
    "Saldo Disponible (KG)": 81250,
    "Estado": "Habilitado para Exportar"
}

coordenadas_majes = [-16.3548, -72.1862]
m = folium.Map(location=coordenadas_majes, zoom_start=14)

folium.Polygon(
    locations=[[-16.3520, -72.1900], [-16.3520, -72.1820], [-16.3580, -72.1820], [-16.3580, -72.1900]],
    color="purple", fill=True, fill_color="purple", fill_opacity=0.4, tooltip=f"CLP: {data_parcelas['CLP']}"
).add_to(m)

col1, col2 = st.columns(2)
with col1:
    st_folium(m, width=600, height=450)
with col2:
    st.success(f"**Estado:** {data_parcelas['Estado']}")
    st.write(f"**Productor:** {data_parcelas['Productor']}")
    st.write(f"**Fundo:** {data_parcelas['Fundo']}")
    st.write(f"**Código CLP:** {data_parcelas['CLP']}")
    st.progress(data_parcelas["Saldo Disponible (KG)"] / data_parcelas["Capacidad Total (KG)"])
    st.metric(label="Saldo Disponible", value=f"{data_parcelas['Saldo Disponible (KG)']} KG")
