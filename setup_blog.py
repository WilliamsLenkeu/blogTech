#!/usr/bin/env python
"""
Script de démarrage complet pour le blog Django
Charge automatiquement les catégories et les données de démonstration
"""

import os
import sys
import subprocess
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from articles.models import Category, Article
from users.models import CustomUser

def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"\n🔄 {description}...")
    print(f"   Commande : {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            print(f"✅ {description} terminé avec succès")
            if result.stdout:
                print(f"   Sortie : {result.stdout.strip()}")
        else:
            print(f"❌ Erreur lors de {description}")
            if result.stderr:
                print(f"   Erreur : {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ Exception lors de {description} : {e}")
        return False
    
    return True

def check_dependencies():
    """Vérifie que les dépendances sont installées"""
    print("🔍 Vérification des dépendances...")
    
    try:
        import faker
        print("✅ Faker est installé")
    except ImportError:
        print("❌ Faker n'est pas installé")
        print("   Installation : pip install Faker")
        return False
    
    try:
        import django
        print("✅ Django est installé")
    except ImportError:
        print("❌ Django n'est pas installé")
        print("   Installation : pip install Django")
        return False
    
    return True

def check_database():
    """Vérifie l'état de la base de données"""
    print("\n🔍 Vérification de la base de données...")
    
    try:
        # Vérifier les catégories
        categories_count = Category.objects.count()
        print(f"   Catégories : {categories_count}")
        
        # Vérifier les articles
        articles_count = Article.objects.count()
        print(f"   Articles : {articles_count}")
        
        # Vérifier les utilisateurs
        users_count = CustomUser.objects.count()
        print(f"   Utilisateurs : {users_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de la base : {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Configuration complète du blog Django")
    print("=" * 50)
    
    # 1. Vérifier les dépendances
    if not check_dependencies():
        print("\n❌ Veuillez installer les dépendances manquantes")
        return
    
    # 2. Vérifier la base de données
    if not check_database():
        print("\n❌ Problème avec la base de données")
        return
    
    # 3. Charger les catégories si nécessaire
    if Category.objects.count() == 0:
        print("\n📚 Aucune catégorie trouvée, chargement des catégories...")
        if not run_command(
            "python manage.py load_categories",
            "Chargement des catégories"
        ):
            print("❌ Échec du chargement des catégories")
            return
    else:
        print("\n✅ Les catégories sont déjà chargées")
    
    # 4. Charger les données de démonstration si nécessaire
    if Article.objects.count() == 0:
        print("\n🎭 Aucun article trouvé, chargement des données de démonstration...")
        if not run_command(
            "python manage.py load_demo_data",
            "Chargement des données de démonstration"
        ):
            print("❌ Échec du chargement des données de démonstration")
            return
    else:
        print("\n✅ Des articles existent déjà")
    
    # 5. Vérification finale
    print("\n🔍 Vérification finale...")
    if not check_database():
        print("❌ Problème lors de la vérification finale")
        return
    
    # 6. Résumé et instructions
    print("\n" + "=" * 50)
    print("🎉 CONFIGURATION TERMINÉE AVEC SUCCÈS !")
    print("=" * 50)
    
    print("\n📊 État de votre blog :")
    print(f"   🏷️  Catégories : {Category.objects.count()}")
    print(f"   📝 Articles : {Article.objects.count()}")
    print(f"   👥 Utilisateurs : {CustomUser.objects.count()}")
    
    print("\n🔑 Identifiants de connexion :")
    print("   Admin : admin/admin123")
    print("   Autres utilisateurs : username/password123")
    
    print("\n🌐 Prochaines étapes :")
    print("   1. Démarrer le serveur : python manage.py runserver")
    print("   2. Accéder à l'admin : http://127.0.0.1:8000/admin/")
    print("   3. Explorer votre blog !")
    
    print("\n🛠️  Commandes utiles :")
    print("   - Recharger les catégories : python manage.py load_categories")
    print("   - Recharger les données : python manage.py load_demo_data --force")
    print("   - Créer un superuser : python manage.py createsuperuser")
    
    print("\n✨ Votre blog est maintenant prêt !")

if __name__ == "__main__":
    main()
