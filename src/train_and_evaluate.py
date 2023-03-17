

# load train, test data, 
# train algorithm
# save metrics, params

import os
import pandas as pd
import joblib
import json
import argparse
import numpy as np

from get_data import read_params

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import ElasticNet


def eval_metics(actual, pred):
    '''This method returns mae, rmse, r2-score'''
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

def train_and_evaluate(config_path):
    config = read_params(config_path=config_path)
    
    train_data_path = config["split_data"]["train_path"]
    test_data_path = config["split_data"]["test_path"]
    model_dir = config["model_dir"] # to save trained_model 
  
    alpha = config["estimators"]["ElasticNet"]["params"]["alpha"]
   
    l1_ratio = config["estimators"]["ElasticNet"]["params"]["l1_ratio"]
    
    random_state = config["base"]["random_state"]
    # target column
    target_col = config["base"]["target_col"]

    train = pd.read_csv(train_data_path, sep= ",")
    test = pd.read_csv(test_data_path, sep = ",")
    
    train_x = train.drop(target_col, axis=1)
    test_x = test.drop(target_col, axis=1)
    
    train_y = train[target_col]
    test_y = test[target_col]
    
    lr = ElasticNet(alpha=alpha,
                    l1_ratio=l1_ratio,
                    random_state=random_state)
    lr.fit(train_x, train_y)
    
    predicted_qualities = lr.predict(test_x)

    (rmse, mae, r2) = eval_metics(test_y, predicted_qualities)
    
    print("Elasticnet model (alpha = %f, l1_ratio = %f):" %(alpha, l1_ratio))
    print(" RMSE: %s" % rmse)
    print(" MAE: %s" % mae)
    print(" R2: %s" % r2)
    print(" alpha: %s" % alpha)
    print(" l1_ratio: %s" % l1_ratio)
################################################
    scores_file = config["reports"]["scores"]
    params_file = config["reports"]["params"]

    if not os.path.exists(scores_file):
        with open(scores_file, "w") as f:
            scores = {
                "rmse": rmse,
                "mae": mae,
                "r2": r2
            }
            json.dump(scores, f, indent=4)
            
    if not os.path.exists(params_file):
        with open(params_file, "w") as f:
            params = {
                "alpha": alpha,
                "l1_ratio": l1_ratio,
            }
            json.dump(params, f, indent=4)
        
####################################################

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.joblib")
    joblib.dump(lr, model_path)
    
if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_and_evaluate(config_path=parsed_args.config)