import pandas as pd
import numpy as np
import scipy.stats as stats
import MyModule_p7

##  Importation des données

df_train = pd.read_csv('df_train_set_1.csv',

                 dtype={'SK_ID_CURR' : 'object',
                        'GENRE': 'object',
                      })
cc = pd.read_csv('credit_card_train_set_1.csv',
                 dtype={'SK_ID_CURR' : 'object',
                      })
pos = pd.read_csv('POS_train_set_1.csv',
                 dtype={'SK_ID_CURR' : 'object',
                      })
b_b = pd.read_csv('Bureau_train_set_1.csv',
                 dtype={'SK_ID_CURR' : 'object',
                      })
inst = pd.read_csv('install_train_set_1.csv',
                 dtype={'SK_ID_CURR' : 'object',
                      })


## Préparation du dataset 
df_train = MyModule_p7.merge_(df_train, cc, pos, inst, b_b)
df_train = MyModule_p7.feat_engineering(df_train)
def supp_outliers(df, FEAT, lim_fact, val):
      iqr = stats.iqr(df[FEAT])
      lim = iqr*lim_fact
      df.loc[df[FEAT] >= iqr+ lim, FEAT] = val
      return df

df_train = supp_outliers(df_train, 'CHARGES_ANNUEL',10, np.nan)
df_train.loc[df_train['CC_RATIO_CREDIT'] == np.inf, 'CC_RATIO_CREDIT']= np.nan
df_train= df_train[~(df_train['REVENUS_TOT'].isna())]
df_train = df_train[~(df_train['REMB_ANNUEL'].isna())]
df_train['ANCIENNETE_EMPLOI'].replace(-1015, 0, inplace=True)
df_train = df_train.dropna()

def dpd_status(value):
    if value == 0:
        return 'Pas de retard de paiement'
    elif 0 < value <= 30:
        return 'Retard < 30j'
    else:
        return 'Retard > 30j'

#df_train['NBRE_J_RETARD'] = df_train['NBRE_J_RETARD'].map(dpd_status)

print(df_train.loc[0])
df_train.to_csv('client_train_db.csv', index = False)