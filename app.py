#todo
#display which index you are using
#create a selector for choosing an indexes
#query an index

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
    st.write("Indexes available: " ,list_files())
    active_index = st.text_input("Type index you want:  " , value="index")

    try:
        st.write("Index is loaded: " , load_index(persist_dir="./indexes/" + active_index))
    except:
        st.write("Please create a new index ")
    
    

elif page == "Indexes":
    st.write("Here's the Indexes page.")

    with st.form("my_form"):
        st.write("Create a new knowledgebase")
        name = st.text_input("Knowledgebase name: ", value = "MyIndex")
        folder = st.text_input("Files folder: ", value = "data")
        embed_model = st.text_input("Embed_model: ", value = "local")

        # submit button
        submitted = st.form_submit_button("Submit")
        if submitted:
            index = index_data(knowledgebase=folder, embed_model=embed_model, index_name=name)
            # st.write("Created a new index: ", name, "From the content folder: ", folder)
            st.write("Created a new index: ", name, "From the content folder: ", folder)


else:
    st.write("You are on the Models page.")

# Add other elements as needed
