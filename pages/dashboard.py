import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modeldb import Base, Lancha, Mantenimiento, Ticket, Administrativo  # Ajusta la importación según la ubicación de tus modelos

# Configurar la conexión a la base de datos SQLite
engine = create_engine('sqlite:///crud_app.db')  # Ajusta según tu conexión
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Función para cargar los datos de ganancias por día y lancha
def cargar_datos_ganancias():
    tickets = session.query(Ticket).all()

    data = {
        'Fecha_Viaje': [ticket.Fecha_Viaje for ticket in tickets],
        'Lancha': [ticket.lancha.Nombre for ticket in tickets],
        'Precio': [ticket.Precio for ticket in tickets]
    }

    df_tickets = pd.DataFrame(data)

    return df_tickets

# Crear un DataFrame con los datos de ganancias
df_ganancias = cargar_datos_ganancias()

# Configurar la página de Streamlit
st.title("Dashboard de Lanchas")

# Gráfico de ganancias por día
st.header("Ganancias por Día")
fig = plt.figure(figsize=(9,7))
sns.barplot(x='Fecha_Viaje', y='Precio', hue='Lancha', data=df_ganancias)

plt.title("Viajes")
# Rotar las etiquetas del eje x
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

# Gráfico de ganancias por lancha
st.header("Ganancias por Lancha")
fig2 = plt.figure(figsize=(9,7))
fig_ganancias_lancha = sns.barplot(x='Lancha', y='Precio', data=df_ganancias, estimator=sum)
st.pyplot(fig2)

# # Otros gráficos o visualizaciones que desees agregar
# visualizacion_actual = 'Día'
# # Configurar la página de Streamlit
# st.title("Dashboard de Lanchas")

# # Gráfico de ganancias por día o mes


# # Mostrar el gráfico
# st.pyplot(fig)


# Cerrar la conexión a la base de datos
session.close()
