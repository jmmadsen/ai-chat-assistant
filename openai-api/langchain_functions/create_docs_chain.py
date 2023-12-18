import os
import logging
logging.getLogger().setLevel(logging.INFO)

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.callbacks import get_openai_callback

def create_docs_chain(vectordb, prompt):
  # connect to OpenAI using LangChain
  llm = ChatOpenAI(api_key = os.environ.get('OPENAI_API_KEY'), model_name = 'gpt-3.5-turbo-1106')
  
  prompt_template = """Your name is mlbGPT. You are a chatbot that will respond to user questions about the 2023 mlb
  season, based on documents you have ingested. Only answer what you know from the documents in the vector db about the 
  2023 mlb season.
  Context: {context}
  Query: {question}
  """
  
  # create prompt for each question sent to bot
  PROMPT = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
  chain_type_kwargs = {"prompt": PROMPT}
  
  docs_chain = RetrievalQA.from_chain_type(
    llm,
    chain_type='stuff',
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={'k': 6}),
    return_source_documents = True,
    verbose = True,
    chain_type_kwargs = chain_type_kwargs
  )
  
  # wrap in callback to track token and cost usage
  with get_openai_callback() as cb:
    result = docs_chain(prompt)
    total_tokens = cb.total_tokens,
    total_cost = cb.total_cost
    
    return result['result'], total_tokens, total_cost