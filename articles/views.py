from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
import markdown
from .models import Article, Category, Comment, Like
from .forms import ArticleForm, CommentForm

def article_list(request):
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    articles = Article.objects.all().select_related('category', 'author').order_by('-created_at')
    
    if category_slug:
        articles = articles.filter(category__slug=category_slug)
    if query:
        articles = articles.filter(Q(title__icontains=query) | Q(content__icontains=query))
    
    for article in articles:
        article.content = markdown.markdown(article.content)
    
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    return render(request, 'articles/article_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
    })

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.content = markdown.markdown(article.content)
    comments = article.comments.all().order_by('-created_at')
    is_liked = article.likes.filter(user=request.user).exists() if request.user.is_authenticated else False
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Vous devez être connecté pour commenter.")
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            messages.success(request, 'Commentaire ajouté avec succès !')
            return redirect('article_detail', slug=article.slug)
    else:
        form = CommentForm()
    
    return render(request, 'articles/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form,
        'is_liked': is_liked,
    })

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

@login_required
def comment_delete(request, slug, comment_id):
    article = get_object_or_404(Article, slug=slug)
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author and request.user != article.author and not request.user.is_staff:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer ce commentaire.")
        return redirect('article_detail', slug=slug)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Commentaire supprimé avec succès !')
        return redirect('article_detail', slug=slug)
    return render(request, 'articles/comment_confirm_delete.html', {'article': article, 'comment': comment})

@login_required
def article_like(request, slug):
    article = get_object_or_404(Article, slug=slug)
    like, created = Like.objects.get_or_create(article=article, user=request.user)
    if not created:
        like.delete()
        messages.success(request, 'Like retiré.')
    else:
        messages.success(request, 'Article liké !')
    return redirect('article_detail', slug=article.slug)