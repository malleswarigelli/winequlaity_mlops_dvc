

# load train, test data, 
# train algorithm
# save metrics, params

import os
import pandas as pd
import joblib
import json
import argparse
import numpy as np
import urllib
from get_data import read_params

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import ElasticNet
import mlflow
# for tracking uri
from urllib.parse import urlparse

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
    
    ##########################   MLFLOW steps ###########################
    # calling mlflow tracking 
    # create configuration for mlflow listed in params.yaml file
    mlflow_config = config["mlflow_config"]
    # from those keys, we need remote_server_uri
    remote_server_uri = mlflow_config["remote_server_uri"]
    
    # call this server by set tracking remote server uri
    mlflow.set_tracking_uri(remote_server_uri)
    # set experiment i.e coming from config
    mlflow.set_experiment(mlflow_config["experiment_name"])
    
    # before fitting the model, we will call mlflow run
    with mlflow.start_run(run_name=mlflow_config["run_name"]) as mlops_run:
    
        lr = ElasticNet(alpha=alpha,
                        l1_ratio=l1_ratio,
                        random_state=random_state)
        lr.fit(train_x, train_y)
        
        predicted_qualities = lr.predict(test_x)

        (rmse, mae, r2) = eval_metics(test_y, predicted_qualities)
        
        # log metrics and parameters (it will create database, saving metrics automatically)
        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metic("r2", r2)

        # log model
        # urlparse check whether server is on, if yes, logging info into database else creates a folder and store all this info
        tracking_url_type_store = urlparse(mlflow.get_artifact_uri()).scheme
        if tracking_url_type_store != "file":
            mlflow.sklearn.log_model(lr, 
                                     "model", 
                                     registered_model_name=mlflow_config["registered_model_name"])
        else:
            mlflow.sklearn.load_model(lr, "model")
    ######### Model part is done #################################
        
    if __name__=="__main__":
        args = argparse.ArgumentParser()
        args.add_argument("--config", default="params.yaml")
        parsed_args = args.parse_args()
        train_and_evaluate(config_path=parsed_args.config)