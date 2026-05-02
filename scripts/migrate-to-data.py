#!/usr/bin/env python3
"""
Migrate all event data from events/SLUG/index.md to _data/events/SLUG.yml
and create _data/event_meta.yml.

Reads:
  - events/SLUG/index.md (all event pages)
  - assets/js/bluesky-cache.json (Bluesky handles)
  - api/v1/hacks.json (enriched hack data)

Writes:
  - _data/events/SLUG.yml (one per event)
  - _data/event_meta.yml (master list)
"""

import os, re, json, sys
import yaml

# Prevent YAML from wrapping long lines
yaml.Dumper.ignore_aliases = lambda *args: True

class LiteralStr(str):
    pass

def literal_str_representer(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(LiteralStr, literal_str_representer)

# Custom representer for regular strings - use double quotes only when needed
def str_representer(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    # Check if the string needs quoting
    if any(c in data for c in [':', '#', '{', '}', '[', ']', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`']):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
    if data.lower() in ('true', 'false', 'null', 'yes', 'no', 'on', 'off'):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
    if data == '' or data.startswith(' ') or data.endswith(' '):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
    try:
        float(data)
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
    except ValueError:
        pass
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_representer)

# None should be empty string
def none_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:null', '')

yaml.add_representer(type(None), none_representer)


BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_DIR = os.path.join(BASE, 'events')
DATA_DIR = os.path.join(BASE, '_data')
DATA_EVENTS_DIR = os.path.join(DATA_DIR, 'events')
BSKY_CACHE = os.path.join(BASE, 'assets', 'js', 'bluesky-cache.json')
HACKS_JSON = os.path.join(BASE, 'api', 'v1', 'hacks.json')

EVENT_SLUGS = [
    'one', 'two', 'three', 'four', 'five', 'six', 'seven',
    'eight', 'nine', 'ten', 'eleven', 'alpha', 'twelve', 'thirteen'
]

EVENT_META = {
    'one':      {'number': '1',   'name': '.Astronomy 1',  'year': 2008, 'city': 'Cardiff',       'country': 'United Kingdom'},
    'two':      {'number': '2',   'name': '.Astronomy 2',  'year': 2009, 'city': 'Leiden',        'country': 'Netherlands'},
    'three':    {'number': '3',   'name': '.Astronomy 3',  'year': 2011, 'city': 'Oxford',        'country': 'United Kingdom'},
    'four':     {'number': '4',   'name': '.Astronomy 4',  'year': 2012, 'city': 'Heidelberg',    'country': 'Germany'},
    'five':     {'number': '5',   'name': '.Astronomy 5',  'year': 2013, 'city': 'Cambridge, MA', 'country': 'United States'},
    'six':      {'number': '6',   'name': '.Astronomy 6',  'year': 2014, 'city': 'Chicago',       'country': 'United States'},
    'seven':    {'number': '7',   'name': '.Astronomy 7',  'year': 2015, 'city': 'Sydney',        'country': 'Australia'},
    'eight':    {'number': '8',   'name': '.Astronomy 8',  'year': 2016, 'city': 'Oxford',        'country': 'United Kingdom'},
    'nine':     {'number': '9',   'name': '.Astronomy 9',  'year': 2017, 'city': 'Cape Town',     'country': 'South Africa'},
    'ten':      {'number': 'X',   'name': '.Astronomy X',  'year': 2018, 'city': 'Baltimore',     'country': 'United States'},
    'eleven':   {'number': '11',  'name': '.Astronomy 11', 'year': 2019, 'city': 'Toronto',       'country': 'Canada'},
    'alpha':    {'number': '\u03b1','name': '.Astronomy \u03b1','year': 2020,'city': 'Online',     'country': 'Online'},
    'twelve':   {'number': '12',  'name': '.Astronomy 12', 'year': 2023, 'city': 'New York',      'country': 'United States'},
    'thirteen': {'number': '13',  'name': '.Astronomy 13', 'year': 2024, 'city': 'Madrid',        'country': 'Spain'},
}


def load_bsky_cache():
    """Load the Bluesky cache and return the 'found' dict."""
    if os.path.exists(BSKY_CACHE):
        with open(BSKY_CACHE) as f:
            data = json.load(f)
        return data.get('found', {})
    return {}


def load_hacks_json():
    """Load enriched hacks from api/v1/hacks.json, keyed by (event, title)."""
    if not os.path.exists(HACKS_JSON):
        return {}
    with open(HACKS_JSON) as f:
        data = json.load(f)
    hacks = data.get('hacks', [])
    lookup = {}
    for h in hacks:
        key = (h.get('event', ''), h.get('title', ''))
        lookup[key] = h
    return lookup


def get_bsky(name, bsky_cache):
    """Look up Bluesky handle for a name."""
    lower = name.lower().strip()
    return bsky_cache.get(lower, None)


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_venue_dates(content):
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


def extract_description(content):
    """Extract the event description from the hero section."""
    desc_match = re.search(r'<p class="event-page-desc">(.*?)</p>', content, re.DOTALL)
    if desc_match:
        desc = desc_match.group(1).strip()
        # Clean HTML tags
        desc = re.sub(r'<[^>]+>', '', desc)
        return desc.strip()
    return ''


def extract_organisers(content, bsky_cache):
    """Extract organisers from the Organisers section."""
    organisers = []
    # Find the section
    org_match = re.search(r'## Organisers.*?\n(.*?)(?=\n<span class="section-label">|\n## [A-Z]|\nSupported by|\nOrganising committee)', content, re.DOTALL)
    if not org_match:
        org_match = re.search(r'## Organisers.*?\n(.*?)(?=\n<span|\n##)', content, re.DOTALL)
    if not org_match:
        return organisers, ''

    full_text = org_match.group(1).strip()
    extra_notes = ''

    lines = full_text.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('- '):
            line = line[2:].strip()
            aff_match = re.match(r'(.+?)\s*\(([^)]+)\)', line)
            if aff_match:
                name = aff_match.group(1).strip()
                affiliation = aff_match.group(2).strip()
            else:
                name = line.strip()
                affiliation = None
            bsky = get_bsky(name, bsky_cache)
            org = {'name': name}
            if affiliation:
                org['affiliation'] = affiliation
            if bsky:
                org['bluesky'] = bsky
            organisers.append(org)
        elif line and not line.startswith('#') and not line.startswith('<'):
            # Extra text like "Organising committee also included..."
            if extra_notes:
                extra_notes += '\n' + line
            else:
                extra_notes = line

    return organisers, extra_notes


def extract_talks_section(content):
    """Get the full talks section text."""
    # Find talks section
    talks_section = re.search(r'## Talks \{#talks\}(.*?)(?=\n<span class="section-label">|\n## [A-Z](?!#))', content, re.DOTALL)
    if not talks_section:
        talks_section = re.search(r'## Talks \{#talks\}(.*?)(?=\n##\s(?!#))', content, re.DOTALL)
    if not talks_section:
        # Try without anchor
        talks_section = re.search(r'## Talks\s*\n(.*?)(?=\n<span class="section-label">|\n## [A-Z])', content, re.DOTALL)
    if talks_section:
        return talks_section.group(1)
    return ''


def parse_talks(section_text, slug):
    """Parse talks from the talks section text. Returns list of talk dicts and extra narrative text."""
    talks = []
    extra_narrative = []
    current_type = 'talk'
    current_heading = ''

    lines = section_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Skip schedule file links
        if '<a href=' in line and ('schedule' in line.lower() or 'btn btn-outline' in line):
            i += 1
            continue

        # Detect headings for talk type
        if line.startswith('### '):
            heading = line[4:].strip()
            current_heading = heading
            lower_heading = heading.lower()

            if any(k in lower_heading for k in ['invited', 'keynote']):
                current_type = 'invited'
            elif 'lightning' in lower_heading:
                current_type = 'lightning'
            elif 'day zero' in lower_heading or 'day 0' in lower_heading or 'tutorial' in lower_heading:
                current_type = 'day_zero'
            elif 'unconference' in lower_heading:
                current_type = 'unconference'
            elif 'contributed' in lower_heading:
                current_type = 'contributed'
            elif 'pre-dinner' in lower_heading:
                current_type = 'talk'
            elif 'public' in lower_heading:
                current_type = 'talk'
            elif any(k in lower_heading for k in ['highlight', 'theme', 'notable', 'proceeding', 'sponsor', 'official', 'opening']):
                current_type = None  # narrative text, not talks
            elif any(k in lower_heading for k in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'day 1', 'day 2', 'day 3']):
                current_type = 'talk'
            elif any(k in lower_heading for k in ['remote', 'skype']):
                current_type = 'remote'
            else:
                current_type = 'talk'
            i += 1
            continue

        # If current type is None (narrative sections), collect as extra text
        if current_type is None:
            extra_narrative.append(line)
            i += 1
            continue

        # Parse talk lines
        if line.startswith('- **') or line.startswith('**'):
            raw_line = line
            if line.startswith('- '):
                line = line[2:]

            # Parse: **Speaker** (Affiliation): *Title* -- notes
            # or **Speaker**: *Title*
            talk_match = re.match(
                r'\*\*(.+?)\*\*\s*(?:\(([^)]*)\))?\s*:?\s*(.*)',
                line
            )
            if talk_match:
                speaker = talk_match.group(1).strip()
                affiliation = talk_match.group(2)
                remainder = talk_match.group(3).strip() if talk_match.group(3) else ''

                # Clean up speaker (remove Twitter handles from name)
                speaker = re.sub(r'\s*\(@\w+\)', '', speaker).strip()

                if affiliation:
                    affiliation = affiliation.strip()
                    # Remove Twitter handles
                    affiliation = re.sub(r',?\s*@\w+', '', affiliation).strip()
                    affiliation = affiliation.rstrip(',').strip()

                # Parse title from remainder
                title = ''
                notes = ''

                if remainder:
                    # Remove leading colon
                    remainder = remainder.lstrip(':').strip()

                    # Check for italicised title: *Title*
                    title_match = re.match(r'\*([^*]+)\*\s*(.*)', remainder)
                    if title_match:
                        title = title_match.group(1).strip()
                        notes = title_match.group(2).strip()
                    else:
                        # Not italicised, whole thing might be title or notes
                        # Check if it starts with a common non-title pattern
                        if remainder.lower().startswith('talk') or remainder.lower().startswith('('):
                            notes = remainder
                        else:
                            title = remainder
                            notes = ''

                # Clean up title
                if title:
                    title = title.rstrip('.')
                    # Clean markdown links
                    title = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', title)
                    # Clean HTML tags
                    title = re.sub(r'<[^>]+>', '', title)
                    title = title.strip()

                # Clean up notes (remove leading --)
                if notes:
                    notes = re.sub(r'^--\s*', '', notes).strip()
                    notes = re.sub(r'<[^>]+>', '', notes)  # clean HTML
                    notes = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', notes)  # clean links
                    # Collect continuation lines
                    while i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and not next_line.startswith('- ') and not next_line.startswith('**') and not next_line.startswith('###') and not next_line.startswith('<'):
                            notes += ' ' + next_line
                            i += 1
                        else:
                            break

                talk = {
                    'speaker': speaker,
                    'type': current_type,
                }
                if affiliation:
                    talk['affiliation'] = affiliation
                if title:
                    talk['title'] = title
                if notes:
                    talk['notes'] = notes.strip()

                talks.append(talk)

        elif line.startswith('- ') and current_type == 'unconference':
            # Unconference session lines
            text = line[2:].strip()
            talks.append({
                'speaker': '',
                'type': 'unconference',
                'title': text,
            })

        elif line.startswith('- ') and current_type == 'day_zero':
            # Day zero contributor/tutorial lines
            text = line[2:].strip()
            # Check if it's a **Name**: Description format
            dz_match = re.match(r'\*\*(.+?)\*\*\s*(?:\(([^)]*)\))?\s*:?\s*(.*)', text)
            if dz_match:
                speaker = dz_match.group(1).strip()
                aff = dz_match.group(2)
                desc = dz_match.group(3).strip() if dz_match.group(3) else ''
                talk = {
                    'speaker': speaker,
                    'type': 'day_zero',
                }
                if aff:
                    talk['affiliation'] = aff.strip()
                if desc:
                    talk['title'] = desc.lstrip(':').strip()
                talks.append(talk)
            else:
                talks.append({
                    'speaker': '',
                    'type': 'day_zero',
                    'title': text,
                })

        else:
            # Narrative text within the talks section
            if line and not line.startswith('<') and not line.startswith('{'):
                extra_narrative.append(line)

        i += 1

    return talks, '\n'.join(extra_narrative).strip()


def extract_hacks(content, slug, hacks_lookup):
    """Extract hacks from hack-card divs, enriched with api/v1/hacks.json data."""
    hacks = []

    # Split by hack-card divs and properly handle nesting
    parts = re.split(r'<div class="hack-card">', content)
    cards = []
    for part in parts[1:]:  # Skip before first hack-card
        # Track div depth to find the closing </div> of the hack-card
        depth = 1
        pos = 0
        while pos < len(part) and depth > 0:
            next_open = re.search(r'<div[^>]*>', part[pos:])
            next_close = re.search(r'</div>', part[pos:])
            if next_close is None:
                break
            if next_open and next_open.start() < next_close.start():
                depth += 1
                pos += next_open.end()
            else:
                depth -= 1
                pos += next_close.end()
        cards.append(part[:pos])

    for card in cards:
        # Title - may contain a link
        title_match = re.search(r'<div class="hack-title">(.*?)</div>', card, re.DOTALL)
        if not title_match:
            continue
        title_html = title_match.group(1).strip()
        # Extract title text (remove links but capture URL)
        title_link = None
        link_match = re.search(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', title_html)
        if link_match:
            title_link = link_match.group(1)
            title = link_match.group(2).strip()
        else:
            title = title_html.strip()
            title = re.sub(r'<[^>]+>', '', title).strip()

        if not title:
            continue

        # Creators
        creators_match = re.search(r'<div class="hack-creators">(.*?)</div>', card, re.DOTALL)
        creators = []
        if creators_match:
            creators_text = creators_match.group(1).strip()
            creators_text = re.sub(r'\s*\(@\w+\)', '', creators_text)  # remove Twitter handles
            creators_text = re.sub(r'<[^>]+>', '', creators_text)  # remove HTML
            parts = re.split(r',\s*|\s+and\s+', creators_text)
            creators = [c.strip() for c in parts if c.strip()]

        # Description
        desc_match = re.search(r'<(?:div|p) class="hack-desc"[^>]*>(.*?)</(?:div|p)>', card, re.DOTALL)
        description = ''
        if desc_match:
            description = desc_match.group(1).strip()
            description = re.sub(r'<[^>]+>', '', description).strip()

        # Links
        source_url = None
        live_url = None
        links_match = re.search(r'<div class="hack-links">(.*?)</div>', card, re.DOTALL)
        if links_match:
            links_html = links_match.group(1)
            all_links = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', links_html, re.DOTALL)
            for url, label in all_links:
                label_lower = label.strip().lower()
                if any(k in label_lower for k in ['source', 'github']):
                    source_url = url
                elif any(k in label_lower for k in ['live', 'install', 'watch', 'listen', 'download']):
                    live_url = url
                elif 'more info' in label_lower:
                    live_url = url
                elif not source_url and 'github.com' in url:
                    source_url = url
                elif not live_url and label_lower not in ['source', 'github']:
                    live_url = url

        # Enrich from hacks.json
        api_key = (slug, title)
        api_hack = hacks_lookup.get(api_key, {})
        if not description and api_hack.get('description'):
            description = api_hack['description']
        if not source_url and api_hack.get('source_url'):
            source_url = api_hack['source_url']
        if not live_url and api_hack.get('live_url'):
            live_url = api_hack['live_url']

        hack = {
            'title': title,
            'creators': creators,
        }
        if description:
            hack['description'] = description
        if source_url:
            hack['source_url'] = source_url
        if live_url:
            hack['live_url'] = live_url

        hacks.append(hack)

    return hacks


def extract_participants(content, bsky_cache):
    """Extract participants from the Participants section."""
    participants = []

    # Find section
    parts_section = re.search(r'## Participants.*?\n(.*?)(?=\n<span class="section-label">|\n## [A-Z]|\n<div class="contribute|\Z)', content, re.DOTALL)
    if not parts_section:
        return participants

    section_text = parts_section.group(1)

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

        if not name:
            continue

        # Clean HTML from name
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
        bsky = get_bsky(name, bsky_cache)
        if bsky:
            p['bluesky'] = bsky
        participants.append(p)

    return participants


def extract_links(content):
    """Extract links from the Links section."""
    links = []
    links_section = re.search(r'## Links \{#links\}(.*?)(?=\n<div class="contribute|\n##\s|\n### Sponsors|\Z)', content, re.DOTALL)
    if not links_section:
        return links, ''

    section_text = links_section.group(1)
    sponsor_text = ''

    for match in re.finditer(r'-\s*\[([^\]]+)\]\(([^)]+)\)(?:\s*:\s*(.*))?', section_text):
        label = match.group(1).strip()
        url = match.group(2).strip()
        desc = match.group(3).strip() if match.group(3) else None
        if '{{ site.baseurl }}' in url:
            url = url.replace('{{ site.baseurl }}', '')
            link = {'label': label, 'url': url, 'internal': True}
        else:
            link = {'label': label, 'url': url}
        if desc:
            link['description'] = desc
        links.append(link)

    # Check for sponsors
    sponsor_match = re.search(r'### Sponsors\s*\n(.*?)(?=\n<div|\n##|\Z)', content, re.DOTALL)
    if sponsor_match:
        sponsor_text = sponsor_match.group(1).strip()

    return links, sponsor_text


def extract_extra_sections(content, slug):
    """Extract any additional content not captured by standard sections."""
    extra = {}

    # Unproceedings
    unproc_match = re.search(r'## Unproceedings.*?\n(.*?)(?=\n<span class="section-label">|\n## [A-Z]|\n<a href)', content, re.DOTALL)
    if unproc_match:
        text = unproc_match.group(1).strip()
        text = re.sub(r'<[^>]+>', '', text).strip()
        extra['unproceedings'] = text

    # Unproceedings authors and link
    unproc_authors = re.search(r'\*\*Authors:\*\*\s*(.*)', content)
    if unproc_authors:
        extra['unproceedings_authors'] = unproc_authors.group(1).strip()

    unproc_link = re.search(r'<a href="(https://arxiv\.org/abs/[^"]+)"', content)
    if unproc_link:
        extra['unproceedings_arxiv'] = unproc_link.group(1)

    # Programme notes (separate from talks)
    prog_match = re.search(r'## Programme \{#programme\}\s*\n(.*?)(?=\n<span class="section-label">|\n## [A-Z])', content, re.DOTALL)
    if prog_match:
        text = prog_match.group(1).strip()
        text = re.sub(r'<[^>]+>', '', text).strip()
        extra['programme_notes'] = text

    # Community posts
    community_posts = []
    for match in re.finditer(r'<div class="community-post">(.*?)</div>\s*</div>', content, re.DOTALL):
        post_html = match.group(1)
        text_match = re.search(r'<div class="cp-text">(.*?)</div>', post_html, re.DOTALL)
        author_match = re.search(r'<span class="cp-author">(.*?)</span>', post_html)
        date_match = re.search(r'<span class="cp-date">(.*?)</span>', post_html)
        source_match = re.search(r'<span class="cp-source">(.*?)</span>', post_html)
        link_match = re.search(r'<a href="([^"]*)" class="cp-link"', post_html)

        if text_match:
            post = {
                'text': text_match.group(1).strip(),
            }
            if author_match:
                post['author'] = author_match.group(1).strip()
            if date_match:
                post['date'] = date_match.group(1).strip()
            if source_match:
                post['source'] = source_match.group(1).strip()
            if link_match:
                post['url'] = link_match.group(1).strip()
            community_posts.append(post)

    if community_posts:
        extra['community_posts'] = community_posts

    # Sponsor text
    sponsor_match = re.search(r'### Sponsors\s*\n(.*?)(?=\n<div|\n##|\Z)', content, re.DOTALL)
    if sponsor_match:
        text = sponsor_match.group(1).strip()
        text = re.sub(r'<[^>]+>', '', text).strip()
        if text:
            extra['sponsors'] = text

    # Support notes from organisers section
    support_match = re.search(r'(?:Supported by|Organising committee also included)\s+(.*?)(?:\n\n|\n<|\n##)', content, re.DOTALL)
    if support_match:
        extra['organisers_notes'] = support_match.group(0).strip()

    return extra


def extract_schedule_links(content):
    """Extract schedule PDF/XLSX links."""
    links = []
    for match in re.finditer(r'<a href="([^"]*)"[^>]*>(?:Full )?[Ss]chedule \(([^)]+)\)</a>', content):
        url = match.group(1).replace('{{ site.baseurl }}', '')
        fmt = match.group(2)
        links.append({'url': url, 'format': fmt})
    return links


def process_event(slug, bsky_cache, hacks_lookup):
    """Process a single event and return its YAML data dict."""
    md_path = os.path.join(EVENTS_DIR, slug, 'index.md')
    if not os.path.exists(md_path):
        print(f"  WARNING: {md_path} not found")
        return None

    content = read_file(md_path)
    meta = EVENT_META[slug]

    dates, venue = extract_venue_dates(content)
    description = extract_description(content)
    organisers, org_notes = extract_organisers(content, bsky_cache)

    talks_text = extract_talks_section(content)
    talks, talks_narrative = parse_talks(talks_text, slug)

    hacks = extract_hacks(content, slug, hacks_lookup)
    participants = extract_participants(content, bsky_cache)
    links, sponsor_text = extract_links(content)
    schedule_links = extract_schedule_links(content)
    extras = extract_extra_sections(content, slug)

    event = {
        'slug': slug,
        'number': meta['number'],
        'name': meta['name'],
        'year': meta['year'],
        'city': meta['city'],
        'country': meta['country'],
        'venue': venue,
        'dates': dates,
        'description': description,
    }

    if schedule_links:
        event['schedule'] = schedule_links

    event['organisers'] = organisers
    if org_notes:
        event['organisers_notes'] = org_notes

    event['talks'] = talks
    if talks_narrative:
        event['talks_narrative'] = talks_narrative

    event['hacks'] = hacks
    event['participants'] = participants
    event['links'] = links

    # Merge extras
    for key, val in extras.items():
        if key not in event:
            event[key] = val

    return event


def write_yaml(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, width=120, sort_keys=False)
    print(f"  Wrote {path}")


def main():
    print("=== .Astronomy Data Migration ===\n")

    # Load enrichment data
    bsky_cache = load_bsky_cache()
    print(f"Loaded {len(bsky_cache)} Bluesky handles from cache")

    hacks_lookup = load_hacks_json()
    print(f"Loaded {len(hacks_lookup)} hacks from API JSON\n")

    # Create output directories
    os.makedirs(DATA_EVENTS_DIR, exist_ok=True)

    # Process all events
    event_meta_list = []
    total_talks = 0
    total_hacks = 0
    total_participants = 0
    issues = []

    for slug in EVENT_SLUGS:
        print(f"Processing {slug}...")
        event = process_event(slug, bsky_cache, hacks_lookup)
        if not event:
            issues.append(f"{slug}: could not read event page")
            continue

        # Write event YAML
        write_yaml(os.path.join(DATA_EVENTS_DIR, f'{slug}.yml'), event)

        # Collect meta
        meta_entry = {
            'slug': slug,
            'number': event['number'],
            'name': event['name'],
            'year': event['year'],
            'city': event['city'],
            'country': event['country'],
            'venue': event['venue'],
            'dates': event['dates'],
        }
        event_meta_list.append(meta_entry)

        n_talks = len(event.get('talks', []))
        n_hacks = len(event.get('hacks', []))
        n_parts = len(event.get('participants', []))
        total_talks += n_talks
        total_hacks += n_hacks
        total_participants += n_parts
        print(f"  {n_talks} talks, {n_hacks} hacks, {n_parts} participants")

    # Write event_meta.yml
    write_yaml(os.path.join(DATA_DIR, 'event_meta.yml'), {'events': event_meta_list})

    # Summary
    print(f"\n=== Migration Summary ===")
    print(f"Events migrated: {len(event_meta_list)}")
    print(f"Total talks:     {total_talks}")
    print(f"Total hacks:     {total_hacks}")
    print(f"Total participants: {total_participants}")

    if issues:
        print(f"\nIssues ({len(issues)}):")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\nNo issues detected.")

    print("\nDone! Files written to _data/events/ and _data/event_meta.yml")


if __name__ == '__main__':
    main()
