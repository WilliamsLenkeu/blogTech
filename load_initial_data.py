#!/usr/bin/env python
"""
Script pour charger les données initiales dans la base de données Django
Exécutez ce script depuis la racine du projet Django
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from articles.models import Category
from users.models import CustomUser
from django.contrib.auth.hashers import make_password

def load_categories():
    """Charge 20 catégories par défaut si aucune n'existe"""
    
    # Liste des 20 catégories par défaut
    default_categories = [
        'Technologie',
        'Science',
        'Santé',
        'Éducation',
        'Voyage',
        'Cuisine',
        'Sport',
        'Musique',
        'Cinéma',
        'Littérature',
        'Art',
        'Mode',
        'Automobile',
        'Finance',
        'Politique',
        'Environnement',
        'Histoire',
        'Philosophie',
        'Psychologie',
        'Économie'
    ]

    # Vérifier si des catégories existent déjà
    if Category.objects.exists():
        print("ℹ️ Des catégories existent déjà dans la base de données.")
        print(f"   Nombre de catégories existantes : {Category.objects.count()}")
        return

    # Créer les catégories
    categories_created = []
    for category_name in default_categories:
        category = Category.objects.create(name=category_name)
        categories_created.append(category)
        print(f"✅ Catégorie créée : {category_name} (slug: {category.slug})")

    print(f"\n🎉 {len(categories_created)} catégories ont été créées avec succès !")

def main():
    """Fonction principale"""
    print("🚀 Chargement des données initiales...\n")
    
    # Charger les catégories
    print("📚 Chargement des catégories...")
    load_categories()
    print()
    
    print("✨ Chargement des données initiales terminé !")
    print("\nVous pouvez maintenant :")
    print("1. Démarrer le serveur Django : python manage.py runserver")
    print("2. Accéder à l'admin : http://127.0.0.1:8000/admin/")
    print("3. Vous connecter avec admin/admin123")

if __name__ == "__main__":
    main()
