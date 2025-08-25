from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
import random
from faker import Faker

from articles.models import Category, Article, Comment, Like
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Charge des données de démonstration : utilisateurs, articles, commentaires et likes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Nombre d\'utilisateurs à créer (défaut: 10)'
        )
        parser.add_argument(
            '--articles',
            type=int,
            default=25,
            help='Nombre d\'articles à créer (défaut: 25)'
        )
        parser.add_argument(
            '--comments',
            type=int,
            default=50,
            help='Nombre de commentaires à créer (défaut: 50)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Forcer la création même si des données existent déjà'
        )

    def handle(self, *args, **options):
        fake = Faker(['fr_FR'])
        
        num_users = options['users']
        num_articles = options['articles']
        num_comments = options['comments']
        force = options['force']

        self.stdout.write("🚀 Chargement des données de démonstration...\n")

        # Vérifier si des catégories existent
        if not Category.objects.exists():
            self.stdout.write(
                self.style.ERROR(
                    '❌ Aucune catégorie trouvée dans la base de données. '
                    'Exécutez d\'abord "python manage.py load_categories"'
                )
            )
            return

        # Vérifier si des données existent déjà
        if not force and (CustomUser.objects.count() > 1 or Article.objects.exists()):
            self.stdout.write(
                self.style.WARNING(
                    '⚠️ Des données existent déjà dans la base de données. '
                    'Utilisez --force pour forcer la création.'
                )
            )
            return

        # 1. CRÉER LES UTILISATEURS
        self.stdout.write("👥 Création des utilisateurs...")
        users = []
        
        # Créer l'utilisateur admin s'il n'existe pas
        admin_user, created = CustomUser.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Administrateur',
                'last_name': 'Système',
                'is_staff': True,
                'is_superuser': True,
                'password': make_password('admin123')
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"✅ Utilisateur admin créé : admin/admin123")
            )
        users.append(admin_user)

        # Créer les autres utilisateurs
        for i in range(num_users):
            username = fake.unique.user_name()
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            
            user = CustomUser.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=make_password('password123'),
                is_active=True
            )
            users.append(user)
            self.stdout.write(
                self.style.SUCCESS(f"✅ Utilisateur créé : {username} ({first_name} {last_name})")
            )

        self.stdout.write(f"✅ {len(users)} utilisateurs créés\n")

        # 2. CRÉER LES ARTICLES
        self.stdout.write("📝 Création des articles...")
        articles = []
        categories = list(Category.objects.all())
        
        # Contenu d'exemple pour les articles
        article_contents = [
            "Cet article explore les dernières avancées technologiques qui révolutionnent notre quotidien. "
            "De l'intelligence artificielle aux énergies renouvelables, découvrez comment l'innovation "
            "transforme notre monde.",
            
            "La science moderne nous révèle des secrets fascinants sur l'univers qui nous entoure. "
            "Des découvertes récentes en astrophysique aux avancées en biologie moléculaire, "
            "chaque jour apporte son lot de surprises.",
            
            "Prendre soin de sa santé est essentiel pour une vie équilibrée. "
            "Cet article vous propose des conseils pratiques et des informations "
            "pour maintenir votre bien-être physique et mental.",
            
            "L'éducation est la clé d'un avenir prometteur. "
            "Découvrez les nouvelles méthodes d'apprentissage et les outils "
            "qui facilitent l'acquisition de connaissances.",
            
            "Partez à la découverte de destinations extraordinaires à travers le monde. "
            "De la culture locale aux paysages époustouflants, "
            "chaque voyage est une aventure unique.",
            
            "La cuisine est un art qui réveille tous nos sens. "
            "Explorez des recettes traditionnelles et modernes "
            "qui vous feront voyager à travers les saveurs du monde.",
            
            "Le sport est bien plus qu'une simple activité physique. "
            "Il développe la discipline, la persévérance et l'esprit d'équipe. "
            "Découvrez comment intégrer le sport dans votre routine quotidienne.",
            
            "La musique a le pouvoir de toucher nos âmes et de transcender les frontières. "
            "Explorez différents genres musicaux et découvrez "
            "comment la musique influence notre humeur et notre créativité.",
            
            "Le cinéma nous transporte dans des mondes imaginaires et nous fait vivre "
            "des émotions intenses. Découvrez les chefs-d'œuvre du 7ème art "
            "et leur impact sur notre culture.",
            
            "La littérature ouvre les portes de l'imagination et nous permet "
            "d'explorer des univers infinis. Plongez dans des œuvres "
            "qui ont marqué l'histoire de la littérature mondiale."
        ]

        for i in range(num_articles):
            # Choisir une catégorie aléatoire
            category = random.choice(categories)
            
            # Choisir un auteur aléatoire
            author = random.choice(users)
            
            # Créer un titre et un contenu
            title = fake.sentence(nb_words=6, variable_nb_words=True)
            content = random.choice(article_contents) + " " + fake.paragraph(nb_sentences=3)
            
            # Créer des dates aléatoires dans les 30 derniers jours
            days_ago = random.randint(0, 30)
            created_at = timezone.now() - timedelta(days=days_ago)
            
            article = Article.objects.create(
                title=title,
                content=content,
                author=author,
                category=category,
                created_at=created_at,
                updated_at=created_at
            )
            articles.append(article)
            self.stdout.write(
                self.style.SUCCESS(f"✅ Article créé : '{title}' par {author.username}")
            )

        self.stdout.write(f"✅ {len(articles)} articles créés\n")

        # 3. CRÉER LES COMMENTAIRES
        self.stdout.write("💬 Création des commentaires...")
        comment_contents = [
            "Excellent article, très instructif !",
            "Merci pour ces informations utiles.",
            "Je ne suis pas d'accord avec certains points, mais c'est intéressant.",
            "Très bien écrit et facile à comprendre.",
            "Cela m'a donné envie d'en savoir plus sur le sujet.",
            "Article passionnant, j'ai appris beaucoup de choses.",
            "Bonne approche du sujet, continuez comme ça !",
            "Je partage complètement votre point de vue.",
            "Cela m'a fait réfléchir différemment.",
            "Merci pour ce partage d'expérience."
        ]

        for i in range(num_comments):
            # Choisir un article et un auteur aléatoires
            article = random.choice(articles)
            author = random.choice(users)
            
            # Créer un contenu de commentaire
            content = random.choice(comment_contents)
            
            # Créer une date aléatoire après la création de l'article
            days_after_article = random.randint(0, 20)
            comment_date = article.created_at + timedelta(days=days_after_article)
            
            comment = Comment.objects.create(
                article=article,
                author=author,
                content=content,
                created_at=comment_date
            )
            
            if i % 10 == 0:  # Afficher un message tous les 10 commentaires
                self.stdout.write(
                    self.style.SUCCESS(f"✅ {i+1} commentaires créés...")
                )

        self.stdout.write(f"✅ {num_comments} commentaires créés\n")

        # 4. CRÉER LES LIKES
        self.stdout.write("❤️ Création des likes...")
        likes_created = 0
        
        for article in articles:
            # Chaque article reçoit entre 0 et 8 likes
            num_likes = random.randint(0, 8)
            # Choisir des utilisateurs aléatoires pour liker
            likers = random.sample(users, min(num_likes, len(users)))
            
            for liker in likers:
                like, created = Like.objects.get_or_create(
                    article=article,
                    user=liker
                )
                if created:
                    likes_created += 1
                    
        self.stdout.write(f"✅ {likes_created} likes créés\n")

        # 5. AFFICHER LE RÉSUMÉ
        self.stdout.write("\n" + "="*50)
        self.stdout.write("📊 RÉSUMÉ DES DONNÉES CRÉÉES")
        self.stdout.write("="*50)
        self.stdout.write(f"👥 Utilisateurs : {CustomUser.objects.count()}")
        self.stdout.write(f"📝 Articles : {Article.objects.count()}")
        self.stdout.write(f"💬 Commentaires : {Comment.objects.count()}")
        self.stdout.write(f"❤️ Likes : {Like.objects.count()}")
        self.stdout.write(f"🏷️ Catégories : {Category.objects.count()}")
        self.stdout.write("="*50)
        
        self.stdout.write(
            self.style.SUCCESS(
                "\n🎉 Données de démonstration chargées avec succès !"
            )
        )
        
        self.stdout.write("\n🔑 Identifiants de connexion :")
        self.stdout.write("   Admin : admin/admin123")
        self.stdout.write("   Autres utilisateurs : username/password123")
        
        self.stdout.write("\n🌐 Vous pouvez maintenant :")
        self.stdout.write("   1. Démarrer le serveur : python manage.py runserver")
        self.stdout.write("   2. Accéder à l'admin : http://127.0.0.1:8000/admin/")
        self.stdout.write("   3. Explorer vos articles et commentaires !")
