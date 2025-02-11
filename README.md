# Application de Suivi des Dépenses

Une application web Flask pour gérer et visualiser vos dépenses personnelles.

## Fonctionnalités

- 📊 Ajout, modification et suppression de transactions (revenus et dépenses)
- 💰 Catégorisation des transactions
- 📈 Visualisations interactives (graphiques en barres, camembert, ligne)
- 💼 Calcul automatique du solde
- 🎨 Interface utilisateur moderne et responsive
- 🔒 Gestion des erreurs et sécurité renforcée

## Installation

1. Clonez le repository :
```bash
git clone https://github.com/baskaure/finance.git
cd finance
```

2. Créez un environnement virtuel et activez-le :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Lancez l'application :
 ⚠ il faut être dans le dossier parent à finance ⚠
```bash
python -m finance.run
```

L'application sera accessible à l'adresse `http://localhost:5000`

## Structure du Projet

```
finance/
├── __init__.py
├── config.py
├── models.py
├── routes.py
├── forms.py
├── utils.py
├── static/
│   └── css/
│       └── base.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add_transaction.html
│   └── edit_transaction.html
└── run.py
```

## Améliorations des Performances

- Mise en cache des graphiques
- Pagination des transactions
- Requêtes SQL optimisées
- Assets minifiés

## Sécurité

- Protection CSRF
- Validation des entrées
- Gestion sécurisée des sessions
- Échappement automatique des données HTML

## Personnalisation des Graphiques

Trois types de visualisations disponibles :
- Graphique en barres : vue d'ensemble des dépenses par catégorie
- Camembert : répartition des dépenses
- Ligne : évolution des dépenses dans le temps

##

authors Aurélien BRANCO & Dorian TATOULIAN