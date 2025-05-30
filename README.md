# Gestion des Employés et Congés

Une application Django pour la gestion des employés et des congés.

## Fonctionnalités

### Gestion des Employés
- Liste des employés avec recherche et filtrage
- Détails des employés avec historique des congés
- Ajout, modification et suppression d'employés
- Statistiques par employé

### Gestion des Services
- Liste des services avec nombre d'employés
- Détails des services avec liste des employés
- Ajout, modification et suppression de services

### Gestion des Congés
- Liste des congés avec filtrage par statut
- Détails des congés avec informations complètes
- Demande de congé avec validation
- Approbation/Rejet des congés par les administrateurs
- Historique des congés par employé

### Interface d'Administration
- Dashboard admin complet (`/admin/`)
- Gestion des congés avec filtres avancés
- Gestion des employés et services
- Recherche et tri des données
- Statistiques globales

## Installation

1. Cloner le repository
```bash
git clone [URL_DU_REPO]
cd gestion_employes
```

2. Créer un environnement virtuel
```bash
python -m venv myenv
source myenv/bin/activate  # Linux/Mac
myenv\Scripts\activate     # Windows
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Configurer la base de données
```bash
python manage.py migrate
```

5. Créer un superuser
```bash
python manage.py createsuperuser
```

6. Lancer le serveur
```bash
python manage.py runserver
```

## Utilisation

### Interface Utilisateur
- Accéder à l'application : `http://localhost:8000`
- Gérer les employés : `/employes/`
- Gérer les services : `/services/`
- Gérer les congés : `/conges/`

### Interface d'Administration
- Accéder à l'admin : `http://localhost:8000/admin`
- Se connecter avec les identifiants superuser
- Gérer tous les aspects de l'application

## Technologies Utilisées

- Django 5.2
- PostgreSQL
- Bootstrap 5
- Font Awesome
- Crispy Forms

## Structure du Projet

```
monprojet/
├── gestion/
│   ├── models.py      # Modèles de données
│   ├── views.py       # Vues de l'application
│   ├── forms.py       # Formulaires
│   ├── admin.py       # Configuration admin
│   └── templates/     # Templates HTML
├── monprojet/
│   ├── settings.py    # Configuration
│   ├── urls.py        # URLs principales
│   └── wsgi.py        # Configuration WSGI
└── manage.py          # Script de gestion Django
```

## Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue. 