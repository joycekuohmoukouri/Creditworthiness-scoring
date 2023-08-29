import pandas as pd
import numpy as np
import requests
import joblib
import MyModule_p7
import shap  # Import the 'shap' module
import os
from flask import Flask, request, jsonify
from projet7package.frequency_encode import frequency_encode

app_prediction = Flask(__name__, static_url_path='/static')
app_prediction.config["DEBUG"] = True

@app_prediction.route('/')
def welcome():
    return "<h1> Hello world </h1>"

@app_prediction.route('/predict/', methods=['GET', 'POST'])
def prediction_credit():
    from projet7package.frequency_encode import frequency_encode
    data_recu = request.get_json()
    client_id = data_recu.get('client_id') 
    if client_id is not None:
        # Chargement des données client using your module
        client_data = MyModule_p7.get_client_data(client_id)
        # Transformation
        loaded_preprocess = MyModule_p7.preprocess_model()
        df_client_pp = loaded_preprocess.transform(client_data)
        df_client_pp = df_client_pp.to_dict()

        return jsonify({'client_id': client_id,
                'client_data' : df_client_pp})
            
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to port 5000 if not specified
    app_prediction.run(host='0.0.0.0', port=port)
    #app_prediction.run(threaded=True, port=7000)

