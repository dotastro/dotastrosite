#!/usr/bin/env python3
"""Generate assets/js/search-index.json from _data/events/*.yml and Markdown files.

Reads structured event data from _data/ (single source of truth) and also
indexes other site pages from their markdown source.

Run from the repo root: python3 generate-search-index.py
"""
import os, re, json, glob, yaml

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_EVENTS_DIR = os.path.join(BASE, '_data', 'events')
EVENT_META_PATH = os.path.join(BASE, '_data', 'event_meta.yml')
BASEURL = ''  # empty for custom domain


def strip_md(text):
    text = re.sub(r'---.*?---', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'[#*`_>|]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_title(text, filepath):
    m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    m = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return os.path.basename(filepath)


def section_label(filepath):
    parts = filepath.replace(BASE + '/', '').split('/')
    return ' / '.join(parts[:-1]).replace('_', ' ').title() or 'Site'


def index_events():
    """Index structured event data from _data/events/*.yml."""
    docs = []

    if not os.path.exists(EVENT_META_PATH):
        return docs

    with open(EVENT_META_PATH) as f:
        meta = yaml.safe_load(f)

    for entry in meta['events']:
        slug = entry['slug']
        path = os.path.join(DATA_EVENTS_DIR, f'{slug}.yml')
        if not os.path.exists(path):
            continue

        with open(path) as f:
            event = yaml.safe_load(f)

        url = f'{BASEURL}/events/{slug}/'
        section = f"{event.get('name', '')} -- {event.get('city', '')} {event.get('year', '')}"

        # Main event page
        body_parts = [
            event.get('name', ''),
            event.get('city', ''),
            str(event.get('year', '')),
            event.get('venue', ''),
            event.get('description', ''),
        ]

        # Add organiser names
        for org in event.get('organisers', []):
            body_parts.append(org.get('name', ''))
            if org.get('affiliation'):
                body_parts.append(org['affiliation'])

        # Add participant names
        for p in event.get('participants', []):
            body_parts.append(p.get('name', ''))
            if p.get('affiliation'):
                body_parts.append(p['affiliation'])

        # Add talk info
        for talk in event.get('talks', []):
            body_parts.append(talk.get('speaker', ''))
            if talk.get('title'):
                body_parts.append(talk['title'])
            if talk.get('notes'):
                body_parts.append(talk['notes'])
            if talk.get('affiliation'):
                body_parts.append(talk['affiliation'])

        body = ' '.join(filter(None, body_parts))[:5000]

        docs.append({
            'title': f"{event.get('name', '')} -- {event.get('city', '')} ({event.get('year', '')})",
            'url': url,
            'section': section,
            'body': body,
        })

        # Individual hacks as separate docs
        for hack in event.get('hacks', []):
            hack_body = ' '.join(filter(None, [
                hack.get('title', ''),
                ', '.join(hack.get('creators', [])),
                hack.get('description', ''),
            ]))
            docs.append({
                'title': hack.get('title', ''),
                'url': url,
                'section': f"{section} / Hack",
                'body': hack_body,
            })

    return docs


def index_pages():
    """Index non-event pages from markdown files."""
    docs = []
    patterns = [
        '*.md', 'community/*.md', 'foundation/*.md',
    ]
    seen_urls = set()

    for pattern in patterns:
        for fpath in glob.glob(os.path.join(BASE, pattern)):
            rel = fpath.replace(BASE + '/', '')
            if rel.startswith('CONTRIBUTING') or rel.startswith('README') or rel.startswith('generate'):
                continue
            with open(fpath) as f:
                raw = f.read()
            title = get_title(raw, fpath)
            body = strip_md(raw)
            if len(body) < 30:
                continue
            url_path = rel.replace('.md', '.html')
            if url_path.endswith('index.html'):
                url_path = url_path[:-len('index.html')]
            url = BASEURL + '/' + url_path
            if url in seen_urls:
                continue
            seen_urls.add(url)
            docs.append({
                'title': title,
                'url': url,
                'section': section_label(fpath),
                'body': body[:5000],
            })

    return docs


def main():
    docs = []

    # Index events from _data/ (single source of truth)
    event_docs = index_events()
    docs.extend(event_docs)
    print(f"Indexed {len(event_docs)} event documents (including hacks)")

    # Index other pages
    page_docs = index_pages()
    docs.extend(page_docs)
    print(f"Indexed {len(page_docs)} other pages")

    out = os.path.join(BASE, 'assets/js/search-index.json')
    with open(out, 'w') as f:
        json.dump(docs, f)
    print(f"Written {len(docs)} total docs to {out}")


if __name__ == '__main__':
    main()
