# 📚 Chargement Automatique des Données Initiales

Ce projet Django est configuré pour charger automatiquement 20 catégories par défaut au démarrage du serveur, ainsi que des données de démonstration complètes.

## 🚀 Méthodes de Chargement

### 1. **Chargement Automatique (Recommandé)**
Les catégories se chargent automatiquement au démarrage du serveur grâce aux signaux Django.

**Avantages :**
- ✅ Automatique
- ✅ Pas d'intervention manuelle
- ✅ Se déclenche après chaque migration

### 2. **Script de Démarrage Complet (Nouveau !)**
```bash
python setup_blog.py
```

**Fonctionnalités :**
- ✅ Vérifie les dépendances
- ✅ Charge automatiquement les catégories si nécessaire
- ✅ Charge automatiquement les données de démonstration si nécessaire
- ✅ Configuration complète en une seule commande

### 3. **Commande Django pour les Catégories**
```bash
python manage.py load_categories
```

**Utilisation :**
- Exécutez cette commande depuis la racine du projet
- Utile pour recharger les catégories si nécessaire

### 4. **Commande Django pour les Données de Démonstration (Nouveau !)**
```bash
python manage.py load_demo_data
```

**Options disponibles :**
```bash
# Charger avec des quantités personnalisées
python manage.py load_demo_data --users 15 --articles 30 --comments 75

# Forcer la création même si des données existent
python manage.py load_demo_data --force

# Aide et options
python manage.py load_demo_data --help
```

**Fonctionnalités :**
- ✅ Crée des utilisateurs avec des noms français réalistes
- ✅ Crée des articles dans toutes les catégories
- ✅ Ajoute des commentaires réalistes
- ✅ Crée des likes aléatoires
- ✅ Utilise les catégories déjà préchargées

### 5. **Script Python Autonome**
```bash
python load_initial_data.py
```

**Fonctionnalités :**
- Charge les 20 catégories
- Crée un superutilisateur par défaut (admin/admin123)
- Script complet et autonome

### 6. **Fichiers de Données (Fixtures)**
```bash
python manage.py loaddata articles/fixtures/initial_categories.json
```

## 📋 Liste des 20 Catégories

1. **Technologie** - Articles sur la tech et l'informatique
2. **Science** - Découvertes et recherches scientifiques
3. **Santé** - Bien-être et médecine
4. **Éducation** - Apprentissage et formation
5. **Voyage** - Destinations et conseils voyage
6. **Cuisine** - Recettes et gastronomie
7. **Sport** - Actualités sportives
8. **Musique** - Artistes et événements musicaux
9. **Cinéma** - Films et séries
10. **Littérature** - Livres et auteurs
11. **Art** - Peinture, sculpture, design
12. **Mode** - Tendances et style
13. **Automobile** - Voitures et mobilité
14. **Finance** - Économie et investissement
15. **Politique** - Actualités politiques
16. **Environnement** - Écologie et développement durable
17. **Histoire** - Événements historiques
18. **Philosophie** - Réflexions philosophiques
19. **Psychologie** - Comportement humain
20. **Économie** - Marchés et entreprises

## 🎭 Données de Démonstration

### **Utilisateurs Créés**
- **Admin** : `admin/admin123` (superutilisateur)
- **Utilisateurs normaux** : `username/password123` (générés automatiquement)
- **Noms français réalistes** générés avec Faker
- **Emails uniques** et valides

### **Articles Créés**
- **Titres réalistes** générés automatiquement
- **Contenu en français** avec du texte de qualité
- **Catégories aléatoires** parmi les 20 disponibles
- **Auteurs aléatoires** parmi les utilisateurs créés
- **Dates de création** réparties sur les 30 derniers jours

### **Commentaires Créés**
- **Contenu réaliste** avec 10 types de commentaires différents
- **Auteurs variés** pour chaque commentaire
- **Dates cohérentes** avec la création des articles
- **Distribution aléatoire** sur tous les articles

