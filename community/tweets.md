---
layout: default
title: "Social Archive"
description: "Recovered tweets, posts, and social media memories from #dotastro events"
permalink: /community/tweets/
---

<style>
.social-archive {
  max-width: 800px;
  margin: 0 auto;
}

.archive-intro {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  color: #e0e0e0;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  border-left: 4px solid #e94560;
}

.archive-intro h2 {
  color: #fff;
  margin-top: 0;
}

.archive-intro .lost-note {
  font-style: italic;
  color: #b0b0b0;
  font-size: 0.9em;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255,255,255,0.1);
}

.event-section {
  margin-bottom: 3rem;
}

.event-header {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  border-bottom: 2px solid #e94560;
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
}

.event-header h2 {
  margin: 0;
  color: #1a1a2e;
}

.event-header .year-badge {
  background: #e94560;
  color: white;
  padding: 0.2rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85em;
  font-weight: bold;
}

.event-header .post-count {
  color: #888;
  font-size: 0.85em;
}

.event-notes {
  color: #666;
  font-size: 0.9em;
  margin-bottom: 1rem;
  padding: 0.8rem;
  background: #f8f8f8;
  border-radius: 8px;
}

.highlights-section {
  margin-bottom: 1.5rem;
}

.highlights-section h3 {
  font-size: 1em;
  color: #555;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.highlight-item {
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
  font-size: 0.95em;
  color: #333;
}

.post-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 1rem 1.2rem;
  margin-bottom: 0.8rem;
  transition: box-shadow 0.2s;
}

