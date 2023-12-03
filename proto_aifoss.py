import streamlit as st
import llama_index
from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader, StorageContext
from llama_index.llms import Ollama
import time

st.set_page_config(page_title="Local: Chat with your own content!", layout="wide", initial_sidebar_state="auto", menu_items=None)
st.image("logo.png", width=400)
st.title("Your content + your local AI language model = your privacy.")

if "config_state" not in st.session_state:
    st.session_state["config_state"] = False
def close_config():
    st.session_state["config_state"] = True
    st.cache_resource.clear()
    del st.session_state["chat_engine"]
config = st.expander("Configurations", expanded=st.session_state["config_state"])

form = config.form(key='config_form')
knowledgebase = form.text_input("Enter the name of the folder you want to explore:", value="data")
system_prompt = form.text_area("Enter the role this AI assitant should play:" , value="You are my expert advisor. Assume that all questions are related to the data folder indicated above. For each fact you respond always include the reference document and page or paragraph. Keep your answers based on facts. Cite the source document next to each paragraph response you provide. Do not hallucinate features.")
language_model = form.selectbox("Choose the LLM:", ("zephyr", "orca-mini"))
temperature = form.number_input("Choose the temperature (0.0 - 1.0):", 0.0, 1.05, 0.5, 0.05)

save = form.form_submit_button('Save', on_click=close_config)

if st.session_state["config_state"] == True:
    st.session_state["config_state"] = False
    time.sleep(0.1)
    st.rerun()

if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question:"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    persist_dir = "./index"
    with st.spinner(text="Loading and indexing docs – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir=knowledgebase, recursive=True, filename_as_id=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(embed_model="local", llm=Ollama(model=language_model, temperature=temperature))
        
        index = None
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        index = llama_index.load_index_from_storage(storage_context, service_context=service_context)
        refreshed_docs = index.refresh_ref_docs(docs)
        try:
            storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
            index = llama_index.load_index_from_storage(storage_context, service_context=service_context)
            refreshed_docs = index.refresh_ref_docs(docs)
        except:
            index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        index.storage_context.persist(persist_dir=persist_dir)
        return index

index = load_data()

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="context", verbose=True) #modes might be "condense_question" or "context" or "simple"

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            lenght_sources = len(response.source_nodes)
            with st.expander("Show References"):
                for i in range(lenght_sources):
                    st.write(response.source_nodes[i].metadata)
            
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history
