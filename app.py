import streamlit as st
from src.indexing import *


# Set page configuration
st.set_page_config(layout="wide")

# Custom CSS to set the sidebar background and font
st.markdown(
    """
    <style>
    .css-1d391kg {background-color: #007bff;}
    .font {font-family: 'Font Awesome 6 Free';}
    </style>
    """, unsafe_allow_html=True)

# Sidebar with default visibility
with st.sidebar:
    st.markdown('<p class="font">Navigation</p>', unsafe_allow_html=True)
    page = st.radio("Go to", ("Magic", "Indexes", "Models"))

# Main page area
st.markdown(welcome_text, unsafe_allow_html=True)

if page == "Magic":
    st.write("Here's the Magic page.")
    load_index(persist_dir="indexes")
    st.write("Index is loaded")

elif page == "Indexes":
    st.write("Here's the Indexes page.")

    with st.form("my_form"):
        st.write("Create a new knowledgebase")
        kb_name = st.text_input("Knowledgebase name: ", value = "MyIndex")
        kb_folder = st.text_input("Files folder: ", value = "data")
        embed_model = st.text_input("Embed_model: ", value = "local")
        persist_dir = st.text_input("Index storage location: " , value = "indexes")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            lala = load_data(knowledgebase=kb_folder,embed_model=embed_model, persist_dir=persist_dir)
            st.write("Knowledgebase name: ", kb_name, "Content folder: ", kb_folder, "Storage directory:" , persist_dir)

# def load_data(knowledgebase = "data", embed_model="local", model="zephyr", temperature=0.2):

else:
    st.write("You are on the Models page.")

# Add other elements as needed
