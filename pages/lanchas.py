from st_on_hover_tabs import on_hover_tabs
import streamlit as st
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from modeldb import Lancha, Mantenimiento, Ticket, Administrativo
st.set_page_config(layout="wide")

st.header("Custom tab component for on-hover navigation bar")
DATABASE_URL = "sqlite:///crud_app.db"
engine = create_engine(DATABASE_URL, echo=True)
with st.sidebar:
    tabs = on_hover_tabs(tabName=['lanchas nuevas', 'Mantenimientos', 'Administrativos', 'Viajes'], 
                         iconName=['dashboard', 'tool', 'economy', 'task'], default_choice=0)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()    
def cargar_lancha():
    st.header("Cargar lancha nueva")
    name = st.text_input("Ingrese nombre:")
    tipo = st.text_input("Ingrese Tipo:")
    capacidad = st.number_input("Ingrese Capacidad:")
    Anio_Fabricacion = st.number_input("Ingrese Año_Fabricacion:")

    if st.button("Create"):
        new_item = Lancha(Nombre=name, Tipo=tipo, Capacidad=int(capacidad), Anio_Fabricacion=int(Anio_Fabricacion))
        session.add(new_item)
        session.commit()
        st.success("Item created successfully!")

def mostrar_lanchas():
    items = session.query(Lancha).all()
    # Convierte los resultados a un DataFrame de pandas
    df = pd.DataFrame([item.__dict__ for item in items])

    # Elimina la columna '_sa_instance_state' que no es necesaria
    df = df.drop('_sa_instance_state', axis=1, errors='ignore')

    # Muestra la tabla en Streamlit
    st.table(df)

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


def cargar_administrativo():
    st.header("Cargar información administrativa")
    # Obtén la lista de lanchas para permitir la selección en el formulario
    lanchas = session.query(Lancha).all()
    lancha_choices = [lancha.Nombre for lancha in lanchas]
    selected_lancha = st.selectbox("Seleccione una lancha:", lancha_choices)
    fecha_vencimiento_permisos = st.date_input("Ingrese la Fecha de Vencimiento de Permisos:")
    fecha_vencimiento_matafuegos = st.date_input("Ingrese la Fecha de Vencimiento de Matafuegos:")
    # Otros campos administrativos que puedas necesitar


    if st.button("Crear Administrativo"):
        # Busca la lancha seleccionada
        lancha_seleccionada = session.query(Lancha).filter_by(Nombre=selected_lancha).first()

        # Crea un nuevo objeto Administrativo
        nuevo_administrativo = Administrativo(
            ID_Lancha=lancha_seleccionada.ID_Lancha,
            Fecha_Vencimiento_Permit_Prefectura=fecha_vencimiento_permisos,
            Fecha_Vencimiento_Matafuegos=fecha_vencimiento_matafuegos
            # Otros campos administrativos
        )

        # Agrega y confirma la transacción en la base de datos
        session.add(nuevo_administrativo)
        session.commit()

        st.success("Información administrativa creada exitosamente!")

def mostrar_administrativo():
    items = session.query(Administrativo).all()

    # Obtén los datos directamente desde los objetos Administrativo y Lancha
    data = {
        'ID_Lancha': [item.ID_Lancha for item in items],
        'Nombre_Lancha': [item.lancha.Nombre for item in items],  # Accede directamente al nombre de la lancha
        'Fecha_Vencimiento_Permit_Prefectura': [item.Fecha_Vencimiento_Permit_Prefectura for item in items],
        'Fecha_Vencimiento_Matafuegos': [item.Fecha_Vencimiento_Matafuegos for item in items],
        # Agrega otros campos administrativos aquí
    }

    # Convierte los resultados a un DataFrame de pandas
    df = pd.DataFrame(data)

    # Muestra la tabla en Streamlit
    st.table(df)

def cargar_ticket():
    st.header("Cargar ticket")
    
    # Obtén la lista de lanchas para permitir la selección en el formulario
    lanchas = session.query(Lancha).all()
    lancha_choices = [lancha.Nombre for lancha in lanchas]
    selected_lancha = st.selectbox("Seleccione una lancha:", lancha_choices)

    fecha_viaje = st.date_input("Ingrese la Fecha del Viaje:")
    precio = st.number_input("Ingrese el Precio:")
    # Otros campos del ticket

    if st.button("Crear Ticket"):
        # Busca la lancha seleccionada
        lancha_seleccionada = session.query(Lancha).filter_by(Nombre=selected_lancha).first()

        # Crea un nuevo objeto Ticket
        nuevo_ticket = Ticket(
            ID_Lancha=lancha_seleccionada.ID_Lancha,
            Fecha_Viaje=fecha_viaje,
            Precio=precio,
            # Otros campos del ticket
        )

        # Agrega y confirma la transacción en la base de datos
        session.add(nuevo_ticket)
        session.commit()

        st.success("Ticket creado exitosamente!")

def mostrar_viajes():
    items = session.query(Ticket).all()

    # Obtén los datos directamente desde los objetos Administrativo y Lancha
    data = {
        'ID_Ticket': [item.ID_Ticket for item in items],
        'Nombre_Lancha': [item.lancha.Nombre for item in items],  # Accede directamente al nombre de la lancha
        'Fecha_Viaje': [item.Fecha_Viaje for item in items],
        'Precio': [item.Precio for item in items],
        # Agrega otros campos administrativos aquí
    }

    # Convierte los resultados a un DataFrame de pandas
    df = pd.DataFrame(data)

    # Muestra la tabla en Streamlit
    st.table(df)

if tabs =='lanchas nuevas':
    st.title("Lanchas")
    cargar_lancha()
    mostrar_lanchas()

elif tabs == 'Mantenimientos':
    st.title("Mantenimiento")
    cargar_mantenimiento()
    mostrar_mantenimiento()

elif tabs == 'Viajes':
    st.title("Viajes")
    cargar_ticket()
    mostrar_viajes()

elif tabs == 'Administrativos':
    st.title("Administrativo")
    cargar_administrativo()
    mostrar_administrativo()
    

