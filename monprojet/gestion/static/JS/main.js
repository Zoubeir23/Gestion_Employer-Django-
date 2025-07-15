/**
 * Fichier JavaScript principal pour l'application Gestion des Employés
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialiser tous les modules
    initThemeToggle();
    initGlobalSearch();
    initKeyboardShortcuts();
    initDashboardUpdates();
    initAnimations();
    initConfirmations();
    initToastNotifications();
});

/**
 * Système de thème sombre/clair
 */
function initThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const htmlElement = document.documentElement;
    
    if (!themeToggle || !themeIcon) return;
    
    // Charger le thème sauvegardé
    const savedTheme = localStorage.getItem('theme') || 'light';
    htmlElement.setAttribute('data-bs-theme', savedTheme);
    updateThemeIcon(savedTheme);
    
    themeToggle.addEventListener('click', function() {
        const currentTheme = htmlElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        htmlElement.setAttribute('data-bs-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
        
        // Animation de transition
        document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
        setTimeout(() => {
            document.body.style.transition = '';
        }, 300);
        
        // Notification
        showToast(`Thème ${newTheme === 'dark' ? 'sombre' : 'clair'} activé`, 'info');
    });
    
    function updateThemeIcon(theme) {
        if (theme === 'dark') {
            themeIcon.className = 'fas fa-sun';
            themeToggle.title = 'Basculer vers le thème clair';
        } else {
            themeIcon.className = 'fas fa-moon';
            themeToggle.title = 'Basculer vers le thème sombre';
        }
    }
}

/**
 * Recherche globale
 */
