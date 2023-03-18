

import yaml
import os
import json
import joblib
import numpy as np


params_path = "params.yaml"
schema_path = os.path.join("prediction_service", "schema_in.json")

class NotInRange(Exception):
    def __init__(self, message="Values entered are not in expected range"):
        self.message = message
        super().__init__(self.message)

class NotInCols(Exception):
    def __init__(self, message="Not in cols"):
        self.message = message
        super().__init__(self.message)



def read_params(config_path=params_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def predict(data):
    config = read_params(params_path)
    model_dir_path = config["webapp_model_dir"]
    model = joblib.load(model_dir_path)
    prediction = model.predict(data).tolist()[0]
    try:
        # since target column ranges between 3 & 8, we are restricting the predictions
        if 3 <= prediction <= 8:
            return prediction
        else:
            raise NotInRange
    except NotInRange:
        return "Unexpected result"


def get_schema(schema_path=schema_path):
    with open(schema_path) as json_file:
        schema = json.load(json_file)
    return schema

def validate_input(dict_request):
    def _validate_cols(col):
        schema = get_schema()
        actual_cols = schema.keys()
        if col not in actual_cols:
            raise NotInCols

    def _validate_values(col, val):
        schema = get_schema()
        if not (schema[col]["min"] <= float(dict_request[col]) <= schema[col]["max"]) :
            raise NotInRange

    for col, val in dict_request.items():
        # let's validate col name; if matches with schema
        # then, validate range of values
        # _function_ is internal function
        _validate_cols(col)
        _validate_values(col, val)
    
    return True

# if request coming from webapp, use this response
def form_response(dict_request):
    if validate_input(dict_request):
        data = dict_request.values()
        # since its coming from webapp, all values will be as string; so map values to float; then map object to list
        data = [list(map(float, data))]
        response = predict(data)
        return response
    
# if response coming from api, use this response
def api_response(dict_request):
    '''dict_request is dictionary form of response from app.py'''
    try:
        # validate dict_request if follows schema range
        if validate_input(dict_request):
            # if yes, create an array from list of dict values
            data = np.array([list(dict_request.values())])
            # predict daa
            response = predict(data)
            # since it's going to be jsonify, pass it as json response
            response = {"response": response}
            return response
            
    except NotInRange as e:
        response = {"the_expected_range": get_schema(), "response": str(e) }
        return response

    except NotInCols as e:
        response = {"the_expected_cols": get_schema().keys(), "response": str(e) }
        return response


    except Exception as e:
        response = {"response": str(e) }
        return response