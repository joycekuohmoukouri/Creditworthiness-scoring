import pandas as pd
import numpy as np
import requests
import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
from flask import Flask, request, jsonify, send_file, render_template, redirect
import subprocess
import os
import json

## Création de l'API

app = Flask(__name__, static_url_path='/static')
app.config["DEBUG"] = True

dashboard_data = {}

@app.route('/')
def welcome():
    return render_template('/index.html')

# Define a route for the welcome page
@app.route('/Dashboard/',methods=['GET','POST'])
def Dashboard():
    # Receive client ID from the form submission
    client_id = request.form.get('client_id')
    api_url = 'https://pacific-badlands-33124-c377cfc7c668.herokuapp.com/predict/'
    headers = {'Content-Type': 'application/json'} 
    response = requests.post(api_url, json={'client_id': client_id}, headers=headers)
    data = response.json()
      # Store the data in the global variable
    global dashboard_data
    dashboard_data = data
    subprocess.Popen(["streamlit", "run", "https://dashboard-projet-7-jkm-bcf05f5e28fb.herokuapp.com"])
    return '<h1> Chargement du dashboard </h1> '


@app.route('/Dashboard_st/',methods=['GET',])
def another_endpoint():
    global dashboard_data
    if not dashboard_data:
        return jsonify({'error': 'No data available from the Dashboard.'}), 404
    
    return jsonify(dashboard_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))  # Default to port 5000 if not specified
    app.run(host='0.0.0.0', port=port)



