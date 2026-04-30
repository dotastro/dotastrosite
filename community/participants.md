---
layout: default
title: "Community Directory"
description: "Everyone who has ever attended a .Astronomy conference."
---

<span class="section-label">// community</span>
# Community Directory

<p class="page-lead">Everyone who has ever attended a .Astronomy conference, drawn from the event archives. Affiliations shown are from the most recent event we have on record. Bluesky profiles sourced from the community.</p>

<div class="dir-stats" id="dir-stats">
  <div class="dir-stats-grid">
    <div class="dir-stat"><span class="dir-stat-num" id="stat-total">...</span><span class="dir-stat-label">unique participants</span></div>
    <div class="dir-stat"><span class="dir-stat-num" id="stat-multi">...</span><span class="dir-stat-label">returned for more</span></div>
    <div class="dir-stat"><span class="dir-stat-num" id="stat-events">14</span><span class="dir-stat-label">events since 2008</span></div>
    <div class="dir-stat"><span class="dir-stat-num" id="stat-bsky">...</span><span class="dir-stat-label">on Bluesky</span></div>
  </div>
</div>

<h2 style="margin-top:2.5rem">Attendance timeline</h2>
<p style="color:var(--text-muted); font-size:0.875rem; margin-bottom:1rem">People who attended two or more events. Gold = organiser, green = speaker, blue = attendee.</p>

<div class="attendance-section">
  <input type="search" class="dir-search" id="grid-search" placeholder="Filter by name..." autocomplete="off" style="margin-bottom:1rem">
  <div id="attendance-grid-wrap">
    <p style="color:var(--text-muted); font-family:var(--font-mono); font-size:0.8rem">Loading...</p>
  </div>
</div>

<h2 style="margin-top:3rem">Full directory</h2>

<div class="dir-search-wrap" style="margin: 1rem 0">
  <input type="search" class="dir-search" id="dir-search" placeholder="Search by name, affiliation, or event..." autocomplete="off" spellcheck="false">
</div>

<div id="dir-table-wrap">
  <p style="color:var(--text-muted); font-family:var(--font-mono); font-size:0.8rem">Loading...</p>
</div>

