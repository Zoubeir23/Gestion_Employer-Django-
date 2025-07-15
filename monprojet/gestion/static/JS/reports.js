/**
 * JavaScript pour les rapports
 */

document.addEventListener('DOMContentLoaded', function() {
    initReportCharts();
    initReportFilters();
    initPrintFunctionality();
});

/**
 * Initialise les graphiques des rapports
 */
function initReportCharts() {
    initServiceReportChart();
    initTypeReportChart();
}

/**
 * Graphique des congés par service (rapport)
 */
function initServiceReportChart() {
    const ctx = document.getElementById('serviceChart');
    if (!ctx) return;

    // Récupérer les données depuis l'élément JSON
    const dataElement = document.getElementById('service-chart-data');
    if (!dataElement) {
        console.warn('Données des services non trouvées');
        return;
    }

    try {
        const chartData = JSON.parse(dataElement.textContent);
        const labels = chartData.labels || [];
        const data = chartData.data || [];

        if (labels.length === 0 || data.length === 0) {
            showChartError(ctx, 'Aucune donnée disponible');
            return;
        }

        const colors = [
            '#0d6efd', '#198754', '#ffc107', '#dc3545', 
            '#0dcaf0', '#6c757d', '#fd7e14', '#6f42c1'
        ];

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors.slice(0, labels.length),
                    borderWidth: 2,
                    borderColor: '#fff',
                    hoverBorderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            usePointStyle: true,
                            font: {
                                size: 11
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${context.parsed} congé(s) (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Erreur lors de la création du graphique des services:', error);
        showChartError(ctx, 'Erreur de chargement des données');
    }
}

/**
 * Graphique des congés par type (rapport)
 */
function initTypeReportChart() {
    const ctx = document.getElementById('typeChart');
    if (!ctx) return;

    // Récupérer les données depuis l'élément JSON
    const dataElement = document.getElementById('type-chart-data');
    if (!dataElement) {
        console.warn('Données des types non trouvées');
        return;
    }

    try {
        const chartData = JSON.parse(dataElement.textContent);
        const labels = chartData.labels || [];
        const data = chartData.data || [];

        if (labels.length === 0 || data.length === 0) {
            showChartError(ctx, 'Aucune donnée disponible');
            return;
        }

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Nombre de congés',
                    data: data,
                    backgroundColor: '#0d6efd',
                    borderColor: '#0d6efd',
                    borderWidth: 1,
                    borderRadius: 4,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.parsed.y} congé(s)`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            callback: function(value) {
                                return Number.isInteger(value) ? value : '';
                            }
                        },
                        grid: {
                            color: '#e9ecef'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Erreur lors de la création du graphique des types:', error);
        showChartError(ctx, 'Erreur de chargement des données');
    }
}

/**
 * Initialise les filtres des rapports
 */
function initReportFilters() {
    const monthSelect = document.getElementById('monthFilter');
    const yearSelect = document.getElementById('yearFilter');
    const applyButton = document.getElementById('applyFilters');

    if (monthSelect && yearSelect && applyButton) {
        applyButton.addEventListener('click', function() {
            const month = monthSelect.value;
            const year = yearSelect.value;
            
            if (month && year) {
                const url = new URL(window.location);
                url.searchParams.set('mois', month);
                url.searchParams.set('annee', year);
                window.location.href = url.toString();
            }
        });

        // Permettre l'application avec Entrée
        [monthSelect, yearSelect].forEach(select => {
            select.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    applyButton.click();
                }
            });
        });
    }
}

/**
 * Initialise la fonctionnalité d'impression
 */
function initPrintFunctionality() {
    const printButtons = document.querySelectorAll('[data-action="print"]');
    
    printButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Masquer les éléments non nécessaires à l'impression
            const elementsToHide = document.querySelectorAll('.no-print, .btn, .navbar, .theme-toggle');
            elementsToHide.forEach(el => el.style.display = 'none');

            // Imprimer
            window.print();

            // Restaurer les éléments
            elementsToHide.forEach(el => el.style.display = '');
        });
    });

    // Gérer l'événement d'impression du navigateur
    window.addEventListener('beforeprint', function() {
        // Optimiser les graphiques pour l'impression
        const charts = Chart.instances;
        Object.values(charts).forEach(chart => {
            if (chart && chart.options) {
                chart.options.animation = false;
                chart.update('none');
            }
        });
    });

    window.addEventListener('afterprint', function() {
        // Restaurer les animations des graphiques
        const charts = Chart.instances;
        Object.values(charts).forEach(chart => {
            if (chart && chart.options) {
                chart.options.animation = true;
                chart.update();
            }
        });
    });
}

/**
 * Exporte les données du rapport en CSV
 */
function exportReportCSV(data, filename) {
    const csvContent = convertToCSV(data);
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

/**
 * Convertit les données en format CSV
 */
function convertToCSV(data) {
    if (!data || data.length === 0) return '';

    const headers = Object.keys(data[0]);
    const csvRows = [];

    // Ajouter les en-têtes
    csvRows.push(headers.join(','));

    // Ajouter les données
    data.forEach(row => {
        const values = headers.map(header => {
            const value = row[header];
            return typeof value === 'string' ? `"${value}"` : value;
        });
        csvRows.push(values.join(','));
    });

    return csvRows.join('\n');
}

/**
 * Affiche un message d'erreur dans un canvas
 */
function showChartError(canvas, message) {
    const ctx = canvas.getContext('2d');
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#dc3545';
    ctx.font = '14px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(message, canvas.width / 2, canvas.height / 2);
}

/**
 * Met à jour les statistiques en temps réel
 */
function updateReportStats() {
    const statsElements = document.querySelectorAll('[data-stat]');
    
    statsElements.forEach(element => {
        const statType = element.dataset.stat;
        const currentValue = parseInt(element.textContent);
        
        // Animation de compteur
        animateCounter(element, 0, currentValue, 1000);
    });
}

/**
 * Anime un compteur numérique
 */
function animateCounter(element, start, end, duration) {
    const startTime = performance.now();
    
    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(start + (end - start) * progress);
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        }
    }
    
    requestAnimationFrame(updateCounter);
}

// Exposer les fonctions globalement
window.exportReportCSV = exportReportCSV;
window.updateReportStats = updateReportStats;