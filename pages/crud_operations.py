import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker

st.set_page_config(page_title="Basic CRUD Operations Demo", layout="wide")
st.title("🗂️ Basic CRUD Operations")

# Setup: SQLite DB in memory (or use 'sqlite:///mydb.db' for file persistence)
engine = create_engine('sqlite:///crud_demo.db', echo=False)
metadata = MetaData()

# Define a users table (id, name, email)
users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String),
)
metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# CREATE
st.subheader("Create New User")
new_name = st.text_input("Name")
new_email = st.text_input("Email")
if st.button("Add User"):
    with engine.connect() as conn:
        conn.execute(users.insert().values(name=new_name, email=new_email))
    st.success(f"User '{new_name}' added!")

# READ
st.subheader("All Users")
with engine.connect() as conn:
    df = pd.read_sql(users.select(), conn)
st.dataframe(df)

# UPDATE
st.subheader("Update Existing User")
selected_id = st.number_input("User ID to update", min_value=1, step=1)
new_name_update = st.text_input("New Name")
new_email_update = st.text_input("New Email")
if st.button("Update User"):
    with engine.connect() as conn:
        result = conn.execute(
            users.update().where(users.c.id == selected_id)
            .values(name=new_name_update, email=new_email_update)
        )
    st.success(f"User ID '{selected_id}' updated!")

# DELETE
st.subheader("Delete User")
delete_id = st.number_input("User ID to delete", min_value=1, step=1, key="delete")
if st.button("Delete User"):
    with engine.connect() as conn:
        result = conn.execute(users.delete().where(users.c.id == delete_id))
    st.success(f"User ID '{delete_id}' deleted!")

st.markdown("---")