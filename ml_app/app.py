import pickle
from flask import Flask, request, jsonify


app = Flask(__name__)

# Load model
with open("model/iris_model.pkl", "rb") as f:
    model = pickle.load(f)


@app.route("/predict", methods=['GET', 'POST'])
def model_predict():
    
    if request.method == "POST":
        input_json = request.get_json()
        print(f"Data recieved: {input_json['data']}")

        y_pred = model.predict(input_json['data']['ndarray'])

        api_result = {
            'result': y_pred.tolist()
        }
    else:
        api_result = {
            'result': None
        }

    return jsonify(api_result)


if __name__=="__main__":
    app.run(host="0.0.0.0")