import os
import glob
import logging
logging.getLogger().setLevel(logging.INFO)

from langchain.document_loaders import PyPDFLoader, UnstructuredHTMLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

def create_vector_db():
    # connect to OpenAI Embeddings
    embeddings = OpenAIEmbeddings(openai_api_key = os.environ.get('OPENAI_API_KEY'), model = "text-embedding-ada-002")
    
    # connect if db already exists
    if os.path.isdir(os.getcwd() + '/data'):
        vectordb = Chroma(
            persist_directory = './data',
            embedding_function = embeddings
        )
    # if db does not exist, load documents into vectordb
    else:
        documents = []

        # loop through documents and load with appropriate file functions
        for file_path in glob.glob(os.getcwd() + '/training_scripts/*'):
            if file_path.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load_and_split())
            if file_path.endswith('.html'):
                loader = UnstructuredHTMLLoader(file_path)
                documents.extend(loader.load())
            
        # chunk documents
        text_splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap = 10)
        chunked_documents = text_splitter.split_documents(documents)
        
        vectordb = Chroma.from_documents(
            chunked_documents,
            embedding = embeddings,
            persist_directory = './data'
        )
        
    return vectordb