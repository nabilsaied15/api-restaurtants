from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenue sur L'api Connard "

@app.route('/restaurants', methods=['GET'])
def restaurants():
    df = pd.read_csv("restaurants-casvp.csv", sep=';')
    df.columns = [col.strip() for col in df.columns]
    data = df.to_dict(orient="records")
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
