from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# Vue pour inscription
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connecte automatiquement après inscription
            messages.success(request, 'Inscription réussie !')
            return redirect('home')  # Redirige vers la page d'accueil (à définir plus tard)
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# Vue pour connexion (on peut utiliser la built-in, mais voici une personnalisée pour exemple)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Connexion réussie !')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Vue pour déconnexion
def logout_view(request):
    logout(request)
    messages.success(request, 'Déconnexion réussie !')
    return redirect('home')

# Create your views here.
