import pandas as pd
import numpy as np
import requests
import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
from flask import Flask, request, jsonify,  send_file, render_template
import subprocess
import os
import json

## Création de l'API

app = Flask(__name__, static_url_path='/static')
app.config["DEBUG"] = True

@app.route('/')
def welcome():
    return render_template('/index.html')

# Define a route for the welcome page
@app.route('/Dashboard/',methods=['POST', 'GET'])
def Dashboard():
    # Receive client ID from the form submission
    client_id = request.form.get('client_id')
    api_url = 'https://pacific-badlands-33124-c377cfc7c668.herokuapp.com/predict/'
    response = requests.post(api_url, json={'client_id': client_id})
    if response.status_code == 200:
        data = response.json()
        with open('shared_score.json', 'w') as json_file:
                json.dump(data, json_file)
                #process = subprocess.Popen(["streamlit", "run", os.path.join('streamlit_app.py')]) 
                subprocess.Popen(["streamlit", "run", "streamlit_app.py"])
        return '<h1> Chargement du dashboard ...</h1>'
    else:
        return 'Nope'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))  # Default to port 5000 if not specified
    app.run(host='0.0.0.0', port=port)
    #app.run(threaded=True, port=7001)


