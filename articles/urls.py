from django.urls import path
from .views import article_list, article_detail, article_create, article_edit, article_delete, comment_delete, article_like

urlpatterns = [
    path('', article_list, name='article_list'),
    path('create/', article_create, name='article_create'),
    path('<slug:slug>/', article_detail, name='article_detail'),
    path('<slug:slug>/edit/', article_edit, name='article_edit'),
    path('<slug:slug>/delete/', article_delete, name='article_delete'),
    path('<slug:slug>/comment/<int:comment_id>/delete/', comment_delete, name='comment_delete'),
    path('<slug:slug>/like/', article_like, name='article_like'),
]