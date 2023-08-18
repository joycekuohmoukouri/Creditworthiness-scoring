import pandas as pd
import numpy as np
import joblib
import requests
import MyModule_p7
from lightgbm import LGBMClassifier
import sklearn

from flask import Flask, request, jsonify
df_train_org = pd.read_csv('df_train_set_1.csv',
                 usecols=['SECTEUR_ACTIVITE'])
freq_by_org_type = df_train_org['SECTEUR_ACTIVITE'].value_counts(normalize=True).to_dict()
def frequency_encode(x):
    return x.replace(freq_by_org_type)
## CHARGEMENT DU PREPROCESING--------------------------------------------------------------
loaded_preprocess = MyModule_p7.preprocess_model()

# CHARGEMENT DE MON MODÈLE DE CLASSIFICATION 
classification_model = joblib.load('LightGBM_bestmodel.pkl')

## Création de l'API

#app = Flask(__name__)

#@app.route('/predict', methods=['POST'])
def prediction_credit():
    client_id = input("Entrer id_clients")
    #data = request.get_json()
    #client_id = data.get('client_id')
    ######------- Importation des données clients 
    client_data = MyModule_p7.get_client_data(client_id)
    df_client_pp = loaded_preprocess.transform(client_data)
    prediction = classification_model.predict(df_client_pp)
    #response_from_other_api = communicate_with_other_api(prediction)

    return {'prediction': prediction}

prediction_credit()


