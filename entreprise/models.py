from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class CustomUser(AbstractUser):
    USER_CATEGORIES = [
        ('admin', 'Admin'),
        ('entreprise', 'Entreprise'),
        ('finance', 'Finance'),
        ('projet_manager', 'Gestionnaire de projet'),
    ]
    category = models.CharField(max_length=20, choices=USER_CATEGORIES, verbose_name="Catégorie utilisateur")
    full_name = models.CharField(max_length=255, verbose_name="Nom complet")
    phone_number = models.CharField(max_length=15, verbose_name="Numéro de téléphone")
    address = models.TextField(blank=True, verbose_name="Adresse")

    def __str__(self):
        return f"{self.full_name} - {self.category}"
    
class Company(models.Model):
    company_name = models.CharField(max_length=255, verbose_name="Nom de l'entreprise")
    address = models.TextField(verbose_name="Adresse")
    contact_person = models.CharField(max_length=255, verbose_name="Personne de contact")
    phone_number = models.CharField(max_length=15, verbose_name="Numéro de téléphone")
    email = models.EmailField(unique=True, verbose_name="Email")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")

    def __str__(self):
        return self.company_name

class Projet(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name="Entreprise associée")
    projet_name = models.CharField(max_length=255, verbose_name="Nom du projet")
    project_code = models.CharField(max_length=100, unique=True, verbose_name="Code du projet")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(null=True, blank=True, verbose_name="Date de fin")
    location = models.CharField(max_length=255, verbose_name="Localisation")
    
    STATUS_CHOICES = [
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('a_demarrer', 'À démarrer'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='a_demarrer', verbose_name="Statut")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")

    def __str__(self):
        return f"{self.projet_name} ({self.project_code})"
    
class Categorie(models.Model):
    category_name = models.CharField(max_length=255, unique=True, verbose_name="Nom de la catégorie")
    
    TYPE_CHOICES = [
        ('produit', 'Produit'),
        ('service', 'Service'),
        ('autre', 'Autre'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='autre', verbose_name="Type de catégorie")

    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")

    def __str__(self):
        return self.category_name
    

class Tresorerie(models.Model):
    projet = models.ForeignKey('Projet', on_delete=models.CASCADE, verbose_name="Projet associé")
    category = models.ForeignKey('Categorie', on_delete=models.SET_NULL, null=True, verbose_name="Catégorie")
    transaction_date = models.DateField(verbose_name="Date de transaction")
    description = models.TextField(verbose_name="Description")
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Montant")
    
    PAYMENT_METHOD_CHOICES = [
        ('virement', 'Virement bancaire'),
        ('espece', 'Espèces'),
        ('cheque', 'Chèque'),
        ('carte', 'Carte bancaire'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Méthode de paiement")

    reference = models.CharField(max_length=100, unique=True, verbose_name="Référence de la transaction")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Use AUTH_USER_MODEL setting
        on_delete=models.SET_NULL,  # Or CASCADE, PROTECT, etc.
        null=True,  # Or False, depending on your requirements
        blank=True, # Or False
        related_name='tresoreries_created' # Optional, but good practice
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")

    def __str__(self):
        return f"Transaction {self.reference} - {self.amount} ({self.payment_method})"

class CompteBancaire(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name="Entreprise associée")
    bank_name = models.CharField(max_length=255, verbose_name="Nom de la banque")
    account_number = models.CharField(max_length=50, unique=True, verbose_name="Numéro de compte")
    account_currency = models.CharField(max_length=10, verbose_name="Devise du compte")
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Solde actuel", default=0.00)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")

    def update_balance(self):
        transactions = self.transactions.all()
        total_credit = sum(t.amount for t in transactions if t.type == "credit")
        total_debit = sum(t.amount for t in transactions if t.type == "debit")
        self.current_balance = total_credit - total_debit
        self.save()

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"
    
class Transaction(models.Model):
    compte = models.ForeignKey('CompteBancaire', on_delete=models.CASCADE, related_name='transactions', verbose_name="Compte associé")
    date = models.DateField(verbose_name="Date de la transaction")
    description = models.CharField(max_length=255, verbose_name="Description")
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Montant")
    type = models.CharField(max_length=10, choices=[
        ('credit', 'Crédit'),
        ('debit', 'Débit'),
    ], verbose_name="Type de transaction")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")  # ✅ Ajout de auto_now=True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.compte.update_balance()

    def __str__(self):
        return f"{self.date} - {self.description} ({self.type})"






    

