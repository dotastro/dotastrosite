---
layout: default
title: API
description: The .Astronomy Archive API -- machine-readable access to all event data.
permalink: /api/
---

<div class="event-page-hero" data-num="{}">
  <div class="event-page-kicker">Developer Tools</div>
  <h1 class="event-page-title">.Astronomy Archive API</h1>
  <div class="event-page-meta">
    <span>v1.0</span>
    <span>Read-only JSON. Free. No auth required.</span>
  </div>
  <p class="event-page-desc">Machine-readable access to every .Astronomy event, talk, and hack since 2008. Built for developers, researchers, bots, and LLMs. Served as static JSON from GitHub Pages -- open CORS, no rate limits, CC BY 4.0.</p>
</div>

<nav class="event-page-nav" aria-label="Jump to section">
  <a href="#base">Base URL</a>
  <a href="#endpoints">Endpoints</a>
  <a href="#try">Try it</a>
  <a href="#llms">For LLMs</a>
  <a href="#licence">Licence</a>
</nav>

<span class="section-label">// base url</span>
<h2 id="base">Base URL</h2>

<div class="api-base-url">
  <code>https://dotastro.github.io/dotastrosite/api/v1</code>
</div>

<p>All endpoints return JSON. GitHub Pages sets <code>Access-Control-Allow-Origin: *</code> by default, so you can fetch from any browser, script, or tool without a proxy.</p>

<span class="section-label">// endpoints</span>
<h2 id="endpoints">Endpoints</h2>

<div class="api-endpoints">

  <div class="api-endpoint-block">
    <div class="api-method-path"><span class="api-method">GET</span><span class="api-path">/events.json</span></div>
    <p class="api-desc">List all 14 .Astronomy events with summary data: name, year, city, venue, dates, talk count, hack count.</p>
    <div class="api-code-block">
      <div class="api-code-label">curl</div>
      <pre><code>curl https://dotastro.github.io/dotastrosite/api/v1/events.json</code></pre>
    </div>
    <details class="api-response-wrap">
      <summary>Example response</summary>
      <pre class="api-response"><code>{"events":[{"slug":"one","number":"1","name":".Astronomy 1","year":2008,"city":"Cardiff","country":"United Kingdom","dates":"22-24 September 2008","talk_count":13,"hack_count":0},...],"total":14}</code></pre>
    </details>
    <button class="api-try-btn" data-url="https://dotastro.github.io/dotastrosite/api/v1/events.json">Try it live</button>
  </div>

  <div class="api-endpoint-block">
    <div class="api-method-path"><span class="api-method">GET</span><span class="api-path">/events/{slug}.json</span></div>
    <p class="api-desc">Full data for a single event: all organisers, talks, hacks, and links. Slugs: <code>one</code>, <code>two</code>, <code>three</code>, <code>four</code>, <code>five</code>, <code>six</code>, <code>seven</code>, <code>eight</code>, <code>nine</code>, <code>ten</code>, <code>eleven</code>, <code>alpha</code>, <code>twelve</code>, <code>thirteen</code>.</p>
    <div class="api-code-block">
      <div class="api-code-label">curl</div>
      <pre><code>curl https://dotastro.github.io/dotastrosite/api/v1/events/eight.json</code></pre>
    </div>
    <button class="api-try-btn" data-url="https://dotastro.github.io/dotastrosite/api/v1/events/eight.json">Try it live</button>
  </div>

  <div class="api-endpoint-block">
    <div class="api-method-path"><span class="api-method">GET</span><span class="api-path">/hacks.json</span></div>
    <p class="api-desc">All hacks from all events -- title, creators, description, source URLs, and which event they came from. 80 hacks across 14 events.</p>
    <div class="api-code-block">
      <div class="api-code-label">curl</div>
      <pre><code>curl https://dotastro.github.io/dotastrosite/api/v1/hacks.json</code></pre>
    </div>
    <div class="api-code-block">
      <div class="api-code-label">filter by event (jq)</div>
      <pre><code>curl -s https://dotastro.github.io/dotastrosite/api/v1/hacks.json \
  | jq '.hacks[] | select(.event == "eight")'</code></pre>
    </div>
    <button class="api-try-btn" data-url="https://dotastro.github.io/dotastrosite/api/v1/hacks.json">Try it live</button>
  </div>

  <div class="api-endpoint-block">
    <div class="api-method-path"><span class="api-method">GET</span><span class="api-path">/talks.json</span></div>
    <p class="api-desc">All talks from all events -- speaker, affiliation, title, talk type (invited, contributed, lightning, day zero). 202 talks.</p>
    <div class="api-code-block">
      <div class="api-code-label">curl</div>
      <pre><code>curl https://dotastro.github.io/dotastrosite/api/v1/talks.json</code></pre>
    </div>
    <div class="api-code-block">
      <div class="api-code-label">search by speaker (jq)</div>
      <pre><code>curl -s https://dotastro.github.io/dotastrosite/api/v1/talks.json \
  | jq '.talks[] | select(.speaker | test("Kendrew"; "i"))'</code></pre>
    </div>
    <button class="api-try-btn" data-url="https://dotastro.github.io/dotastrosite/api/v1/talks.json">Try it live</button>
  </div>

  <div class="api-endpoint-block">
    <div class="api-method-path"><span class="api-method">GET</span><span class="api-path">/people.json</span></div>
    <p class="api-desc">Everyone who has attended a .Astronomy conference, with their event history, roles, Bluesky handles, and affiliations. 404 people.</p>
    <div class="api-code-block">
      <div class="api-code-label">curl</div>
      <pre><code>curl https://dotastro.github.io/dotastrosite/api/v1/people.json</code></pre>
    </div>
    <button class="api-try-btn" data-url="https://dotastro.github.io/dotastrosite/api/v1/people.json">Try it live</button>
  </div>

  <div class="api-endpoint-block">
    <div class="api-method-path"><span class="api-method">GET</span><span class="api-path">/index.json</span></div>
    <p class="api-desc">API root: endpoint index, version, licence, and generation timestamp. Good starting point for discovery.</p>
    <div class="api-code-block">
      <div class="api-code-label">curl</div>
      <pre><code>curl https://dotastro.github.io/dotastrosite/api/v1/index.json</code></pre>
    </div>
    <button class="api-try-btn" data-url="https://dotastro.github.io/dotastrosite/api/v1/index.json">Try it live</button>
  </div>

