# Import libraries
import pandas as pd
import numpy as np
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

import logging

logging.basicConfig(level=logging.INFO)

# import warnings

# warnings.filterwarnings("ignore", category=UserWarning)

# Load Data
heart = pd.read_csv('data/heart_cleveland_upload.csv')

# Rename columns based on data dictionary
heart_new = heart.copy()
heart_new['sex'] = heart_new['sex'].replace([0,1],['Female','Male'])
heart_new['exang'] = heart_new['exang'].replace([0,1],['No','Yes'])
heart_new['fbs'] = heart_new['fbs'].replace([0,1],['<120 mg/dl','>120 mg/dl'])
heart_new['restecg'] = heart_new['restecg'].replace([0,1,2],['Normal','ST-T wave abnormality','Left ventricular hypertrophy'])
heart_new['cp'] = heart_new['cp'].replace([0,1,2,3],['Typical angina','Atypical angina','Non-anginal pain','Asymptomatic'])
heart_new['slope'] = heart_new['slope'].replace([0,1,2],['Upsloping', 'Flat', 'Downsloping'])
heart_new['thal'] = heart_new['thal'].replace([0,1,2],['Normal','Fixed defect','Reversable defect'])

# Import libraries
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn import metrics

# Split data
def train_model(model, data):
    # Split data into x and y
    y = data.iloc[:, -1].values
    x = data.iloc[:, 0:-1].values


    # Split into train and test
    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.2, stratify = y, random_state = 0)

    # Set categorical and numerical columns
    categorical_cols = [1, 2, 5, 6, 8, 10, 12]
    numerical_cols = [0, 3, 4, 7, 9, 11]

    # Scale based on training data
    sc_x = StandardScaler()
    x_train[:, numerical_cols] = sc_x.fit_transform(x_train[:, numerical_cols])
    x_test[:, numerical_cols] = sc_x.transform(x_test[:, numerical_cols])

    # One hot encode train and apply to test
    ct = ColumnTransformer([('Encoder',
                                 OneHotEncoder(drop = 'first',
                                               categories = 'auto'),
                             categorical_cols)],
                           remainder = 'passthrough')

    x_train = ct.fit_transform(x_train)
    x_test = ct.transform(x_test)

    # Train model
    model.fit(x_train, y_train)
    
    # Save data objects
    pickle.dump(sc_x, open('model/scaler.pkl', 'wb'))
    pickle.dump(ct, open('model/column_transformer.pkl', 'wb'))

    # Evaluate on test data
    test_preds = model.predict(x_test)
    test_proba = model.predict_proba(x_test)[:,1]

    return test_preds, y_test, test_proba

# Logistic Regression
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr_preds, y_test, y_proba = train_model(lr, heart_new)

# Dump model into pickle file
pickle.dump(lr, open('model/model_lr.pkl', 'wb'))