from django import forms
from .models import Categorie, CompteBancaire, Projet, Transaction

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
