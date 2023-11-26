# import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
from llama_index.llms import Ollama

# from llama_index import StorageContext, load_index_from_storage
# Creating a new index
def index_data(knowledgebase = "data", embed_model="local", model="zephyr", temperature=0.2, index_name="newindex"):
    persist_dir = "./indexes/" + index_name
    reader = SimpleDirectoryReader(input_dir=knowledgebase, recursive=True)
    docs = reader.load_data()
    service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=Ollama(model=model, temperature=temperature))  #try model="zephyr" for better but slower results.
    index = VectorStoreIndex.from_documents(docs, service_context=service_context)
    index.storage_context.persist(persist_dir=persist_dir)

#Loading an index from disk
from llama_index import StorageContext, load_index_from_storage
def load_index(embed_model="local", model="zephyr", temperature=0.2, persist_dir="./indexes/index"):
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=Ollama(model=model, temperature=temperature))  #try model="zephyr" for better but slower results.
    index = load_index_from_storage(storage_context, service_context=service_context)
    return index

# listing indexes available
import os
def list_files(directory = "./indexes/"):
    return os.listdir(directory)

########## Questions & Answers ######



########## content management ########
welcome_text = "Welcome"