import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import re
import seaborn as sns
import missingno as msno
import clean #mon module de fontions qui me permettent de nettoyer un dataframe
import plot_
import joblib
import os
import MyModule_p7

#-------------------------Filter warnings-------------------------
import warnings
warnings.filterwarnings('ignore')
pip install category_encoders --quiet
pip install shap --quiet
pip install Flask

from flask import Flask, request, jsonify



app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Get JSON data from the request
    prediction = your_ml_model_module.predict(data)  # Use your ML model for prediction
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the app on localhost at port 5000
