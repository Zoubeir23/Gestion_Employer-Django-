#!/usr/bin/env python
"""
Script de test pour vérifier l'ajout de congés
"""

import os
import sys
import django
from datetime import date, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

def test_conge_creation():
    """Teste la création de congés"""
    from gestion.models import Employer, Service, Conge
    from gestion.forms import CongeForm
    
    print("🔍 TEST DE CRÉATION DE CONGÉS")
    print("=" * 50)
    
    # Vérifier qu'il y a des employés
    employers = Employer.objects.all()
    print(f"Nombre d'employés disponibles : {employers.count()}")
    
    if employers.count() == 0:
        print("❌ Aucun employé trouvé. Création d'un employé de test...")
        
        # Créer un service de test
        service, created = Service.objects.get_or_create(
            nom="Service Test",
            defaults={'description': 'Service créé pour les tests'}
        )
        
        # Créer un employé de test
        employer = Employer.objects.create(
            nom="Dupont",
            prenom="Jean",
            email="jean.dupont@test.com",
            genre="M",
            service=service,
            date_embauche=date.today() - timedelta(days=365),
            salaire=35000.00,
            poste="Développeur"
        )
        print(f"✅ Employé créé : {employer}")
    else:
        employer = employers.first()
        print(f"✅ Utilisation de l'employé : {employer}")
    
    # Tester la création d'un congé
    print("\n📅 TEST DE CRÉATION DE CONGÉ")
    
    # Données de test pour un congé
    conge_data = {
        'employer': employer.id,
        'type_conge': 'ANNUEL',
        'date_debut': date.today() + timedelta(days=30),
        'date_fin': date.today() + timedelta(days=35),
        'raison': 'Congés d\'été'
    }
    
    # Tester le formulaire
    form = CongeForm(data=conge_data)
    
    if form.is_valid():
        print("✅ Formulaire valide")
        conge = form.save()
        print(f"✅ Congé créé : {conge}")
        print(f"   - Employé : {conge.employer}")
        print(f"   - Type : {conge.get_type_conge_display()}")
        print(f"   - Période : {conge.date_debut} au {conge.date_fin}")
        print(f"   - Durée : {conge.duree_jours} jours")
        print(f"   - Statut : {conge.get_statut_display()}")
    else:
        print("❌ Formulaire invalide")
        print("Erreurs :")
        for field, errors in form.errors.items():
            print(f"  - {field}: {errors}")

def test_conge_validations():
    """Teste les validations des congés"""
    from gestion.models import Employer, Service
    from gestion.forms import CongeForm
    
    print("\n🔍 TEST DES VALIDATIONS")
    print("=" * 50)
    
    # Récupérer un employé
    employer = Employer.objects.first()
    if not employer:
        print("❌ Aucun employé disponible pour les tests")
        return
    
    # Test 1: Date dans le passé
    print("\n1. Test date dans le passé :")
    form_data = {
        'employer': employer.id,
        'type_conge': 'ANNUEL',
        'date_debut': date.today() - timedelta(days=1),
        'date_fin': date.today() + timedelta(days=5),
        'raison': 'Test passé'
    }
    form = CongeForm(data=form_data)
    if form.is_valid():
        print("❌ Le formulaire devrait être invalide (date passée)")
    else:
        print("✅ Validation correcte - date passée rejetée")
        print(f"   Erreur : {form.non_field_errors()}")
    
    # Test 2: Date fin avant date début
    print("\n2. Test date fin avant date début :")
    form_data = {
        'employer': employer.id,
        'type_conge': 'ANNUEL',
        'date_debut': date.today() + timedelta(days=10),
        'date_fin': date.today() + timedelta(days=5),
        'raison': 'Test ordre dates'
    }
    form = CongeForm(data=form_data)
    if form.is_valid():
        print("❌ Le formulaire devrait être invalide (dates inversées)")
    else:
        print("✅ Validation correcte - dates inversées rejetées")
        print(f"   Erreur : {form.non_field_errors()}")
    
    # Test 3: Durée excessive
    print("\n3. Test durée excessive (congé annuel > 30 jours) :")
    form_data = {
        'employer': employer.id,
        'type_conge': 'ANNUEL',
        'date_debut': date.today() + timedelta(days=30),
        'date_fin': date.today() + timedelta(days=65),  # 35 jours
        'raison': 'Test durée excessive'
    }
    form = CongeForm(data=form_data)
    if form.is_valid():
        print("❌ Le formulaire devrait être invalide (durée excessive)")
    else:
        print("✅ Validation correcte - durée excessive rejetée")
        print(f"   Erreur : {form.non_field_errors()}")

def test_conge_urls():
    """Teste les URLs des congés"""
    from django.urls import reverse
    
    print("\n🔍 TEST DES URLs")
    print("=" * 50)
    
    urls_to_test = [
        ('conge-list', 'Liste des congés'),
        ('conge-create', 'Création de congé'),
    ]
    
    for url_name, description in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"✅ {description}: {url}")
        except Exception as e:
            print(f"❌ {description}: {e}")

def test_conge_model():
    """Teste le modèle Conge"""
    from gestion.models import Conge
    
    print("\n🔍 TEST DU MODÈLE CONGÉ")
    print("=" * 50)
    
    # Statistiques des congés
    total_conges = Conge.objects.count()
    conges_en_attente = Conge.objects.filter(statut='EN_ATTENTE').count()
    conges_approuves = Conge.objects.filter(statut='APPROUVE').count()
    conges_rejetes = Conge.objects.filter(statut='REJETE').count()
    
    print(f"Total des congés : {total_conges}")
    print(f"En attente : {conges_en_attente}")
    print(f"Approuvés : {conges_approuves}")
    print(f"Rejetés : {conges_rejetes}")
    
    # Afficher quelques congés récents
    conges_recents = Conge.objects.order_by('-date_demande')[:5]
    print(f"\nDerniers congés créés :")
    for conge in conges_recents:
        print(f"  - {conge.employer} : {conge.get_type_conge_display()} du {conge.date_debut} au {conge.date_fin}")

def main():
    """Fonction principale"""
    print("🧪 TESTS COMPLETS DES CONGÉS")
    print("=" * 60)
    
    test_conge_model()
    test_conge_urls()
    test_conge_creation()
    test_conge_validations()
    
    print("\n" + "=" * 60)
    print("✅ TESTS TERMINÉS")
    print("\n📋 POUR TESTER MANUELLEMENT :")
    print("1. Lance le serveur : python manage.py runserver")
    print("2. Va sur : http://127.0.0.1:8000/conges/nouveau/")
    print("3. Remplis le formulaire et teste les validations")
    print("4. Vérifie que le congé apparaît dans la liste")

if __name__ == "__main__":
    main()