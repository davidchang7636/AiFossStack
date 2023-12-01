

import streamlit as st
from src.resources import *

# Set page configuration
st.set_page_config(layout="wide")

#Load index
# db = load_index(index_name = default_index)
index = load_index(index_name = default_index)

# Sidebar with default visibility
with st.sidebar:
    #Model configuration form
    with st.form("App config"):
        st.write("Model configuration")
        temperature = st.number_input("Temp: ", value = temperature , min_value = 0.0, max_value = 1.0, step = 0.1)
        model = st.selectbox('Model :',('zephyr', 'mistral-openorca', 'orca-mini', 'mistral') )
        top_k = st.number_input('Similarity Top K' , value = top_k)
        search_type = st.selectbox('Search type :',('similarity', 'mmr') )
        # submit button
        submitted = st.form_submit_button("Apply")
        if submitted:
            st.write("Temp: ", temperature, "Model: ", model, "top k: ", top_k, "LLM url", base_url, "Search type: ", search_type)

    #Index selector form
    with st.form("Index_Selector"):
        index = load_index(index_name = default_index)
        # active_index = default_index
        st.write("Default index :", default_index)
        selected_index = st.selectbox('Select index :',list_indexes())
        #button
        submitted = st.form_submit_button("Change")
        if submitted:
            index = load_index(index_name = selected_index)
            st.write("Selected index :", selected_index)
                    
    #index creation form
    with st.form("NewIndex"):
        st.write("New index")
        input_dir = st.text_input("From folder (e.g. ./data/): ", value = input_dir)
        index_name = st.text_input("Name: ", value = "Newindex")
        chunk_size = st.number_input('Chunk size' , value = chunk_size)
        chunk_overlap = st.number_input('Chunk overlap' , value = chunk_overlap)
        # submit button
        submitted = st.form_submit_button("Create")
        if submitted:
            docs = load_data(input_dir = input_dir)
            st.write("loaded docs" , len(docs))
            chunks = chunking(docs)
            st.write("chunked docs" , len(chunks))
            # db = vectorize(chunks, index_name = index_name)
            vectorize(chunks, index_name = index_name)
            st.write("vectors stored")
            st.write("done! ")

#### Testing queryng LLM
from langchain.prompts import PromptTemplate
# Build prompt
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)# Run chain

from langchain.chains import RetrievalQA
# expose this index in a retriever interface
retriever = index.as_retriever(search_type="similarity", search_kwargs={"k":5})   #k = 10 gives nice results # can use "mmr" or "similarity"

qa_chain = RetrievalQA.from_chain_type(
    llm=llm, retriever=retriever, return_source_documents=True, chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)
#st.write("Building template and query chain done! ")

### Testing querying

question = st.text_input("Question: ", value = "What is the UN?")
result = qa_chain({"query": question})
# Check the result of the query
result["result"]
# Check the source document from where we 
result["source_documents"][:]
st.write("query done! ")







# testing
# query = "umoja"
# docs = index.similarity_search(query)
# st.write(docs)

#### NEXT STEPS
# create query & response forms
# create text_input to edit the prompt & template

# Use minimum similarity score