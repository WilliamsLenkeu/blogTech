from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps
from .models import Category


@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    """
    Crée automatiquement 20 catégories par défaut après les migrations
    si aucune catégorie n'existe dans la base de données
    """
    # Vérifier que l'application articles est prête
    if sender.name != 'articles':
        return
    
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
    if not Category.objects.exists():
        # Créer les catégories
        for category_name in default_categories:
            Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': category_name.lower().replace(' ', '-')}
            )
        print(f"✅ {len(default_categories)} catégories par défaut ont été créées automatiquement !")
    else:
        print("ℹ️ Des catégories existent déjà dans la base de données.")
