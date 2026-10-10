import streamlit as st
import folium
from streamlit_folium import st_folium

# Configuración de la pantalla ancha
st.set_page_config(page_title="AgroTrace - Uva Arequipa", layout="wide")

st.title("🚜 AgroTrace: Control de Trazabilidad y Saldos")
st.subheader("Foco Único: Piloto de Uva de Mesa — Región Arequipa")

# 1. Base de datos real con 3 parcelas de Uva en Majes
db_parcelas = {
    "CLP-040501-2024-0187": {
        "Productor": "Agroexportaciones Valle de Majes S.A.C.",
        "Fundo": "Fundo Santa Isabel — Lote A",
        "Variedad": "Sweet Globe (Uva Blanca)",
        "MTD": "0.012 (Habilitado)",
        "Vigencia": "2026-08-01 al 2027-07-31",
        "Capacidad Total (KG)": 125000,
        "Saldo Disponible (KG)": 81250,
        "Estado": "Habilitado para Exportar",
        "Centro": [-16.3548, -72.1862],
        "Color": "purple",
        "Poligono": [
            [-16.3520, -72.1900],
            [-16.3520, -72.1820],
            [-16.3580, -72.1820],
            [-16.3580, -72.1900]
        ]
    },
    "CLP-040501-2024-0294": {
        "Productor": "Vitivinícola Del Pedregal E.I.R.L.",
        "Fundo": "Fundo El Tambo — Sector 3",
        "Variedad": "Red Globe (Uva Roja con semilla)",
        "MTD": "0.008 (Habilitado)",
        "Vigencia": "2026-09-15 al 2027-09-14",
        "Capacidad Total (KG)": 200000,
        "Saldo Disponible (KG)": 45000,
        "Estado": "Habilitado - ¡Saldo Crítico!",
        "Centro": [-16.3420, -72.2050],
        "Color": "crimson",
        "Poligono": [
            [-16.3380, -72.2100],
            [-16.3380, -72.2000],
            [-16.3450, -72.2000],
            [-16.3450, -72.2100]
        ]
    },
    "CLP-040501-2024-0512": {
        "Productor": "Agrícola Pampa Baja Sucursal",
        "Fundo": "Fundo Don Alberto — Lote 12",
        "Variedad": "Autumn Crisp (Uva Blanca sin semilla)",
        "MTD": "0.045 (RESTRICCIÓN)",
        "Vigencia": "VENCIDA o Suspendida por SENASA",
        "Capacidad Total (KG)": 150000,
        "Saldo Disponible (KG)": 0,
        "Estado": "BLOQUEADO - Problema Fitosanitario",
        "Centro": [-16.3680, -72.1650],
        "Color": "red",
        "Poligono": [
            [-16.3630, -72.1700],
            [-16.3630, -72.1600],
            [-16.3720, -72.1600],
            [-16.3720, -72.1700]
        ]
    }
}

# 2. SECCIÓN DEL BUSCADOR DE SENASA (Interfaz de Usuario)
st.markdown("### 🔍 Buscador Oficial de Códigos CLP (SENASA)")

# Barra desplegable para seleccionar o escribir el código
lista_codigos = list(db_parcelas.keys())
clp_seleccionado = st.selectbox(
    "Seleccione o escriba el código CLP de la parcela a consultar:",
    options=lista_codigos,
    index=0
)

# Extraer los datos de la parcela elegida en el buscador
parcela = db_parcelas[clp_seleccionado]

st.markdown("---")

# 3. Distribución de pantallas en 2 columnas
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### 🗺️ Geolocalización: {parcela['Fundo']}")
    
    # Crear mapa dinámico centrado exactamente en la parcela buscada
    m = folium.Map(location=parcela["Centro"], zoom_start=14, tiles="OpenStreetMap")
    
    # Dibujar la parcela seleccionada
    folium.Polygon(
        locations=parcela["Poligono"],
        color=parcela["Color"],
        fill=True,
        fill_color=parcela["Color"],
        fill_opacity=0.4,
        tooltip=f"CLP: {clp_seleccionado}"
    ).add_to(m)
    
    # Renderizar el mapa en la web
    st_folium(m, width=650, height=450, key=f"mapa_{clp_seleccionado}")

with col2:
    st.markdown("### 📋 Ficha de Trazabilidad en Tiempo Real")
    
    # Mostrar alertas visuales según el estado de SENASA
    if "BLOQUEADO" in parcela["Estado"]:
        st.error(f"⚠️ **Estado:** {parcela['Estado']}")
    elif "Crítico" in parcela["Estado"]:
        st.warning(f"⚠️ **Estado:** {parcela['Estado']}")
    else:
        st.success(f"✅ **Estado:** {parcela['Estado']}")
        
    st.write(f"**Productor Comercial:** {parcela['Productor']}")
    st.write(f"**Nombre del Fundo:** {parcela['Fundo']}")
    st.write(f"**Variedad de Uva:** {parcela['Variedad']}")
    st.write(f"**Código Oficial CLP:** `{clp_seleccionado}`")
    st.write(f"**Monitoreo MTD (Mosca/Fruta):** {parcela['MTD']}")
    st.write(f"**Vigencia de Certificación:** {parcela['Vigencia']}")
    
    st.markdown("---")
    st.markdown("### 📊 Balance de Saldos Disponibles")
    
    # Calcular y dibujar la barra de progreso
    if parcela["Capacidad Total (KG)"] > 0:
        porcentaje = parcela["Saldo Disponible (KG)"] / parcela["Capacidad Total (KG)"]
    else:
        porcentaje = 0.0
        
    st.progress(porcentaje)
    
    st.metric(
        label="Saldo de Fruta Libre para Despacho", 
        value=f"{parcela['Saldo Disponible (KG)']} KG", 
        delta=f"Capacidad Máxima del Terreno: {parcela['Capacidad Total (KG)']} KG"
    )

