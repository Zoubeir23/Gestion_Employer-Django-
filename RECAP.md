# Documentation Technique - Système de Gestion des Employés

**Auteur :** Zoubeir23  
**Email :** Zoubeiribrahima@gmail.com

## Table des Matières
1. [Introduction](#introduction)
2. [Architecture du Projet](#architecture-du-projet)
3. [Modèles de Données](#modèles-de-données)
4. [Vues et Templates](#vues-et-templates)
5. [Formulaires](#formulaires)
6. [URLs et Routage](#urls-et-routage)
7. [Authentification et Sécurité](#authentification-et-sécurité)
8. [Interface Utilisateur](#interface-utilisateur)
9. [Base de Données](#base-de-données)
10. [Déploiement](#déploiement)
11. [Ressources Utiles](#ressources-utiles)
12. [Dépannage](#dépannage)
13. [Bonnes Pratiques](#bonnes-pratiques)

## Introduction

Ce document fournit une documentation technique détaillée du système de gestion des employés. Il est conçu pour aider les développeurs à comprendre l'architecture et les composants du système.

## Architecture du Projet

### Structure des Dossiers
```
monprojet/
├── gestion/
│   ├── templates/
│   │   └── gestion/
│   │       ├── base.html          # Template de base
│   │       ├── form_base.html     # Template de base pour les formulaires
│   │       ├── home.html          # Page d'accueil
│   │       ├── employer_list.html # Liste des employés
│   │       ├── employer_form.html # Formulaire employé
│   │       ├── service_list.html  # Liste des services
│   │       ├── service_form.html  # Formulaire service
│   │       ├── conge_list.html    # Liste des congés
│   │       └── conge_form.html    # Formulaire congé
│   ├── models.py                  # Modèles de données
│   ├── views.py                   # Vues
│   ├── forms.py                   # Formulaires
│   └── urls.py                    # Configuration des URLs
└── monprojet/
    ├── settings.py                # Configuration du projet
    ├── urls.py                    # URLs principales
    └── wsgi.py                    # Configuration WSGI
```

## Modèles de Données

### Employer
```python
class Employer(models.Model):
    GENRE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_embauche = models.DateField()
    salaire = models.DecimalField(max_digits=10, decimal_places=2)
    poste = models.CharField(max_length=100)
```

### Service
```python
class Service(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
```

### Conge
```python
class Conge(models.Model):
    TYPE_CHOICES = [
        ('ANNUEL', 'Congé annuel'),
        ('MALADIE', 'Congé maladie'),
        ('MATERNITE', 'Congé maternité'),
        ('PATERNITE', 'Congé paternité'),
        ('AUTRE', 'Autre'),
    ]
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('APPROUVE', 'Approuvé'),
        ('REJETE', 'Rejeté'),
    ]
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    type_conge = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField()
    raison = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
```

## Vues et Templates

### Types de Vues Utilisées
- `ListView` : Affichage des listes (employés, services, congés)
- `DetailView` : Affichage des détails
- `CreateView` : Création de nouveaux éléments
- `UpdateView` : Modification des éléments existants
- `DeleteView` : Suppression d'éléments

### Exemple de Vue
```python
class EmployerCreateView(LoginRequiredMixin, CreateView):
    model = Employer
    form_class = EmployerForm
    template_name = 'gestion/employer_form.html'
    success_url = reverse_lazy('employer-list')

    def form_valid(self, form):
        messages.success(self.request, 'Employé créé avec succès !')
        return super().form_valid(form)
```

## Formulaires

### Configuration de django-crispy-forms
```python
INSTALLED_APPS = [
    ...
    'crispy_forms',
    'crispy_bootstrap5',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
```

### Exemple de Formulaire
```python
class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['nom', 'prenom', 'email', 'telephone', 'genre', 
                 'date_embauche', 'poste', 'salaire', 'service']
        widgets = {
            'date_embauche': forms.DateInput(attrs={'type': 'date'}),
            'salaire': forms.NumberInput(attrs={'step': '0.01'}),
        }
```

## URLs et Routage

### Configuration des URLs
```python
urlpatterns = [
    path('employes/', views.EmployerListView.as_view(), name='employer-list'),
    path('employes/nouveau/', views.EmployerCreateView.as_view(), name='employer-create'),
    path('employes/<int:pk>/', views.EmployerDetailView.as_view(), name='employer-detail'),
    path('employes/<int:pk>/modifier/', views.EmployerUpdateView.as_view(), name='employer-update'),
    path('employes/<int:pk>/supprimer/', views.EmployerDeleteView.as_view(), name='employer-delete'),
]
```

## Authentification et Sécurité

### Protection des Vues
- Utilisation de `LoginRequiredMixin` pour toutes les vues
- Protection CSRF pour tous les formulaires
- Validation des données côté serveur

### Configuration de l'Authentification
```python
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

## Interface Utilisateur

### Composants Bootstrap
- Navigation responsive
- Cartes pour l'affichage des données
- Formulaires stylisés
- Messages d'alerte
- Boutons d'action

### Template de Base
```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Gestion des Employés{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    {% block content %}{% endblock %}
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

## Base de Données

### Configuration PostgreSQL
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gestion_employes',
        'USER': 'postgres',
        'PASSWORD': 'votre_mot_de_passe',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Déploiement

### Étapes de Déploiement
1. Préparer l'environnement de production
2. Configurer les variables d'environnement
3. Collecter les fichiers statiques
4. Configurer le serveur web (Nginx/Apache)
5. Configurer Gunicorn
6. Mettre en place SSL/TLS

## Ressources Utiles

### Documentation
- [Documentation Django](https://docs.djangoproject.com/)
- [Documentation Bootstrap](https://getbootstrap.com/docs/)
- [Documentation django-crispy-forms](https://django-crispy-forms.readthedocs.io/)

### Outils
- [PostgreSQL](https://www.postgresql.org/docs/)
- [Gunicorn](https://docs.gunicorn.org/)
- [Nginx](https://nginx.org/en/docs/)

## Dépannage

### Problèmes Courants
1. Erreur de template manquant
   - Vérifier le chemin du template
   - Vérifier l'extension du template

2. Erreur de base de données
   - Vérifier les migrations
   - Vérifier la connexion à la base de données

3. Erreur de formulaire
   - Vérifier les champs requis
   - Vérifier la validation des données

## Bonnes Pratiques

### Code
- Suivre les conventions PEP 8
- Documenter le code
- Utiliser des noms explicites
- Écrire des tests unitaires

### Sécurité
- Valider toutes les entrées utilisateur
- Utiliser des requêtes préparées
- Protéger contre les attaques CSRF
- Gérer correctement les sessions

### Performance
- Optimiser les requêtes de base de données
- Mettre en cache les données fréquemment utilisées
- Minimiser les fichiers statiques
- Utiliser la pagination pour les grandes listes 