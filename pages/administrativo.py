from pages.lanchas import cargar_administrativo, mostrar_administrativo
import streamlit as st
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from modeldb import Lancha, Mantenimiento, Ticket, Administrativo



st.title("Administrativo")
cargar_administrativo()
mostrar_administrativo()