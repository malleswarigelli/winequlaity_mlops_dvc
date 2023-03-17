
# read params
## process, read csv and return dataframe

import os
import yaml
import pandas as pd
import argparse

def read_params(config_path):
    '''This function reads params.yaml file, return dictionary'''
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config # dictionary

def get_data(config_path):
    '''This function access dataset from params.yaml, returns pandas dataframe'''
    config = read_params(config_path) # has dictionary of params.yaml
    data_path = config['data_source']['s3_source']
    df = pd.read_csv(data_path, sep=",", encoding = 'utf-8')
    #print(df.head())
    return df

# this is the entry point for your project
if __name__ == "__main__":
    args = argparse.ArgumentParser()
    # add an argument, calling it as config, default is params.yaml; if forget to provide, program calls pramas.yaml by default
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    get_data(config_path=parsed_args.config)