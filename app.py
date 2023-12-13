# Import necessary libraries
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up database connection
DATABASE_URL = "sqlite:///crud_app.db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

# Define the data model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Set up Streamlit app
def main():

    st.title("Transpilot")

    # Sidebar for CRUD operations


if __name__ == "__main__":
    main()
