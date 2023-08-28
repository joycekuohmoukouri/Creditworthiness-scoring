import pandas as pd
import numpy as np
import joblib
import MyModule_p7
import requests
import shap  # Import the 'shap' module
from flask import Flask, request, jsonify

#Test communication API 2

app_com2 = Flask(__name__)
app_com2.config["DEBUG"] = True

@app_com2.route('/')
def test2():
    # Get 'a' from the POST request sent by API 1
    data_received = request.json
    
    # Create 'b'
    b = '<h1>assia</h1>'
    
    # Combine 'a' and 'b' in the HTML response
    response_content = f"{data_received}\n{b}"
    
    return data_received

if __name__ == '__main__':
    app_com2.run(host='0.0.0.0', port=5002)