function initGlobalSearch() {
    const searchInput = document.getElementById('globalSearch');
    const searchResults = document.getElementById('searchResults');
    let searchTimeout;

    if (!searchInput || !searchResults) return;

    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length < 2) {
            searchResults.style.display = 'none';
            return;
        }

        // Afficher un loader
        searchResults.innerHTML = '<div class="p-3 text-center"><div class="spinner-border spinner-border-sm" role="status"></div></div>';
        searchResults.style.display = 'block';

        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    });

    function performSearch(query) {
        const apiUrl = document.querySelector('[data-api-search]')?.dataset.apiSearch || '/api/recherche/';
        
        fetch(`${apiUrl}?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                displaySearchResults(data);
            })
            .catch(error => {
                console.error('Erreur de recherche:', error);
                searchResults.innerHTML = '<div class="p-3 text-center text-danger">Erreur de recherche</div>';
            });
    }

    function displaySearchResults(data) {
        let html = '';
        
        // Employés
        if (data.employers && data.employers.length > 0) {
            html += '<div class="search-category"><i class="fas fa-user-tie me-1"></i>Employés</div>';
            data.employers.forEach(emp => {
                html += `
                    <a href="${emp.url}" class="search-result-item">
                        <div class="fw-bold">${emp.nom}</div>
                        <small class="text-muted">${emp.poste} - ${emp.service}</small>
                    </a>
                `;
            });
        }
        
        // Services
        if (data.services && data.services.length > 0) {
            html += '<div class="search-category"><i class="fas fa-building me-1"></i>Services</div>';
            data.services.forEach(service => {
                html += `
                    <a href="${service.url}" class="search-result-item">
                        <div class="fw-bold">${service.nom}</div>
                        <small class="text-muted">${service.description}</small>
                    </a>
                `;
            });
        }
        
        // Congés
        if (data.conges && data.conges.length > 0) {
            html += '<div class="search-category"><i class="fas fa-calendar-alt me-1"></i>Congés</div>';
            data.conges.forEach(conge => {
                html += `
                    <a href="${conge.url}" class="search-result-item">
                        <div class="fw-bold">${conge.employer}</div>
                        <small class="text-muted">${conge.type} - ${conge.date_debut} - ${conge.statut}</small>
                    </a>
                `;
            });
        }
        
        if (html === '') {
            html = '<div class="p-3 text-center text-muted">Aucun résultat trouvé</div>';
        }
        
        searchResults.innerHTML = html;
        searchResults.style.display = 'block';
    }

    // Fermer les résultats quand on clique ailleurs
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });

    // Fermer avec Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            searchResults.style.display = 'none';
            searchInput.blur();
        }
    });
}

/**
 * Raccourcis clavier
 */
function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ignorer si on est dans un champ de saisie
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            return;
        }

        // Ctrl + N : Nouvel employé
        if (e.ctrlKey && e.key === 'n') {
            e.preventDefault();
            const url = document.querySelector('[data-url-employer-create]')?.dataset.urlEmployerCreate;
            if (url) window.location.href = url;
        }
        
        // Ctrl + S : Nouveau service
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            const url = document.querySelector('[data-url-service-create]')?.dataset.urlServiceCreate;
            if (url) window.location.href = url;
        }
        
        // Ctrl + C : Nouveau congé
        if (e.ctrlKey && e.key === 'c') {
            e.preventDefault();
            const url = document.querySelector('[data-url-conge-create]')?.dataset.urlCongeCreate;
            if (url) window.location.href = url;
        }
        
        // Ctrl + / : Focus sur la recherche
        if (e.ctrlKey && e.key === '/') {
            e.preventDefault();
            const globalSearch = document.getElementById('globalSearch');
            if (globalSearch) {
                globalSearch.focus();
                globalSearch.select();
            }
        }

        // T : Toggle theme
        if (e.key === 't' || e.key === 'T') {
            const themeToggle = document.getElementById('themeToggle');
            if (themeToggle) themeToggle.click();
        }
    });
}

/**
 * Actualisation automatique du dashboard
 */
function initDashboardUpdates() {
    if (window.location.pathname !== '/') return;

    const apiUrl = document.querySelector('[data-api-dashboard]')?.dataset.apiDashboard || '/api/dashboard/';
    
    setInterval(function() {
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                updateCounters(data);
            })
            .catch(error => console.log('Erreur actualisation:', error));
    }, 30000); // Actualiser toutes les 30 secondes
}

function updateCounters(data) {
    const counters = {
        'employers': data.total_employers,
        'services': data.total_services,
        'conges': data.total_conges,
        'conges-attente': data.conges_en_attente
    };

    Object.entries(counters).forEach(([key, value]) => {
        const element = document.querySelector(`[data-counter="${key}"]`);
        if (element && element.textContent !== value.toString()) {
            // Animation de mise à jour
            element.style.transform = 'scale(1.2)';
            element.style.transition = 'transform 0.2s ease';
            element.textContent = value;
            
            setTimeout(() => {
                element.style.transform = 'scale(1)';
            }, 200);
        }
    });
}

/**
 * Animations d'entrée
 */
function initAnimations() {
    const cards = document.querySelectorAll('.card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    cards.forEach(card => {
        observer.observe(card);
    });
}

/**
 * Confirmations de suppression
 */
function initConfirmations() {
    document.addEventListener('click', function(e) {
        const deleteLink = e.target.closest('a[href*="supprimer"]') || 
                          e.target.closest('button[data-action="delete"]');
        
        if (deleteLink) {
            const confirmMessage = deleteLink.dataset.confirmMessage || 
                                 'Êtes-vous sûr de vouloir supprimer cet élément ?';
            
            if (!confirm(confirmMessage)) {
                e.preventDefault();
            }
        }
    });
}

/**
 * Système de notifications toast
 */
function initToastNotifications() {
    // Créer le conteneur de toasts s'il n'existe pas
    if (!document.getElementById('toastContainer')) {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1055';
        document.body.appendChild(container);
    }
}

function showToast(message, type = 'info', duration = 5000) {
    const toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) return;

    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas fa-${getToastIcon(type)} me-2"></i>${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast, {
        delay: duration
    });
    
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

function getToastIcon(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-circle',
        'info': 'info-circle',
        'primary': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

/**
 * Utilitaires
 */
function showLoader() {
    const loader = document.createElement('div');
    loader.id = 'globalLoader';
    loader.className = 'spinner-overlay';
    loader.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(loader);
}

function hideLoader() {
    const loader = document.getElementById('globalLoader');
    if (loader) {
        loader.remove();
    }
}

function formatNumber(num) {
    return new Intl.NumberFormat('fr-FR').format(num);
}

function formatDate(dateString) {
    return new Intl.DateTimeFormat('fr-FR').format(new Date(dateString));
}

// Exposer les fonctions globalement
window.showToast = showToast;
window.showLoader = showLoader;
window.hideLoader = hideLoader;
window.formatNumber = formatNumber;
window.formatDate = formatDate;