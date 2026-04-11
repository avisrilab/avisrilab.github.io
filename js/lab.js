/* ============================================================
   Srivastava Lab — site JS
   No build step, no dependencies.
   ============================================================ */

/* ── Theme toggle ────────────────────────────────────────────── */
(function () {
  const html    = document.documentElement;
  const stored  = localStorage.getItem('lab-theme');

  // Apply stored preference immediately (before paint) to avoid flash
  if (stored) html.setAttribute('data-theme', stored);

  window.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('themeToggle');
    if (!btn) return;

    const sunIcon  = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`;
    const moonIcon = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;

    const updateIcon = () => {
      btn.innerHTML = html.getAttribute('data-theme') === 'dark' ? sunIcon : moonIcon;
    };
    updateIcon();

    btn.addEventListener('click', () => {
      const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('lab-theme', next);
      updateIcon();
    });
  });
})();

/* ── Mobile nav ──────────────────────────────────────────────── */
window.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('navToggle');
  const links  = document.getElementById('navLinks');
  if (!toggle || !links) return;

  toggle.addEventListener('click', () => {
    const open = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
  });

  // Close when a nav link is clicked
  links.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => links.classList.remove('open'));
  });

  // Close when clicking outside
  document.addEventListener('click', (e) => {
    if (!toggle.contains(e.target) && !links.contains(e.target)) {
      links.classList.remove('open');
    }
  });
});

/* ── Active nav link ─────────────────────────────────────────── */
window.addEventListener('DOMContentLoaded', () => {
  const page = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav__links a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === page || (page === '' && href === 'index.html')) {
      a.classList.add('active');
    }
  });
});

/* ── Helpers ─────────────────────────────────────────────────── */
function journalClass(journal) {
  const j = (journal || '').toLowerCase();
  if (j.includes('nature')) return 'journal-badge--nature';
  if (j.includes('cell') && !j.includes('computational')) return 'journal-badge--cell';
  if (j.includes('genome')) return 'journal-badge--genome';
  if (j.includes('plos')) return 'journal-badge--plos';
  if (j.includes('biorxiv') || j.includes('preprint') || j.includes('arxiv') || j.includes('recomb')) return 'journal-badge--preprint';
  return '';
}

function shortAuthorList(authors) {
  // Bold "Avi Srivastava", truncate very long lists
  const MAX = 8;
  const bold = (name) => name === 'Avi Srivastava'
    ? `<strong>${name}</strong>`
    : name;
  if (authors.length <= MAX) return authors.map(bold).join(', ');
  const displayed = authors.slice(0, MAX).map(bold).join(', ');
  return `${displayed}, <span class="text-muted">et al.</span>`;
}

/* ── Render news (index.html) ────────────────────────────────── */
async function renderNews(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = '<li class="loading">Loading…</li>';
  try {
    const res  = await fetch('data/news.json');
    const news = await res.json();
    container.innerHTML = '';
    news.forEach(item => {
      const li = document.createElement('li');
      li.className = 'news-item';
      li.innerHTML = `
        <span class="news-item__date">${item.date}</span>
        <p class="news-item__text">${item.text}</p>
      `;
      container.appendChild(li);
    });
  } catch (e) {
    container.innerHTML = '<li class="loading">Unable to load news.</li>';
  }
}

/* ── Render publications ─────────────────────────────────────── */
async function renderPublications(containerId, selectedOnly = false) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = '<p class="loading">Loading publications…</p>';
  try {
    const res    = await fetch('data/papers.json');
    let papers   = await res.json();
    if (selectedOnly) papers = papers.filter(p => p.selected);

    // Group by year descending
    const byYear = {};
    papers.forEach(p => {
      (byYear[p.year] = byYear[p.year] || []).push(p);
    });
    const years = Object.keys(byYear).map(Number).sort((a, b) => b - a);

    container.innerHTML = '';
    years.forEach(year => {
      const yearEl = document.createElement('div');
      yearEl.innerHTML = `<span class="pub-year-header">${year}</span>`;
      container.appendChild(yearEl);

      const ul = document.createElement('ul');
      ul.className = 'pub-list';

      byYear[year].forEach(pub => {
        const li = document.createElement('li');
        li.className = 'pub-item';

        const thumb = pub.preview
          ? `<img class="pub-item__thumb" src="${pub.preview}" alt="${pub.title}" loading="lazy">`
          : `<div class="pub-item__thumb--placeholder">📄</div>`;

        const badge    = `<span class="journal-badge ${journalClass(pub.journal)}">${pub.journal}</span>`;
        const doiLink  = pub.doi
          ? `<a class="doi-link" href="https://doi.org/${pub.doi}" target="_blank" rel="noopener">↗ DOI</a>`
          : '';
        const titleLink = pub.doi
          ? `<a href="https://doi.org/${pub.doi}" target="_blank" rel="noopener">${pub.title}</a>`
          : pub.title;

        li.innerHTML = `
          ${thumb}
          <div class="pub-item__body">
            <div class="pub-item__title">${titleLink}</div>
            <div class="pub-item__authors">${shortAuthorList(pub.authors)}</div>
            <div class="pub-item__meta">${badge} ${doiLink}</div>
          </div>
        `;
        ul.appendChild(li);
      });

      container.appendChild(ul);
    });
  } catch (e) {
    container.innerHTML = '<p class="loading">Unable to load publications.</p>';
  }
}

/* ── Render people ───────────────────────────────────────────── */
async function renderPeople() {
  try {
    const res    = await fetch('data/people.json');
    const people = await res.json();

    // PI card
    const pi = people.find(p => p.role === 'Principal Investigator');
    const piEl = document.getElementById('piSection');
    if (pi && piEl) {
      const links = [];
      if (pi.email)    links.push(`<a class="pi-link" href="mailto:${pi.email}">✉ Email</a>`);
      if (pi.github)   links.push(`<a class="pi-link" href="https://github.com/${pi.github}" target="_blank" rel="noopener">⌥ GitHub</a>`);
      if (pi.twitter)  links.push(`<a class="pi-link" href="https://twitter.com/${pi.twitter}" target="_blank" rel="noopener">𝕏 Twitter</a>`);
      if (pi.scholar)  links.push(`<a class="pi-link" href="https://scholar.google.com/citations?user=${pi.scholar}" target="_blank" rel="noopener">◉ Scholar</a>`);
      if (pi.orcid)    links.push(`<a class="pi-link" href="https://orcid.org/${pi.orcid}" target="_blank" rel="noopener">⊙ ORCID</a>`);
      if (pi.linkedin) links.push(`<a class="pi-link" href="https://linkedin.com/in/${pi.linkedin}" target="_blank" rel="noopener">in LinkedIn</a>`);

      piEl.innerHTML = `
        <div class="pi-card">
          ${pi.photo ? `<img class="pi-card__photo" src="${pi.photo}" alt="${pi.name}">` : ''}
          <div>
            <h2 class="pi-card__name">${pi.name}</h2>
            <p class="pi-card__title">${pi.title} · ${pi.institution}</p>
            <p class="pi-card__bio">${pi.bio}</p>
            <div class="pi-card__links">${links.join('')}</div>
          </div>
        </div>
      `;
    }

    // Other members grouped by role
    const roleOrder = [
      'Postdoctoral Researchers',
      'Graduate Students',
      'Research Assistants',
      'Undergraduate Researchers',
      'Visiting Scientists',
    ];
    const current = people.filter(p => p.status === 'current' && p.role !== 'Principal Investigator');
    const alumni  = people.filter(p => p.status === 'alumni');

    const memberEl = document.getElementById('memberSection');
    if (!memberEl) return;

    roleOrder.forEach(role => {
      const members = current.filter(p => p.role === role);
      if (!members.length) return;
      memberEl.appendChild(makePeopleSection(role, members));
    });

    if (alumni.length) {
      memberEl.appendChild(makePeopleSection('Alumni', alumni));
    }

    // If no non-PI members exist, show a placeholder
    if (!current.length && !alumni.length) {
      memberEl.innerHTML = `<p class="text-muted" style="margin-top:1rem">Lab members coming soon.</p>`;
    }
  } catch (e) {
    console.error('Could not load people:', e);
  }
}

function makePeopleSection(role, members) {
  const section = document.createElement('div');
  section.innerHTML = `
    <div class="role-header">
      <span class="role-header__title">${role}</span>
      <span class="role-header__line"></span>
    </div>
    <div class="people-grid">${members.map(memberCard).join('')}</div>
  `;
  return section;
}

function memberCard(person) {
  const photo = person.photo
    ? `<img class="person-card__photo" src="${person.photo}" alt="${person.name}" loading="lazy">`
    : `<div class="person-card__initials">${initials(person.name)}</div>`;

  const tagline = person.tagline || person.role || '';
  return `
    <div class="person-card">
      ${photo}
      <span class="person-card__name">${person.name}</span>
      ${tagline ? `<span class="person-card__role">${tagline}</span>` : ''}
    </div>
  `;
}

function initials(name) {
  return name.split(' ').map(w => w[0]).slice(0, 2).join('').toUpperCase();
}

/* ── Auto-init on page load ──────────────────────────────────── */
window.addEventListener('DOMContentLoaded', () => {
  renderNews('newsList');
  renderPublications('pubContainer');
  renderPublications('featuredPubs', true);
  renderPeople();
});
