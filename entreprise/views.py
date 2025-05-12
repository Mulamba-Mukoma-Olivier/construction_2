from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from entreprise.forms import CategorieForm, CompteBancaireForm, ProjetForm, TransactionForm, CompanyForm, EntreeForm, SortieForm
from entreprise.models import Projet, Transaction, Tresorerie, Company, Categorie, CompteBancaire
from rest_framework import viewsets
from entreprise.serializers import TransactionSerializer
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate
from .forms import CustomLoginForm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Transaction
from .serializers import TransactionSerializer


@login_required
def index(request):
    return render(request, 'index.html', {"comptes": CompteBancaire.objects.all()})


# Gestion des catégories
@login_required
def categorie(request):
    categorie_donnee = Categorie.objects.all()
    return render(request, './categories/categories.html', {'categorie_donnee': categorie_donnee})


@login_required
def ajouter_categorie(request):
    if request.method == "POST":
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Catégorie ajoutée avec succès !")
            return redirect('categorie')
    else:
        form = CategorieForm()

    return render(request, 'categories/ajouter_categorie.html', {'form': form})


@login_required
def modifier_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, pk=categorie_id)

    if request.method == "POST":
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            messages.success(request, "Catégorie modifiée avec succès !")
            return redirect('categorie')

    else:
        form = CategorieForm(instance=categorie)
    return render(request, 'categories/modifier_categorie.html', {'form': form})


@login_required
def supprimer_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, pk=categorie_id)
    if request.method == "POST":
        categorie.delete()
        messages.success(request, "Catégorie supprimée avec succès !")
        return redirect('categorie')

    return render(request, './categories/supprimer_categorie.html', {'categorie': categorie})


# Gestion des comptes bancaires
@login_required
def compte_bancaire(request):
    comptes = CompteBancaire.objects.all()
    return render(request, "./compte_bancaire/compte_bancaire.html", {'comptes': comptes})


@login_required
def ajouter_compte_bancaire(request):
    if request.method == "POST":
        form = CompteBancaireForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte bancaire ajouté avec succès !")
            return redirect('compte_bancaire')
    else:
        form = CompteBancaireForm()

    return render(request, './compte_bancaire/ajouter_compte_bancaire.html', {"form": form})


@login_required
def modifier_compte_bancaire(request, compte_id):
    compte = get_object_or_404(CompteBancaire, pk=compte_id)

    if request.method == "POST":
        form = CompteBancaireForm(request.POST, instance=compte)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte bancaire modifié avec succès !")
            return redirect('compte_bancaire')
    else:
        form = CompteBancaireForm(instance=compte)

    return render(request, './compte_bancaire/modifier_compte_bancaire.html', {"form": form})


@login_required
def supprimer_compte_bancaire(request, compte_id):
    compte = get_object_or_404(CompteBancaire, pk=compte_id)  # Use pk here
    if request.method == 'POST':
        compte.delete()
        messages.success(request, "Compte bancaire supprimé avec succès !")
        return redirect('compte_bancaire')

    return render(request, './compte_bancaire/supprimer_compte_bancaire.html', {'compte': compte})


# Gestion des transactions
@login_required
def transaction(request):
    transactions = Transaction.objects.all()

    date_debut = request.GET.get('dateDebut')
    date_fin = request.GET.get('dateFin')
    type_transaction = request.GET.get('typeTransaction')
    compte_id = request.GET.get('compte')

    if date_debut:
        transactions = transactions.filter(date__gte=date_debut)
    if date_fin:
        transactions = transactions.filter(date__lte=date_fin)
    if type_transaction:
        transactions = transactions.filter(type=type_transaction)
    if compte_id:
        transactions = transactions.filter(compte__id=compte_id)

    return render(request, './transactions/transactions.html', {'transactions': transactions})


@login_required
def ajouter_entree(request):
    if request.method == "POST":
        form = EntreeForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.created_by = request.user
            transaction.save()
            return redirect('transaction')  # Redirection après ajout
    else:
        form = EntreeForm()

    return render(request, "./transactions/entree.html", {"form": form})


