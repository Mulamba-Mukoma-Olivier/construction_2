from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Categorie, CompteBancaire, Projet, Transaction, Company
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d’utilisateur'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )
    
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'full_name', 'phone_number', 'category', 'password1', 'password2']

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'address', 'contact_person', 'phone_number', 'email']
        # Optionally, you can exclude fields like created_at and updated_at:
        # exclude = ['created_at', 'updated_at']

        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'company_name': "Nom de l'entreprise",
            'address': "Adresse",
            'contact_person': "Personne de contact",
            'phone_number': "Numéro de téléphone",
            'email': "Email",
        }
        help_texts = {
            'email': 'Veuillez entrer une adresse email valide.',
        }
        error_messages = {
            'company_name': {
                'required': "Le nom de l'entreprise est obligatoire.",
                'max_length': "Le nom de l'entreprise ne doit pas dépasser 255 caractères.",
            },
            'email': {
                'unique': "Cet email est déjà utilisé.",
            },
        }
        
class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['category_name', 'type', 'description']


class CompteBancaireForm(forms.ModelForm):
    
    class Meta:
        model = CompteBancaire
        fields ="__all__"
        widgets={
            "company":forms.Select(
                attrs={"class":"form-select",
                       "placeholder": "Entrez le nom du companie"
                    }
                ),
            "bank_name":forms.TextInput(
                attrs={"class":"form-control",
                       "placeholder": "Entrez le nom de la banque"
                    }
                ),
            "account_number": forms.TextInput(
                attrs={"class":"form-control",
                       "placeholder": "Entrez le numero du compte"
                    }
                ),
            "account_currency": forms.TextInput(
                attrs={"class":"form-control",
                        "placeholder": "Entrez la devise"
                    }
                ),
            "current_balance": forms.NumberInput(
                attrs={"class":"form-control",
                       "placeholder": "Entrez le solde acteulle"
                    }
                )
        }

class ProjetForm(forms.ModelForm):
    class Meta:
        model = Projet
        fields = '__all__'
        widgets={
            "company":forms.Select({
                'class':'form-control',
                'placeholder':'Entrez le nom du projet'}),
            "projet_name":forms.TextInput({
                'class':'form-control',
                'placeholder':'Entrez le nom du projet'
            }),
            "project_code":forms.TextInput({
                'class':'form-control',
                'placeholder':'Entrez le nom du projet'
            }),
            "start_date":forms.DateInput({
                'class':'form-control',
                'placeholder':'Entrez le nom du projet',
                'type':'date'
            }),
            "end_date":forms.DateInput({
                'class':'form-control',
                'placeholder':'Entrez le nom du projet',
                'type':'date'
            }),
            "location":forms.TextInput({
                'class':'form-control',
                'placeholder':'Entrez le nom du projet'
            }),
            "status":forms.Select({
                'class':'form-control',
                'placeholder':'Entrez le nom du projet'
            }),

            "created_at":forms.TextInput({
                'class':'form-control',
                'placeholder':'Entrez le nom du projet'
            }),
            "updated_at":forms.TextInput({
                'class':'form-control',
                'placeholder':'Entrez le nom du projet'
            }),
        }
        
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'compte': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'create_at': forms.DateInput(attrs={'type':'date','class': 'form-control'}),
            'update_at': forms.DateInput(attrs={'type':'date','class': 'form-control'}),
        }

class StyledFormMixin:
    """Ajoute des classes Bootstrap aux champs du formulaire."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control shadow-sm rounded-lg',
                'placeholder': field.label
            })

class EntreeForm(forms.ModelForm, StyledFormMixin):
    class Meta:
        model = Transaction
        fields = ['compte', 'date', 'description', 'amount']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Détail de la transaction'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control','step': '0.01'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.type = 'credit'  # Forcer comme entrée
        if commit:
            instance.save()
        return instance

class SortieForm(forms.ModelForm, StyledFormMixin):
    class Meta:
        model = Transaction
        fields = ['compte', 'date', 'description', 'amount']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motif du paiement'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control','step': '0.01'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.type = 'debit'  # Forcer comme sortie
        if commit:
            instance.save()
        return instance