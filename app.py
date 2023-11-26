#todo
#Use minimum similarity score
#Configure the system prompt
#allow model and temp selection (on settings tab)

import streamlit as st
from src.indexing import *

# Set page configuration
st.set_page_config(layout="wide")

# Sidebar with default visibility
with st.sidebar:
    st.markdown('Knowledgebases')
    active_index = st.text_input("Active:  " , value="index")
    st.write("Available: " ,list_files())
    try:
        base = load_index(persist_dir="./indexes/" + active_index)
        st.write("Knowledge base loaded")
        query_engine = base.as_query_engine(similarity_top_k=4)
        st.write("Query base ready")
    except:
        st.write("Create a new knowledge base ")

    #Create Knowledgbase
    with st.form("create_knowledgebase"):
        st.write("Create new knowledge base")
        name = st.text_input("Name: ", value = "MyIndex")
        folder = st.text_input("From folder: ", value = "data")
        embed_model = st.text_input("Embedding model: ", value = "local")

        # submit button
        submitted = st.form_submit_button("Create")
        if submitted:
            index = index_data(knowledgebase=folder, embed_model=embed_model, index_name=name)
            st.write("Created a new knowledgebase: ", name, "From the content folder: ", folder)

# Main page area
st.markdown(welcome_text)

#Question zone
with st.form("Question"):
    question = st.text_input("Question: ", value = "Hello.")
    submitted = st.form_submit_button("Ask")
    if submitted:
        response = query_engine.query(question)
        st.write(response.response)
        with st.expander("Show References"):
            for i in range(len(response.source_nodes)):
                st.write(response.source_nodes[i].metadata)
            #st.write(response) <-uncomment to see all info return in the response

