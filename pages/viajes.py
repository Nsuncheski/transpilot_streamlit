from pages.lanchas import cargar_ticket, mostrar_viajes
import streamlit as st

st.title("Viajes")
cargar_ticket()
mostrar_viajes()