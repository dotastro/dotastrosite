---
layout: default
title: API
description: The .Astronomy Archive API -- machine-readable access to all event data.
permalink: /api/
---

<div class="api-page">

<div class="event-page-hero" data-num="API">
  <div class="event-page-kicker">Developer Tools</div>
  <h1 class="event-page-title">.Astronomy Archive API</h1>
  <div class="event-page-meta">
    <span>v1.0</span>
    <span>Read-only JSON API. Free to use. No auth required.</span>
  </div>
  <p class="event-page-desc">Machine-readable access to every .Astronomy event, talk, hack, and participant since 2008. Built for developers, researchers, bots, and LLMs. All data is served as static JSON from GitHub Pages.</p>
</div>

<nav class="event-page-nav" aria-label="Jump to section">
  <a href="#base-url">Base URL</a>
  <a href="#endpoints">Endpoints</a>
  <a href="#try-it">Try It</a>
  <a href="#for-llms">For LLMs</a>
  <a href="#licence">Licence</a>
</nav>

<span class="section-label">// base url</span>
## Base URL {#base-url}

```
https://dotastro.github.io/dotastrosite/api/v1
```

All endpoints return JSON with `Content-Type: application/json`. CORS is handled by GitHub Pages (cross-origin requests are allowed by default).

The API root at [`/api/v1/index.json`]({{ site.baseurl }}/api/v1/index.json) describes all available endpoints.

---

<span class="section-label">// endpoints</span>
## Endpoints {#endpoints}

### GET /events.json

List all 14 .Astronomy events with summary data.

<div class="api-example">

```bash
curl https://dotastro.github.io/dotastrosite/api/v1/events.json
```

</div>

<div class="api-response">

```json
{
  "events": [
    {
      "slug": "one",
      "number": "1",
      "name": ".Astronomy 1",
      "year": 2008,
      "city": "Cardiff",
      "country": "United Kingdom",
      "venue": "Cardiff University Department of Physics and Astronomy",
      "dates": "22-24 September 2008",
      "url": "https://dotastro.github.io/dotastrosite/events/one/",
      "participant_count": 32,
      "hack_count": 0,
      "talk_count": 13
    }
  ],
  "total": 14,
  "generated_at": "2026-04-30T..."
}
```

</div>

<button class="try-btn" data-url="{{ site.baseurl }}/api/v1/events.json">Try it live</button>

---

### GET /events/{slug}.json

Full data for a single event. Slugs: `one`, `two`, `three`, `four`, `five`, `six`, `seven`, `eight`, `nine`, `ten`, `eleven`, `alpha`, `twelve`, `thirteen`.

<div class="api-example">

```bash
curl https://dotastro.github.io/dotastrosite/api/v1/events/eight.json
```

</div>

<div class="api-response">

```json
{
  "slug": "eight",
  "number": "8",
  "name": ".Astronomy 8",
  "year": 2016,
  "city": "Oxford",
  "country": "United Kingdom",
  "venue": "Pembroke College, Oxford University",
  "dates": "20-23 June 2016",
  "organisers": [
    {"name": "Becky Smethurst", "affiliation": "Oxford, lead organiser", "bluesky": "drbecky.bsky.social"}
  ],
  "talks": [
    {"event": "eight", "year": 2016, "speaker": "Sarah Kendrew", "affiliation": "ESA, STScI", "title": "JWST and Astronomy..."}
  ],
  "hacks": [
    {"title": ".draft", "event": "eight", "year": 2016, "creators": ["Andy Casey"], "description": "..."}
  ],
  "participants": [
    {"name": "Alasdair Allan"}
  ]
}
```

</div>

<button class="try-btn" data-url="{{ site.baseurl }}/api/v1/events/eight.json">Try it live</button>

---

### GET /people.json

Every person who has attended a .Astronomy event, with their events and roles.

<div class="api-example">

```bash
curl https://dotastro.github.io/dotastrosite/api/v1/people.json
```

</div>

<div class="api-response">

```json
{
  "people": [
    {
      "name": "Sarah Kendrew",
      "events": ["two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "alpha", "twelve", "thirteen"],
      "event_count": 12,
      "roles": {"two": ["organiser"], "eight": ["organiser", "speaker"]},
      "bluesky": "sarahkendrew.bsky.social",
      "current_affiliation": "ESA, Baltimore"
    }
  ],
  "total": 404,
  "generated_at": "2026-04-30T..."
}
```

</div>

<button class="try-btn" data-url="{{ site.baseurl }}/api/v1/people.json">Try it live</button>

---

### GET /hacks.json

All hacks across all events.

<div class="api-example">

```bash
curl https://dotastro.github.io/dotastrosite/api/v1/hacks.json
```

</div>

<div class="api-response">

```json
{
  "hacks": [
    {
      "title": "Chromotone",
      "event": "three",
      "year": 2011,
      "creators": ["Jon Yardley", "Chris North", "Haley Gomez", "Edward Gomez"],
      "description": "Exploring multiwavelength astronomy with sound...",
      "source_url": "https://github.com/jonyardley/Chromotone",
      "live_url": null
    }
  ],
  "total": 80,
  "generated_at": "2026-04-30T..."
}
```

</div>

