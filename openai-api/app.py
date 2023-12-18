from flask import Flask, request
import json
from flask_cors import CORS
from datetime import datetime

# utility functions
from utils.exception_handler import exception_handler
from utils.postgres_logging import postgres_logging

# langchain functions
from langchain_functions.create_vector_db import create_vector_db
from langchain_functions.create_docs_chain import create_docs_chain
from langchain_functions.create_sql_chain import create_sql_chain

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# instantiate vectordb to store document embeddings to query
vectordb = create_vector_db()

# ping health of app
@app.route("/health_check")
def health_check():
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

# ask qualitative questions against training documents
@app.route("/docs_chain_query", methods=['POST'])
def docs_chain_query():
    try:
        inbound = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        res, total_tokens, total_cost = create_docs_chain(vectordb, request.json['message'])
        return res
    except Exception as err:
        error = exception_handler(err)
        return error
    finally:
        postgres_logging({
            'prompt': request.json['message'],
            'response': res if 'res' in locals() else error,
            'inbound': inbound,
            'outbound': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'error': True if 'error' in locals() else False,
            'generated_sql': None,
            'total_tokens': total_tokens if 'total_tokens' in locals() else None,
            'total_cost': total_cost if 'total_cost' in locals() else None
        })

# ask quantitative questions against Postgresql - NLP to SQL to NLP
@app.route("/db_chain_query", methods = ['POST'])
def db_chain_query():
    try:
        inbound = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql, res, total_tokens, total_cost = create_sql_chain(request.json['message'])
        return res
    except Exception as err:
        error = exception_handler(err)
        return error
    finally:
        postgres_logging({
            'prompt': request.json['message'],
            'response': res if 'res' in locals() else error,
            'inbound': inbound,
            'outbound': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'error': True if 'error' in locals() else False,
            'generated_sql': sql if 'sql' in locals() else None,
            'total_tokens': total_tokens if 'total_tokens' in locals() else None,
            'total_cost': total_cost if 'total_cost' in locals() else None
        })