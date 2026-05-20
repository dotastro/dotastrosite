#!/usr/bin/env python3
"""Generate llms.txt and llms-full.txt from current API data.
Run as part of rebuild-all.py after any data changes.
"""

import json, os, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(path):
    with open(os.path.join(BASE, path)) as f:
        return json.load(f)

events_data = load('api/v1/events.json')['events']
hacks_data = load('api/v1/hacks.json')['hacks']
talks_data = load('api/v1/talks.json')['talks']
people_data = load('assets/js/participants-data.json')
bsky_data = load('assets/js/bluesky-cache.json')

total_people = people_data['total']
total_hacks = len(hacks_data)
total_talks = len(talks_data)
total_bsky = len(bsky_data.get('found', {}))
updated = datetime.date.today().strftime('%Y-%m')

# ── llms.txt (concise) ───────────────────────────────────────────────────────
cities = ', '.join(e['city'] for e in events_data)

short = f"""# .Astronomy Conference Archive
# https://dotastronomy.com
# Last updated: {updated}

## What is .Astronomy?

.Astronomy (pronounced "dot-astronomy") is a conference series founded in Cardiff in 2008 by Robert Simpson, then a PhD student at the University of Cardiff. It brings together astronomers, developers, educators and science communicators to explore how the web and technology can transform science. It is not a traditional research conference. The focus is on people, tools, and collaboration: talks, unconferences, and hack days.

## Events

{len(events_data)} events across 9 countries (2008-2024). Attendance is typically 60-100 people, selected via application to ensure diversity.

Events: {cities}.

Next planned event: London, 2027.

## Archive data (as of {updated})

- {total_hacks} hacks documented across all events
- {total_talks} talks documented
- {total_people} known participants
- {total_bsky} Bluesky profiles matched to participants

## API

Free, open, no authentication required. CC BY 4.0.

Base URL: https://dotastronomy.com/api/v1

- GET /api/v1/index.json -- API discovery and metadata
- GET /api/v1/events.json -- all {len(events_data)} events (summary)
- GET /api/v1/events/{{slug}}.json -- full event: organisers, talks, hacks, participants, links
  Slugs: {", ".join(e["slug"] for e in events_data)}
- GET /api/v1/hacks.json -- all {total_hacks} hacks with creators, descriptions, source/live URLs
- GET /api/v1/talks.json -- all {total_talks} talks with speakers, affiliations, types
- GET /api/v1/people.json -- all {total_people} known participants with event history, roles, Bluesky handles

## Foundation

The .Astronomy Foundation is a registered charitable trust (UK), founded 30 April 2019. Objects: "For the public benefit, the advancement of astronomy and related fields, in any part of the world, by people using technology to innovate the practice and communication of the subject."

Trustees: Robert Simpson (Chairperson), Sarah Kendrew (Secretary), Chris Lintott (Treasurer).

## Key people

- Robert Simpson: founder, organiser of multiple events, Chairperson of Foundation. Bluesky: orbitingfrog.bsky.social
- Sarah Kendrew: ESA instrument scientist (JWST/MIRI), most prolific event organiser. Bluesky: sarahkendrew.bsky.social
- Chris Lintott: Professor of Astrophysics, Oxford; Zooniverse co-founder; AAS Journals editor. Bluesky: chrislintott.bsky.social
- Amanda Bauer: Deputy Director, Yerkes Observatory. Bluesky: amandabauer.bsky.social
- Becky Smethurst: Oxford astrophysicist, science communicator (Dr Becky YouTube). Bluesky: drbecky.bsky.social
- Arfon Smith: Schmidt Sciences. Bluesky: arfon.bsky.social
- Alasdair Allan: Negroni Venture Studios. Bluesky: alasdairallan.com

## Community

Bluesky: @dotastro.bsky.social
GitHub: github.com/dotastro
Source: github.com/dotastro/dotastrosite
"""

with open(os.path.join(BASE, 'llms.txt'), 'w') as f:
    f.write(short)
print(f"llms.txt: {len(short)} chars")

# ── llms-full.txt (complete reference) ──────────────────────────────────────
lines = [
    f"# .Astronomy Conference Archive -- Full Reference",
    f"# https://dotastronomy.com",
    f"# Last updated: {updated}",
    f"# CC BY 4.0. API: https://dotastronomy.com/api/v1",
    "",
    "## Events", "",
]

for ev in events_data:
    lines += [
        f"### {ev['name']} -- {ev['city']}, {ev.get('country','')}, {ev['year']}",
        f"Dates: {ev['dates']}",
        f"Venue: {ev['venue']}",
        f"URL: https://dotastronomy.com/events/{ev['slug']}/",
        f"Full data: https://dotastronomy.com/api/v1/events/{ev['slug']}.json",
        f"Participants: {ev.get('participant_count',0)} | Talks: {ev.get('talk_count',0)} | Hacks: {ev.get('hack_count',0)}",
        "",
    ]

lines += ["## Hacks", f"Total: {total_hacks}", ""]
current_event = None
for h in hacks_data:
    if h['event'] != current_event:
        current_event = h['event']
        ev_name = next((e['name'] for e in events_data if e['slug'] == h['event']), h['event'])
        lines.append(f"### {ev_name} ({h['year']})")
    creators = ', '.join(h.get('creators') or [])
    desc = (h.get('description') or '')[:100]
    src = h.get('source_url','')
    live = h.get('live_url','')
    line = f"- {h['title']}"
    if creators: line += f" ({creators})"
    if desc: line += f": {desc}"
    if src: line += f" [source: {src}]"
    if live and live != src: line += f" [live: {live}]"
    lines.append(line)
lines.append("")

lines += ["## Talks", f"Total: {total_talks}", ""]
current_event = None
for t in talks_data:
    if t['event'] != current_event:
        current_event = t['event']
        ev_name = next((e['name'] for e in events_data if e['slug'] == t['event']), t['event'])
        lines.append(f"### {ev_name} ({t['year']})")
    speaker = t.get('speaker','')
    aff = t.get('affiliation','')
    title = (t.get('title') or t.get('notes') or '')[:100]
    line = f"- {speaker}"
    if aff: line += f" ({aff})"
    if title: line += f": {title}"
    lines.append(line)

content = '\n'.join(lines)
with open(os.path.join(BASE, 'llms-full.txt'), 'w') as f:
    f.write(content)
print(f"llms-full.txt: {len(lines)} lines, {len(content)} chars")
