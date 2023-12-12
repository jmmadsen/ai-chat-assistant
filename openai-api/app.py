from flask import Flask
import json
from flask_cors import CORS

# utility functions
from utils.exception_handler import exception_handler
from utils.postgres_logging import postgres_logging

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# ping health of app
@app.route("/health_check")
def health_check():
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

# ask qualitative questions against training documents
@app.route("/docs_chain_query")
def docs_chain_query():
    try:
        return "docs chain"
    except Exception as err:
        error = exception_handler(err)
        return error
    finally:
        postgres_logging({
            'prompt': 'test',
            'response': 'test',
            'inbound': '2016-06-22 19:10:25-07',
            'outbound': '2016-06-22 19:10:25-07',
            'error': False,
            'generated_sql': 'test',
            'total_tokens': 2.5,
            'total_cost': 3.5
        })

# ask quantitative questions against Postgresql - NLP to SQL to NLP
@app.route("/db_chain_query")
def db_chain_query():
    try:
        return "db chain"
    except Exception as err:
        error = exception_handler(err)
        return error
    finally:
        postgres_logging({
            'prompt': 'test',
            'response': 'test',
            'inbound': '2016-06-22 19:10:25-07',
            'outbound': '2016-06-22 19:10:25-07',
            'error': False,
            'generated_sql': 'test',
            'total_tokens': 2.5,
            'total_cost': 3.5
        })