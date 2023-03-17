
import os
from get_data import read_params, get_data 
import argparse

def load_and_save(config_path):
    '''Function loads dataframe from get_data.py, save into raw directory'''
    config = read_params(config_path)
    df = get_data(config_path)
    # alter column headers
    new_cols = [col.replace(" ","_") for col in df.columns]
    # get path for saving df
    raw_data_path = config["load_data"]["raw_dataset_csv"]
    #print(raw_data_path)
    # now save df to raw_data_path
    df.to_csv(raw_data_path, sep=",", index=False, header=new_cols)
    
if __name__ == "__main__":
    args = argparse.ArgumentParser()
    # add an argument, calling it as config, default is params.yaml; if forget to provide, program calls pramas.yaml by default
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    load_and_save(config_path=parsed_args.config)    