<button class="try-btn" data-url="{{ site.baseurl }}/api/v1/hacks.json">Try it live</button>

---

### GET /talks.json

All talks across all events.

<div class="api-example">

```bash
curl https://dotastro.github.io/dotastrosite/api/v1/talks.json
```

</div>

<div class="api-response">

```json
{
  "talks": [
    {
      "event": "one",
      "year": 2008,
      "speaker": "Joshua Bloom",
      "affiliation": "UC Berkeley",
      "title": "PAIRITEL and robotic telescope networks",
      "type": "talk",
      "slides_url": null,
      "video_url": null
    }
  ],
  "total": 202,
  "generated_at": "2026-04-30T..."
}
```

</div>

<button class="try-btn" data-url="{{ site.baseurl }}/api/v1/talks.json">Try it live</button>

---

<span class="section-label">// searching and filtering</span>
## Searching {#searching}

This is a static JSON API, so there is no server-side search. All endpoints return the complete dataset, which is small enough to load in a browser or script and filter client-side.

Example: find all events in the United Kingdom:

```javascript
const data = await fetch('https://dotastro.github.io/dotastrosite/api/v1/events.json').then(r => r.json());
const uk = data.events.filter(e => e.country === 'United Kingdom');
```

Example: find all talks by a specific speaker:

```javascript
const data = await fetch('https://dotastro.github.io/dotastrosite/api/v1/talks.json').then(r => r.json());
const talks = data.talks.filter(t => t.speaker.includes('Kendrew'));
```

---

<span class="section-label">// try it</span>
## Try It {#try-it}

Click any "Try it live" button above to fetch data directly from the API. The response will appear below:

<div id="api-result-container" style="display:none;">
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
    <span class="section-label" style="margin:0;">// response</span>
    <button id="api-result-close" class="try-btn" style="font-size:0.75rem; padding:0.25rem 0.75rem;">Close</button>
  </div>
  <pre id="api-result" class="api-response-live"><code>Loading...</code></pre>
</div>

---

<span class="section-label">// for llms and ai agents</span>
## For LLMs and AI Agents {#for-llms}

This API is designed to be useful for large language models and AI agents. The data is clean, well-structured, and covers 16 years of conference history.

### Suggested approach

1. Start with [`/api/v1/events.json`]({{ site.baseurl }}/api/v1/events.json) to get an overview of all events
2. Fetch individual events with `/api/v1/events/{slug}.json` for full detail
3. Use [`/api/v1/people.json`]({{ site.baseurl }}/api/v1/people.json) to find connections between attendees across events
4. Use [`/api/v1/hacks.json`]({{ site.baseurl }}/api/v1/hacks.json) and [`/api/v1/talks.json`]({{ site.baseurl }}/api/v1/talks.json) for the full creative and intellectual output of the conference series

### Example prompts that work well with this data

- "Who has attended the most .Astronomy events?"
- "What hacks were created at .Astronomy 8 in Oxford?"
- "Show me all talks about citizen science across all events"
- "Which people have been both organisers and speakers?"
- "What is the geographic distribution of .Astronomy events?"
- "Find all hacks with GitHub repositories"

### Data notes for machines

- Event slugs are English words (one, two, three... thirteen, alpha), not numbers
- The `alpha` event (2020) was online due to COVID-19
- The `ten` event used Roman numeral X as its official number
- Bluesky handles are included where known but are not comprehensive
- `source_url` and `live_url` on hacks may be dead links (some date from 2008)
- Talks without titles have `null` in the title field
- Not all participants have affiliations listed

---

<span class="section-label">// licence and contributing</span>
## Licence {#licence}

All data is available under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) licence. You are free to use, share, and adapt the data for any purpose, with attribution.

**Attribution:** .Astronomy Conference Archive, [dotastro.github.io/dotastrosite](https://dotastro.github.io/dotastrosite/)

### Contributing

The API is generated from the event pages in the [dotastrosite GitHub repository](https://github.com/dotastro/dotastrosite). If you spot missing data, wrong affiliations, or broken links, please open an issue or pull request.

The generation script lives at [`scripts/generate-api.py`](https://github.com/dotastro/dotastrosite/blob/main/scripts/generate-api.py).

</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const container = document.getElementById('api-result-container');
  const resultEl = document.getElementById('api-result').querySelector('code');
  const closeBtn = document.getElementById('api-result-close');

  document.querySelectorAll('.try-btn[data-url]').forEach(function(btn) {
    btn.addEventListener('click', function() {
      const url = this.getAttribute('data-url');
      container.style.display = 'block';
      resultEl.textContent = 'Loading...';

      fetch(url)
        .then(function(r) { return r.json(); })
        .then(function(data) {
          // Truncate if too large
          var text = JSON.stringify(data, null, 2);
          if (text.length > 5000) {
            text = text.substring(0, 5000) + '\n\n... (truncated, ' + text.length + ' chars total)';
          }
          resultEl.textContent = text;
          container.scrollIntoView({ behavior: 'smooth', block: 'start' });
        })
        .catch(function(err) {
          resultEl.textContent = 'Error: ' + err.message;
        });
    });
  });

  closeBtn.addEventListener('click', function() {
    container.style.display = 'none';
  });
});
</script>
