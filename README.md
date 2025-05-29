# Gestion des Employés

Une application Django pour la gestion des employés, des services et des congés.

## Fonctionnalités

- Gestion des employés
- Gestion des services
- Gestion des congés
- Interface d'administration Django

## Prérequis

- Python 3.x
- PostgreSQL
- pip (gestionnaire de paquets Python)

## Installation

1. Cloner le repository :
```bash
git clone [URL_DU_REPO]
cd Gestion_employes
```

2. Créer un environnement virtuel :
```bash
python -m venv myenv
```

3. Activer l'environnement virtuel :
- Windows :
```bash
myenv\Scripts\activate
```
- Linux/Mac :
```bash
source myenv/bin/activate
```

4. Installer les dépendances :
```bash
pip install -r requirements.txt
```

5. Configurer la base de données PostgreSQL :
- Créer une base de données nommée 'gestion_employes'
- Configurer les paramètres de connexion dans `monprojet/monprojet/settings.py`

6. Effectuer les migrations :
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Créer un superutilisateur :
```bash
python manage.py createsuperuser
```

8. Lancer le serveur de développement :
```bash
python manage.py runserver
```

## Structure du Projet

- `gestion/` : Application principale
  - `models.py` : Définition des modèles (Employer, Service, Conge)
  - `admin.py` : Configuration de l'interface d'administration
  - `views.py` : Logique de l'application
  - `urls.py` : Configuration des URLs

## Modèles

### Service
- nom : Nom du service

### Employer
- nom : Nom de l'employé
- service : Relation avec le modèle Service
- date_embauche : Date d'embauche

### Conge
- employer : Relation avec le modèle Employer
- date_debut : Date de début du congé
- date_fin : Date de fin du congé
- raison : Raison du congé (optionnel)

## Utilisation

1. Accéder à l'interface d'administration :
   - URL : http://localhost:8000/admin
   - Utiliser les identifiants du superutilisateur créé

2. Gérer les données :
   - Ajouter/modifier/supprimer des services
   - Gérer les employés
   - Gérer les congés

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. 