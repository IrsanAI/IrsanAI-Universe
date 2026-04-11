document.addEventListener('DOMContentLoaded', () => {
    const repoGrid = document.getElementById('repo-grid');
    const totalReposEl = document.getElementById('total-repos');
    const lastUpdateEl = document.getElementById('last-update-time');
    const totalStarsEl = document.getElementById('total-stars');
    fetch('repo_manifest.json').then(response => response.json()).then(data => {
        const repos = data.repositories;
        const lastUpdated = new Date(data.last_updated);
        totalReposEl.textContent = repos.length;
        lastUpdateEl.textContent = lastUpdated.toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });
        const totalStars = repos.reduce((sum, repo) => sum + (repo.stars || 0), 0);
        totalStarsEl.textContent = totalStars;
        repos.sort((a, b) => new Date(b.last_pushed) - new Date(a.last_pushed));
        repos.forEach(repo => { repoGrid.appendChild(createRepoCard(repo)); });
    }).catch(error => { console.error('Error loading manifest:', error); });
    function createRepoCard(repo) {
        const card = document.createElement('div');
        card.className = 'repo-card';
        const lastPushed = new Date(repo.last_pushed);
        const timeAgo = getTimeAgo(lastPushed);
        const categoryClass = 'cat-' + repo.category;
        card.innerHTML = '<div class=\"repo-header\"><a href=\"' + repo.url + '\" class=\"repo-name\" target=\"_blank\">' + repo.name + '</a><span class=\"category-badge ' + categoryClass + '\">' + repo.category + '</span></div><p class=\"repo-desc\">' + (repo.description || 'Keine Beschreibung verfügbar.') + '</p><div class=\"repo-footer\"><div class=\"update-time\"><span class=\"live-indicator\"></span><span>Aktualisiert: ' + timeAgo + '</span></div><div class=\"repo-links\"><a href=\"' + repo.homepage + '\" title=\"GitHub Page\" target=\"_blank\">🌐 Page</a><a href=\"' + repo.url + '\" title=\"Source Code\" target=\"_blank\">💻 Code</a></div></div>';
        return card;
    }
    function getTimeAgo(date) {
        const seconds = Math.floor((new Date() - date) / 1000);
        let interval = seconds / 31536000;
        if (interval > 1) return Math.floor(interval) + " Jahren";
        interval = seconds / 2592000;
        if (interval > 1) return Math.floor(interval) + " Monaten";
        interval = seconds / 86400;
        if (interval > 1) return Math.floor(interval) + " Tagen";
        interval = seconds / 3600;
        if (interval > 1) return Math.floor(interval) + " Stunden";
        interval = seconds / 60;
        if (interval > 1) return Math.floor(interval) + " Minuten";
        return Math.floor(seconds) + " Sekunden";
    }
});
