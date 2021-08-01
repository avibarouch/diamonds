import sklearn.ensemble as ske
import numpy as np
import pandas as pd
import pickle


def build_it():
    df = pd.read_csv("data/diamond.csv")
    X = df.drop(['cut', 'color', 'clarity', 'price'],  axis=1)
    y = df['price']

    # Random Forest Method
    model_rf = ske.RandomForestRegressor()
    model_rf.fit(X, y)

    # Export model to pickle format as 'model.pkl':
    with open('model.pkl', 'wb') as f:
        pickle.dump(model_rf, f)



