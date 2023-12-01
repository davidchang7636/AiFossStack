import streamlit as st
from src.resources import *

# Set page configuration
st.set_page_config(layout="wide")

#Load index
try:
    index = load_index(index_name = default_index)
except:
    st.write("No initial index")

# Sidebar with default visibility
with st.sidebar:

    #Index selector form
    with st.form("Index_Selector"):
        index = load_index(index_name = default_index)
        st.write("## Default knowledge base:", default_index)
        selected_index = st.selectbox('Change:',list_indexes())
        #button
        submitted = st.form_submit_button("Apply changes")
        if submitted:
            index = load_index(index_name = selected_index)
            st.write("You've selected index:", selected_index)
                    
    #index creation form
    with st.expander("## Create a new index", expanded=False):
        with st.form("NewIndex"):
            st.write("## Create a new index:")
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
                vectorize(chunks, index_name = index_name)
                st.write("vectors stored")
                st.write("done! ")
    
    #Model configuration form
    with st.expander("Model configuration", expanded=False):
        with st.form("App config"):
            st.write("Model configuration (not implemented yet)")
            temperature = st.number_input("Temp: ", value = temperature , min_value = 0.0, max_value = 1.0, step = 0.1)
            model = st.selectbox('Model :',('zephyr', 'mistral-openorca', 'orca-mini', 'mistral') )
            top_k = st.number_input('Similarity Top K' , value = top_k)
            search_type = st.selectbox('Search type :',('similarity', 'mmr') )
            # submit button
            submitted = st.form_submit_button("Apply")
            if submitted:
                st.write("Temp: ", temperature, "Model: ", model, "top k: ", top_k, "LLM url", base_url, "Search type: ", search_type)

#### Building the querying chain LLM ######
from langchain.prompts import PromptTemplate
# Build prompt
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)# Load a template with system prompts
# define a retriever 
from langchain.chains import RetrievalQA
retriever = index.as_retriever(search_type="similarity", search_kwargs={"k":5})   #k = 10 gives nice results # can use "mmr" or "similarity"
# assemble all
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, 
return_source_documents=True, chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

########## Main page area ########
st.image("logo.png", width=400)
st.title("Your content + your local AI = your privacy.")
st.markdown(app_welcome_text)  #Welcome text edit it on the rsources.py file

####### Query formm
#index creation form
with st.form("Query"):
    question = st.text_area("Task me!", value = default_question)
    # submit button
    submitted = st.form_submit_button("Go")
    if submitted:
        result = qa_chain({"query": question})
        st.write(result["result"])
        with st.expander("References: ", expanded=False):
            result["source_documents"][:]







### Tests ###
# question = st.text_input("Question: ", value = "What is the UN?")
# result = qa_chain({"query": question})
# # Check the result of the query
# result["result"]
# # Check the source document from where we 
# result["source_documents"][:]
# st.write("query done! ")







# testing
# query = "umoja"
# docs = index.similarity_search(query)
# st.write(docs)

#### NEXT STEPS
# create query & response forms
# create text_input to edit the prompt & template

# Use minimum similarity score