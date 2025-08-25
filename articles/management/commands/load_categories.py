from django.core.management.base import BaseCommand
from articles.models import Category


class Command(BaseCommand):
    help = 'Charge 20 catégories par défaut dans la base de données'

    def handle(self, *args, **options):
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
            self.stdout.write(
                self.style.WARNING(
                    'Des catégories existent déjà dans la base de données. '
                    'Aucune nouvelle catégorie n\'a été créée.'
                )
            )
            return

        # Créer les catégories
        categories_created = []
        for category_name in default_categories:
            category = Category.objects.create(name=category_name)
            categories_created.append(category)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Catégorie créée : {category_name} (slug: {category.slug})'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ {len(categories_created)} catégories ont été créées avec succès !'
            )
        )
