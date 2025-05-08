from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Importation pour les messages de succès
from .forms import CategorieForm, CompteBancaireForm, ProjetForm, TransactionForm
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html', {"comptes": CompteBancaire.objects.all()})

def categorie(request):
    categorie_donnee = Categorie.objects.all()
    return render(request, './categories/categories.html', {'categorie_donnee' : categorie_donnee})

#ajouter categorie
def ajouter_categorie(request):
    if request.method == "POST":
        category_name = request.POST.get('categorie_name', '').strip()
        type = request.POST.get('type', '').strip()
        description = request.POST.get('description', '').strip()

        if category_name and type:  
            Categorie.objects.create(
                category_name=category_name,
                type=type,
                description=description
            )
            return redirect('categorie')  # Redirection après ajout

    return render(request, 'categories/ajouter_categorie.html')


def modifier_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, pk=categorie_id)

    if request.method == "POST":
        categorie.category_name = request.POST.get('category_name', '').strip()
        categorie.type = request.POST.get('type', '').strip()
        categorie.description = request.POST.get('description', '').strip()
        categorie.save()

        return redirect('categorie')  

    return render(request, 'categories/modifier_categorie.html', {'categorie': categorie})


def supprimer_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, pk=categorie_id)
    if request.method == "POST":
        categorie.delete() 
        return redirect('categorie') 

    return render(request, './categories/supprimer_categorie.html', {'categorie': categorie})

def compte_bancaire(request,):
   
    return render(request, "./compte_bancaire/compte_bancaire.html")

def ajouter_compte_bancaire(request):
    form = CompteBancaireForm()
    if request.method == "POST":
        form = CompteBancaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('compte_bancaire')  # Redirection après ajout
    return render(request, './compte_bancaire/ajouter_compte_bancaire.html', {"form":form})

def modifier_compte_bancaire(request, id):
    compte = get_object_or_404(CompteBancaire, pk=id)
    form = CompteBancaireForm(instance=compte)
    if request.method == "POST":
        form = CompteBancaireForm(request.POST, instance=compte)
        if form.is_valid():
            form.save()
            return redirect('compte_bancaire')
    return render(request, './compte_bancaire/ajouter_compte_bancaire.html',{"form":form})

def detail_compte_bancaire(request, compte_id):
    compte = get_object_or_404(CompteBancaire, id=compte_id)
    transactions = compte.transactions.all()  # Utilisez le related_name
    {'compte': compte,'transactions': transactions}
    return render(request, './compte_bancaire/detail_compte_bancaire.html', {'compte': compte,'transactions': transactions})

def supprimer_compte_bancaire(request):
    return render(request, './compte_bancaire/supprimer_compte_bancaire.html')

#projet
def projet(request):
    donnee = Projet.objects.all()
    return render(request, './projets/projets.html',{'donnee' : donnee})

def ajouter_projet(request):
    if request.method == 'POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projet')
        else:
            return redirect('ajouter_projet')
    else:
        form = ProjetForm()
        return render(request, './projets/ajouter_projet.html', {'form':form})

def details_projet(request, projet_id):
    projet = get_object_or_404(Projet, pk=projet_id)
    transactions = Tresorerie.objects.filter(projet=projet)
    return render(request, './projets/details_projet.html', {'projet': projet, 'transactions': transactions})

def apercu_projet(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)  # Récupération du projet
    tresorerie = Tresorerie.objects.filter(projet=projet)  # Transactions financières

    return render(request, "apercu_projet.html", {"projet": projet, "tresorerie": tresorerie})

def modifier_projet(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    form = ProjetForm(instance=projet)
    if request.method == "POST":
        form = ProjetForm(request.POST, instance=projet)
        if form.is_valid():
            form.save()
            return redirect('projet')
    return render(request, './projets/modifier_projet.html', {'form': form})

#transaction
def transaction(request):
    donnee_t = Transaction.objects.all()
    return render(request, './transactions/transactions.html', {'donnee_t' : donnee_t })

def ajouter_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction')
    else:
        form = TransactionForm()
        return render(request, './transactions/ajouter_transaction.html',{'form':form})

#tableau de bord
def tableau_de_bord(request):
    return render(request, './tableau_de_bord/tableau_de_bord.html')

def incription(request):
    return render(request, 'inscription.html')

def connexion(request):
    return render(request, 'connexion.html')

