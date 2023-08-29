# Test du package projet-7-package
import pandas as pd
import MyModule_p7
from projet7package.frequency_encode import frequency_encode

data = pd.read_csv('client_test_db.csv', nrows = 1)
loaded_preprocess = MyModule_p7.preprocess_model()
data_bis = loaded_preprocess.transform(data)
print(data_bis)