---
layout: default
title: Hacks
description: Every hack ever built at a .Astronomy conference, in one place.
permalink: /hacks/
---

<span class="section-label">// hacks</span>
<h1>All Hacks</h1>

<p class="page-lead">Every hack built at a .Astronomy conference since the first hack day in Leiden in 2009. <span id="hacks-total-count">...</span> projects and counting: websites, apps, tools, songs, bots, games, and more. This list is incomplete. If you built something at a .Astronomy hack day that isn't here, please add it.</p>

<a href="https://github.com/dotastro/dotastrosite/issues/new?template=add_hack.yml&title=hack%3A+%5Bevent%5D+%5Btitle%5D" target="_blank" rel="noopener" class="btn btn-outline btn-sm" style="margin-bottom:1.5rem">Add a hack via GitHub</a>

<div class="hacks-controls">
  <input type="search" id="hacks-search" class="dir-search" placeholder="Search by title, creator, or event..." autocomplete="off" spellcheck="false" style="max-width:400px">
  <div class="hacks-filters" id="hacks-filters"></div>
</div>

<div class="hacks-stats" id="hacks-stats" style="font-family:var(--font-mono); font-size:0.75rem; color:var(--text-muted); margin: 0.75rem 0 1.5rem"></div>

<div id="hacks-grid-wrap">
  <p style="color:var(--text-muted); font-family:var(--font-mono); font-size:0.8rem">Loading...</p>
</div>

<script>
(function() {
  var BASE = document.querySelector('meta[name="site-baseurl"]').content;

  var EVENT_LABELS = {
    one:'1', two:'2', three:'3', four:'4', five:'5', six:'6', seven:'7',
    eight:'8', nine:'9', ten:'X', eleven:'11', alpha:'α', twelve:'12', thirteen:'13'
  };
  var EVENT_YEARS = {
    one:2008, two:2009, three:2011, four:2012, five:2013, six:2014, seven:2015,
    eight:2016, nine:2017, ten:2018, eleven:2019, alpha:2020, twelve:2023, thirteen:2024
  };
  var EVENT_CITIES = {
    one:'Cardiff', two:'Leiden', three:'Oxford', four:'Heidelberg', five:'Cambridge MA',
    six:'Chicago', seven:'Sydney', eight:'Oxford', nine:'Cape Town', ten:'Baltimore',
    eleven:'Toronto', alpha:'Online', twelve:'New York', thirteen:'Madrid'
  };

  var allHacks = [];
  var activeFilter = null;

  fetch(BASE + '/api/v1/hacks.json')
    .then(function(r) { return r.json(); })
    .then(function(data) {
      allHacks = data.hacks;
      buildFilters();
      render(allHacks);
      document.getElementById('hacks-search').addEventListener('input', function() {
        filterAndRender();
      });
    })
    .catch(function() {
      document.getElementById('hacks-grid-wrap').innerHTML = '<p style="color:var(--text-muted)">Could not load hacks data.</p>';
    });

  function buildFilters() {
    var events = {};
    allHacks.forEach(function(h) {
      if (!events[h.event]) events[h.event] = 0;
      events[h.event]++;
    });

    var wrap = document.getElementById('hacks-filters');
    wrap.innerHTML = '<button class="hf-btn hf-active" data-event="">All</button>';

    // Sort by year
    Object.keys(events).sort(function(a,b) {
      return (EVENT_YEARS[a]||0) - (EVENT_YEARS[b]||0);
    }).forEach(function(ev) {
      var label = EVENT_LABELS[ev] || ev;
      var btn = document.createElement('button');
      btn.className = 'hf-btn event-badge-xs eb-' + ev;
      btn.setAttribute('data-event', ev);
      btn.textContent = label + ' (' + events[ev] + ')';
      btn.addEventListener('click', function() {
        activeFilter = activeFilter === ev ? null : ev;
        document.querySelectorAll('.hf-btn').forEach(function(b) {
          b.classList.toggle('hf-active', b.getAttribute('data-event') === (activeFilter || ''));
        });
        filterAndRender();
      });
      wrap.appendChild(btn);
    });

    document.querySelector('.hf-btn[data-event=""]').addEventListener('click', function() {
      activeFilter = null;
      document.querySelectorAll('.hf-btn').forEach(function(b) {
        b.classList.toggle('hf-active', b.getAttribute('data-event') === '');
      });
      filterAndRender();
    });
  }

  function filterAndRender() {
    var q = document.getElementById('hacks-search').value.toLowerCase().trim();
    var filtered = allHacks.filter(function(h) {
      if (activeFilter && h.event !== activeFilter) return false;
      if (!q) return true;
      var text = [h.title, (h.creators||[]).join(' '), h.description||'', h.event].join(' ').toLowerCase();
      return text.includes(q);
    });
    render(filtered);
  }

  function render(hacks) {
    document.getElementById('hacks-stats').textContent = hacks.length + ' of ' + allHacks.length + ' hacks';
    var totalEl = document.getElementById('hacks-total-count');
    if (totalEl) totalEl.textContent = allHacks.length;

    if (!hacks.length) {
      document.getElementById('hacks-grid-wrap').innerHTML = '<p style="color:var(--text-muted); font-family:var(--font-mono); font-size:0.85rem; margin-top:1rem">No hacks match.</p>';
      return;
    }

    var html = '<div class="hacks-grid">';
    hacks.forEach(function(h) {
      var label = EVENT_LABELS[h.event] || h.event;
      var year = EVENT_YEARS[h.event] || '';
      var city = EVENT_CITIES[h.event] || '';
      var creators = (h.creators||[]).join(', ');
      var links = '';
      if (h.source_url) links += '<a href="' + esc(h.source_url) + '" class="hack-link" target="_blank" rel="noopener">Source</a>';
      if (h.live_url) links += '<a href="' + esc(h.live_url) + '" class="hack-link" target="_blank" rel="noopener">Live</a>';

      // Primary link: source > live > event page
      var primaryUrl = h.source_url || h.live_url || (BASE + '/events/' + h.event + '/#hacks');
      var primaryLabel = h.source_url ? 'View source' : h.live_url ? 'View live' : null;

      html += '<div class="hack-card">';
      html += '<a href="' + BASE + '/events/' + esc(h.event) + '/#hacks" class="hack-event-badge event-badge-xs eb-' + esc(h.event) + '" title=".Astronomy ' + label + ', ' + city + ' ' + year + '">' + label + '</a>';
      // Title links to source/live if available
      if (h.source_url || h.live_url) {
        html += '<div class="hack-title"><a href="' + esc(primaryUrl) + '" target="_blank" rel="noopener">' + esc(h.title) + '</a></div>';
      } else {
        html += '<div class="hack-title">' + esc(h.title) + '</div>';
      }
      if (creators) html += '<div class="hack-creators">' + esc(creators) + '</div>';
      if (h.description) html += '<p class="hack-desc">' + esc(h.description) + '</p>';
      // Show secondary links (both if different)
      var extraLinks = '';
      if (h.source_url) extraLinks += '<a href="' + esc(h.source_url) + '" class="hack-link" target="_blank" rel="noopener">Source</a>';
      if (h.live_url && h.live_url !== h.source_url) extraLinks += '<a href="' + esc(h.live_url) + '" class="hack-link" target="_blank" rel="noopener">Live</a>';
      if (extraLinks) html += '<div class="hack-links">' + extraLinks + '</div>';
      html += '</div>';
    });
    html += '</div>';
    document.getElementById('hacks-grid-wrap').innerHTML = html;
  }

  function esc(s) {
    return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }
})();
</script>
