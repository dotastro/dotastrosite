#!/usr/bin/env python3
"""Generate assets/js/search-index.json from all Markdown files.
Run from the repo root: python3 generate-search-index.py
"""
import os, re, json, glob

BASE = os.path.dirname(os.path.abspath(__file__))
BASEURL = '/dotastrosite'

def strip_md(text):
    text = re.sub(r'---.*?---', '', text, flags=re.DOTALL)  # frontmatter
    text = re.sub(r'<[^>]+>', ' ', text)                    # HTML tags
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)   # links
    text = re.sub(r'[#*`_>|]+', ' ', text)                 # markdown
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_title(text, filepath):
    m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', text, re.MULTILINE)
    if m: return m.group(1).strip()
    m = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    if m: return m.group(1).strip()
    return os.path.basename(filepath)

def section_label(filepath):
    parts = filepath.replace(BASE + '/', '').split('/')
    if 'events' in parts:
        idx = parts.index('events')
        if len(parts) > idx + 1:
            evdir = parts[idx + 1]
            # e.g. dotastro8_oxford_2016 -> .Astronomy 8 Oxford
            m = re.match(r'dotastro(\d+|_alpha|_x)_(\w+)_(\d+)', evdir)
            if m:
                num = m.group(1).replace('_alpha', 'α')
                city = m.group(2).title()
                year = m.group(3)
                return f'.Astronomy {num} — {city} {year}'
    return ' / '.join(parts[:-1]).replace('_', ' ').title() or 'Site'

docs = []
patterns = [
    '*.md', 'events/*/*.md', 'community/*.md',
    'foundation/*.md', 'about.md', 'brain-trust.md', 'nominate.md',
]

seen_urls = set()
for pattern in patterns:
    for fpath in glob.glob(os.path.join(BASE, pattern)):
        rel = fpath.replace(BASE + '/', '')
        # Skip files we don't want indexed
        if rel.startswith('CONTRIBUTING') or rel.startswith('README') or rel.startswith('generate'):
            continue
        with open(fpath) as f:
            raw = f.read()
        title = get_title(raw, fpath)
        body = strip_md(raw)
        if len(body) < 30:
            continue
        # Build URL
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
            'body': body[:2000],
        })

out = os.path.join(BASE, 'assets/js/search-index.json')
with open(out, 'w') as f:
    json.dump(docs, f)
print(f"Written {len(docs)} docs to {out}")