<script>
(function () {
  var BASE = document.querySelector('meta[name="site-baseurl"]').content;

  var EVENT_ORDER = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','alpha','twelve','thirteen'];
  var EVENT_LABELS = {
    one:'1', two:'2', three:'3', four:'4', five:'5', six:'6', seven:'7',
    eight:'8', nine:'9', ten:'X', eleven:'11', alpha:'α', twelve:'12', thirteen:'13'
  };
  var EVENT_YEARS = {
    one:2008, two:2009, three:2011, four:2012, five:2013, six:2014, seven:2015,
    eight:2016, nine:2017, ten:2018, eleven:2019, alpha:2020, twelve:2023, thirteen:2024
  };

  // Known Bluesky handles
  var BSKY = {
    'robert simpson': 'orbitingfrog.bsky.social',
    'rob simpson': 'orbitingfrog.bsky.social',
    'chris lintott': 'chrislintott.bsky.social',
    'sarah kendrew': 'sarahkendrew.bsky.social',
    'amanda bauer': 'amandabauer.bsky.social',
    'alasdair allan': 'alasdairallan.com',
    'becky smethurst': 'drbecky.bsky.social',
    'arfon smith': 'arfon.bsky.social',
    'phil plait': 'philplait.bsky.social',
    'emily lakdawalla': 'elakdawalla.bsky.social',
    'alyssa goodman': 'alyssagoodman.bsky.social',
    'jane rigby': 'janerigby.bsky.social',
    'jessie christiansen': 'aussiastronomer.bsky.social',
    'geert barentsen': 'geert.bsky.social',
    'emily hunt': 'emilyhunt.bsky.social',
  };

  fetch(BASE + '/assets/js/participants-data.json')
    .then(function(r) { return r.json(); })
    .then(function(data) { render(data); })
    .catch(function() { document.getElementById('dir-table-wrap').innerHTML = '<p style="color:var(--text-muted)">Could not load directory data.</p>'; });

  function latestAffiliation(person) {
    var affs = person.affiliations || {};
    for (var i = EVENT_ORDER.length - 1; i >= 0; i--) {
      var ev = EVENT_ORDER[i];
      if (affs[ev]) return affs[ev];
    }
    return person.affiliation || '';
  }

  function affiliationHistory(person) {
    var affs = person.affiliations || {};
    var seen = {};
    var history = [];
    EVENT_ORDER.forEach(function(ev) {
      if (affs[ev] && !seen[affs[ev]]) {
        seen[affs[ev]] = true;
        var label = EVENT_LABELS[ev];
        var year = EVENT_YEARS[ev];
        history.push(label + ' \u2019' + String(year).slice(2) + ': ' + affs[ev]);
      }
    });
    return history;
  }

  function renderGrid(people) {
    var multi = people.filter(function(p){ return p.events.length > 1; });
    // Sort by event count desc, then name
    multi.sort(function(a,b){ return b.events.length - a.events.length || a.name.localeCompare(b.name); });

    var html = '<div class="ag-scroll"><div class="attendance-grid">';

    // Header row
    html += '<div class="ag-row ag-header">';
    html += '<div class="ag-name">Name</div>';
    EVENT_ORDER.forEach(function(ev) {
      var label = EVENT_LABELS[ev];
      var year = EVENT_YEARS[ev];
      html += '<div class="ag-cell ag-header-cell" title=".Astronomy ' + label + ' (' + year + ')">' + label + '</div>';
    });
    html += '</div>';

    // Person rows
    multi.forEach(function(p) {
      html += '<div class="ag-row" data-agname="' + esc(p.name.toLowerCase()) + '">';
      html += '<div class="ag-name">' + esc(p.name) + '</div>';
      EVENT_ORDER.forEach(function(ev) {
        if (p.events.indexOf(ev) > -1) {
          var roles = p.roles[ev] || ['attendee'];
          var cls = 'ag-cell ag-filled ev-' + ev;
          if (roles.indexOf('organiser') > -1) cls += ' ag-org';
          else if (roles.indexOf('speaker') > -1) cls += ' ag-spk';
          var label = EVENT_LABELS[ev];
          var roleLabel = roles.indexOf('organiser') > -1 ? 'organiser' : roles.indexOf('speaker') > -1 ? 'speaker' : 'attendee';
          html += '<div class="' + cls + '" title="' + esc(p.name) + ' at .Astronomy ' + label + ' (' + roleLabel + ')"></div>';
        } else {
          html += '<div class="ag-cell ag-empty"></div>';
        }
      });
      html += '</div>';
    });

    html += '</div></div>';
    document.getElementById('attendance-grid-wrap').innerHTML = html;

    // Grid search
    document.getElementById('grid-search').addEventListener('input', function() {
      var q = this.value.toLowerCase().trim();
      document.querySelectorAll('.ag-row:not(.ag-header)').forEach(function(row) {
        row.style.display = !q || (row.getAttribute('data-agname') || '').includes(q) ? '' : 'none';
      });
    });
  }

  function render(data) {
    var people = data.people;

    // Grid
    renderGrid(people);

    // Stats
    document.getElementById('stat-total').textContent = people.length;
    document.getElementById('stat-multi').textContent = people.filter(function(p){ return p.events.length > 1; }).length;
    var bskyCount = people.filter(function(p){ return BSKY[p.name.toLowerCase()] || p.bluesky; }).length;
    document.getElementById('stat-bsky').textContent = bskyCount;

    // Build table
    var html = '<table class="participants-table" id="participants-table">';
    html += '<thead><tr>';
    html += '<th>Name</th>';
    html += '<th>Affiliation</th>';
    html += '<th>Events</th>';
    html += '<th>Bluesky</th>';
    html += '</tr></thead><tbody>';

    people.forEach(function(p) {
      var bsky = BSKY[p.name.toLowerCase()] || p.bluesky || '';
      var aff = latestAffiliation(p);
      var history = affiliationHistory(p);
      var nameKey = p.name.toLowerCase();

      // Event badges -- sort by EVENT_ORDER for consistent chronological display
      var sortedEvents = p.events.slice().sort(function(a, b) {
        return EVENT_ORDER.indexOf(a) - EVENT_ORDER.indexOf(b);
      });
      var badges = sortedEvents.map(function(ev) {
        var roles = p.roles[ev] || ['attendee'];
        var roleClass = roles.indexOf('organiser') > -1 ? ' eb-role-org' : roles.indexOf('speaker') > -1 ? ' eb-role-spk' : '';
        var label = EVENT_LABELS[ev] || ev;
        var year = EVENT_YEARS[ev] || '';
        return '<span class="event-badge-xs eb-' + ev + roleClass + '" title=".Astronomy ' + label + (year ? ', ' + year : '') + '">' + label + '</span>';
      }).join('');

      // Bluesky link
      var bskyHtml = bsky ? '<a href="https://bsky.app/profile/' + esc(bsky) + '" target="_blank" rel="noopener" class="bsky-link">' + esc(bsky) + '</a>' : '';

      var rowClass = p.events.length > 1 ? 'p-multi' : '';
      html += '<tr class="' + rowClass + '" data-name="' + esc(p.name.toLowerCase()) + '" data-aff="' + esc(aff.toLowerCase()) + '" data-events="' + esc(p.events.join(' ')) + '">';
      html += '<td class="p-name">' + esc(p.name) + '</td>';
      if (history.length > 1) {
        var tooltip = history.join('\n');
        html += '<td class="p-aff"><span class="p-aff-tip" title="' + esc(tooltip) + '">' + esc(aff) + '<span class="p-aff-hist-dot" aria-hidden="true"></span></span></td>';
      } else {
        html += '<td class="p-aff">' + esc(aff) + '</td>';
      }
      html += '<td class="p-events">' + badges + '</td>';
      html += '<td class="p-bsky">' + bskyHtml + '</td>';
      html += '</tr>';
    });

    html += '</tbody></table>';
    document.getElementById('dir-table-wrap').innerHTML = html;

    // Search
    document.getElementById('dir-search').addEventListener('input', function() {
      var q = this.value.toLowerCase().trim();
      var rows = document.querySelectorAll('#participants-table tbody tr');
      rows.forEach(function(row) {
        var name = row.getAttribute('data-name') || '';
        var aff = row.getAttribute('data-aff') || '';
        var evs = row.getAttribute('data-events') || '';
        var visible = !q || name.includes(q) || aff.includes(q) || evs.includes(q);
        row.style.display = visible ? '' : 'none';
      });
    });
  }

  function esc(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }
})();
</script>

<div class="dir-footer-actions">
<p>Role key: <span class="event-badge-xs eb-eight eb-role-org">8</span> organiser &nbsp; <span class="event-badge-xs eb-eight eb-role-spk">8</span> speaker &nbsp; <span class="event-badge-xs eb-eight">8</span> attendee</p>
<div class="dir-footer-links">
<a href="https://github.com/dotastro/dotastrosite/issues/new?template=add_participant.yml" target="_blank" rel="noopener" class="btn btn-outline btn-sm">Add someone missing</a>
<a href="https://github.com/dotastro/dotastrosite/issues/new?template=update_participant.yml" target="_blank" rel="noopener" class="btn btn-outline btn-sm">Correct my record</a>
</div>
<p style="font-family:var(--font-mono); font-size:0.68rem; color:var(--text-dim); margin-top:0.75rem">Directory rebuilt nightly from event pages. Changes submitted via GitHub are reviewed before being applied.</p>
</div>
