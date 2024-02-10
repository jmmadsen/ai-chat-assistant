import os
import glob
import logging
logging.getLogger().setLevel(logging.INFO)
import requests

from langchain.document_loaders import PyPDFLoader, UnstructuredHTMLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from chromadb.config import Settings

def create_vector_db():
    # connect to OpenAI Embeddings
    embeddings = OpenAIEmbeddings(openai_api_key = os.environ.get('OPENAI_API_KEY'), model = "text-embedding-ada-002")
    
    client_settings = Settings(
        chroma_api_impl = 'rest',
        chroma_server_host = os.environ.get('CHROMA_HOST'),
        chroma_server_http_port = os.environ.get('CHROMA_PORT')
    )
    
    print(client_settings)
    
    # connect if db already exists
    print('***** zero check ******')
    check_chroma = requests.get(os.environ.get('CHROMA_URL') + '/api/v1/collections').json()
    print('***** one check ******')
    print(check_chroma)
    if check_chroma and any(collection for collection in check_chroma if collection['name'] == 'mlb_docs_collection'):
        print('***** two check ******')
        vectordb = Chroma(
            embedding_function = embeddings,
            client_settings = client_settings,
            collection_name = 'mlb_docs_collection'
        )
    # if db does not exist, load documents into vectordb
    else:
        print('***** three check ******')
        documents = []
        # loop through documents and load with appropriate file functions
        for file_path in glob.glob(os.getcwd() + '/training_scripts/*'):
            if file_path.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load_and_split())
            if file_path.endswith('.html'):
                loader = UnstructuredHTMLLoader(file_path)
                documents.extend(loader.load())
            
        print('***** four check ******')
        # chunk documents
        text_splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap = 10)
        chunked_documents = text_splitter.split_documents(documents)
        
        print('***** five check ******')
        vectordb = Chroma.from_documents(
            chunked_documents,
            embedding = embeddings,
            collection_name = 'mlb_docs_collection',
            client_settings = client_settings
        )
        print('***** six check ******')
        
    return vectordb