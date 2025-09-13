# 🚀 Système de Gestion des Employés et Congés

Une application Django moderne et complète pour la gestion des employés, services et congés avec interface interactive et fonctionnalités avancées.

## ✨ Fonctionnalités Principales

### 📊 Dashboard Interactif
- **Graphiques en temps réel** avec Chart.js
- **Statistiques dynamiques** (employés, services, congés)
- **Alertes automatiques** pour congés en attente
- **Actualisation automatique** toutes les 30 secondes
- **Indicateurs visuels** de performance

### 👥 Gestion des Employés
- **Liste avancée** avec recherche et filtres multiples
- **Profils détaillés** avec historique complet
- **Ajout/modification/suppression** sécurisés
- **Filtrage par service, poste, date d'embauche**
- **Export CSV** des données

### 🏢 Gestion des Services
- **Vue d'ensemble** avec nombre d'employés
- **Détails par service** avec liste des employés
- **Gestion complète** CRUD
- **Statistiques par service**

### 🏖️ Gestion des Congés Avancée
- **Validation automatique** des chevauchements
- **Calcul automatique** des durées
- **Workflow d'approbation** complet
- **Détection des demandes urgentes** (>7 jours)
- **Rapports mensuels** avec graphiques
- **Export et impression** des rapports

### 🔍 Recherche et Navigation
- **Recherche globale** en temps réel
- **Suggestions automatiques** multi-entités
- **Filtres avancés** combinables
- **Navigation intuitive** avec breadcrumbs

### 🎨 Interface Utilisateur Moderne
- **Thème sombre/clair** avec basculement
- **Design responsive** optimisé mobile
- **Animations fluides** et transitions
- **Notifications toast** élégantes
- **Indicateurs de statut** colorés

### ⌨️ Productivité
- **Raccourcis clavier** :
  - `Ctrl+N` : Nouvel employé
  - `Ctrl+S` : Nouveau service  
  - `Ctrl+C` : Nouveau congé
  - `Ctrl+/` : Focus recherche
- **Actions rapides** depuis le dashboard
- **Confirmations intelligentes**

### 📄 Rapports et Exports
- **Export CSV** employés et congés
- **Rapports mensuels** détaillés
- **Graphiques interactifs** par service/type
- **Impression optimisée**
- **Données prêtes pour Excel**

### 🔒 Sécurité et Permissions
- **Authentification obligatoire**
- **Permissions granulaires** par rôle
- **Protection CSRF** complète
- **Validation des données** côté serveur
- **Audit trail** des modifications

## 🛠️ Installation

### 1. Cloner le repository
```bash
git clone [URL_DU_REPO]
cd gestion_employes
```

### 2. Créer un environnement virtuel
```bash
python -m venv myenv
# Windows
myenv\Scripts\activate
# Linux/Mac
source myenv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer la base de données
```bash
# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser
```

### 5. Tester l'installation (optionnel)
```bash
python test_project.py
```

### 6. Lancer le serveur
```bash
python manage.py runserver
```

🎉 **L'application est maintenant accessible sur** `http://127.0.0.1:8000/`

## 🚀 Démarrage Rapide

### Première Connexion
1. **Aller sur** `http://127.0.0.1:8000/`
2. **Se connecter** avec votre compte superutilisateur
3. **Explorer le dashboard** avec graphiques interactifs
4. **Tester la recherche globale** dans la barre de navigation
5. **Basculer le thème** avec le bouton en bas à droite

### Créer vos Premières Données
1. **Créer un service** : Menu Services → Nouveau Service
2. **Ajouter un employé** : Menu Employés → Nouvel Employé
3. **Enregistrer un congé** : Menu Congés → Nouveau Congé
4. **Voir les rapports** : Menu Rapports → Congés mensuels