@login_required
def ajouter_sortie(request):
    if request.method == "POST":
        form = SortieForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.created_by = request.user
            transaction.save()
            return redirect('transaction')
    else:
        form = SortieForm()

    return render(request, "./transactions/sortie.html", {"form": form})


@login_required
def ajouter_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction ajoutée avec succès !")
            return redirect('transaction')
    else:
        form = TransactionForm()

    return render(request, './transactions/ajouter_transaction.html', {'form': form})


@login_required
def modifier_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction modifiée avec succès !")
            return redirect('transaction')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, './transactions/modifier_transaction.html', {'form': form})


@login_required
def supprimer_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)

    if request.method == "POST":
        transaction.delete()
        messages.success(request, "Transaction supprimée avec succès !")
        return redirect('transaction')

    return render(request, './transactions/supprimer_transaction.html', {'transaction': transaction})


# Tableau de bord
@login_required
def tableau_de_bord(request):
    comptes = CompteBancaire.objects.all()
    transactions = Transaction.objects.order_by('-date')

    # Vérification que des transactions existent
    total_credit = sum(t.amount for t in transactions if t.type == 'credit') if transactions.exists() else 0
    total_debit = sum(t.amount for t in transactions if t.type == 'debit') if transactions.exists() else 0
    solde_total = total_credit - total_debit  # Calcul du solde global

    return render(request, "tableau_de_bord/tableau_de_bord.html", {
        "comptes": comptes,
        "transactions": transactions,
        "total_credit": total_credit,
        "total_debit": total_debit,
        "solde_total": solde_total,
    })

@login_required
def projet(request):
    donnee = Projet.objects.all()
    return render(request, "projets/projets.html", {"donnee": donnee})

@login_required
def ajouter_projet(request):
    if request.method == "POST":
        form = ProjetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("projet")
    else:
        form = ProjetForm()
    return render(request, "projets/ajouter_projet.html", {"form": form})


@login_required
def details_projet(request, projet_id):
    projet = get_object_or_404(Projet, pk=projet_id)
    transactions = Tresorerie.objects.filter(projet=projet)
    return render(request, './projets/details_projet.html', {'projet': projet, 'transactions': transactions})


@login_required
def apercu_projet(request, projet_id):
    projet = get_object_or_404(Projet, pk=projet_id)  # Récupération du projet
    tresorerie = Tresorerie.objects.filter(projet=projet)  # Transactions financières

    return render(request, "apercu_projet.html", {"projet": projet, "tresorerie": tresorerie})


@login_required
def modifier_projet(request, projet_id):
    projet = get_object_or_404(Projet, pk=projet_id)
    if request.method == "POST":
        form = ProjetForm(request.POST, instance=projet)
        if form.is_valid():
            form.save()
            return redirect('projet')
    else:
        form = ProjetForm(instance=projet)
    return render(request, './projets/modifier_projet.html', {'form': form})


@login_required
def companie(request):
    companie = Company.objects.all()
    return render(request, './entreprise/entreprise.html', {'companie': companie})


@login_required
def ajouter_companie(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('companie')
    else:
        form = CompanyForm()
        return render(request, './entreprise/ajouter_companie.html', {'form': form})


@login_required
def detail_compte_bancaire(request, compte_id):
    compte = get_object_or_404(CompteBancaire, pk=compte_id)
    transactions = compte.transactions.all()  # Utilisez le related_name
    return render(request, './compte_bancaire/detail_compte_bancaire.html', {'compte': compte, 'transactions': transactions})


@login_required
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


# @login_required  # Consider if you want this to be login required
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connecte directement l'utilisateur après inscription
            return redirect("tableau_de_bord")  # Redirection vers le tableau de bord
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("tableau_de_bord")  # Redirection après connexion
    else:
        form = CustomLoginForm()

    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")

@method_decorator(login_required, name='dispatch')  # Protect all methods in the class
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @method_decorator(login_required, name='create')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @method_decorator(login_required, name='update')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @method_decorator(login_required, name='destroy')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)