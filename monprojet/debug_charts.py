#!/usr/bin/env python
"""
Script de diagnostic pour les graphiques
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

def test_chart_data():
    """Teste les données des graphiques"""
    from gestion.models import Service, Employer, Conge
    from django.db.models import Count
    from datetime import datetime, timedelta
    
    print("🔍 DIAGNOSTIC DES DONNÉES DES GRAPHIQUES")
    print("=" * 50)
    
    # Test des données de services
    print("\n📊 DONNÉES DES SERVICES :")
    services_data = Service.objects.annotate(
        nb_employes=Count('employer')
    ).values('nom', 'nb_employes')
    
    services_list = list(services_data)
    print(f"Nombre de services : {len(services_list)}")
    for service in services_list:
        print(f"  - {service['nom']}: {service['nb_employes']} employé(s)")
    
    print(f"\nJSON des services : {services_list}")
    
    # Test des données de congés
    print("\n📅 DONNÉES DES CONGÉS :")
    conges_stats = {
        'en_attente': Conge.objects.filter(statut='EN_ATTENTE').count(),
        'approuves': Conge.objects.filter(statut='APPROUVE').count(),
        'rejetes': Conge.objects.filter(statut='REJETE').count()
    }
    
    print(f"En attente : {conges_stats['en_attente']}")
    print(f"Approuvés : {conges_stats['approuves']}")
    print(f"Rejetés : {conges_stats['rejetes']}")
    print(f"\nJSON des congés : {conges_stats}")
    
    # Test des données d'embauches
    print("\n👥 DONNÉES DES EMBAUCHES :")
    today = datetime.now().date()
    embauches_data = []
    
    for i in range(6):
        month_start = today.replace(day=1) - timedelta(days=i*30)
        month_end = month_start.replace(day=28) + timedelta(days=4)
        month_end = month_end - timedelta(days=month_end.day)
        
        count = Employer.objects.filter(
            date_embauche__gte=month_start,
            date_embauche__lte=month_end
        ).count()
        
        embauches_data.append({
            'mois': month_start.strftime('%B %Y'),
            'count': count
        })
    
    embauches_data = list(reversed(embauches_data))
    
    print(f"Nombre de mois : {len(embauches_data)}")
    for embauche in embauches_data:
        print(f"  - {embauche['mois']}: {embauche['count']} embauche(s)")
    
    print(f"\nJSON des embauches : {embauches_data}")

def test_template_context():
    """Teste le contexte du template"""
    from gestion.views import HomeView
    from django.test import RequestFactory
    from django.contrib.auth.models import User
    
    print("\n🔍 TEST DU CONTEXTE DU TEMPLATE")
    print("=" * 50)
    
    # Créer une requête factice
    factory = RequestFactory()
    request = factory.get('/')
    
    # Créer un utilisateur factice
    user = User.objects.first()
    if user:
        request.user = user
        
        # Créer la vue
        view = HomeView()
        view.request = request
        
        # Obtenir le contexte
        context = view.get_context_data()
        
        print("Clés du contexte :")
        for key in context.keys():
            print(f"  - {key}")
        
        # Vérifier les données des graphiques
        if 'services_chart_data' in context:
            print(f"\n✅ services_chart_data trouvé : {context['services_chart_data']}")
        else:
            print("\n❌ services_chart_data MANQUANT")
            
        if 'conges_chart_data' in context:
            print(f"✅ conges_chart_data trouvé : {context['conges_chart_data']}")
        else:
            print("❌ conges_chart_data MANQUANT")
            
        if 'embauches_chart_data' in context:
            print(f"✅ embauches_chart_data trouvé : {context['embauches_chart_data']}")
        else:
            print("❌ embauches_chart_data MANQUANT")
    else:
        print("❌ Aucun utilisateur trouvé")

def check_static_files():
    """Vérifie les fichiers statiques"""
    print("\n🔍 VÉRIFICATION DES FICHIERS STATIQUES")
    print("=" * 50)
    
    static_files = [
        'gestion/static/js/dashboard-charts.js',
        'gestion/static/js/main.js',
        'gestion/static/css/main.css'
    ]
    
    for file_path in static_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} ({size} bytes)")
            
            # Vérifier le contenu du fichier JavaScript
            if 'dashboard-charts.js' in file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'initDashboardCharts' in content:
                        print("  ✅ Fonction initDashboardCharts trouvée")
                    if 'Chart(' in content:
                        print("  ✅ Appels Chart.js trouvés")
                    if 'showChartError' in content:
                        print("  ✅ Fonction showChartError trouvée")
        else:
            print(f"❌ {file_path} - MANQUANT")

def generate_test_html():
    """Génère un fichier HTML de test"""
    print("\n🔍 GÉNÉRATION D'UN FICHIER DE TEST")
    print("=" * 50)
    
    html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Test des Graphiques</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .chart-container { width: 400px; height: 300px; margin: 20px; }
        canvas { border: 1px solid #ccc; }
    </style>
</head>
<body>
    <h1>Test des Graphiques</h1>
    
    <div class="chart-container">
        <h3>Services</h3>
        <canvas id="servicesChart"></canvas>
    </div>
    
    <div class="chart-container">
        <h3>Congés</h3>
        <canvas id="congesChart"></canvas>
    </div>
    
    <div class="chart-container">
        <h3>Embauches</h3>
        <canvas id="embauchesChart"></canvas>
    </div>
    
    <!-- Données de test -->
    <script id="services-chart-data" type="application/json">
    [{"nom": "IT", "nb_employes": 5}, {"nom": "RH", "nb_employes": 3}]
    </script>
    
    <script id="conges-chart-data" type="application/json">
    {"en_attente": 2, "approuves": 8, "rejetes": 1}
    </script>
    
    <script id="embauches-chart-data" type="application/json">
    [{"mois": "Janvier 2024", "count": 2}, {"mois": "Février 2024", "count": 1}]
    </script>
    
    <script>
    // Test simple des graphiques
    document.addEventListener('DOMContentLoaded', function() {
        console.log('DOM chargé');
        
        // Test graphique services
        const servicesCtx = document.getElementById('servicesChart');
        const servicesData = JSON.parse(document.getElementById('services-chart-data').textContent);
        
        console.log('Données services:', servicesData);
        
        new Chart(servicesCtx, {
            type: 'doughnut',
            data: {
                labels: servicesData.map(item => item.nom),
                datasets: [{
                    data: servicesData.map(item => item.nb_employes),
                    backgroundColor: ['#0d6efd', '#198754', '#ffc107']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
        
        console.log('Graphique services créé');
    });
    </script>
</body>
</html>
    """
    
    with open('test_charts.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Fichier test_charts.html créé")
    print("📋 Pour tester :")
    print("   1. Ouvrir test_charts.html dans un navigateur")
    print("   2. Ouvrir la console développeur (F12)")
    print("   3. Vérifier les messages de console")

def main():
    """Fonction principale"""
    print("🔍 DIAGNOSTIC COMPLET DES GRAPHIQUES")
    print("=" * 60)
    
    test_chart_data()
    test_template_context()
    check_static_files()
    generate_test_html()
    
    print("\n" + "=" * 60)
    print("✅ DIAGNOSTIC TERMINÉ")
    print("\n📋 ÉTAPES DE DÉBOGAGE :")
    print("1. Vérifier que les données sont présentes dans la base")
    print("2. Vérifier que les fichiers JavaScript sont chargés")
    print("3. Ouvrir la console développeur du navigateur")
    print("4. Tester avec le fichier test_charts.html")
    print("5. Vérifier les erreurs JavaScript dans la console")

if __name__ == "__main__":
    main()