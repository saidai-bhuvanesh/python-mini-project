// State Manager
const state = {
    projects: [],
    health: {},
    dependencies: {},
    lint: {},
    tests: {},
    security: {},
    benchmarks: {},
    contributors: [],
    learningPaths: { master_sequence: [], tracks: {} },
    activeSection: 'dashboard-section',
    selectedInterests: []
};

// Start initialization on page load
document.addEventListener('DOMContentLoaded', () => {
    initApp();
    setupEventListeners();
});

async function initApp() {
    // Attempt to fetch data files, falling back to mocks if files are missing
    await loadData();
    
    // Populate UI
    updateStats();
    populateQuizTags();
    renderProjectsDeck();
    populateSandboxSelect();
    renderContributors();
    renderRoadmaps();
    
    // Set system status synced
    document.getElementById('scan-status-text').innerText = "System Sync Success";
}

async function loadData() {
    // Utility to fetch or return fallback
    const fetchJson = async (url, fallback) => {
        try {
            const res = await fetch(url);
            if (!res.ok) throw new Error(`Status ${res.status}`);
            return await res.json();
        } catch (e) {
            console.warn(`Could not load ${url}. Using fallback mock dataset.`);
            return fallback;
        }
    };

    // Load files
    state.projects = await fetchJson('../projects_registry.json', [
        {
            "name": "calculator",
            "description": "A simple arithmetic calculator supporting add, subtract, multiply, and divide operations.",
            "author": "Alice",
            "difficulty": "Beginner",
            "tags": ["math", "utility", "cli"],
            "dependencies": [],
            "entry_point": "main.py"
        },
        {
            "name": "weather_cli",
            "description": "CLI utility to fetch mock weather details by city name.",
            "author": "Bob",
            "difficulty": "Intermediate",
            "tags": ["weather", "api", "cli"],
            "dependencies": ["requests"],
            "entry_point": "main.py"
        }
    ]);

    state.health = await fetchJson('../reports/broken_projects_report.json', {
        "calculator": { "health_score": 100, "status": "Healthy", "issues": [], "imports": [] },
        "weather_cli": { "health_score": 90, "status": "Healthy", "issues": [], "imports": ["requests"] },
        "unsupported_project": { "health_score": 30, "status": "Broken", "issues": ["Missing metadata.json", "Syntax error in main.py: SyntaxError on line 2"], "imports": [] }
    });

    // Add unsupported project if it exists in health report but not in registry
    Object.keys(state.health).forEach(name => {
        if (!state.projects.some(p => p.name === name)) {
            state.projects.push({
                name: name,
                description: "This project has critical standards violations and cannot be registered standardly.",
                author: "Unknown",
                difficulty: "Beginner",
                tags: ["broken"],
                dependencies: [],
                entry_point: "main.py",
                is_unsupported: true
            });
        }
    });

    state.dependencies = await fetchJson('../reports/dependency_report.json', {
        "calculator": { "declared": [], "imported_third_party": [], "unused": [], "undeclared": [] },
        "weather_cli": { "declared": ["requests"], "imported_third_party": ["requests"], "unused": [], "undeclared": [] }
    });

    state.lint = await fetchJson('../reports/lint_report.json', {
        "calculator": { "score": 95.0, "grade": "A", "violations": [] },
        "weather_cli": { "score": 88.0, "grade": "B", "violations": [] }
    });

    state.tests = await fetchJson('../reports/test_report.json', {
        "calculator": { "ran": true, "pass_rate": 100.0, "total": 4, "passed": 4, "failed": 0, "coverage": 95.0 },
        "weather_cli": { "ran": true, "pass_rate": 100.0, "total": 2, "passed": 2, "failed": 0, "coverage": 90.0 }
    });

    state.security = await fetchJson('../reports/security_report.json', {
        "calculator": { "security_score": 100, "severity": "Secure", "vulnerabilities": [] },
        "weather_cli": { "security_score": 100, "severity": "Secure", "vulnerabilities": [] }
    });

    state.benchmarks = await fetchJson('../reports/benchmark_report.json', {
        "calculator": { "success": true, "runtime_ms": 12.4, "memory_mb": 15.6 },
        "weather_cli": { "success": true, "runtime_ms": 145.2, "memory_mb": 18.2 }
    });

    state.contributors = await fetchJson('../reports/contributors_report.json', [
        { "name": "Alice", "email": "alice@example.com", "commits": 42, "projects": ["calculator"], "score": 470 },
        { "name": "Bob", "email": "bob@example.com", "commits": 28, "projects": ["weather_cli"], "score": 330 },
        { "name": "Charlie", "email": "charlie@example.com", "commits": 15, "projects": ["calculator", "weather_cli"], "score": 250 }
    ]);

    state.learningPaths = await fetchJson('../reports/learning_paths.json', {
        "master_sequence": ["calculator", "weather_cli"],
        "tracks": {
            "Core Python Mastery": ["calculator", "weather_cli"],
            "CLI & Scripting": ["calculator", "weather_cli"]
        }
    });
}

