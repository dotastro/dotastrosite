#!/usr/bin/env python3
"""
Generate static JSON API files for the .Astronomy conference archive.
Reads event pages (index.md) and participants-data.json, writes API files to api/v1/.
"""

import json
import os
import re
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_DIR = os.path.join(REPO_ROOT, 'events')
API_DIR = os.path.join(REPO_ROOT, 'api', 'v1')
EVENTS_API_DIR = os.path.join(API_DIR, 'events')
PARTICIPANTS_JSON = os.path.join(REPO_ROOT, 'assets', 'js', 'participants-data.json')
BASE_URL = 'https://dotastro.github.io/dotastrosite'
API_BASE = f'{BASE_URL}/api/v1'

NOW = datetime.now(timezone.utc).isoformat()

BSKY = {
    'robert simpson': 'orbitingfrog.bsky.social',
    'rob simpson': 'orbitingfrog.bsky.social',
    'chris lintott': 'chrislintott.bsky.social',
    'sarah kendrew': 'sarahkendrew.bsky.social',
    'amanda bauer': 'amandabauer.bsky.social',
    'alasdair allan': 'alasdairallan.com',
    'becky smethurst': 'drbecky.bsky.social',
    'arfon smith': 'arfon.bsky.social',
    'emily hunt': 'emilyhunt.bsky.social',
    'geert barentsen': 'geert.bsky.social',
}

# Slugs to process (exclude 'live')
EVENT_SLUGS = [
    'one', 'two', 'three', 'four', 'five', 'six', 'seven',
    'eight', 'nine', 'ten', 'eleven', 'alpha', 'twelve', 'thirteen'
]

EVENT_META = {
    'one':      {'number': '1',  'name': '.Astronomy 1',  'year': 2008, 'city': 'Cardiff',      'country': 'United Kingdom'},
    'two':      {'number': '2',  'name': '.Astronomy 2',  'year': 2009, 'city': 'Leiden',       'country': 'Netherlands'},
    'three':    {'number': '3',  'name': '.Astronomy 3',  'year': 2011, 'city': 'Oxford',       'country': 'United Kingdom'},
    'four':     {'number': '4',  'name': '.Astronomy 4',  'year': 2012, 'city': 'Heidelberg',   'country': 'Germany'},
    'five':     {'number': '5',  'name': '.Astronomy 5',  'year': 2013, 'city': 'Cambridge, MA','country': 'United States'},
    'six':      {'number': '6',  'name': '.Astronomy 6',  'year': 2014, 'city': 'Chicago',      'country': 'United States'},
    'seven':    {'number': '7',  'name': '.Astronomy 7',  'year': 2015, 'city': 'Sydney',       'country': 'Australia'},
    'eight':    {'number': '8',  'name': '.Astronomy 8',  'year': 2016, 'city': 'Oxford',       'country': 'United Kingdom'},
    'nine':     {'number': '9',  'name': '.Astronomy 9',  'year': 2017, 'city': 'Cape Town',    'country': 'South Africa'},
    'ten':      {'number': 'X',  'name': '.Astronomy X',  'year': 2018, 'city': 'Baltimore',    'country': 'United States'},
    'eleven':   {'number': '11', 'name': '.Astronomy 11', 'year': 2019, 'city': 'Toronto',      'country': 'Canada'},
    'alpha':    {'number': '\u03b1','name': '.Astronomy \u03b1','year': 2020,'city': 'Online',   'country': 'Online'},
    'twelve':   {'number': '12', 'name': '.Astronomy 12', 'year': 2023, 'city': 'New York',     'country': 'United States'},
    'thirteen': {'number': '13', 'name': '.Astronomy 13', 'year': 2024, 'city': 'Madrid',       'country': 'Spain'},
}


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Wrote {path}")


