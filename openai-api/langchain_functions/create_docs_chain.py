import os
import logging
logging.getLogger().setLevel(logging.INFO)

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.callbacks import get_openai_callback

def create_docs_chain(vectordb, prompt):
  pass