function updateStats() {
    const totalProj = state.projects.filter(p => !p.is_unsupported).length;
    document.getElementById('stat-total-projects').innerText = totalProj;
    
    // Average test pass rate
    let totalTests = 0, passedTests = 0;
    Object.values(state.tests).forEach(t => {
        if (t.ran) {
            totalTests += t.total;
            passedTests += t.passed;
        }
    });
    const testRate = totalTests > 0 ? Math.round((passedTests / totalTests) * 100) : 100;
    document.getElementById('stat-passing-tests').innerText = `${testRate}%`;

    // Average security score
    let totalSec = 0, secCount = 0;
    Object.values(state.security).forEach(s => {
        totalSec += s.security_score;
        secCount++;
    });
    const avgSec = secCount > 0 ? Math.round(totalSec / secCount) : 100;
    document.getElementById('stat-security-score').innerText = `${avgSec}/100`;

    document.getElementById('stat-contributors').innerText = state.contributors.length;

    // Insights panel values
    let coverageSum = 0, coverageCount = 0;
    Object.values(state.tests).forEach(t => {
        if (t.ran && t.coverage) {
            coverageSum += t.coverage;
            coverageCount++;
        }
    });
    const avgCoverage = coverageCount > 0 ? Math.round(coverageSum / coverageCount) : 0;
    document.getElementById('insight-coverage').innerText = `${avgCoverage}%`;

    const brokenProjects = state.projects.filter(p => {
        const h = state.health[p.name] || {};
        return h.status === 'Broken' || p.is_unsupported;
    }).length;
    const brokenRate = Math.round((brokenProjects / state.projects.length) * 100);
    document.getElementById('insight-broken-val').innerText = `${brokenRate}%`;
    document.getElementById('insight-broken-bar').style.width = `${brokenRate}%`;
}

// Populate search and tags
function populateQuizTags() {
    const tagsContainer = document.getElementById('quiz-tags-container');
    tagsContainer.innerHTML = '';
    
    const tags = new Set();
    state.projects.forEach(p => p.tags && p.tags.forEach(t => tags.add(t)));
    
    tags.forEach(tag => {
        const span = document.createElement('span');
        span.className = 'tag-option';
        span.innerText = tag;
        span.addEventListener('click', () => {
            span.classList.toggle('selected');
            if (span.classList.contains('selected')) {
                state.selectedInterests.push(tag);
            } else {
                state.selectedInterests = state.selectedInterests.filter(t => t !== tag);
            }
        });
        tagsContainer.appendChild(span);
    });
}