def load_participants_data():
    """Load the existing participants-data.json"""
    with open(PARTICIPANTS_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_bsky(name):
    """Get Bluesky handle for a person, checking the hardcoded list first."""
    lower = name.lower().strip()
    return BSKY.get(lower, None)


def extract_venue_dates(content):
    """Extract venue and dates from the event-page-meta spans."""
    dates = ''
    venue = ''
    meta_match = re.search(r'<div class="event-page-meta">(.*?)</div>', content, re.DOTALL)
    if meta_match:
        spans = re.findall(r'<span>(.*?)</span>', meta_match.group(1), re.DOTALL)
        if len(spans) >= 1:
            dates = spans[0].strip()
        if len(spans) >= 2:
            venue = spans[1].strip()
    return dates, venue


def extract_organisers(content):
    """Extract organisers from the Organisers section."""
    organisers = []
    # Find the Organisers section
    org_match = re.search(r'## Organisers.*?\n(.*?)(?=\n<span class="section-label">|\n##\s|\nSupported by|\nOrganising committee)', content, re.DOTALL)
    if not org_match:
        org_match = re.search(r'## Organisers.*?\n(.*?)(?=\n<span|\n##)', content, re.DOTALL)
    if org_match:
        lines = org_match.group(1).strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('- '):
                line = line[2:].strip()
                # Parse "Name (Affiliation, role)"
                aff_match = re.match(r'(.+?)\s*\(([^)]+)\)', line)
                if aff_match:
                    name = aff_match.group(1).strip()
                    affiliation = aff_match.group(2).strip()
                else:
                    name = line.strip()
                    affiliation = None
                bsky = get_bsky(name)
                org = {'name': name}
                if affiliation:
                    org['affiliation'] = affiliation
                if bsky:
                    org['bluesky'] = bsky
                organisers.append(org)
    return organisers


def extract_talks(content, slug):
    """Extract talks from the Talks section. Returns list of talk dicts."""
    talks = []
    year = EVENT_META[slug]['year']

    # Find the Talks section
    talks_section = re.search(r'## Talks \{#talks\}(.*?)(?=\n<span class="section-label">|\n## [A-Z])', content, re.DOTALL)
    if not talks_section:
        talks_section = re.search(r'## Talks \{#talks\}(.*?)(?=\n##\s(?!#))', content, re.DOTALL)
    if not talks_section:
        return talks

    section_text = talks_section.group(1)

    # Detect current talk type heading
    current_type = 'talk'

    # Parse talk lines: **Speaker** (Affiliation): *Title*
    # or - **Speaker** (Affiliation): *Title*
    lines = section_text.split('\n')
    for line in lines:
        line = line.strip()

        # Detect headings for talk type
        if re.match(r'###\s+(Invited|Keynote)', line, re.IGNORECASE):
            current_type = 'invited'
            continue
        elif re.match(r'###\s+Lightning', line, re.IGNORECASE):
            current_type = 'lightning'
            continue
        elif re.match(r'###\s+(Day Zero|Day 0|Contributed|Pre-Dinner)', line, re.IGNORECASE):
            if 'tutorial' in line.lower():
                current_type = 'tutorial'
            elif 'contributed' in line.lower():
                current_type = 'contributed'
            elif 'pre-dinner' in line.lower():
                current_type = 'talk'
            else:
                current_type = 'talk'
            continue
        elif re.match(r'###\s+Day\s+\d', line, re.IGNORECASE):
            current_type = 'talk'
            continue
        elif re.match(r'###\s+Invited Speakers', line, re.IGNORECASE):
            current_type = 'invited'
            continue
        elif re.match(r'###\s+', line):
            # Other headings (Themes, Highlights, etc.) -- skip processing
            if any(kw in line.lower() for kw in ['theme', 'highlight', 'notable', 'unconference', 'proceeding', 'official', 'public', 'sponsor']):
                current_type = None
                continue
            # Other day headings
            current_type = 'talk'
            continue

        if current_type is None:
            continue

        # Skip non-talk lines
        if not line.startswith('- **') and not line.startswith('**'):
            continue

        # Remove leading - if present
        if line.startswith('- '):
            line = line[2:]

        # Parse: **Speaker** (Affiliation): *Title*
        # or **Speaker**: *Title*
        # or **Speaker** (Affiliation): Title
        talk_match = re.match(
            r'\*\*(.+?)\*\*\s*(?:\(([^)]*)\))?\s*:?\s*(?:\*([^*]+)\*|(.+))?',
            line
        )
        if talk_match:
            speaker = talk_match.group(1).strip()
            affiliation = talk_match.group(2)
            title = talk_match.group(3) or talk_match.group(4)

            if affiliation:
                affiliation = affiliation.strip()
                # Remove Twitter handles from affiliation
                affiliation = re.sub(r',?\s*@\w+', '', affiliation).strip()
                # Remove trailing comma
                affiliation = affiliation.rstrip(',').strip()

            if title:
                title = title.strip().rstrip('.')
                # Clean up markdown links in title
                title = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', title)
                # Remove HTML tags
                title = re.sub(r'<[^>]+>', '', title)
                # Skip if title is just a link or very short
                title = title.strip()

            talk = {
                'event': slug,
                'year': year,
                'speaker': speaker,
                'affiliation': affiliation if affiliation else None,
                'title': title if title else None,
                'type': current_type,
                'slides_url': None,
                'video_url': None
            }
            talks.append(talk)

    return talks


def extract_hacks(content, slug):
    """Extract hacks from the hack-card divs."""
    hacks = []
    year = EVENT_META[slug]['year']

    # Find all hack cards
    hack_cards = re.findall(
        r'<div class="hack-card">(.*?)</div>\s*</div>',
        content, re.DOTALL
    )

    # If that doesn't match well, try a looser pattern
    if not hack_cards:
        hack_cards = re.findall(
            r'<div class="hack-card">(.*?)\n</div>',
            content, re.DOTALL
        )

    # Even looser: grab everything between hack-card divs
    if not hack_cards:
        # Split by hack-card divs
        parts = re.split(r'<div class="hack-card">', content)
        for part in parts[1:]:  # Skip first (before first hack-card)
            end = part.find('</div>\n</div>')
            if end == -1:
                end = part.find('\n</div>')
            if end >= 0:
                hack_cards.append(part[:end])

    for card in hack_cards:
        title_match = re.search(r'<div class="hack-title">(.*?)</div>', card)
        creators_match = re.search(r'<div class="hack-creators">(.*?)</div>', card)
        desc_match = re.search(r'<(?:div|p) class="hack-desc">(.*?)</(?:div|p)>', card, re.DOTALL)
        links_match = re.search(r'<div class="hack-links">(.*?)</div>', card, re.DOTALL)

        title = title_match.group(1).strip() if title_match else None
        if not title:
            continue

        creators_text = creators_match.group(1).strip() if creators_match else ''
        # Parse creators: split by comma or " and "
        creators = []
        if creators_text:
            # Handle "Name (@handle)" patterns
            creators_text = re.sub(r'\s*\(@\w+\)', '', creators_text)
            # Split by comma or " and "
            parts = re.split(r',\s*|\s+and\s+', creators_text)
            creators = [c.strip() for c in parts if c.strip()]

        description = ''
        if desc_match:
            description = desc_match.group(1).strip()
            # Clean HTML tags from description
            description = re.sub(r'<[^>]+>', '', description)
            description = description.strip()

        source_url = None
        live_url = None
        if links_match:
            links_html = links_match.group(1)
            # Find source/GitHub links
            source_matches = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>\s*(?:Source|GitHub)\s*</a>', links_html, re.IGNORECASE)
            if source_matches:
                source_url = source_matches[0]
            # Find live links
            live_matches = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>\s*(?:Live|Install|Watch|Listen|Download)\s*</a>', links_html, re.IGNORECASE)
            if live_matches:
                live_url = live_matches[0]

        hack = {
            'title': title,
            'event': slug,
            'year': year,
            'creators': creators,
            'description': description,
            'source_url': source_url,
            'live_url': live_url
        }
        hacks.append(hack)

    return hacks


def extract_participants(content, slug):
    """Extract participants from the Participants section."""
    participants = []

    # Find participants section
    parts_section = re.search(r'## Participants.*?\n(.*?)(?=\n<span class="section-label">|\n## [A-Z]|\n<div class="contribute)', content, re.DOTALL)
    if not parts_section:
        parts_section = re.search(r'## Participants.*?\n(.*?)$', content, re.DOTALL)
    if not parts_section:
        return participants

    section_text = parts_section.group(1)

    # Parse both formats:
    # - Name (Affiliation)
    # <li>Name (Affiliation)</li>
    lines = section_text.split('\n')
    for line in lines:
        line = line.strip()

        name = None
        affiliation = None

        # <li> format
        li_match = re.match(r'<li>(.+?)(?:\s*\(([^)]*)\))?\s*</li>', line)
        if li_match:
            name = li_match.group(1).strip()
            affiliation = li_match.group(2)
        else:
            # - Name (Affiliation) format
            dash_match = re.match(r'-\s+(.+?)(?:\s*\(([^)]*)\))?\s*$', line)
            if dash_match:
                name = dash_match.group(1).strip()
                affiliation = dash_match.group(2)

        if name:
            # Clean up name
            name = re.sub(r'<[^>]+>', '', name).strip()
            if not name:
                continue

            if affiliation:
                affiliation = affiliation.strip()
                # Remove Twitter handles
                affiliation = re.sub(r',?\s*@\w+', '', affiliation).strip()
                affiliation = affiliation.rstrip(',').strip()

            p = {'name': name}
            if affiliation:
                p['affiliation'] = affiliation
            participants.append(p)

    return participants


def extract_links(content, slug):
    """Extract links from the Links section."""
    links = []
    links_section = re.search(r'## Links \{#links\}(.*?)(?=\n<div class="contribute|\n##\s|\n### Sponsors|\Z)', content, re.DOTALL)
    if not links_section:
        return links

    section_text = links_section.group(1)

    # Parse markdown links: [label](url)
    for match in re.finditer(r'-\s*\[([^\]]+)\]\(([^)]+)\)', section_text):
        label = match.group(1).strip()
        url = match.group(2).strip()
        # Skip template URLs
        if '{{ site.baseurl }}' in url:
            continue
        links.append({'label': label, 'url': url})

    return links


def process_event(slug):
    """Process a single event and return its full data."""
    md_path = os.path.join(EVENTS_DIR, slug, 'index.md')
    if not os.path.exists(md_path):
        print(f"  WARNING: {md_path} not found")
        return None

    content = read_file(md_path)
    meta = EVENT_META[slug]

    dates, venue = extract_venue_dates(content)
    organisers = extract_organisers(content)
    talks = extract_talks(content, slug)
    hacks = extract_hacks(content, slug)
    participants = extract_participants(content, slug)
    links = extract_links(content, slug)

    event = {
        'slug': slug,
        'number': meta['number'],
        'name': meta['name'],
        'year': meta['year'],
        'city': meta['city'],
        'country': meta['country'],
        'venue': venue,
        'dates': dates,
        'url': f'{BASE_URL}/events/{slug}/',
        'organisers': organisers,
        'talks': talks,
        'hacks': hacks,
        'participants': participants,
        'links': links,
        'participant_count': len(participants),
        'hack_count': len(hacks),
        'talk_count': len(talks),
    }

    return event


def build_people_endpoint(participants_data, all_events):
    """Build the people endpoint from participants-data.json, enriched with event data."""
    people = []

    # Build a lookup from participants-data.json
    for person in participants_data['people']:
        name = person['name']
        events = person.get('events', [])
        event_count = len(events)
        roles = person.get('roles', {})
        bsky = person.get('bluesky', '') or get_bsky(name) or None

        # Get current affiliation
        affiliation = person.get('affiliation', '')
        if affiliation:
            # Clean Twitter handles from affiliation
            affiliation = re.sub(r',?\s*@\w+', '', affiliation).strip()
            affiliation = affiliation.rstrip(',').strip()

        # Clean up roles - convert to simpler format
        clean_roles = {}
        for evt, role_list in roles.items():
            # Filter to just organiser and speaker roles (skip attendee as it's implied)
            notable = [r for r in role_list if r in ('organiser', 'speaker')]
            if notable:
                clean_roles[evt] = notable

        p = {
            'name': name,
            'events': events,
            'event_count': event_count,
        }
        if clean_roles:
            p['roles'] = clean_roles
        if bsky:
            p['bluesky'] = bsky
        if affiliation:
            p['current_affiliation'] = affiliation

        people.append(p)

    # Sort by event count (descending), then name
    people.sort(key=lambda x: (-x['event_count'], x['name']))

    return {
        'people': people,
        'total': len(people),
        'generated_at': NOW
    }


def main():
    print("=== .Astronomy API Generator ===\n")

    # Load participants data
    participants_data = load_participants_data()
    print(f"Loaded {len(participants_data['people'])} people from participants-data.json\n")

    # Process all events
    all_events = []
    all_talks = []
    all_hacks = []

    for slug in EVENT_SLUGS:
        print(f"Processing {slug}...")
        event = process_event(slug)
        if event:
            all_events.append(event)
            all_talks.extend(event['talks'])
            all_hacks.extend(event['hacks'])
            print(f"  {event['participant_count']} participants, {event['talk_count']} talks, {event['hack_count']} hacks")

    print(f"\nTotal events: {len(all_events)}")
    print(f"Total talks: {len(all_talks)}")
    print(f"Total hacks: {len(all_hacks)}")

    # Create API directory structure
    os.makedirs(EVENTS_API_DIR, exist_ok=True)

    # 1. Write api/v1/index.json
    index_data = {
        'name': '.Astronomy Conference Archive API',
        'version': '1.0',
        'description': 'A read-only JSON API for the .Astronomy conference series archive. Free to use, no auth required.',
        'base_url': API_BASE,
        'endpoints': {
            'events': '/events.json',
            'event': '/events/{slug}.json  (slug: one, two, three, ..., thirteen, alpha)',
            'people': '/people.json',
            'hacks': '/hacks.json',
            'talks': '/talks.json',
            'search': 'See documentation -- use client-side filtering on the JSON endpoints'
        },
        'generated_at': NOW,
        'source': 'https://github.com/dotastro/dotastrosite',
        'licence': 'CC BY 4.0'
    }
    write_json(os.path.join(API_DIR, 'index.json'), index_data)

    # 2. Write api/v1/events.json (minimal event list)
    events_list = []
    for event in all_events:
        events_list.append({
            'slug': event['slug'],
            'number': event['number'],
            'name': event['name'],
            'year': event['year'],
            'city': event['city'],
            'country': event['country'],
            'venue': event['venue'],
            'dates': event['dates'],
            'url': event['url'],
            'participant_count': event['participant_count'],
            'hack_count': event['hack_count'],
            'talk_count': event['talk_count']
        })
    write_json(os.path.join(API_DIR, 'events.json'), {
        'events': events_list,
        'total': len(events_list),
        'generated_at': NOW
    })

    # 3. Write individual event files
    for event in all_events:
        event_file = os.path.join(EVENTS_API_DIR, f'{event["slug"]}.json')
        write_json(event_file, event)

    # 4. Write api/v1/people.json
    people_data = build_people_endpoint(participants_data, all_events)
    write_json(os.path.join(API_DIR, 'people.json'), people_data)
    print(f"\nPeople: {people_data['total']}")

    # 5. Write api/v1/hacks.json
    hacks_data = {
        'hacks': all_hacks,
        'total': len(all_hacks),
        'generated_at': NOW
    }
    write_json(os.path.join(API_DIR, 'hacks.json'), hacks_data)

    # 6. Write api/v1/talks.json
    talks_data = {
        'talks': all_talks,
        'total': len(all_talks),
        'generated_at': NOW
    }
    write_json(os.path.join(API_DIR, 'talks.json'), talks_data)

    # Summary
    print(f"\n=== API Generation Complete ===")
    print(f"Events:  {len(all_events)}")
    print(f"People:  {people_data['total']}")
    print(f"Hacks:   {len(all_hacks)}")
    print(f"Talks:   {len(all_talks)}")
    print(f"Base URL: {API_BASE}")
    print(f"Generated at: {NOW}")


if __name__ == '__main__':
    main()
