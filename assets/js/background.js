/* .Astronomy background image system
   - Session-consistent random selection (same image per visit, changes next visit)
   - Per-image accent colour theming
   - Glassmorphism on cards/nav
   - Image credit widget
*/

const BACKGROUNDS = [
  {
    id: 'cosmic-cliffs',
    file: 'jwst-cosmic-cliffs.jpg',
    title: 'Cosmic Cliffs, Carina Nebula',
    credit: 'NASA, ESA, CSA, and STScI',
    creditUrl: 'https://science.nasa.gov/mission/webb/multimedia/images/',
    instrument: 'James Webb Space Telescope (NIRCam)',
    // Accent: blue from the upper sky region
    accent: '#4a9eff',
    accentDim: 'rgba(74, 158, 255, 0.12)',
    accentBorder: 'rgba(74, 158, 255, 0.3)',
    accentGlow: 'rgba(74, 158, 255, 0.25)',
  },
  {
    id: 'artemis-earth',
    file: 'artemis-earth.jpg',
    title: 'Earth from Artemis I',
    credit: 'NASA',
    creditUrl: 'https://www.nasa.gov/image-detail/amf-art002e009289/',
    instrument: 'Artemis I mission, 2022',
    // Accent: warm amber from the sunlit Earth limb
    accent: '#f5a94a',
    accentDim: 'rgba(245, 169, 74, 0.12)',
    accentBorder: 'rgba(245, 169, 74, 0.3)',
    accentGlow: 'rgba(245, 169, 74, 0.25)',
  },
  {
    id: 'hubble-ngc1084',
    file: 'hubble-ngc1084.jpg',
    title: 'Starry Spiral: NGC 1084',
    credit: 'ESA/Hubble & NASA, D. Thilker and the PHANGS-HST Team',
    creditUrl: 'https://www.esa.int/ESA_Multimedia/Images',
    instrument: 'Hubble Space Telescope',
    // Accent: rose/pink from the star-forming regions
    accent: '#e87a9f',
    accentDim: 'rgba(232, 122, 159, 0.12)',
    accentBorder: 'rgba(232, 122, 159, 0.3)',
    accentGlow: 'rgba(232, 122, 159, 0.25)',
  },
];

function pickBackground() {
  // Session-consistent: pick once per session, store in sessionStorage
  let idx = sessionStorage.getItem('dotastro-bg-idx');
  if (idx === null) {
    idx = Math.floor(Math.random() * BACKGROUNDS.length);
    sessionStorage.setItem('dotastro-bg-idx', idx);
  }
  return { bg: BACKGROUNDS[parseInt(idx)], idx: parseInt(idx) };
}

function nextBackground() {
  let idx = parseInt(sessionStorage.getItem('dotastro-bg-idx') || '0');
  idx = (idx + 1) % BACKGROUNDS.length;
  sessionStorage.setItem('dotastro-bg-idx', idx);
  return { bg: BACKGROUNDS[idx], idx };
}

function applyBackground(bg) {
  const root = document.documentElement;
  const base = document.querySelector('meta[name="site-baseurl"]')?.content || '';

  // Background image
  document.body.style.setProperty('--bg-image', `url("${base}/assets/images/${bg.file}")`);

  // Accent colour overrides (only for non-default images)
  if (bg.accent !== '#4a9eff') {
    root.style.setProperty('--blue', bg.accent);
    root.style.setProperty('--blue-dim', bg.accentDim);
    root.style.setProperty('--blue-border', bg.accentBorder);
    root.style.setProperty('--blue-glow', bg.accentGlow);
  } else {
    root.style.removeProperty('--blue');
    root.style.removeProperty('--blue-dim');
    root.style.removeProperty('--blue-border');
    root.style.removeProperty('--blue-glow');
  }

  // Update credit widget
  const titleEl = document.getElementById('bg-credit-title');
  const creditEl = document.getElementById('bg-credit-text');
  const linkEl = document.getElementById('bg-credit-link');
  const instrEl = document.getElementById('bg-credit-instrument');

  if (titleEl) titleEl.textContent = bg.title;
  if (creditEl) creditEl.textContent = bg.credit;
  if (instrEl) instrEl.textContent = bg.instrument;
  if (linkEl) {
    linkEl.href = bg.creditUrl;
  }

  // Update corner credit
  const cornerLink = document.getElementById('bg-corner-link');
  if (cornerLink) {
    cornerLink.href = bg.creditUrl;
    cornerLink.textContent = bg.title;
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const { bg, idx } = pickBackground();
  applyBackground(bg);

  // Cycle function -- shared by corner button and about page button
  function cycleBackground() {
    const { bg: next } = nextBackground();
    applyBackground(next);
    document.body.classList.add('bg-transitioning');
    setTimeout(() => document.body.classList.remove('bg-transitioning'), 600);
    // Update count on about page if present
    const countEl = document.getElementById('bg-count');
    const newIdx = parseInt(sessionStorage.getItem('dotastro-bg-idx') || '0');
    if (countEl) countEl.textContent = `${newIdx + 1} of ${BACKGROUNDS.length}`;
  }

  // Corner cycle button
  const cornerCycleBtn = document.getElementById('bg-corner-cycle-btn');
  if (cornerCycleBtn) {
    cornerCycleBtn.addEventListener('click', function (e) {
      e.preventDefault();
      cycleBackground();
    });
  }

  // Rotate button on about page
  const rotateBtn = document.getElementById('bg-rotate-btn');
  if (rotateBtn) {
    rotateBtn.addEventListener('click', cycleBackground);
    // Show count
    const countEl = document.getElementById('bg-count');
    if (countEl) countEl.textContent = `${idx + 1} of ${BACKGROUNDS.length}`;
  }

  // Corner credit tooltip toggle
  const cornerCredit = document.getElementById('bg-corner-credit');
  if (cornerCredit) {
    cornerCredit.querySelector('a').textContent = bg.title;
    cornerCredit.querySelector('a').href = bg.creditUrl;
  }
});

/* =====================================================
   PENDING CONTRIBUTIONS COUNTER
   Fetches open issues labelled 'content' for this event
   and shows a count in the contribute section.
   ===================================================== */
(function () {
  var section = document.querySelector('.contribute-section[data-event]');
  if (!section) return;

  var eventName = section.getAttribute('data-event');
  if (!eventName) return;

  // GitHub API: search open issues with label:content mentioning this event
  var q = encodeURIComponent('repo:dotastro/dotastrosite is:issue is:open label:content ' + eventName);
  var url = 'https://api.github.com/search/issues?q=' + q + '&per_page=1';

  fetch(url, { headers: { 'Accept': 'application/vnd.github.v3+json' } })
    .then(function (r) { return r.json(); })
    .then(function (data) {
      var count = data.total_count;
      if (!count || count < 1) return;

      var label = section.querySelector('.section-label');
      if (!label) return;

      var pill = document.createElement('a');
      pill.href = 'https://github.com/dotastro/dotastrosite/issues?q=is%3Aissue+is%3Aopen+label%3Acontent+' + encodeURIComponent(eventName);
      pill.target = '_blank';
      pill.rel = 'noopener';
      pill.className = 'pending-pill';
      pill.textContent = count + ' pending ' + (count === 1 ? 'submission' : 'submissions');
      label.insertAdjacentElement('afterend', pill);
    })
    .catch(function () { /* fail silently */ });
})();
