# API Restaurants CASVP

API REST pour accéder aux données des restaurants du Centre d'Action Sociale de la Ville de Paris (CASVP).

## Installation

1. Cloner le dépôt :
```bash
git clone <url-du-depot>
cd api-restaurtants
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Lancer l'application :
```bash
python app.py
```

L'API sera disponible à l'adresse : http://localhost:5000

## Endpoints disponibles

### Page d'accueil
```
GET /
```
Retourne la documentation des endpoints disponibles.

### Liste de tous les restaurants
```
GET /restaurants
```
Retourne la liste complète des restaurants.

### Restaurants par code postal
```
GET /restaurants/{code_postal}
```
Exemple : `/restaurants/75014`

### Restaurants par type
```
GET /restaurants/type/{type}
```
Type peut être `E` ou `S`.
Exemple : `/restaurants/type/E`

### Recherche de restaurants
```
GET /search?q={terme_recherche}
```
Recherche dans les noms, adresses et villes des restaurants.
Exemple : `/search?q=montparnasse`

## Format des données

Chaque restaurant est représenté au format JSON avec les propriétés suivantes :
- `code_postal` : Le code postal du restaurant
- `nom` : Le nom du restaurant
- `adresse` : L'adresse du restaurant
- `ville` : La ville (généralement Paris)
- `latitude` : Coordonnée géographique
- `longitude` : Coordonnée géographique
- `type` : Type de restaurant (E ou S)

## Déploiement en production

Pour le déploiement en production, vous pouvez utiliser Gunicorn :
```bash
gunicorn app:app -b 0.0.0.0:5000
```

## Licence

Ce projet est sous licence libre.
