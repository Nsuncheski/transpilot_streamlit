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

    st.title("CRUD App with Streamlit")

    # Sidebar for CRUD operations
    menu = ["Create", "Read", "Update", "Delete"]
    lanchas = ["Create", "Read", "Update", "Delete"]
    choice = st.sidebar.selectbox("Select Operation", menu)
    if choice == "Create":
        create_item()
    elif choice == "Read":
        read_items()
    elif choice == "Update":
        update_item()
    elif choice == "Delete":
        delete_item()

# Function to create a new item
def create_item():
    st.header("Create Item")
    name = st.text_input("Enter Item Name:")
    description = st.text_area("Enter Item Description:")
    if st.button("Create"):
        session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
        new_item = Item(name=name, description=description)
        session.add(new_item)
        session.commit()
        st.success("Item created successfully!")

# Function to read all items
def read_items():
    st.header("Read Items")
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    items = session.query(Item).all()
    for item in items:
        st.write(f"ID: {item.id}, Name: {item.name}, Description: {item.description}")

# Function to update an item
def update_item():
    st.header("Update Item")
    item_id = st.number_input("Enter Item ID to Update:")
    new_name = st.text_input("Enter New Name:")
    new_description = st.text_area("Enter New Description:")
    if st.button("Update"):
        session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
        item = session.query(Item).filter(Item.id == item_id).first()
        if item:
            item.name = new_name
            item.description = new_description
            session.commit()
            st.success("Item updated successfully!")
        else:
            st.error("Item not found.")

# Function to delete an item
def delete_item():
    st.header("Delete Item")
    item_id = st.number_input("Enter Item ID to Delete:")
    if st.button("Delete"):
        session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
        item = session.query(Item).filter(Item.id == item_id).first()
        if item:
            session.delete(item)
            session.commit()
            st.success("Item deleted successfully!")
        else:
            st.error("Item not found.")

if __name__ == "__main__":
    main()