function renderProjectsDeck(filterText = '') {
    const deck = document.getElementById('projects-deck');
    deck.innerHTML = '';
    
    const diffFilter = document.getElementById('filter-difficulty').value;
    const statusFilter = document.getElementById('filter-status').value;
    
    state.projects.forEach(p => {
        const h = state.health[p.name] || { status: 'Broken', health_score: 0 };
        const l = state.lint[p.name] || { grade: 'F' };
        
        // Apply Filters
        if (diffFilter && p.difficulty !== diffFilter) return;
        if (statusFilter && h.status !== statusFilter) return;
        
        if (filterText) {
            const query = filterText.toLowerCase();
            const matchesQuery = p.name.toLowerCase().includes(query) || 
                                 p.description.toLowerCase().includes(query) ||
                                 p.tags.some(t => t.toLowerCase().includes(query));
            if (!matchesQuery) return;
        }

        const card = document.createElement('div');
        card.className = 'project-card';
        card.addEventListener('click', () => openProjectModal(p));
        
        const tagsHtml = p.tags ? p.tags.map(t => `<span class="tag">${t}</span>`).join('') : '';
        const healthClass = h.status.toLowerCase();
        
        card.innerHTML = `
            <div class="project-card-header">
                <h3>${p.name}</h3>
                <span class="badge ${p.difficulty.toLowerCase()}">${p.difficulty}</span>
            </div>
            <div class="project-card-body">
                <p>${p.description}</p>
            </div>
            <div class="project-card-tags">
                ${tagsHtml}
            </div>
            <div class="project-card-footer">
                <span class="status-badge ${healthClass}">
                    <i class="fa-solid fa-circle"></i> ${h.status}
                </span>
                <span class="quality-badge">Lint: ${l.grade}</span>
            </div>
        `;
        deck.appendChild(card);
    });
}

// Modal management
function openProjectModal(p) {
    const h = state.health[p.name] || { health_score: 0, issues: ["No registry details found."] };
    const modal = document.getElementById('project-detail-modal');
    
    document.getElementById('modal-project-title').innerText = p.name;
    document.getElementById('modal-project-desc').innerText = p.description;
    document.getElementById('modal-project-author').innerText = p.author || 'Anonymous';
    document.getElementById('modal-project-entry').innerText = p.entry_point || 'main.py';
    
    const badgesContainer = document.getElementById('modal-project-badges');
    badgesContainer.innerHTML = `
        <span class="badge ${p.difficulty.toLowerCase()}">${p.difficulty}</span>
        <span class="status-badge ${h.status.toLowerCase()}"><i class="fa-solid fa-circle"></i> ${h.status}</span>
    `;
    
    const depsContainer = document.getElementById('modal-project-deps');
    depsContainer.innerHTML = p.dependencies && p.dependencies.length > 0 
        ? p.dependencies.map(d => `<span class="tag">${d}</span>`).join('') 
        : '<span class="text-muted">None</span>';
        
    const scoreElem = document.getElementById('modal-health-score');
    scoreElem.innerText = h.health_score;
    // Set color based on score
    if (h.health_score >= 80) scoreElem.style.color = 'var(--accent-green)';
    else if (h.health_score >= 50) scoreElem.style.color = 'var(--accent-yellow)';
    else scoreElem.style.color = 'var(--accent-red)';
    
    const issuesContainer = document.getElementById('modal-health-issues');
    issuesContainer.innerHTML = h.issues && h.issues.length > 0 
        ? h.issues.map(i => `<li>${i}</li>`).join('') 
        : '<li style="color: var(--accent-green); list-style: none;"><i class="fa-solid fa-check"></i> Standard structure verified.</li>';
        
    modal.style.display = 'flex';
}

// Sandbox execution simulator
function populateSandboxSelect() {
    const select = document.getElementById('sandbox-project-select');
    select.innerHTML = '';
    state.projects.forEach(p => {
        if (!p.is_unsupported) {
            const opt = document.createElement('option');
            opt.value = p.name;
            opt.innerText = p.name;
            select.appendChild(opt);
        }
    });
}

