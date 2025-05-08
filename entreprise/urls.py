from django.urls import path
from .views import *

urlpatterns = [
    path('', incription, name='inscription'),
    path('connexion/', connexion, name='connexion'),
    path('accueil/', index, name='accueil'),
    path('categorie/', categorie, name='categorie'),
    path('ajouter_categorie/', ajouter_categorie, name='ajouter_categorie'),
    path('modifier_categorie/<int:categorie_id>/', modifier_categorie, name='modifier_categorie'),    
    path('supprimer_categorie/<int:categorie_id>/', supprimer_categorie, name='supprimer_categorie'),
    path('projet/', projet, name='projet' ),
    path('modifier_projet/<int:projet_id>/', modifier_projet, name='modifier_projet'),
    path('transaction/', transaction, name='transaction'),
    path('compte_bancaire/', compte_bancaire, name='compte_bancaire'),
    path('ajouter_compte_bancaire/', ajouter_compte_bancaire, name='ajouter_compte_bancaire'),
    path('detail_compte_bancaire/<int:compte_id>/', detail_compte_bancaire, name='detail_compte_bancaire'),
    path('details_projet/<int:projet_id>', details_projet, name='details_projet' ),
    path('ajouter_transaction/', ajouter_transaction, name='ajouter_transaction'),
    path('ajouter_projet/', ajouter_projet, name='ajouter_projet'),
    path('tableau_de_bord/', tableau_de_bord, name='tableau_de_bord'),
    path('modifier_compte_bancaire/<int:id>/', modifier_compte_bancaire, name='modifier_compte_bancaire'),
    path('supprimer_compte_bancaire/', supprimer_compte_bancaire, name='supprimer_compte_bancaire'),
    path('apercu_projet/<int:projet_id>/', apercu_projet, name='apercu_projet'),
]