### Raccourcis Utiles
- **Ctrl+N** : Créer un nouvel employé
- **Ctrl+S** : Créer un nouveau service
- **Ctrl+C** : Créer un nouveau congé
- **Ctrl+/** : Focus sur la recherche

## 📱 Utilisation

### 🏠 Dashboard Principal
- **Statistiques en temps réel** des employés, services et congés
- **Graphiques interactifs** : répartition par service, évolution des embauches
- **Alertes automatiques** : congés en attente, anniversaires d'embauche
- **Actions rapides** : création directe depuis le dashboard

### 👥 Gestion des Employés (`/employes/`)
- **Liste complète** avec recherche avancée
- **Filtres multiples** : service, poste, date d'embauche
- **Profils détaillés** avec historique des congés
- **Export CSV** pour Excel

### 🏢 Gestion des Services (`/services/`)
- **Vue d'ensemble** avec statistiques
- **Détails par service** avec liste des employés
- **Gestion complète** CRUD

### 🏖️ Gestion des Congés (`/conges/`)
- **Liste avec filtres** par statut
- **Validation automatique** des chevauchements
- **Workflow d'approbation** pour les managers
- **Calcul automatique** des durées

### 📊 Rapports (`/rapports/`)
- **Rapport mensuel** des congés avec graphiques
- **Export CSV** des données
- **Impression optimisée**
- **Statistiques par service et type**

### 🔧 Administration (`/admin/`)
- **Interface Django Admin** complète
- **Gestion avancée** des utilisateurs et permissions
- **Configuration système**

## 🛠️ Technologies Utilisées

### Backend
- **Django 5.2** - Framework web Python
- **PostgreSQL** - Base de données relationnelle
- **Django Crispy Forms** - Formulaires stylisés

### Frontend
- **Bootstrap 5** - Framework CSS responsive
- **Chart.js** - Graphiques interactifs
- **Font Awesome** - Icônes vectorielles
- **JavaScript ES6** - Interactions dynamiques

### Fonctionnalités Avancées
- **API REST** pour données en temps réel
- **Recherche full-text** multi-entités
- **Système de thèmes** sombre/clair
- **Notifications toast** en temps réel
- **Validation côté client et serveur**

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
├── sauvegardes_db/    # Sauvegardes de la base de données
└── manage.py          # Script de gestion Django
```

## Sauvegarde de la Base de Données

### Méthode 1 : Utilisation de pgAdmin
1. Ouvrir pgAdmin
2. Clic droit sur la base de données "gestion_employes"
3. Sélectionner "Backup..."
4. Choisir le format "Custom"
5. Sélectionner le dossier `sauvegardes_db` comme destination
6. Nommer le fichier avec la date (ex: `export_YYYYMMDD.sql`)

### Méthode 2 : Utilisation de la ligne de commande
```bash
pg_dump -h localhost -U postgres -p 5432 -d gestion_employes > monprojet/sauvegardes_db/export_YYYYMMDD.sql
```

### Restauration de la Base de Données
```bash
psql -h localhost -U postgres -d gestion_employes < monprojet/sauvegardes_db/export_YYYYMMDD.sql
```

## Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

**Copyright (c) 2025 Zoubeir Ibrahim**

Vous êtes libre de :
- ✅ Utiliser ce logiciel à des fins commerciales et personnelles
- ✅ Modifier et distribuer le code source
- ✅ Créer des œuvres dérivées
- ✅ Utiliser le code dans des projets privés

**Conditions :**
- 📋 Inclure la notice de copyright et de licence
- 🚫 Aucune garantie fournie

## 👨‍💻 Auteur

**Zoubeir Ibrahim**
- 📧 Email : Zoubeiribrahima@gmail.com
- 🐙 GitHub : Zoubeir23

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. **Fork** le projet
2. **Créer** une branche feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** vos changements (`git commit -m 'Add some AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrir** une Pull Request

### 📝 Guidelines de Contribution
- Suivre les conventions PEP 8 pour Python
- Ajouter des tests pour les nouvelles fonctionnalités
- Documenter les changements dans le README
- Respecter la structure existante du projet

## 💬 Support

Pour toute question, suggestion ou problème :
- 🐛 **Issues** : Ouvrir une issue sur GitHub
- 📧 **Email** : Zoubeiribrahima@gmail.com
- 📖 **Documentation** : Consulter le fichier [RECAP.md](RECAP.md) 