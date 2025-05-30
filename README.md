# Système de Gestion des Employés

Une application Django moderne pour la gestion des employés, des services et des congés.

## Fonctionnalités

### Gestion des Employés
- Création, modification et suppression d'employés
- Informations détaillées (nom, prénom, email, téléphone, genre, etc.)
- Association avec un service
- Gestion des salaires et des postes
- Pagination et recherche des employés
- Interface utilisateur intuitive avec Bootstrap 5

### Gestion des Services
- Création et gestion des services
- Nombre d'employés par service
- Description détaillée des services
- Interface de gestion complète

### Gestion des Congés
- Demandes de congés (annuel, maladie, maternité, paternité)
- Suivi des statuts (en attente, approuvé, rejeté)
- Validation des demandes
- Filtrage et recherche des congés
- Interface de gestion des demandes

### Interface Utilisateur
- Design moderne avec Bootstrap 5
- Formulaires stylisés avec django-crispy-forms
- Messages de confirmation pour chaque action
- Navigation intuitive
- Tableau de bord avec statistiques
- Responsive design

## Technologies Utilisées
- Python 3.8+
- Django 5.2
- PostgreSQL
- Bootstrap 5
- django-crispy-forms
- crispy-bootstrap5

## Prérequis
- Python 3.8 ou supérieur
- PostgreSQL
- pip (gestionnaire de paquets Python)

## Installation

1. Cloner le dépôt :
```bash
git clone [URL_DU_REPO]
cd gestion_employes
```

2. Créer un environnement virtuel :
```bash
python -m venv myenv
source myenv/bin/activate  # Linux/Mac
myenv\Scripts\activate     # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer la base de données :
- Créer une base de données PostgreSQL
- Mettre à jour les paramètres de connexion dans `settings.py`

5. Effectuer les migrations :
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Créer un superutilisateur :
```bash
python manage.py createsuperuser
```

7. Lancer le serveur de développement :
```bash
python manage.py runserver
```

## Structure du Projet
```
monprojet/
├── gestion/
│   ├── templates/
│   │   └── gestion/
│   │       ├── base.html
│   │       ├── form_base.html
│   │       ├── home.html
│   │       ├── employer_list.html
│   │       ├── employer_form.html
│   │       ├── service_list.html
│   │       ├── service_form.html
│   │       ├── conge_list.html
│   │       └── conge_form.html
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── monprojet/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```

## Utilisation

1. Accéder à l'interface d'administration :
   - URL : http://localhost:8000/admin
   - Utiliser les identifiants du superutilisateur

2. Accéder à l'application :
   - URL : http://localhost:8000
   - Interface principale avec tableau de bord

## Fonctionnalités des Formulaires
- Validation des données en temps réel
- Messages d'erreur clairs
- Champs obligatoires marqués
- Interface utilisateur intuitive
- Support des dates avec sélecteur de calendrier
- Gestion des relations entre modèles

## Sécurité
- Authentification requise pour toutes les actions
- Protection CSRF
- Validation des données côté serveur
- Gestion sécurisée des mots de passe

## Contribution
Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence
Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue. 