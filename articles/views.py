from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import markdown
from .models import Article, Category
from .forms import ArticleForm

def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    for article in articles:
        article.content = markdown.markdown(article.content)  # Convertir Markdown en HTML
    return render(request, 'articles/article_list.html', {'articles': articles})

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.content = markdown.markdown(article.content)  # Convertir Markdown
    return render(request, 'articles/article_detail.html', {'article': article})

@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Article créé avec succès !')
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm()
    return render(request, 'articles/article_form.html', {'form': form, 'action': 'Créer'})

@login_required
def article_edit(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.user != article.author and not request.user.is_staff:
        messages.error(request, "Vous n'êtes pas autorisé à modifier cet article.")
        return redirect('article_detail', slug=slug)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article mis à jour avec succès !')
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/article_form.html', {'form': form, 'action': 'Modifier'})

@login_required
def article_delete(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.user != article.author and not request.user.is_staff:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer cet article.")
        return redirect('article_detail', slug=slug)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article supprimé avec succès !')
        return redirect('article_list')
    return render(request, 'articles/article_confirm_delete.html', {'article': article})