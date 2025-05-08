from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Company, Projet, Categorie, Tresorerie, CompteBancaire

# Enregistrer chaque modèle
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'category', 'phone_number', 'address')
    search_fields = ('full_name', 'phone_number', 'category')
    list_filter = ('category',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'phone_number', 'email')
    search_fields = ('company_name', 'contact_person')
    list_filter = ('created_at',)

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('projet_name', 'project_code', 'company', 'status', 'start_date', 'end_date')
    search_fields = ('projet_name', 'project_code')
    list_filter = ('status', 'company')

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'type', 'created_at')
    search_fields = ('category_name',)
    list_filter = ('type',)

@admin.register(Tresorerie)
class TresorerieAdmin(admin.ModelAdmin):
    list_display = ('projet', 'category', 'transaction_date', 'amount', 'payment_method', 'created_by')
    search_fields = ('reference', 'description')
    list_filter = ('payment_method', 'transaction_date')

@admin.register(CompteBancaire)
class CompteBancaireAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'account_number', 'company', 'account_currency', 'current_balance')
    search_fields = ('bank_name', 'account_number')
    list_filter = ('company', 'account_currency')
