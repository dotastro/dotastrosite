/* .Astronomy site search
   Builds an index from the page DOM, searches across all loaded pages via
   a pre-built JSON index, then navigates to the result page with a highlight.
*/

(function () {
  var overlay, input, results;

  function init() {
    overlay = document.getElementById('search-overlay');
    input = document.getElementById('search-input');
    results = document.getElementById('search-results');
    if (!overlay) return;

    // Open on button click
    document.querySelectorAll('[data-search-open]').forEach(function (el) {
      el.addEventListener('click', openSearch);
    });

    // Close
    document.getElementById('search-close').addEventListener('click', closeSearch);
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeSearch();
    });

    // Keyboard shortcut: / or Cmd+K
    document.addEventListener('keydown', function (e) {
      if ((e.key === '/' || (e.key === 'k' && (e.metaKey || e.ctrlKey))) && !isTyping()) {
        e.preventDefault();
        openSearch();
      }
      if (e.key === 'Escape') closeSearch();
    });

    // Search on input
    input.addEventListener('input', debounce(runSearch, 150));
  }

  function isTyping() {
    var tag = document.activeElement && document.activeElement.tagName;
    return tag === 'INPUT' || tag === 'TEXTAREA';
  }

  function openSearch() {
    overlay.classList.add('is-open');
    input.focus();
    input.select();
  }

  function closeSearch() {
    overlay.classList.remove('is-open');
    input.blur();
  }

  function debounce(fn, ms) {
    var t;
    return function () {
      clearTimeout(t);
      t = setTimeout(fn, ms);
    };
  }

  // Search index -- loaded from search-index.json
  var INDEX = null;

  function loadIndex() {
    if (INDEX !== null) return Promise.resolve(INDEX);
    var base = document.querySelector('meta[name="site-baseurl"]');
    var baseurl = base ? base.content : '';
    return fetch(baseurl + '/assets/js/search-index.json')
      .then(function (r) { return r.json(); })
      .then(function (data) { INDEX = data; return data; })
      .catch(function () { INDEX = []; return []; });
  }

  function runSearch() {
    var q = input.value.trim().toLowerCase();
    if (q.length < 2) {
      results.innerHTML = '<div class="search-empty">Type to search talks, hacks, people, events...</div>';
      return;
    }

    loadIndex().then(function (idx) {
      var hits = [];
      var words = q.split(/\s+/).filter(Boolean);

      idx.forEach(function (doc) {
        var text = (doc.title + ' ' + doc.body).toLowerCase();
        var score = 0;
        words.forEach(function (w) {
          var titleCount = (doc.title.toLowerCase().match(new RegExp(w, 'g')) || []).length;
          var bodyCount = (doc.body.toLowerCase().match(new RegExp(w, 'g')) || []).length;
          score += titleCount * 3 + bodyCount;
        });
        if (score > 0) hits.push({ doc: doc, score: score });
      });

      hits.sort(function (a, b) { return b.score - a.score; });
      hits = hits.slice(0, 12);

      if (hits.length === 0) {
        results.innerHTML = '<div class="search-empty">No results for "' + escHtml(q) + '"</div>';
        return;
      }

      results.innerHTML = hits.map(function (hit) {
        var doc = hit.doc;
        var excerpt = snippet(doc.body, words, 120);
        return '<a class="search-result-item" href="' + escHtml(doc.url) + '">' +
          '<div class="search-result-title">' + highlight(escHtml(doc.title), words) + '</div>' +
          '<div class="search-result-context">' + escHtml(doc.section) + '</div>' +
          (excerpt ? '<div class="search-result-excerpt" style="font-size:0.8rem;color:var(--text-muted);margin-top:0.2rem">' + highlight(escHtml(excerpt), words) + '</div>' : '') +
          '</a>';
      }).join('');
    });
  }

  function snippet(text, words, maxLen) {
    var lower = text.toLowerCase();
    var best = -1;
    words.forEach(function (w) {
      var idx = lower.indexOf(w);
      if (idx > -1 && (best === -1 || idx < best)) best = idx;
    });
    if (best === -1) return text.slice(0, maxLen);
    var start = Math.max(0, best - 40);
    var end = Math.min(text.length, start + maxLen);
    return (start > 0 ? '...' : '') + text.slice(start, end) + (end < text.length ? '...' : '');
  }

  function highlight(text, words) {
    words.forEach(function (w) {
      var re = new RegExp('(' + escRe(w) + ')', 'gi');
      text = text.replace(re, '<mark>$1</mark>');
    });
    return text;
  }

  function escHtml(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function escRe(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  document.addEventListener('DOMContentLoaded', init);
})();
