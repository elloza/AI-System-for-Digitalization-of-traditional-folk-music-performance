import streamlit as st
import requests

# URL del archivo README en GitHub
readme_url = "https://raw.githubusercontent.com/elloza/AI-System-for-Digitalization-of-traditional-folk-music-performance/main/README.md"

# Obtener el contenido del README
response = requests.get(readme_url)

if response.status_code == 200:
    readme_content = response.text
    # Mostrar el contenido en markdown
    st.markdown(readme_content, unsafe_allow_html=True)
else:
    st.error("No se pudo cargar el README desde GitHub.")