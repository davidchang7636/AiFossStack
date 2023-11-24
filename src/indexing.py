import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
from llama_index.llms import Ollama


# def load_data(knowledgebase = "data", embed_model="local", model="zephyr", temperature=0.2):
#     reader = SimpleDirectoryReader(input_dir=knowledgebase, recursive=True)
#     docs = reader.load_data()
#     service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=Ollama(model=model, temperature=temperature))  #try model="zephyr" for better but slower results.
#     index = VectorStoreIndex.from_documents(docs, service_context=service_context)
#     return index

# from llama_index import StorageContext, load_index_from_storage
# Creating a new index
def load_data(knowledgebase = "data", embed_model="local", model="zephyr", temperature=0.2, persist_dir="indexes"):
    reader = SimpleDirectoryReader(input_dir=knowledgebase, recursive=True)
    docs = reader.load_data()
    service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=Ollama(model=model, temperature=temperature))  #try model="zephyr" for better but slower results.
    index = VectorStoreIndex.from_documents(docs, service_context=service_context)
    index.storage_context.persist(persist_dir=persist_dir)
    # storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    # index = load_index_from_storage(storage_context)

#Loading an index from disk
from llama_index import StorageContext, load_index_from_storage
def load_index(embed_model="local", model="zephyr", temperature=0.2, persist_dir="indexes"):
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=Ollama(model=model, temperature=temperature))  #try model="zephyr" for better but slower results.
    index = load_index_from_storage(storage_context, service_context=service_context)


def myfunc():
    return "My name is Jo JO"


welcome_text = "Welcome. Get started by creating an index."


def suma(a,b):
    return a + b