.post-card:hover {
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.post-author {
  font-weight: 600;
  color: #1a1a2e;
}

.post-handle {
  color: #666;
  font-size: 0.85em;
}

.post-date {
  color: #999;
  font-size: 0.8em;
  white-space: nowrap;
}

.post-text {
  color: #333;
  line-height: 1.5;
  margin-bottom: 0.5rem;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-source {
  font-size: 0.75em;
  padding: 0.15rem 0.5rem;
  border-radius: 10px;
  display: inline-block;
}

.source-storify {
  background: #f0e4ff;
  color: #6b21a8;
}

.source-bluesky {
  background: #e0f0ff;
  color: #0066cc;
}

.source-wayback-liveblog {
  background: #fff3e0;
  color: #e65100;
}

.post-link {
  font-size: 0.8em;
  color: #0066cc;
  text-decoration: none;
}

.post-link:hover {
  text-decoration: underline;
}

.show-more-btn {
  display: block;
  width: 100%;
  padding: 0.8rem;
  background: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9em;
  color: #555;
  text-align: center;
  margin-top: 0.5rem;
}

.show-more-btn:hover {
  background: #e5e5e5;
}

.gap-events {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #fafafa;
  border-radius: 12px;
  border: 1px dashed #ccc;
}

.gap-events h3 {
  color: #888;
  margin-top: 0;
}

.gap-list {
  list-style: none;
  padding: 0;
}

.gap-list li {
  padding: 0.3rem 0;
  color: #999;
  font-size: 0.9em;
}

.gap-list li::before {
  content: "\25CB ";
  color: #ccc;
}

.stats-bar {
  display: flex;
  gap: 2rem;
  margin: 1.5rem 0;
  padding: 1rem;
  background: #f0f4f8;
  border-radius: 8px;
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 1.5em;
  font-weight: bold;
  color: #e94560;
  display: block;
}

.stat-label {
  font-size: 0.8em;
  color: #666;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #888;
}

@media (max-width: 600px) {
  .archive-intro { padding: 1.2rem; }
  .post-card { padding: 0.8rem; }
  .stats-bar { gap: 1rem; }
}
</style>

<div class="social-archive">

<div class="archive-intro">
  <h2>The Twitter Memory of .Astronomy</h2>
  <p>
    For over a decade, the #dotastro hashtag was the heartbeat of .Astronomy conferences. 
    Hundreds of astronomers tweeted their way through talks, hack days, and unconferences, 
    creating a real-time record of ideas, collaborations, and community.
  </p>
  <p>
    When Storify shut down in 2018 and Twitter locked its API, much of that record was lost. 
    This page is a preservation effort: what we could recover from the Wayback Machine, 
    Storify archives, and the community's migration to Bluesky.
  </p>
  <p class="lost-note">
    What you see here is a fraction of what once existed. Thousands of #dotastro tweets 
    from 2008 to 2018 are likely gone forever. But these fragments tell the story of a 
    community that believed in openness, collaboration, and having fun with science online.
  </p>
</div>

<div class="stats-bar" id="stats-bar">
  <div class="stat-item"><span class="stat-number" id="stat-posts">--</span><span class="stat-label">posts recovered</span></div>
  <div class="stat-item"><span class="stat-number" id="stat-events">--</span><span class="stat-label">events with data</span></div>
  <div class="stat-item"><span class="stat-number" id="stat-sources">--</span><span class="stat-label">sources searched</span></div>
  <div class="stat-item"><span class="stat-number" id="stat-authors">--</span><span class="stat-label">unique voices</span></div>
</div>

<div id="timeline" class="loading">Loading social archive...</div>

</div>

<script>
(function() {
  var baseurlMeta = document.querySelector('meta[name="site-baseurl"]');
  var BASEURL = baseurlMeta ? baseurlMeta.content : '';
  var BASE = BASEURL + '/assets/social/';
  var EVENT_ORDER = [
    {name: 'one', label: '.Astronomy 1', year: 2008},
    {name: 'two', label: '.Astronomy 2', year: 2009},
    {name: 'three', label: '.Astronomy 3', year: 2011},
    {name: 'four', label: '.Astronomy 4', year: 2012},
    {name: 'five', label: '.Astronomy 5', year: 2013},
    {name: 'six', label: '.Astronomy 6', year: 2014},
    {name: 'seven', label: '.Astronomy 7', year: 2015},
    {name: 'eight', label: '.Astronomy 8', year: 2016},
    {name: 'nine', label: '.Astronomy 9', year: 2017},
    {name: 'ten', label: '.Astronomy X', year: 2018},
    {name: 'twelve', label: '.Astronomy 12', year: 2023},
    {name: 'thirteen', label: '.Astronomy 13', year: 2024},
    {name: 'general', label: 'Community Posts', year: 0}
  ];

  var GAPS = {
    one: 'No social media archive found. Pre-widespread Twitter archiving.',
    two: 'No social media archive found.',
    four: 'No social media archive found. Storify pages were not captured by the Wayback Machine.',
    six: 'No social media archive found. Storify pages were not captured.',
    seven: 'No social media archive found.',
    eight: 'No social media archive found.',
    nine: 'No social media archive found.',
    ten: 'No social media archive found.'
  };

  function escapeHtml(text) {
    var div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  function sourceClass(source) {
    if (source === 'storify') return 'source-storify';
    if (source === 'bluesky') return 'source-bluesky';
    return 'source-wayback-liveblog';
  }

  function sourceLabel(source) {
    if (source === 'storify') return 'Storify (Wayback)';
    if (source === 'bluesky') return 'Bluesky';
    if (source === 'wayback-liveblog') return 'Liveblog (Wayback)';
    return source;
  }

  function renderPost(post) {
    var linkHtml = post.url ? '<a href="' + escapeHtml(post.url) + '" class="post-link" target="_blank" rel="noopener">View original</a>' : '';
    return '<div class="post-card">' +
      '<div class="post-header">' +
        '<div><span class="post-author">' + escapeHtml(post.author_name || 'Unknown') + '</span> ' +
        '<span class="post-handle">' + escapeHtml(post.author) + '</span></div>' +
        '<span class="post-date">' + escapeHtml(post.date) + '</span>' +
      '</div>' +
      '<div class="post-text">' + escapeHtml(post.text) + '</div>' +
      '<div class="post-footer">' +
        '<span class="post-source ' + sourceClass(post.source) + '">' + sourceLabel(post.source) + '</span>' +
        linkHtml +
      '</div>' +
    '</div>';
  }

  function renderEvent(eventInfo, data) {
    var html = '<div class="event-section">';
    html += '<div class="event-header">';
    html += '<h2>' + escapeHtml(eventInfo.label) + '</h2>';
    if (eventInfo.year > 0) {
      html += '<span class="year-badge">' + eventInfo.year + '</span>';
    }
    html += '<span class="post-count">' + data.posts.length + ' posts</span>';
    html += '</div>';

    if (data.notes) {
      html += '<div class="event-notes">' + escapeHtml(data.notes) + '</div>';
    }

    if (data.highlights && data.highlights.length > 0) {
      html += '<div class="highlights-section"><h3>Highlights</h3>';
      data.highlights.forEach(function(h) {
        html += '<div class="highlight-item">' + escapeHtml(h) + '</div>';
      });
      html += '</div>';
    }

    var INITIAL_SHOW = 5;
    var posts = data.posts || [];
    var showing = Math.min(posts.length, INITIAL_SHOW);
    
    for (var i = 0; i < showing; i++) {
      html += renderPost(posts[i]);
    }

    if (posts.length > INITIAL_SHOW) {
      var hiddenId = 'hidden-' + eventInfo.name;
      var btnId = 'btn-' + eventInfo.name;
      html += '<div id="' + hiddenId + '" style="display:none">';
      for (var j = INITIAL_SHOW; j < posts.length; j++) {
        html += renderPost(posts[j]);
      }
      html += '</div>';
      html += '<button class="show-more-btn" id="' + btnId + '" onclick="document.getElementById(\'' + hiddenId + '\').style.display=\'block\';this.style.display=\'none\';">Show ' + (posts.length - INITIAL_SHOW) + ' more posts</button>';
    }

    html += '</div>';
    return html;
  }

  function renderGaps(gapEvents) {
    if (gapEvents.length === 0) return '';
    var html = '<div class="gap-events">';
    html += '<h3>Events Without Social Data</h3>';
    html += '<p style="font-size:0.9em;color:#888;margin-top:0">These events happened, but their social media trail could not be recovered.</p>';
    html += '<ul class="gap-list">';
    gapEvents.forEach(function(evt) {
      html += '<li><strong>' + escapeHtml(evt.label) + '</strong> (' + evt.year + '): ' + escapeHtml(GAPS[evt.name] || 'No data recovered') + '</li>';
    });
    html += '</ul></div>';
    return html;
  }

  // Fetch index and render
  fetch(BASE + 'index.json')
    .then(function(r) { return r.json(); })
    .then(function(index) {
      var eventNames = (index.events || []).map(function(e) { return e.event; });
      
      // Fetch all event JSONs
      var fetches = eventNames.map(function(name) {
        return fetch(BASE + name + '.json').then(function(r) { return r.json(); });
      });

      return Promise.all(fetches).then(function(eventDataList) {
        var eventMap = {};
        eventDataList.forEach(function(d) { eventMap[d.event] = d; });

        var container = document.getElementById('timeline');
        var html = '';
        var gapEvents = [];
        var totalPosts = 0;
        var allAuthors = {};
        var eventCount = 0;

        EVENT_ORDER.forEach(function(info) {
          if (eventMap[info.name]) {
            html += renderEvent(info, eventMap[info.name]);
            totalPosts += (eventMap[info.name].posts || []).length;
            eventCount++;
            (eventMap[info.name].posts || []).forEach(function(p) {
              allAuthors[p.author] = true;
            });
          } else if (GAPS[info.name]) {
            gapEvents.push(info);
          }
        });

        // Insert gaps section before general posts
        var generalIdx = html.lastIndexOf('<div class="event-section">');
        if (gapEvents.length > 0 && generalIdx > -1) {
          html = html.substring(0, generalIdx) + renderGaps(gapEvents) + html.substring(generalIdx);
        } else if (gapEvents.length > 0) {
          html += renderGaps(gapEvents);
        }

        container.innerHTML = html;

        // Update stats
        document.getElementById('stat-posts').textContent = totalPosts;
        document.getElementById('stat-events').textContent = eventCount;
        document.getElementById('stat-sources').textContent = Object.keys(index.sources_searched || {}).length;
        document.getElementById('stat-authors').textContent = Object.keys(allAuthors).length;
      });
    })
    .catch(function(err) {
      document.getElementById('timeline').innerHTML = '<p>Could not load social archive data. Error: ' + err.message + '</p>';
    });
})();
</script>
