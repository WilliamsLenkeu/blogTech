from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'articles'

    def ready(self):
        """
        Cette méthode est appelée quand Django démarre
        Elle permet de charger les signaux automatiquement
        """
        try:
            import articles.signals
        except ImportError:
            pass
