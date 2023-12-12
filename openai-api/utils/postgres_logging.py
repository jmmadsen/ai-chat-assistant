import psycopg2
import os
import copy
import logging
logging.getLogger().setLevel(logging.INFO)

# connect to postgresql, insert logs row to "chatgpt_logs" table
def postgres_logging(logs):
    try:
        # create postgresql connection
        conn = psycopg2.connect(
            database = os.environ.get('POSTGRES_DB'), 
            user = os.environ.get('POSTGRES_USER'),
            password = os.environ.get('POSTGRES_PASSWORD'),
            host = os.environ.get('POSTGRES_HOST'),
            port = 5432
        )
        
        # shallow copy parameter obj, then limit prompts and responses to 255 chars to fit in text column
        pg_list = copy.copy(logs)
        pg_list['prompt'] = pg_list['prompt'][:255]
        pg_list['response'] = pg_list['response'][:255]
        
        # create log row
        pg_str = "INSERT INTO chatgpt_logs(prompt, response, inbound, outbound, error, generated_sql, total_tokens, total_cost) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        
        # insert log row into table, then close connection
        cur = conn.cursor()
        cur.execute(pg_str, (pg_list['prompt'], pg_list['response'], pg_list['inbound'], pg_list['outbound'], pg_list['error'], pg_list['generated_sql'], pg_list['total_tokens'], pg_list['total_cost']))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as err:
        logging.error(err)
        pass