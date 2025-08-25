from django import forms
from .models import Article, Category, Comment
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'category']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Cette méthode s'occupe uniquement de la validation
            if image.size > 5 * 1024 * 1024:  # 5MB max
                raise ValidationError("L'image ne doit pas dépasser 5 Mo.")
            if not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise ValidationError("Seuls les formats PNG et JPG sont acceptés.")
        return image

    def save(self, commit=True):
        # Cette méthode est surchargée pour compresser l'image avant l'enregistrement
        article = super().save(commit=False)
        
        image = self.cleaned_data.get('image')
        if image:
            # Ouvrir l'image avec Pillow
            pil_image = Image.open(image)
            
            # Créer un buffer pour sauvegarder l'image compressée
            output = BytesIO()
            
            # Redimensionner l'image si elle est trop grande (facultatif)
            if pil_image.width > 800 or pil_image.height > 600:
                pil_image.thumbnail((800, 600))
            
            # Compresser et sauvegarder l'image dans le buffer
            # Ajustez la qualité (quality) pour trouver le bon équilibre taille/qualité
            if pil_image.mode in ('RGBA', 'P'):
                pil_image = pil_image.convert('RGB')
            pil_image.save(output, format='JPEG', quality=85)
            output.seek(0)
            
            # Mettre à jour l'objet image de l'article avec le fichier compressé
            article.image = InMemoryUploadedFile(output, 'ImageField', f"{image.name.split('.')[0]}.jpeg", 'image/jpeg', output.getbuffer().nbytes, None)

        if commit:
            article.save()
        return article


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Votre commentaire...'}),
        }
        
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > 1000:
            raise ValidationError("Le commentaire ne doit pas dépasser 1000 caractères.")
        return content