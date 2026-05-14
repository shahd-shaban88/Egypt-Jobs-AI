const JOBS_DATA_URL = './data/jobs.json';

let allJobs = [];
let activeFilter = 'All';
let searchQuery = '';

async function fetchJobs() {
    try {
        const response = await fetch(JOBS_DATA_URL);
        if (!response.ok) throw new Error('Failed to fetch jobs');
        allJobs = await response.json();
        renderJobs();
    } catch (error) {
        document.getElementById('jobsList').innerHTML = `
            <div class="no-results">
                <i class="fa-solid fa-triangle-exclamation" style="font-size:2rem; margin-bottom:10px;"></i>
                <p>Could not load jobs. Please try again later.</p>
            </div>`;
        document.getElementById('jobCount').textContent = 'Error loading opportunities.';
    }
}

function getFilteredJobs() {
    return allJobs.filter(job => {
        const matchesFilter =
            activeFilter === 'All' ||
            job.type === activeFilter ||
            (activeFilter === 'Remote' && job.location.toLowerCase().includes('remote'));

        const searchLower = searchQuery.toLowerCase();
        const matchesSearch =
            !searchQuery ||
            job.title.toLowerCase().includes(searchLower) ||
            job.company.toLowerCase().includes(searchLower) ||
            job.category.toLowerCase().includes(searchLower) ||
            job.description.toLowerCase().includes(searchLower);

        return matchesFilter && matchesSearch;
    });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return '1 day ago';
    return `${diffDays} days ago`;
}

function renderJobs() {
    const filtered = getFilteredJobs();
    const jobsList = document.getElementById('jobsList');
    const jobCount = document.getElementById('jobCount');

    jobCount.textContent = `${filtered.length} opportunit${filtered.length !== 1 ? 'ies' : 'y'} found`;

    if (filtered.length === 0) {
        jobsList.innerHTML = `
            <div class="no-results">
                <i class="fa-solid fa-magnifying-glass" style="font-size:2rem; margin-bottom:10px;"></i>
                <p>No opportunities found matching your search.</p>
            </div>`;
        return;
    }

    jobsList.innerHTML = filtered.map(job => `
        <div class="job-card" id="job-${job.id}">
            <span class="job-type-badge ${job.type === 'Internship' ? 'internship' : ''}">
                ${job.type}
            </span>
            <h3 class="job-title">${job.title}</h3>
            <p class="job-company">
                <i class="fa-solid fa-building"></i>
                ${job.company}
            </p>
            <div class="job-details">
                <div class="detail-item">
                    <i class="fa-solid fa-location-dot"></i>
                    <span>${job.location}</span>
                </div>
                <div class="detail-item">
                    <i class="fa-solid fa-tag"></i>
                    <span>${job.category}</span>
                </div>
                <div class="detail-item">
                    <i class="fa-regular fa-clock"></i>
                    <span>${formatDate(job.date_posted)}</span>
                </div>
            </div>
            <p class="job-description">${job.description}</p>
            <a href="${job.link}" target="_blank" rel="noopener noreferrer" class="apply-btn">
                Apply Now &rarr;
            </a>
        </div>
    `).join('');
}

// Event: Search input
document.getElementById('searchInput').addEventListener('input', (e) => {
    searchQuery = e.target.value.trim();
    renderJobs();
});

// Event: Filter buttons
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeFilter = btn.dataset.filter;
        renderJobs();
    });
});

// Init
fetchJobs();
