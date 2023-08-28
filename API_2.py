import pandas as pd
import numpy as np
import joblib
import MyModule_p7
import requests
import shap  # Import the 'shap' module
from flask import Flask, request, jsonify

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


app_prediction = Flask(__name__, static_url_path='/static')
app_prediction.config["DEBUG"] = True

@app_prediction.route('/predict/', methods=['GET', 'POST'])
def prediction_credit():
    data_recu = request.get_json()
    client_id = data_recu.get('client_id') 
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
    
        return {
        'client_id': client_id,
        'score': score,
        'feat_imp' :sv_df,
        'client_data' : df_client_pp
    }
 
if __name__ == '__main__':
    app_prediction.run(host='0.0.0.0', port=7000)

