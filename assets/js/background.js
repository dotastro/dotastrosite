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
  // Add more images here. Example structure:
  // {
  //   id: 'pillars',
  //   file: 'jwst-pillars-of-creation.jpg',
  //   title: 'Pillars of Creation',
  //   credit: 'NASA, ESA, CSA, STScI; J. DePasquale, A. Koekemoer, A. Pagan (STScI)',
  //   creditUrl: 'https://science.nasa.gov/mission/webb/multimedia/images/',
  //   instrument: 'James Webb Space Telescope (NIRCam)',
  //   accent: '#c17b3a',        // warm amber from the pillars
  //   accentDim: 'rgba(193, 123, 58, 0.12)',
  //   accentBorder: 'rgba(193, 123, 58, 0.3)',
  //   accentGlow: 'rgba(193, 123, 58, 0.25)',
  // },
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
  const cornerEl = document.getElementById('bg-corner-credit');
  if (cornerEl) {
    cornerEl.querySelector('a').href = bg.creditUrl;
    cornerEl.querySelector('a').textContent = bg.title;
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const { bg, idx } = pickBackground();
  applyBackground(bg);

  // Rotate button (on about page)
  const rotateBtn = document.getElementById('bg-rotate-btn');
  if (rotateBtn) {
    rotateBtn.addEventListener('click', function () {
      const { bg: next } = nextBackground();
      applyBackground(next);

      // Crossfade the background
      document.body.classList.add('bg-transitioning');
      setTimeout(() => document.body.classList.remove('bg-transitioning'), 600);
    });

    // Show count if multiple images
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
