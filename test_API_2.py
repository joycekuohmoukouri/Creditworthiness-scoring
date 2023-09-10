import pytest
from API_2 import app_prediction
from unittest.mock import patch
import requests
import json
import pandas as pd
import numpy as np
import joblib
import MyModule_p7
import shap  # Import the 'shap' module
from flask import Flask, request, jsonify
from projet7package.frequency_encode import frequency_encode

@pytest.fixture
#Je crée un test 'client'
def client():
    with app_prediction.test_client() as client:
        yield client
    
def test_welcome_route(client):
    response = client.get('/')
    assert response.status_code == 200  # Je teste si j'obtiens un code 200

def test_prediction_credit_route(client):
    input_data = {'client_id': '100066'}
    # Send a POST request to the /predict/ route with JSON data
    response = client.post('/predict/', data=input_data)
    assert response.status_code == 200
    data_recu = response.json()
    assert 'client_id' in data_recu
    assert 'score' in data_recu
    assert 'feat_imp' in data_recu
    assert 'client_data' in data_recu
