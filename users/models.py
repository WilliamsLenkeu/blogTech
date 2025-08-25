from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Ajoutez des champs si besoin, ex. :
    # bio = models.TextField(blank=True)
    pass
