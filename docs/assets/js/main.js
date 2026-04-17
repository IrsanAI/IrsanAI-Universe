const translations = {
    de: {
        subtitle: "Spec-First Multi-Agent Resonance Framework. Der zentrale Hub für alle IrsanAI Protokolle und Tools.",
        stats_repos: "Repositories",
        stats_stars: "Sterne",
        stats_update: "Letztes Update",
        search_placeholder: "Projekte durchsuchen...",
        filter_all: "Alle",
        filter_hub: "Hub",
        filter_protocol: "Protokolle",
        filter_tool: "Tools",
        filter_agent: "Agenten",
        updated_prefix: "Aktualisiert: ",
        no_desc: "Keine Beschreibung verfügbar.",
        error_load: "Fehler beim Laden der Repository-Daten.",
        time_years: " Jahren",
        time_months: " Monaten",
        time_days: " Tagen",
        time_hours: " Stunden",
        time_minutes: " Minuten",
        time_seconds: " Sekunden",
        link_page: "🌐 Page",
        link_code: "💻 Code"
    },
    en: {
        subtitle: "Spec-First Multi-Agent Resonance Framework. The central hub for all IrsanAI protocols and tools.",
        stats_repos: "Repositories",
        stats_stars: "Stars",
        stats_update: "Last Update",
        search_placeholder: "Search projects...",
        filter_all: "All",
        filter_hub: "Hub",
        filter_protocol: "Protocols",
        filter_tool: "Tools",
        filter_agent: "Agents",
        updated_prefix: "Updated: ",
        no_desc: "No description available.",
        error_load: "Error loading repository data.",
        time_years: " years ago",
        time_months: " months ago",
        time_days: " days ago",
        time_hours: " hours ago",
        time_minutes: " minutes ago",
        time_seconds: " seconds ago",
        link_page: "🌐 Page",
        link_code: "💻 Code"
    }
};

let currentLang = localStorage.getItem('irsanai_lang') || 'de';
let allRepos = [];
let currentFilter = 'all';
let searchQuery = '';

document.addEventListener('DOMContentLoaded', () => {
    const repoGrid = document.getElementById('repo-grid');
    const searchBox = document.getElementById('search-box');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const langBtns = document.querySelectorAll('.lang-btn');

    // Initial Language Setup
    updateLanguageUI();

    // Load Data
    fetch('repo_manifest.json')
        .then(response => response.json())
        .then(data => {
            allRepos = data.repositories;
            const lastUpdated = new Date(data.last_updated);
            
            updateStats(allRepos, lastUpdated);
            renderRepos();
        })
        .catch(error => {
            console.error('Error loading manifest:', error);
            repoGrid.innerHTML = `<p style="color: #ff6b35; text-align: center; grid-column: 1/-1;">${translations[currentLang].error_load}</p>`;
        });

    // Search Event
    searchBox.addEventListener('input', (e) => {
        searchQuery = e.target.value.toLowerCase();
        renderRepos();
    });

    // Filter Events
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            renderRepos();
        });
    });

    // Language Switcher
    langBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            langBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentLang = btn.dataset.lang;
            localStorage.setItem('irsanai_lang', currentLang);
            updateLanguageUI();
            renderRepos();
        });
    });

    function updateLanguageUI() {
        const t = translations[currentLang];
        document.querySelector('.subtitle').textContent = t.subtitle;
        document.getElementById('search-box').placeholder = t.search_placeholder;
        document.querySelectorAll('.stat-label')[0].textContent = t.stats_repos;
        document.querySelectorAll('.stat-label')[1].textContent = t.stats_stars;
        document.querySelectorAll('.stat-label')[2].textContent = t.stats_update;
        
        // Update Filter Buttons
        document.querySelector('[data-filter="all"]').textContent = t.filter_all;
        document.querySelector('[data-filter="hub"]').textContent = t.filter_hub;
        document.querySelector('[data-filter="protocol"]').textContent = t.filter_protocol;
        document.querySelector('[data-filter="tool"]').textContent = t.filter_tool;
        document.querySelector('[data-filter="agent"]').textContent = t.filter_agent;

        // Active Button State
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.lang === currentLang);
        });
    }

    function updateStats(repos, lastUpdated) {
        document.getElementById('total-repos').textContent = repos.length;
        document.getElementById('total-stars').textContent = repos.reduce((sum, r) => sum + (r.stars || 0), 0);
        document.getElementById('last-update-time').textContent = lastUpdated.toLocaleDateString(currentLang === 'de' ? 'de-DE' : 'en-US', {
            day: '2-digit', month: '2-digit', year: 'numeric'
        });
    }

    function renderRepos() {
        repoGrid.innerHTML = '';
        const filtered = allRepos.filter(repo => {
            const matchesFilter = currentFilter === 'all' || repo.category === currentFilter;
            const matchesSearch = repo.name.toLowerCase().includes(searchQuery) || 
                                 (repo.description && repo.description.toLowerCase().includes(searchQuery));
            return matchesFilter && matchesSearch;
        });

        filtered.sort((a, b) => new Date(b.last_pushed) - new Date(a.last_pushed));

        filtered.forEach(repo => {
            repoGrid.appendChild(createRepoCard(repo));
        });
    }

    function createRepoCard(repo) {
        const t = translations[currentLang];
        const card = document.createElement('div');
        card.className = 'repo-card';
        
        const lastPushed = new Date(repo.last_pushed);
        const timeAgo = getTimeAgo(lastPushed);
        const categoryClass = `cat-${repo.category}`;
        
        card.innerHTML = `
            <div class="repo-header">
                <a href="${repo.url}" class="repo-name" target="_blank">${repo.name}</a>
                <span class="category-badge ${categoryClass}">${repo.category}</span>
            </div>
            <p class="repo-desc">${repo.description || t.no_desc}</p>
            <div class="repo-footer">
                <div class="update-time">
                    <span class="live-indicator"></span>
                    <span>${t.updated_prefix}${timeAgo}</span>
                </div>
                <div class="repo-links">
                    <a href="${repo.homepage}" target="_blank">${t.link_page}</a>
                    <a href="${repo.url}" target="_blank">${t.link_code}</a>
                </div>
            </div>
        `;
        return card;
    }

    function getTimeAgo(date) {
        const t = translations[currentLang];
        const seconds = Math.floor((new Date() - date) / 1000);
        let interval = seconds / 31536000;
        if (interval > 1) return Math.floor(interval) + t.time_years;
        interval = seconds / 2592000;
        if (interval > 1) return Math.floor(interval) + t.time_months;
        interval = seconds / 86400;
        if (interval > 1) return Math.floor(interval) + t.time_days;
        interval = seconds / 3600;
        if (interval > 1) return Math.floor(interval) + t.time_hours;
        interval = seconds / 60;
        if (interval > 1) return Math.floor(interval) + t.time_minutes;
        return Math.floor(seconds) + t.time_seconds;
    }
});
