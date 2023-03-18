from flask import Flask, render_template, request, jsonify
import os
import numpy as np
# from prediction_service import prediction
import joblib
import yaml

params_path = "params.yaml"
webapp_root = "webapp"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir,template_folder=template_dir)

from src.get_data import read_params
def predict(config_path):
    config = read_params(config_path)
    model_dir_path = config["webapp_model_dir"]
    model = joblib.load(model_dir_path)
    prediction = model.predict(data)
    print(prediction)
    return prediction

def api_response(request):
    try:
        data = np.array([list(request.json.values())])
        response = predict(data)
        response = {"response": response} # as json format
        return response
    except Exception as e:
        print(e)
        error = {"error": "Something went wrong!! Try again"}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pass 
        try:
            # if request coming from webapp
            if request.form:
                # convert request.form to dictionary, get values
                data = dict(request.form).values()
                # since we get data from text as string, convert to float and create nested list
                data = [list(map(float, data))]
                # predict on this data
                response = predict(data)
                return render_template("index.html", response=response)
            
            # if request coming from API/POSTMAN
            elif request.jon:
                response = api_response(request)
                # jsonify result
                return jsonify(response)
                
        except Exception as e:
            print(e)
            error = {"error": "Something went wrong"}
            return render_template("404.html", error=error)
        
    
    else:
        return render_template("index.html")


if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)