import os
from langchain.utilities import SQLDatabase
from langchain.chat_models import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback

import logging
logging.getLogger().setLevel(logging.INFO)

def create_sql_chain(prompt):
  
  # connect to postgres db
  postgres_connection = 'postgresql://' + os.environ.get('POSTGRES_USER') + ':' + os.environ.get('POSTGRES_PASSWORD') + '@' + os.environ.get('POSTGRES_HOST') + '/' + os.environ.get('POSTGRES_DB')
  # sample rows to send to LLM
  sample_rows = 5
  # identify which table metadata to send for query building
  db = SQLDatabase.from_uri(postgres_connection, sample_rows_in_table_info = sample_rows, include_tables = ['batting_averages_2023'])
  
  # connect to OpenAI
  llm = ChatOpenAI(api_key = os.environ.get('OPENAI_API_KEY'), model_name = 'gpt-3.5-turbo-1106')
  
  # prompt for querying the 2023 batting averages table
  _DEFAULT_TEMPLATE = """
  Given an input, first create a syntactically correct {dialect} query to run, then look at the results of the query
  and return the answer succinctly.
  
  Question: "Question here"
  SQLQuery: "SQL Query to run"
  SQLResult: "Result of the SQLQuery"
  Answer: "Final answer here"
  
  Only use the following table: {table_info}
  
  Question: {input}
  """
  
  PROMPT = PromptTemplate(
    input_variables = ['input', 'table_info', 'dialect'], template = _DEFAULT_TEMPLATE
  )
  
  # create chain with prompt and generating intermediate steps
  db_chain = SQLDatabaseChain.from_llm(llm, db, prompt = PROMPT, verbose = True, use_query_checker = True, return_intermediate_steps = True, top_k = 5)
  # wrap in callback to track token and cost usage
  with get_openai_callback() as cb:
    result = db_chain(prompt)
    generated_sql = result['intermediate_steps'][2]['sql_cmd']
    response = result['result']
    
    # usage
    total_tokens = cb.total_tokens
    total_cost = cb.total_cost
    
    return (generated_sql, response, total_tokens, total_cost)