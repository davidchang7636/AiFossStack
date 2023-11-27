from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
from llama_index.llms import Ollama

# global variables
model = "mistral-openorca"
temperature = 0.2
embed_model = "local"
llm=Ollama(model=model, temperature=temperature)
similarity_top_k = 10
system_prompt = '''
You are an expert. Write your answer following these criteria:
* Respond exclusively based on the documents provided.
* Cite the exact source next to each paragraph.
* Indicate date, location, and entities related to each fact you cite.
* Write in an elegant, professional, diplomatic style.

If the documents provided do not contain the answer:
* do not generate a response based on your neural network, 
* instead respond with this sentence exactly: "The knowledge base does not have enough information about your question." 

This is the question you are responding: \n
'''

# Creating a new index
def index_data(knowledgebase = "data", embed_model="local", model="zephyr", temperature=0.2, index_name="newindex"):
    persist_dir = "./indexes/" + index_name
    reader = SimpleDirectoryReader(input_dir=knowledgebase, recursive=True)
    docs = reader.load_data()
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)  #try model="zephyr" for better but slower results.
    index = VectorStoreIndex.from_documents(docs, service_context=service_context)
    index.storage_context.persist(persist_dir=persist_dir)

#Loading an index from disk
from llama_index import StorageContext, load_index_from_storage
def load_index(embed_model="local", model="zephyr", temperature=0.2, persist_dir="./indexes/index"):
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    service_context = ServiceContext.from_defaults(llm=llm , embed_model=embed_model)  #try model="zephyr" for better but slower results.
    index = load_index_from_storage(storage_context, service_context=service_context)
    return index

# listing indexes available
import os
def list_files(directory = "./indexes/"):
    return os.listdir(directory)

########## content management ########
welcome_text = '''# Welcome, I am your expert companion. \n ## I will respond only based on the data sources provided to me.'''