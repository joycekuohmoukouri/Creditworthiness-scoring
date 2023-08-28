import pandas as pd
import numpy as np
import joblib
import MyModule_p7
import requests
import shap  # Import the 'shap' module
from flask import Flask, request, jsonify

# This is the data you want to send
# Create some test data for our catalog in the form of a list of dictionaries.
books = [
{'id': 0,
'title': 'A Fire Upon the Deep',
'author': 'Vernor Vinge',
'first_sentence': 'The coldsleep itself was dreamless.',
'year_published': '1992'},
{'id': 1,
'title': 'The Ones Who Walk Away From Omelas',
'author': 'Ursula K. Le Guin',
'first_sentence': 'With a clamor of',
'published': '1973'},
{'id': 2,
'title': 'Dhalgren',
'author': 'Samuel R. Delany',
'first_sentence': 'to wound the autumnal city.',
'published': '1975'}
]
#Test communication API 

app = Flask(__name__)
app.config["DEBUG"] = True
@app.route('/', methods=['GET'])
def test(): 
    response = requests.post('http://localhost:5002/', json=books)
    # Process the response from API 2
    if response.status_code == 200:
        response_data = response.json()
        return jsonify({'message': 'Data sent successfully to API 2', 'response_data': response_data})
    else:
        return jsonify({'message': 'Failed to send data to API 2'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)




