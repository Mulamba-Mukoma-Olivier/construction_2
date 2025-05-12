from django.urls import path, include
from rest_framework.routers import DefaultRouter
from entreprise.views import register, login_view, logout_view, index, ajouter_entree, ajouter_sortie, categorie, ajouter_categorie, modifier_categorie, supprimer_categorie,projet, ajouter_projet, modifier_projet, details_projet, transaction, ajouter_transaction,modifier_transaction, supprimer_transaction, compte_bancaire, ajouter_compte_bancaire,modifier_compte_bancaire, supprimer_compte_bancaire, detail_compte_bancaire, companie, ajouter_companie, tableau_de_bord, TransactionViewSet


# Configuration du routeur pour l'API REST
router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename="transaction")  

urlpatterns = [
    # 🔹 API REST
    path('api/', include(router.urls)),  

    # 🔹 Authentification
    path('', register, name='register'), 
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # 🔹 Accueil & Tableau de bord
    path('accueil/', index, name='accueil'),
    path('tableau_de_bord/', tableau_de_bord, name='tableau_de_bord'),

    # 🔹 Gestion des catégories
    path('categorie/', categorie, name='categorie'),
    path('categorie/ajouter/', ajouter_categorie, name='ajouter_categorie'),
    path('categorie/modifier/<int:categorie_id>/', modifier_categorie, name='modifier_categorie'),    
    path('categorie/supprimer/<int:categorie_id>/', supprimer_categorie, name='supprimer_categorie'),

    # 🔹 Gestion des projets
    path('projet/', projet, name='projet'),
    path('projet/ajouter/', ajouter_projet, name='ajouter_projet'),
    path('projet/modifier/<int:projet_id>/', modifier_projet, name='modifier_projet'),
    path('projet/details/<int:projet_id>/', details_projet, name='details_projet'),

    # 🔹 Gestion des transactions
    path('transaction/', transaction, name='transaction'),
    path('transaction/ajouter/', ajouter_transaction, name='ajouter_transaction'),
    path('transaction/modifier/<int:transaction_id>/', modifier_transaction, name='modifier_transaction'),
    path('transaction/supprimer/<int:transaction_id>/', supprimer_transaction, name='supprimer_transaction'),
    path('transaction/entree/', ajouter_entree, name='ajouter_entree'),
    path('transaction/sorties/', ajouter_sortie, name='ajouter_sortie'),



    # 🔹 Gestion des comptes bancaires
    path('compte_bancaire/', compte_bancaire, name='compte_bancaire'),
    path('compte_bancaire/ajouter/', ajouter_compte_bancaire, name='ajouter_compte_bancaire'),
    path('compte_bancaire/modifier/<int:id>/', modifier_compte_bancaire, name='modifier_compte_bancaire'),
    path('compte_bancaire/supprimer/<int:compte_id>/', supprimer_compte_bancaire, name='supprimer_compte_bancaire'),
    path('compte_bancaire/details/<int:compte_id>/', detail_compte_bancaire, name='detail_compte_bancaire'),

    # 🔹 Gestion des entreprises
    path('entreprise/', companie, name='companie'),
    path('entreprise/ajouter/', ajouter_companie, name='ajouter_companie'),
]
