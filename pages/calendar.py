from streamlit_calendar import calendar
import streamlit as st

calendar_options = {
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
    },
    "slotMinTime": "06:00:00",
    "slotMaxTime": "18:00:00",
    "initialView": "resourceTimelineDay",
    "resourceGroupField": "building",
    "resources": [
        {"id": "a", "building": "Building A", "title": "Building A"},
        {"id": "b", "building": "Building A", "title": "Building B"},
        {"id": "c", "building": "Building B", "title": "Building C"},
        {"id": "d", "building": "Building B", "title": "Building D"},
        {"id": "e", "building": "Building C", "title": "Building E"},
        {"id": "f", "building": "Building C", "title": "Building F"},
    ],
}
calendar_events = [

]
custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modeldb import Administrativo
from streamlit_calendar import calendar
import streamlit as st
# Crea la conexión a la base de datos
engine = create_engine('sqlite:///crud_app.db')
Session = sessionmaker(bind=engine)
session = Session()

# Obtén las fechas de vencimiento desde la base de datos
fechas_vencimiento = session.query(Administrativo.Fecha_Vencimiento_Permit_Prefectura, Administrativo.Fecha_Vencimiento_Matafuegos).all()


calendar_events = []

for fecha in fechas_vencimiento:
    event = {
        "title": "Fecha de vencimiento",
        "start": fecha[0].isoformat(),  # Ajusta el índice si es necesario
        "end": fecha[1].isoformat(),    # Ajusta el índice si es necesario
        # Otros detalles del evento si es necesario
    }
    calendar_events.append(event)

calendar = calendar(events=calendar_events, options=calendar_options, custom_css=custom_css)
st.write(calendar)
