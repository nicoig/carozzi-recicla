import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import folium_static

# Función para obtener la ubicación aproximada del usuario
def get_user_location():
    try:
        response = requests.get('http://ipinfo.io/json')
        response.raise_for_status()
        data = response.json()
        location_str = data['loc']
        location = list(map(float, location_str.split(',')))
        return location
    except requests.RequestException as e:
        st.error(f"Error al obtener la ubicación: {e}")
        return None

# Leer los datos del archivo Excel
@st.cache_data
def load_data(filename):
    return pd.read_excel(filename)

df = load_data('Data/Maestra_Puntos_Reciclaje.xlsx')

# Intentar obtener la ubicación real del usuario
user_location = get_user_location()

if user_location is None:
    # Si no se pudo obtener la ubicación, usar una ubicación predeterminada
    user_location = [-33.6479903, -70.7096326]  # Ubicación de reserva

# Configurar el tamaño del mapa
map_width, map_height = 500, 300  # Ancho y alto en píxeles

# Crear un mapa con Folium
m = folium.Map(location=user_location, zoom_start=18)

# Añadir un marcador para la ubicación del usuario con un mensaje personalizado
folium.Marker(
    user_location, 
    popup='Tu Ubicación', 
    tooltip='Aquí estás tú', 
    icon=folium.Icon(color='red')
).add_to(m)

# Añadir marcadores para los puntos de reciclaje con un mensaje personalizado
for index, row in df.iterrows():
    folium.Marker(
        [row['Latitud'], row['Longitud']],
        popup=row
        ['Nombre'],
        tooltip=row['Nombre'],
        icon=folium.Icon(color='blue')
        ).add_to(m)

# Mostrar el mapa en Streamlit con el tamaño especificado
folium_static(m, width=map_width, height=map_height)