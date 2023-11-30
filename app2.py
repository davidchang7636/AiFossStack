#TO DO
# Use minimum similarity score

import streamlit as st
from src.resources import *

# Set page configuration
st.set_page_config(layout="wide")

# Sidebar with default visibility
with st.sidebar:
    #All configuration form
    with st.form("App config"):
        st.write("App configuration")
        temperature = st.number_input("Temp: ", value = temperature , min_value = 0.0, max_value = 1.0, step = 0.1)
        model = st.selectbox('Model :',('zephyr', 'mistral-openorca', 'orca-mini', 'mistral') )
        top_k = st.number_input('Similarity Top K' , value = top_k)
        search_type = st.selectbox('Search type :',('similarity', 'mmr') )
        active_index = st.selectbox('Select index :',list_indexes() )
        st.write("Active index :", active_index)
#         folder = st.text_input("From folder: ", value = "data")
#         embed_model = st.text_input("Embedding model: ", value = "local")

        # submit button
        submitted = st.form_submit_button("Apply")
        if submitted:
            st.write("Temp: ", temperature, "Model: ", model, "top k: ", top_k, "LLM url", base_url, "Search type: ", search_type, "Active index :", active_index)

#creating an index : wrap these below in a form
    docs = load_data(input_dir = "./data/") #works
    st.write("loaded docs" , len(docs))

    chunks = chunking(docs) #works
    st.write("chunked docs" , len(chunks))

    db = vectorize(chunks, index_name = "totoindex") #works
    st.write("vectors stored")

#create index selector