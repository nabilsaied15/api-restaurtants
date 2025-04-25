from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # ✅ Activation réelle de CORS

# Configuration
CSV_FILE = "restaurants-casvp-with-images.csv"
CSV_SEPARATOR = ";"

def load_data():
    """Charge les données des restaurants depuis le fichier CSV"""
    try:
        if not os.path.exists(CSV_FILE):
            return [], f"Fichier {CSV_FILE} introuvable"

        df = pd.read_csv(CSV_FILE, sep=CSV_SEPARATOR)
        df.columns = [col.strip() for col in df.columns]

        # Nettoyage des données
        df.fillna("", inplace=True)

        # Conversion des coordonnées géographiques (depuis 'tt')
        if 'tt' in df.columns:
            df['latitude'] = df['tt'].apply(lambda x: x.split(',')[0].strip() if isinstance(x, str) and ',' in x else "")
            df['longitude'] = df['tt'].apply(lambda x: x.split(',')[1].strip() if isinstance(x, str) and ',' in x else "")

        # Standardisation des noms de colonnes
        df.rename(columns={
            'code': 'code_postal',
            'Nom restaurant': 'nom',
            'TYPE': 'type'
        }, inplace=True)

        return df.to_dict(orient="records"), None
    except Exception as e:
        return [], str(e)

@app.route('/')
def home():
    """Page d'accueil avec documentation de base"""
    return jsonify({
        "message": "Bienvenue sur l'API des restaurants du CASVP",
        "endpoints": {
            "/restaurants": "Liste tous les restaurants",
            "/restaurants/<code_postal>": "Restaurants par code postal",
            "/restaurants/type/<type>": "Restaurants par type (E/S)",
            "/search?q=mot": "Recherche globale (nom, adresse, ville)"
        },
        "version": "1.1"
    })

@app.route('/restaurants', methods=['GET'])
def get_all_restaurants():
    data, error = load_data()
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"count": len(data), "restaurants": data})

@app.route('/restaurants/<code_postal>', methods=['GET'])
def get_restaurant_by_code(code_postal):
    data, error = load_data()
    if error:
        return jsonify({"error": error}), 500

    restaurants = [r for r in data if str(r.get('code_postal', '')).strip() == code_postal]
    if not restaurants:
        return jsonify({"message": f"Aucun restaurant trouvé avec le code postal {code_postal}"}), 404

    return jsonify({"count": len(restaurants), "restaurants": restaurants})

@app.route('/restaurants/type/<type>', methods=['GET'])
def get_restaurant_by_type(type):
    data, error = load_data()
    if error:
        return jsonify({"error": error}), 500

    type = type.upper()
    restaurants = [r for r in data if str(r.get('type', '')).strip().upper() == type]
    return jsonify({"count": len(restaurants), "restaurants": restaurants})

@app.route('/search', methods=['GET'])
def search_restaurants():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"error": "Paramètre de recherche 'q' requis"}), 400

    data, error = load_data()
    if error:
        return jsonify({"error": error}), 500

    results = [r for r in data if
               query in str(r.get('nom', '')).lower() or
               query in str(r.get('adresse', '')).lower() or
               query in str(r.get('ville', '')).lower()]
    return jsonify({"count": len(results), "query": query, "restaurants": results})

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route non trouvée"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Erreur serveur interne"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