function triggerSandboxRun() {
    const name = document.getElementById('sandbox-project-select').value;
    const args = document.getElementById('sandbox-args').value.trim();
    const timeout = document.getElementById('sandbox-timeout').value;
    const terminal = document.getElementById('sandbox-terminal-output');
    
    terminal.innerHTML = `<span class="term-line prompt">system@hub_sandbox:~$</span> Executing: python projects/${name}/main.py ${args}...<br>`;
    
    setTimeout(() => {
        if (name === 'calculator') {
            terminal.innerHTML += `
<span class="term-line info">[Sandbox Init] Creating isolated process container...</span><br>
Simple Calculator<br>
Add (2 + 3): 5<br>
Subtract (5 - 2): 3<br>
<span class="term-line prompt">system@hub_sandbox:~$</span> <span class="term-line info">Execution completed successfully in 14.5ms. (Exit code: 0)</span>
            `;
        } else if (name === 'weather_cli') {
            const city = args || 'London';
            terminal.innerHTML += `
<span class="term-line info">[Sandbox Init] Creating isolated process container...</span><br>
Fetching API request logs...<br>
Weather in ${city}: 15C, Cloudy<br>
<span class="term-line prompt">system@hub_sandbox:~$</span> <span class="term-line info">Execution completed successfully in 142.1ms. (Exit code: 0)</span>
            `;
        } else {
            terminal.innerHTML += `
<span class="term-line error">Process execution timed out or exited with non-zero code.</span>
            `;
        }
        terminal.scrollTop = terminal.scrollHeight;
    }, 800);
}

// Roadmaps rendering
function renderRoadmaps() {
    const canvas = document.getElementById('roadmap-canvas-container');
    canvas.innerHTML = '';
    
    const buttons = document.getElementById('learning-track-buttons');
    buttons.innerHTML = '';
    
    const tracks = state.learningPaths.tracks;
    
    Object.keys(tracks).forEach((trackName, idx) => {
        const btn = document.createElement('button');
        btn.className = `btn btn-secondary ${idx === 0 ? 'active' : ''}`;
        btn.innerText = trackName;
        btn.addEventListener('click', () => {
            // Toggle active
            Array.from(buttons.children).forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            displayTrackRoadmap(trackName);
        });
        buttons.appendChild(btn);
    });
    
    // Initial load first track
    if (Object.keys(tracks).length > 0) {
        displayTrackRoadmap(Object.keys(tracks)[0]);
    }
}

function displayTrackRoadmap(trackName) {
    const canvas = document.getElementById('roadmap-canvas-container');
    canvas.innerHTML = '';
    
    const trackProj = state.learningPaths.tracks[trackName];
    const flow = document.createElement('div');
    flow.className = 'roadmap-flow';
    
    trackProj.forEach((name, idx) => {
        const p = state.projects.find(proj => proj.name === name);
        if (!p) return;
        
        const node = document.createElement('div');
        node.className = `roadmap-node ${idx === 0 ? 'active' : ''}`;
        node.innerHTML = `
            <h4>Step ${idx + 1}: ${p.name}</h4>
            <p>${p.description}</p>
            <span class="badge ${p.difficulty.toLowerCase()}" style="margin-top: 8px; display: inline-block;">${p.difficulty}</span>
        `;
        
        flow.appendChild(node);
        
        // Add arrow if not last
        if (idx < trackProj.length - 1) {
            const arrow = document.createElement('div');
            arrow.className = 'roadmap-arrow';
            arrow.innerHTML = `<i class="fa-solid fa-arrow-down"></i>`;
            flow.appendChild(arrow);
        }
    });
    canvas.appendChild(flow);
}

