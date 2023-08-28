import pandas as pd
import numpy as np
import joblib
import MyModule_p7
import requests
import shap  # Import the 'shap' module
from flask import Flask, request, jsonify,  send_file, render_template
import subprocess
import os
import json

### les fonctions 
df_train_org = pd.read_csv('./df_train_set_1.csv',
                 usecols=['SECTEUR_ACTIVITE'])
print(df_train_org.head())

freq_by_org_type = df_train_org['SECTEUR_ACTIVITE'].value_counts(normalize=True).to_dict()

def frequency_encode(x):
    return x.replace(freq_by_org_type)
loaded_preprocess = MyModule_p7.preprocess_model()
classification_model = joblib.load('LightGBM_bestmodel.pkl')


def feat_local(df_client_pp):
  # J'instancie le Shap explainer -----------------------------------
  explainer = shap.TreeExplainer(classification_model)

  # Calculate SHAP values for the client's prediction
  shap_values = explainer.shap_values(df_client_pp)
  ##-------- df_pp
  prefixes_to_remove = ['oneHot__', 'remainder__', 'frequency__']
  new_column_names = [col.replace(prefix, '') for col in df_client_pp.columns for prefix in prefixes_to_remove if col.startswith(prefix)]
  df_client_pp.columns = new_column_names
  return shap_values, df_client_pp


###_____________________________ Mon API 

app_prediction = Flask(__name__, static_url_path='/static')
app_prediction.config["DEBUG"] = True

@app_prediction.route('/')
def welcome():
    return render_template('index.html')

# Define a route for the welcome page
@app_prediction.route('/Dashboard/',methods=['POST', 'GET'])
def Dashboard():
    # Receive client ID from the form submission
    client_id = request.form.get('client_id')
    if client_id is not None:
        # Chargement des données client using your module
        client_data = MyModule_p7.get_client_data(client_id)
        # Transformation
        df_client_pp = loaded_preprocess.transform(client_data)
        #Prédiction
        prediction = classification_model.predict(df_client_pp)
        proba = classification_model.predict_proba(df_client_pp)
        score = int(round((proba[0][0])*100)) #probabilité complémentaire
        # Feature analysis using SHAP values
        SV, df_client_pp = feat_local(df_client_pp)
        # Dataframe sv_df
        sv_df = pd.DataFrame(columns=['Class_0', 'Class_1'], index=df_client_pp.columns)
        sv_df['Class_0'] = SV[0].T
        sv_df['Class_1'] = SV[1].T
        sv_df = sv_df.reset_index()
        sv_df = sv_df.to_dict()

        df_client_pp = df_client_pp.to_dict()
    
        dict_prediction =  {
        'client_id': client_id,
        'score': score,
        'feat_imp' :sv_df,
        'client_data' : df_client_pp }
        dict_prediction = dict_prediction.tojson()
        with open('shared_score.json', 'w') as json_file:
                json.dump(dict_prediction, json_file)
                process = subprocess.Popen(["streamlit", "run", os.path.join('streamlit_app.py')]) 
 
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the dynamic Heroku port
    app_prediction.run(host='0.0.0.0', port=port)

