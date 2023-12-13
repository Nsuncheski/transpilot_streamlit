from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Lancha(Base):
    __tablename__ = 'lanchas'

    ID_Lancha = Column(Integer, primary_key=True)
    Nombre = Column(String)
    Tipo = Column(String)
    Capacidad = Column(Integer)
    Anio_Fabricacion = Column(Integer)
    # Otros atributos específicos de las lanchas

    mantenimientos = relationship('Mantenimiento', back_populates='lancha')
    tickets = relationship('Ticket', back_populates='lancha')
    administrativos = relationship('Administrativo', back_populates='lancha')

class Mantenimiento(Base):
    __tablename__ = 'mantenimientos'

    ID_Mantenimiento = Column(Integer, primary_key=True)
    ID_Lancha = Column(Integer, ForeignKey('lanchas.ID_Lancha'))
    Tipo_Mantenimiento = Column(String)
    Fecha_Mantenimiento = Column(Date)
    Costo = Column(Float)
    Descripcion = Column(String)
    # Otros detalles del mantenimiento

    lancha = relationship('Lancha', back_populates='mantenimientos')

class Ticket(Base):
    __tablename__ = 'tickets'

    ID_Ticket = Column(Integer, primary_key=True)
    ID_Lancha = Column(Integer, ForeignKey('lanchas.ID_Lancha'))
    Fecha_Viaje = Column(Date)
    Precio = Column(Float)
    # Otros detalles del ticket

    lancha = relationship('Lancha', back_populates='tickets', lazy='joined')

class Administrativo(Base):
    __tablename__ = 'administrativos'

    ID_Administrativo = Column(Integer, primary_key=True)
    ID_Lancha = Column(Integer, ForeignKey('lanchas.ID_Lancha'))
    Fecha_Vencimiento_Permit_Prefectura = Column(Date)
    Fecha_Vencimiento_Matafuegos = Column(Date)
    # Otros detalles administrativos

    lancha = relationship('Lancha', back_populates='administrativos', lazy='joined')

# Aquí deberías tener tu clase Capitan ya definida con su tabla correspondiente

# Crear la base de datos
engine = create_engine('sqlite:///crud_app.db',echo=True)  # Puedes cambiar a tu conexión de base de datos real
Base.metadata.create_all(engine)