// Contributor Leaderboard
function renderContributors() {
    const tbody = document.getElementById('contributors-table-body');
    tbody.innerHTML = '';
    
    state.contributors.forEach((c, idx) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>#${idx + 1}</strong></td>
            <td>
                <div style="font-weight: 600;">${c.name}</div>
                <div style="font-size: 11px; color: var(--text-muted);">${c.email}</div>
            </td>
            <td>${c.commits}</td>
            <td>${c.projects.join(', ')}</td>
            <td><span class="rec-score">${c.score}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

// Recommendations engine quiz runner
function generateRecommendations() {
    const level = document.querySelector('.difficulty-select .diff-btn.active').dataset.level;
    const recsList = document.getElementById('recs-list-container');
    recsList.innerHTML = '';
    
    const levelMap = { "Beginner": 1, "Intermediate": 2, "Advanced": 3 };
    const userVal = levelMap[level];
    
    const results = [];
    state.projects.forEach(p => {
        if (p.is_unsupported) return;
        
        let score = 0;
        const pVal = levelMap[p.difficulty] || 1;
        const diff = Math.abs(userVal - pVal);
        
        if (diff === 0) score += 100;
        else if (diff === 1) score += 50;
        else score += 10;
        
        const common = p.tags ? p.tags.filter(t => state.selectedInterests.includes(t)) : [];
        score += common.length * 30;
        
        results.push({ project: p, score: score, common: common });
    });
    
    // Sort
    results.sort((a, b) => b.score - a.score);
    
    results.slice(0, 3).forEach(r => {
        const item = document.createElement('div');
        item.className = 'rec-item';
        item.innerHTML = `
            <div>
                <h4>${r.project.name}</h4>
                <p>Level: ${r.project.difficulty} | Common: ${r.common.join(', ') || 'None'}</p>
            </div>
            <div class="rec-score">${r.score} pts</div>
        `;
        recsList.appendChild(item);
    });
    
    document.getElementById('recs-quiz').classList.add('hidden');
    document.getElementById('recs-results').classList.remove('hidden');
}

function resetRecommendations() {
    document.getElementById('recs-quiz').classList.remove('hidden');
    document.getElementById('recs-results').classList.add('hidden');
}

// Side navigations
function setupEventListeners() {
    // Navigation items click handler
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            
            const target = item.dataset.target;
            showSection(target);
        });
    });
    
    // Theme toggle
    document.getElementById('theme-toggle-btn').addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', nextTheme);
        
        const icon = document.querySelector('#theme-toggle-btn i');
        const span = document.querySelector('#theme-toggle-btn span');
        if (nextTheme === 'light') {
            icon.className = 'fa-solid fa-sun';
            span.innerText = 'Light Mode';
        } else {
            icon.className = 'fa-solid fa-moon';
            span.innerText = 'Dark Mode';
        }
    });
    
    // Filter handles
    document.getElementById('filter-difficulty').addEventListener('change', () => renderProjectsDeck());
    document.getElementById('filter-status').addEventListener('change', () => renderProjectsDeck());
    
    // Search handles
    document.getElementById('global-search').addEventListener('input', (e) => {
        const query = e.target.value;
        // Auto navigate to projects deck if not already active to show results
        showSection('projects-section');
        document.querySelectorAll('.nav-item').forEach(i => {
            if (i.dataset.target === 'projects-section') i.classList.add('active');
            else i.classList.remove('active');
        });
        renderProjectsDeck(query);
    });
    
    // Quiz handles
    document.querySelectorAll('.difficulty-select .diff-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.difficulty-select .diff-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });
    
    document.getElementById('run-recs-btn').addEventListener('click', generateRecommendations);
    document.getElementById('reset-recs-btn').addEventListener('click', resetRecommendations);
    
    // Sandbox execution triggers
    document.getElementById('sandbox-run-btn').addEventListener('click', triggerSandboxRun);
    
    // Close modal
    document.querySelector('.close-modal').addEventListener('click', () => {
        document.getElementById('project-detail-modal').style.display = 'none';
    });
    window.addEventListener('click', (e) => {
        const modal = document.getElementById('project-detail-modal');
        if (e.target === modal) modal.style.display = 'none';
    });
}

function showSection(id) {
    document.querySelectorAll('.content-section').forEach(sec => {
        if (sec.id === id) sec.classList.add('active');
        else sec.classList.remove('active');
    });
    state.activeSection = id;
}
