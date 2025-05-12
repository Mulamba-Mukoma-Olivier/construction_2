from pathlib import Path

# Définition du chemin de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️ Sécurité : SECRET_KEY doit être cachée en production
SECRET_KEY = 'django-insecure-04z&!4numc-278bk8t+cv(6eh(0ebcj*guswoqi43ypz37&i2q'

# Débogage (⚠️ Définir DEBUG = False en production)
DEBUG = True  # ⚠️ À changer en False pour le déploiement

# ⚠️ Sécurité : éviter ALLOWED_HOSTS = ['*'] en production
ALLOWED_HOSTS = ['127.0.0.1', 'localhost','*']

# Applications installées
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # API REST
    'entreprise.apps.EntrepriseConfig',  # Application principale
]

# Middleware (gestion des requêtes)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 🔹 Vérification du bon ROOT_URLCONF
ROOT_URLCONF = 'construction.urls'  

# Gestion des templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Correction du chemin
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI (Serveur web)
WSGI_APPLICATION = 'construction.wsgi.application'

# 🔹 Base de données SQLite (changer pour PostgreSQL en production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Sécurité des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🔹 Définition du modèle utilisateur personnalisé
AUTH_USER_MODEL = "entreprise.CustomUser"

# Paramètres d'internationalisation
LANGUAGE_CODE = 'fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 🔹 Gestion des fichiers statiques
STATIC_URL = '/static/'


# Configuration du champ par défaut des clés primaires
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
