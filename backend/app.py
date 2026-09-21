from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import joblib
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model and preprocessor paths
MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "student_model.keras"
)

PREPROCESSOR_PATH = os.path.join(
    BASE_DIR,
    "model",
    "preprocessor.pkl"
)

# Load trained model
model = tf.keras.models.load_model(MODEL_PATH)

# Load preprocessing object
preprocessor = joblib.load(PREPROCESSOR_PATH)

print("Model loaded successfully!")
print("Preprocessor loaded successfully!")


@app.route("/")
def home():
    return jsonify({
        "message": "Student Performance Prediction API is running!"
    })


@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        # Convert JSON into DataFrame
        input_data = pd.DataFrame([data])

        # Preprocess input
        processed_data = preprocessor.transform(input_data)

        # Make prediction
        prediction = model.predict(
            processed_data,
            verbose=0
        )

        predicted_score = float(prediction[0][0])

        return jsonify({
            "predicted_score": round(predicted_score, 2)
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )