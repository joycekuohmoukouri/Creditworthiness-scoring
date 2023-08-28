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

api_root = 'https://app-jkm-demo-projet7-4712b713aabd.herokuapp.com'

@app.route(api_root)
def welcome():
    return render_template('index.html')

# Define a route for the welcome page
@app.route('/Dashboard/',methods=['POST', 'GET'])
def Dashboard():
    # Receive client ID from the form submission
    client_id = request.form.get('client_id')
    api_url = api_root+'predict/'

    try:
        response = requests.post(api_url, json={'client_id': client_id})
        if response.status_code == 200:
            data = response.json()
            with open('shared_score.json', 'w') as json_file:
                json.dump(data, json_file)
                process = subprocess.Popen(["streamlit", "run", os.path.join('streamlit_app.py')]) 
            return '<h1> Chargement du dashboard ...</h1>'
        else:
            return 'Nope'
    except requests.exceptions.RequestException as e:
        return str(e)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the dynamic Heroku port
    app.run(host='0.0.0.0', port=port)