### **Likes Créés**
- **Distribution aléatoire** : 0 à 8 likes par article
- **Utilisateurs variés** qui likent différents articles
- **Pas de doublons** (un utilisateur ne peut liker qu'une fois)

## ⚙️ Configuration Technique

### **Dépendances Requises**
```bash
pip install -r requirements.txt
```

**Fichier requirements.txt :**
- Django >= 5.2.5
- Faker >= 20.0.0 (pour les données réalistes)

### **Structure des Fichiers**
```
articles/
├── management/
│   └── commands/
│       ├── load_categories.py      # Commande pour les catégories
│       └── load_demo_data.py       # Commande pour les données de démo
├── signals.py                       # Signaux automatiques
├── fixtures/
│   └── initial_categories.json     # Données JSON des catégories
└── apps.py                         # Configuration app

users/
└── fixtures/
    └── initial_users.json          # Utilisateurs par défaut

setup_blog.py                       # Script de démarrage complet
load_initial_data.py                # Script autonome
requirements.txt                     # Dépendances Python
```

### **Signaux Django**
Le fichier `articles/signals.py` utilise le signal `post_migrate` pour :
- Détecter automatiquement le démarrage de l'application
- Vérifier si des catégories existent
- Créer les 20 catégories si la base est vide

### **Configuration App**
Le fichier `articles/apps.py` charge automatiquement les signaux au démarrage.

## 🔧 Utilisation

### **Premier Démarrage (Recommandé)**
```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Configuration complète automatique
python setup_blog.py

# 3. Démarrer le serveur
python manage.py runserver
```

### **Démarrage Manuel Étape par Étape**
```bash
# 1. Charger les catégories
python manage.py load_categories

# 2. Charger les données de démonstration
python manage.py load_demo_data

# 3. Démarrer le serveur
python manage.py runserver
```

### **Rechargement des Données**
```bash
# Recharger les catégories
python manage.py load_categories

# Recharger toutes les données de démonstration
python manage.py load_demo_data --force

# Recharger avec des quantités personnalisées
python manage.py load_demo_data --users 20 --articles 50 --comments 100 --force
```

### **Création d'un Superutilisateur**
```bash
python manage.py createsuperuser
```

## 🚨 Notes Importantes

- **Les catégories ne se créent qu'une seule fois** - si elles existent déjà, rien ne sera modifié
- **Les données de démonstration ne se créent qu'une fois** - utilisez `--force` pour recharger
- **Les slugs sont générés automatiquement** à partir des noms des catégories
- **Les mots de passe par défaut** sont `admin123` (admin) et `password123` (autres utilisateurs)
- **Changez les mots de passe** en production !
- **Les signaux se déclenchent après chaque migration** - utile pour les déploiements

## 🎯 Personnalisation

### **Modifier les Catégories**
1. **Éditer `articles/signals.py`** - modifie la liste `default_categories`
2. **Éditer `articles/management/commands/load_categories.py`** - modifie la même liste
3. **Éditer `load_initial_data.py`** - modifie la même liste
4. **Éditer `articles/fixtures/initial_categories.json`** - modifie le fichier JSON

### **Modifier les Données de Démonstration**
1. **Éditer `articles/management/commands/load_demo_data.py`** - modifie le contenu des articles et commentaires
2. **Ajuster les quantités** avec les paramètres `--users`, `--articles`, `--comments`

### **Modifier les Mots de Passe**
1. **Éditer `articles/management/commands/load_demo_data.py`** - ligne avec `password123`
2. **Éditer `setup_blog.py`** - ligne avec `admin123`

## 🔍 Vérification

### **Dans l'Interface d'Administration**
- Allez sur http://127.0.0.1:8000/admin/
- Connectez-vous avec `admin/admin123`
- Vérifiez les sections :
  - **Catégories** : 20 catégories
  - **Articles** : 25+ articles
  - **Commentaires** : 50+ commentaires
  - **Likes** : likes distribués
  - **Utilisateurs** : 10+ utilisateurs

### **Avec les Commandes Django**
```bash
# Vérifier le nombre d'objets
python manage.py shell
>>> from articles.models import Category, Article, Comment, Like
>>> from users.models import CustomUser
>>> print(f"Catégories: {Category.objects.count()}")
>>> print(f"Articles: {Article.objects.count()}")
>>> print(f"Commentaires: {Comment.objects.count()}")
>>> print(f"Likes: {Like.objects.count()}")
>>> print(f"Utilisateurs: {CustomUser.objects.count()}")
```

---

**🎉 Votre blog est maintenant prêt avec 20 catégories et des données de démonstration complètes !**
