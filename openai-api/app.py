from flask import Flask
import json

app = Flask(__name__)

# ping health of app
@app.route("/health_check")
def health_check():
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'} 