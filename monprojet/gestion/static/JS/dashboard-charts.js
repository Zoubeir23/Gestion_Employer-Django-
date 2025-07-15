/**
 * Graphiques du dashboard
 */

// Configuration des couleurs
const CHART_COLORS = {
    primary: '#0d6efd',
    success: '#198754',
    warning: '#ffc107',
    danger: '#dc3545',
    info: '#0dcaf0',
    secondary: '#6c757d',
    light: '#f8f9fa',
    dark: '#212529'
};

// Configuration par défaut des graphiques
const DEFAULT_CHART_OPTIONS = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'bottom',
            labels: {
                padding: 20,
                usePointStyle: true,
                font: {
                    size: 12
                }
            }
        }
    }
};

document.addEventListener('DOMContentLoaded', function() {
    initDashboardCharts();
});

function initDashboardCharts() {
    initServicesChart();
    initCongesChart();
    initEmbauchesChart();
}

/**
 * Graphique des employés par service
 */
function initServicesChart() {
    const ctx = document.getElementById('servicesChart');
    if (!ctx) return;

    const dataElement = document.getElementById('services-chart-data');
    if (!dataElement) {
        console.warn('Données des services non trouvées');
        showChartError(ctx, 'Données non disponibles');
        return;
    }

    try {
        const servicesData = JSON.parse(dataElement.textContent);
        
        if (!servicesData || servicesData.length === 0) {
            showChartError(ctx, 'Aucune donnée de service');
            return;
        }
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: servicesData.map(item => item.nom),
                datasets: [{
                    data: servicesData.map(item => item.nb_employes),
                    backgroundColor: [
                        CHART_COLORS.primary,
                        CHART_COLORS.success,
                        CHART_COLORS.warning,
                        CHART_COLORS.info,
                        CHART_COLORS.secondary,
                        CHART_COLORS.danger
                    ],
                    borderWidth: 2,
                    borderColor: '#fff',
                    hoverBorderWidth: 3
                }]
            },
            options: {
                ...DEFAULT_CHART_OPTIONS,
                plugins: {
                    ...DEFAULT_CHART_OPTIONS.plugins,
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = total > 0 ? ((context.parsed / total) * 100).toFixed(1) : 0;
                                return `${context.label}: ${context.parsed} employé(s) (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Erreur lors de la création du graphique des services:', error);
        showChartError(ctx, 'Erreur de chargement des données des services');
    }
}

/**
 * Graphique des congés par statut
 */
function initCongesChart() {
    const ctx = document.getElementById('congesChart');
    if (!ctx) return;

    const dataElement = document.getElementById('conges-chart-data');
    if (!dataElement) {
        console.warn('Données des congés non trouvées');
        showChartError(ctx, 'Données non disponibles');
        return;
    }

    try {
        const congesData = JSON.parse(dataElement.textContent);
        
        if (!congesData) {
            showChartError(ctx, 'Aucune donnée de congé');
            return;
        }
        
        const data = [
            congesData.en_attente || 0, 
            congesData.approuves || 0, 
            congesData.rejetes || 0
        ];
        
        const total = data.reduce((a, b) => a + b, 0);
        if (total === 0) {
            showChartError(ctx, 'Aucun congé enregistré');
            return;
        }
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['En attente', 'Approuvés', 'Rejetés'],
                datasets: [{
                    data: data,
                    backgroundColor: [
                        CHART_COLORS.warning,
                        CHART_COLORS.success,
                        CHART_COLORS.danger
                    ],
                    borderWidth: 2,
                    borderColor: '#fff',
                    hoverBorderWidth: 3
                }]
            },
            options: {
                ...DEFAULT_CHART_OPTIONS,
                plugins: {
                    ...DEFAULT_CHART_OPTIONS.plugins,
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = total > 0 ? ((context.parsed / total) * 100).toFixed(1) : 0;
                                return `${context.label}: ${context.parsed} congé(s) (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Erreur lors de la création du graphique des congés:', error);
        showChartError(ctx, 'Erreur de chargement des données des congés');
    }
}

/**
 * Graphique d'évolution des embauches
 */
function initEmbauchesChart() {
    const ctx = document.getElementById('embauchesChart');
    if (!ctx) return;

    const dataElement = document.getElementById('embauches-chart-data');
    if (!dataElement) {
        console.warn('Données des embauches non trouvées');
        showChartError(ctx, 'Données non disponibles');
        return;
    }

    try {
        const embauchesData = JSON.parse(dataElement.textContent);
        
        if (!embauchesData || embauchesData.length === 0) {
            showChartError(ctx, 'Aucune donnée d\'embauche');
            return;
        }
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: embauchesData.map(item => item.mois),
                datasets: [{
                    label: 'Nouvelles embauches',
                    data: embauchesData.map(item => item.count),
                    borderColor: CHART_COLORS.primary,
                    backgroundColor: CHART_COLORS.primary + '20',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: CHART_COLORS.primary,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8
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
                                return `Embauches: ${context.parsed.y}`;
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
                            color: '#f8f9fa'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                }
            }
        });
    } catch (error) {
        console.error('Erreur lors de la création du graphique des embauches:', error);
        showChartError(ctx, 'Erreur de chargement des données des embauches');
    }
}

/**
 * Affiche un message d'erreur dans un canvas
 */
function showChartError(canvas, message) {
    const ctx = canvas.getContext('2d');
    const rect = canvas.getBoundingClientRect();
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#dc3545';
    ctx.font = '14px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(message, canvas.width / 2, canvas.height / 2);
}

/**
 * Fonction utilitaire pour créer des graphiques dynamiques
 */
function createChart(canvasId, type, data, options = {}) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    const defaultOptions = {
        ...DEFAULT_CHART_OPTIONS,
        ...options
    };

    return new Chart(ctx, {
        type: type,
        data: data,
        options: defaultOptions
    });
}

// Exposer les fonctions globalement si nécessaire
window.createChart = createChart;
window.CHART_COLORS = CHART_COLORS;