from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Importation pour les messages de succès
from .forms import CategorieForm, CompteBancaireForm, ProjetForm, TransactionForm, CompanyForm
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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

# @login_required  # Optional: Require the user to be logged in
def compte_bancaire(request):
    comptes = CompteBancaire.objects.all()  # Get bank accounts for the current user's company
    return render(request, "./compte_bancaire/compte_bancaire.html", {'comptes': comptes,})

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

def supprimer_compte_bancaire(request, compte_id):
    """
    A view to delete a bank account.
    """
    compte = get_object_or_404(CompteBancaire, id=compte_id)

    if request.method == 'POST':
        compte.delete()
        messages.success(request, "Le compte bancaire a été supprimé avec succès.")
        return redirect('compte_bancaire')  # Redirect to the account list view

    return render(request, './compte_bancaire/supprimer_compte_bancaire.html', {'compte': compte})

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
    transactions = Transaction.objects.all()  # Start with all transactions

    date_debut = request.GET.get('dateDebut')
    date_fin = request.GET.get('dateFin')
    type_transaction = request.GET.get('typeTransaction')

    if date_debut:
        transactions = transactions.filter(date__gte=date_debut)
    if date_fin:
        transactions = transactions.filter(date__lte=date_fin)
    if type_transaction:
        transactions = transactions.filter(type=type_transaction)

    context = {
        'transactions': transactions,  # Pass the filtered transactions
        'date_debut': date_debut,      # Pass filter values back to the template
        'date_fin': date_fin,
        'type_transaction': type_transaction,
    }
    return render(request, './transactions/transactions.html', context)

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
    # Project data
    projets_actifs = Projet.objects.count()
    projets_termines = Projet.objects.filter(status='termine').count()  # Assuming you have a 'status' field

    # Bank account data
    compte_bancaire = CompteBancaire.objects.all()
    total_solde = sum(compte.current_balance for compte in compte_bancaire)

    # Recent transactions
    transactions_recentes = Transaction.objects.order_by('-date')[:3]  # Get the 3 most recent

    # Alerts (example - adjust to your logic)
    alertes = []
    for compte in compte_bancaire:
        if compte.current_balance < 1000:  # Example: Low balance alert
            alertes.append(f"Compte bancaire {compte.bank_name} : faible solde")
    # Corrected line: Assuming 'end_date' is the correct field name
    if Projet.objects.filter(end_date__lt=timezone.now(), status='en_cours').exists():
        alertes.append("Projet en retard")
    alertes.append("Nouvelle transaction à vérifier")  # Example: Always show this alert

    context = {
        'projets_actifs': projets_actifs,
        'projets_termines': projets_termines,
        'total_comptes': compte_bancaire.count(),
        'total_solde': total_solde,
        'transactions_recentes': transactions_recentes,
        'alertes': alertes,
        'projet': Projet.objects.all() #Pass all projects for sidebar
    }
    return render(request, './tableau_de_bord/tableau_de_bord.html',context)

def incription(request):
    return render(request, 'inscription.html')

def connexion(request):
    return render(request, 'connexion.html')

def companie(request):
    companie = Company.objects.all()
    return render(request, './entreprise/entreprise.html', {'companie': companie})

def ajouter_companie(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('companie')
    else:
        form = CompanyForm()
        return render(request, './entreprise/ajouter_companie.html', {'form': form})