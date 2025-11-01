# DU---Project
Le but de ce projet est de permettre à un investisseur d’accéder à un reporting complet sur le fonds géré par une société de gestion dans lequel il a placé son capital.

1. Trois fonds ont été créés, et l’investisseur peut sélectionner celui qu’il souhaite analyser.
2. Les informations affichées sont les suivantes :
3.   - Une vision d’ensemble des principaux indices européens
     - La performance de ces indices depuis la création du fonds
     - Les caracteristiques du fonds
     - Un graphique comparant la performance du fonds à celle de son indice de référence
     - Les principales statistiques du fonds

--------
## 🧩 Structure du projet :

```text
├── config.toml      # Fichier de configuration du projet (fonds, indices, graphes, textes)
├── main.py          # Point d’entrée principal de l’application
├── repository.py    # Fonctions de récupération et de traitement des données financières
├── streamlit.py     # Interface Streamlit pour l’affichage du reporting
├── view.py          # Gestion des graphiques et de la présentation
```
---

## ⚙️ Description des fichiers

---

### `streamlit.py`
Implémente l’**interface utilisateur** à l’aide de Streamlit

---

### `main.py`
Ce fichier lance l’application Streamlit et coordonne les différents modules.
Il charge la configuration via `repository.py`, récupère les sélections de l’utilisateur avec `view.py`, puis affiche les informations, graphiques et statistiques du fonds choisi.

---

### `repository.py`
Contient les **fonctions métiers** :
- Téléchargement des données via `yfinance`
- Calcul des performances et indices de référence
- Normalisation et mise en forme des données pour l’affichage

---

### `view.py`
Gère la partie **visuelle** (graphiques et mise en page) :
Comparaison fonds/benchmark, affichage des indices européens et mise en forme des textes.

---

### `config.toml`
Ce fichier centralise tous les **paramètres du projet** :
- Compositions des fonds (`Fund_1`, `Fund_2`, `Fund_3`) et de leur poids dans le fonds
- Liste des indices boursiers utilisés (Euro Stoxx 50, CAC 40, DAX, IBEX)
- Titres et libellés des pages et graphiques
- Informations légales et avertissements réglementaires
- ...

> 🔧 Ce fichier rend le projet entièrement **paramétrable** sans modifier le code Python.


