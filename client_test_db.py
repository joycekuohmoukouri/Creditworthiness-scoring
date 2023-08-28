import pandas as pd
import numpy as np
import scipy.stats as stats
import MyModule_p7

##  Importation des données

df_test = pd.read_csv('df_test_set_1.csv',

                 dtype={'SK_ID_CURR' : 'object',
                        'GENRE': 'object',
                      })
cc = pd.read_csv('credit_card_test_set_1.csv',
                 dtype={'SK_ID_CURR' : 'object',
                      })
pos = pd.read_csv('POS_test_set_1.csv',
                 dtype={'SK_ID_CURR' : 'object',
                      })
b_b = pd.read_csv('Bureau_test_set_1.csv',
                 dtype={'SK_ID_CURR' : 'object',
                      })
inst = pd.read_csv('install_test_set_1.csv',
                 dtype={'SK_ID_CURR' : 'object',
                      })


## Préparation du dataset 
df_test = MyModule_p7.merge_(df_test, cc, pos, inst, b_b)
df_test = MyModule_p7.feat_engineering(df_test)
def supp_outliers(df, FEAT, lim_fact, val):
      iqr = stats.iqr(df[FEAT])
      lim = iqr*lim_fact
      df.loc[df[FEAT] >= iqr+ lim, FEAT] = val
      return df

df_test = supp_outliers(df_test, 'CHARGES_ANNUEL',10, np.nan)
df_test.loc[df_test['CC_RATIO_CREDIT'] == np.inf, 'CC_RATIO_CREDIT']= np.nan
df_test= df_test[~(df_test['REVENUS_TOT'].isna())]
df_test = df_test[~(df_test['REMB_ANNUEL'].isna())]
df_test['ANCIENNETE_EMPLOI'].replace(-1015, 0, inplace=True)
df_test = df_test.dropna()

def dpd_status(value):
    if value == 0:
        return 'Pas de retard de paiement'
    elif 0 < value <= 30:
        return 'Retard < 30j'
    else:
        return 'Retard > 30j'

#df_test['NBRE_J_RETARD'] = df_test['NBRE_J_RETARD'].map(dpd_status)

print(df_test.loc[0])

df_test.to_csv('client_test_db.csv', index = False)