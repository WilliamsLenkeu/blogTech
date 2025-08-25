# 📚 Chargement Automatique des Données Initiales

Ce projet Django est configuré pour charger automatiquement 20 catégories par défaut au démarrage du serveur.

## 🚀 Méthodes de Chargement

### 1. **Chargement Automatique (Recommandé)**
Les catégories se chargent automatiquement au démarrage du serveur grâce aux signaux Django.

**Avantages :**
- ✅ Automatique
- ✅ Pas d'intervention manuelle
- ✅ Se déclenche après chaque migration

### 2. **Commande Django Personnalisée**
```bash
python manage.py load_categories
```

**Utilisation :**
- Exécutez cette commande depuis la racine du projet
- Utile pour recharger les catégories si nécessaire

### 3. **Script Python Autonome**
```bash
python load_initial_data.py
```

**Fonctionnalités :**
- Charge les 20 catégories
- Crée un superutilisateur par défaut (admin/admin123)
- Script complet et autonome

### 4. **Fichiers de Données (Fixtures)**
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

## ⚙️ Configuration Technique

### Structure des Fichiers
```
articles/
├── management/
│   └── commands/
│       └── load_categories.py    # Commande Django
├── signals.py                     # Signaux automatiques
├── fixtures/
│   └── initial_categories.json   # Données JSON
└── apps.py                       # Configuration app

users/
└── fixtures/
    └── initial_users.json        # Utilisateurs par défaut

load_initial_data.py              # Script autonome
```

### Signaux Django
Le fichier `articles/signals.py` utilise le signal `post_migrate` pour :
- Détecter automatiquement le démarrage de l'application
- Vérifier si des catégories existent
- Créer les 20 catégories si la base est vide

### Configuration App
Le fichier `articles/apps.py` charge automatiquement les signaux au démarrage.

## 🔧 Utilisation

### Premier Démarrage
1. **Démarrer le serveur :**
   ```bash
   python manage.py runserver
   ```

2. **Vérifier les catégories :**
   - Aller sur http://127.0.0.1:8000/admin/
   - Se connecter avec vos identifiants admin
   - Vérifier la section "Catégories"

### Rechargement Manuel
Si vous voulez recharger les catégories :
```bash
python manage.py load_categories
```

### Création d'un Superutilisateur
```bash
python manage.py createsuperuser
```

## 🚨 Notes Importantes

- **Les catégories ne se créent qu'une seule fois** - si elles existent déjà, rien ne sera modifié
- **Les slugs sont générés automatiquement** à partir des noms des catégories
- **Le script autonome crée un compte admin temporaire** - changez le mot de passe en production !
- **Les signaux se déclenchent après chaque migration** - utile pour les déploiements

## 🎯 Personnalisation

Pour modifier la liste des catégories :

1. **Éditer `articles/signals.py`** - modifie la liste `default_categories`
2. **Éditer `articles/management/commands/load_categories.py`** - modifie la même liste
3. **Éditer `load_initial_data.py`** - modifie la même liste
4. **Éditer `articles/fixtures/initial_categories.json`** - modifie le fichier JSON

Après modification, redémarrez le serveur pour que les changements prennent effet.

---

**🎉 Votre blog est maintenant prêt avec 20 catégories par défaut !**
