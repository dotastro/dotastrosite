# _data/ -- Single Source of Truth for Event Data

This directory contains the canonical, structured data for all .Astronomy conferences. Everything else (event pages, API JSON, search index, participants directory) is generated from these files.

## Structure

```
_data/
  event_meta.yml          # Master list of all events (ordering, basic metadata)
  events/
    one.yml               # .Astronomy 1, Cardiff, 2008
    two.yml               # .Astronomy 2, Leiden, 2009
    three.yml             # .Astronomy 3, Oxford, 2011
    ...
    thirteen.yml          # .Astronomy 13, Madrid, 2024
```

## Schema

### event_meta.yml

```yaml
events:
  - slug: one             # URL-safe identifier, used as filename
    number: "1"           # Display number (string: "1", "X", "alpha" etc.)
    name: ".Astronomy 1"  # Full display name
    year: 2008
    city: Cardiff
    country: United Kingdom
    venue: Cardiff University Department of Physics and Astronomy
    dates: "22-24 September 2008"
```

### events/SLUG.yml

```yaml
slug: eight
number: "8"
name: .Astronomy 8
year: 2016
city: Oxford
country: United Kingdom
venue: "Pembroke College, Oxford University"
dates: "20-23 June 2016"
description: "The eighth .Astronomy conference was held at..."

schedule:                         # Optional: links to schedule files
  - url: /assets/talks/eight/schedule.pdf
    format: PDF

organisers:
  - name: Becky Smethurst
    affiliation: Oxford University  # Optional
    bluesky: drbecky.bsky.social   # Optional
organisers_notes: "..."            # Optional: extra text about organising committee

talks:
  - speaker: Sarah Kendrew
    affiliation: "ESA, STScI"      # Optional
    title: "JWST and Astronomy"    # Optional (some talks have no recorded title)
    type: invited                  # invited | contributed | lightning | day_zero | unconference | remote | talk
    notes: "Discussion notes..."   # Optional: any extra context
    slides_url: ""                 # Optional
    video_url: ""                  # Optional
talks_narrative: "..."             # Optional: freeform text about the talks

hacks:
  - title: ArXiv Mailer
    creators:
      - Dan Foreman-Mackey
    description: "A hack to modernise..."  # Optional
    source_url: "https://github.com/..."   # Optional
    live_url: "https://..."                # Optional

participants:
  - name: Becky Smethurst
    affiliation: Oxford University  # Optional
    bluesky: drbecky.bsky.social   # Optional

links:
  - label: dotastronomy.com
    url: https://www.dotastronomy.com/eight
    internal: false                # Optional: true for site-relative URLs
    description: ""                # Optional

# Optional sections (present in some events)
programme_notes: "..."
unproceedings: "..."
unproceedings_authors: "..."
unproceedings_arxiv: "https://arxiv.org/abs/..."
sponsors: "..."
community_posts:
  - text: "Great conference!"
    author: Someone
    date: "2016-06-22"
    source: bluesky
    url: "https://bsky.app/..."
```

## How to Add a New Event

1. Add an entry to `event_meta.yml` with the slug, number, name, year, city, country, venue, and dates.
2. Create `events/SLUG.yml` following the schema above.
3. Create `events/SLUG/index.md` with minimal front matter:
   ```yaml
   ---
   layout: event
   title: ".Astronomy N, City, Year"
   event_slug: SLUG
   event_num: "N"
   ---
   ```
4. Run the rebuild scripts: `python3 scripts/rebuild-all.py --no-bsky`
5. Commit and push.

## Rebuild Scripts

After any changes to `_data/events/*.yml`:

```bash
# Full rebuild (includes Bluesky handle lookup for new participants)
python3 scripts/rebuild-all.py

# Quick rebuild (skip Bluesky API calls)
python3 scripts/rebuild-all.py --no-bsky
```

This regenerates:
- `api/v1/*.json` (public API)
- `assets/js/participants-data.json` (participants directory)
- `assets/js/search-index.json` (site search)

## Notes

- Jekyll automatically loads `_data/` files as `site.data.*`
- `site.data.events.eight` gives you the full YAML for .Astronomy 8
- `site.data.event_meta.events` gives you the ordered list of all events
- The event page layout (`_layouts/event.html`) renders everything from the YAML
- Do not use em dashes in any content
