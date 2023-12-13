import streamlit as st
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from modeldb import Lancha, Mantenimiento, Ticket, Administrativo

DATABASE_URL = "sqlite:///crud_app.db"
engine = create_engine(DATABASE_URL, echo=True)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()   


def cargar_mantenimiento():
    st.header("Cargar mantenimiento")
    
    # Obtén la lista de lanchas para permitir la selección en el formulario
    lanchas = session.query(Lancha).all()
    lancha_choices = [lancha.Nombre for lancha in lanchas]
    selected_lancha = st.selectbox("Seleccione una lancha:", lancha_choices)

    tipo_mantenimiento = st.text_input("Ingrese Tipo de Mantenimiento:")
    fecha_mantenimiento = st.date_input("Ingrese la Fecha de Mantenimiento:")
    costo = st.number_input("Ingrese el Costo:")
    descripcion = st.text_area("Ingrese la Descripción:")

    if st.button("Crear Mantenimiento"):
        # Busca la lancha seleccionada
        lancha_seleccionada = session.query(Lancha).filter_by(Nombre=selected_lancha).first()

        # Crea un nuevo objeto Mantenimiento
        nuevo_mantenimiento = Mantenimiento(
            ID_Lancha=lancha_seleccionada.ID_Lancha,
            Tipo_Mantenimiento=tipo_mantenimiento,
            Fecha_Mantenimiento=fecha_mantenimiento,
            Costo=costo,
            Descripcion=descripcion
        )

        # Agrega y confirma la transacción en la base de datos
        session.add(nuevo_mantenimiento)
        session.commit()

        st.success("Mantenimiento creado exitosamente!")

def mostrar_mantenimiento():
    items = session.query(Mantenimiento).all()
    # Convierte los resultados a un DataFrame de pandas
    df = pd.DataFrame([item.__dict__ for item in items])

    # Elimina la columna '_sa_instance_state' que no es necesaria
    df = df.drop('_sa_instance_state', axis=1, errors='ignore')

    # Muestra la tabla en Streamlit
    st.table(df)


st.title("Mantenimiento")
cargar_mantenimiento()
mostrar_mantenimiento()