</div>

<div class="api-response-output" id="api-response-output" style="display:none">
  <div class="api-response-output-header">
    <span id="api-response-url"></span>
    <button onclick="document.getElementById('api-response-output').style.display='none'">close</button>
  </div>
  <pre id="api-response-body"></pre>
</div>

<span class="section-label">// for llms and ai agents</span>
<h2 id="llms">For LLMs and AI Agents</h2>

<p>The .Astronomy API is designed to be easy to consume programmatically. Here are suggested prompts and patterns:</p>

<div class="api-code-block">
  <div class="api-code-label">Python</div>
  <pre><code>import requests

# Get all events
events = requests.get(
    "https://dotastro.github.io/dotastrosite/api/v1/events.json"
).json()["events"]

# Get full data for .Astronomy 8
dotastro8 = requests.get(
    "https://dotastro.github.io/dotastrosite/api/v1/events/eight.json"
).json()

# Search hacks by keyword
hacks = requests.get(
    "https://dotastro.github.io/dotastrosite/api/v1/hacks.json"
).json()["hacks"]
sonification_hacks = [h for h in hacks if "sonif" in h.get("description","").lower()]</code></pre>
</div>

<div class="api-code-block">
  <div class="api-code-label">Suggested prompts for LLMs</div>
  <pre><code>"Fetch https://dotastro.github.io/dotastrosite/api/v1/events.json
 and summarise how the conference has evolved since 2008."

"Using the .Astronomy API at https://dotastro.github.io/dotastrosite/api/v1,
 find all hacks that involved machine learning or AI."

"From https://dotastro.github.io/dotastrosite/api/v1/people.json,
 find everyone who attended more than 5 events."</code></pre>
</div>

<p>The API returns plain JSON with no authentication, pagination tokens, or rate limits. All data is suitable for training, research, and analysis under CC BY 4.0.</p>

<span class="section-label">// licence</span>
<h2 id="licence">Licence</h2>

<p>All data in the .Astronomy Archive API is released under <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">Creative Commons Attribution 4.0 International (CC BY 4.0)</a>. You are free to use, share, and build on this data for any purpose, including commercial use, as long as you credit the .Astronomy Archive.</p>

<p>Suggested attribution: <em>".Astronomy Archive, dotastro.github.io/dotastrosite, CC BY 4.0"</em></p>

<p>The archive itself is open source: <a href="https://github.com/dotastro/dotastrosite" target="_blank" rel="noopener">github.com/dotastro/dotastrosite</a>. Contributions and corrections welcome.</p>

<script>
document.querySelectorAll('.api-try-btn').forEach(function(btn) {
  btn.addEventListener('click', function() {
    var url = btn.getAttribute('data-url');
    var out = document.getElementById('api-response-output');
    var body = document.getElementById('api-response-body');
    var urlEl = document.getElementById('api-response-url');
    body.textContent = 'Loading...';
    out.style.display = 'block';
    urlEl.textContent = url;
    out.scrollIntoView({ behavior: 'smooth', block: 'start' });
    fetch(url)
      .then(function(r) { return r.json(); })
      .then(function(data) {
        body.textContent = JSON.stringify(data, null, 2).slice(0, 3000) + '\n// ... (truncated)';
      })
      .catch(function(e) { body.textContent = 'Error: ' + e.message; });
  });
});
</script>
