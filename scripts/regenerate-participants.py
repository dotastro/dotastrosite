#!/usr/bin/env python3
"""Regenerate participants-data.json and run incremental Bluesky lookup.

Usage:
  python3 scripts/regenerate-participants.py           # rebuild + Bluesky lookup
  python3 scripts/regenerate-participants.py --no-bsky # rebuild only, skip Bluesky
"""

import os, re, json, sys, time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_DIR = os.path.join(BASE, 'events')
OUT = os.path.join(BASE, 'assets/js/participants-data.json')
BSKY_CACHE = os.path.join(BASE, 'assets/js/bluesky-cache.json')
SKIP_BSKY = '--no-bsky' in sys.argv

# Known Bluesky handles (ground truth, never overwritten by search)
KNOWN_BSKY = {
    'robert simpson': 'orbitingfrog.bsky.social',
    'rob simpson': 'orbitingfrog.bsky.social',
    'chris lintott': 'chrislintott.bsky.social',
    'sarah kendrew': 'sarahkendrew.bsky.social',
    'amanda bauer': 'amandabauer.bsky.social',
    'alasdair allan': 'alasdairallan.com',
    'becky smethurst': 'drbecky.bsky.social',
    'arfon smith': 'arfon.bsky.social',
    'phil plait': 'philplait.bsky.social',
    'emily lakdawalla': 'elakdawalla.bsky.social',
    'alyssa goodman': 'alyssagoodman.bsky.social',
    'jane rigby': 'janerigby.bsky.social',
    'jessie christiansen': 'aussiastronomer.bsky.social',
    'geert barentsen': 'geert.bsky.social',
    'emily hunt': 'emilyhunt.bsky.social',
    'meg schwamb': 'megschwamb.bsky.social',
    'katie mack': 'astrokatie.com',
}

ASTRO_KEYWORDS = {
    'astronomer','astrophysics','astrophysicist','telescope','galaxy','galaxies',
    'nasa','esa','stsci','zooniverse','astropy','mpi','observatory','planetarium',
    'cosmology','cosmologist','exoplanet','stellar','solar','meerkat','ska',
    'lsst','rubin','hubble','jwst','fermilab','caltech','mit','cambridge','oxford',
    'heidelberg','cape town','saao','dunlap','university','institute','postdoc',
    'phd','professor','researcher','scientist','science','data science',
}

def load_bsky_cache():
    if os.path.exists(BSKY_CACHE):
        with open(BSKY_CACHE) as f:
            return json.load(f)
    return {'searched': {}, 'found': {}}

def save_bsky_cache(cache):
    with open(BSKY_CACHE, 'w') as f:
        json.dump(cache, f, indent=2)

def search_bluesky(name):
    """Search Bluesky for a person. Returns handle string or None."""
    try:
        import urllib.request, urllib.parse
        url = 'https://public.api.bsky.app/xrpc/app.bsky.actor.searchActors?q=' + urllib.parse.quote(name) + '&limit=8'
        req = urllib.request.Request(url, headers={'User-Agent': 'dotastro-archive/1.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        actors = data.get('actors', [])
        name_lower = name.lower()
        name_parts = set(name_lower.split())
        for actor in actors:
            display = (actor.get('displayName') or '').lower()
            handle = (actor.get('handle') or '').lower()
            bio = (actor.get('description') or '').lower()
            # Name must match closely
            display_parts = set(display.split())
            if not name_parts.issubset(display_parts) and not display_parts.issubset(name_parts):
                # Try partial: at least first+last name match
                name_words = name_lower.split()
                if len(name_words) >= 2:
                    if not (name_words[0] in display and name_words[-1] in display):
                        continue
            # Bio must suggest astronomy
            if not any(kw in bio for kw in ASTRO_KEYWORDS):
                continue
            return actor.get('handle')
    except Exception:
        pass
    return None

event_map = {
    'one':     {'num': '1',  'name': '.Astronomy 1',  'year': 2008, 'city': 'Cardiff'},
    'two':     {'num': '2',  'name': '.Astronomy 2',  'year': 2009, 'city': 'Leiden'},
    'three':   {'num': '3',  'name': '.Astronomy 3',  'year': 2011, 'city': 'Oxford'},
    'four':    {'num': '4',  'name': '.Astronomy 4',  'year': 2012, 'city': 'Heidelberg'},
    'five':    {'num': '5',  'name': '.Astronomy 5',  'year': 2013, 'city': 'Cambridge MA'},
    'six':     {'num': '6',  'name': '.Astronomy 6',  'year': 2014, 'city': 'Chicago'},
    'seven':   {'num': '7',  'name': '.Astronomy 7',  'year': 2015, 'city': 'Sydney'},
    'eight':   {'num': '8',  'name': '.Astronomy 8',  'year': 2016, 'city': 'Oxford'},
    'nine':    {'num': '9',  'name': '.Astronomy 9',  'year': 2017, 'city': 'Cape Town'},
    'ten':     {'num': 'X',  'name': '.Astronomy X',  'year': 2018, 'city': 'Baltimore'},
    'eleven':  {'num': '11', 'name': '.Astronomy 11', 'year': 2019, 'city': 'Toronto'},
    'alpha':   {'num': 'α',  'name': '.Astronomy α',  'year': 2020, 'city': 'Online'},
    'twelve':  {'num': '12', 'name': '.Astronomy 12', 'year': 2023, 'city': 'New York'},
    'thirteen':{'num': '13', 'name': '.Astronomy 13', 'year': 2024, 'city': 'Madrid'},
}

all_people = {}

def add_person(name, affiliation, event_dir, role):
    if not name or len(name) < 3 or name.startswith('http'):
        return
    key = name.lower().strip()
    if key not in all_people:
        all_people[key] = {
            'name': name,
            'affiliations': {},   # event_dir -> affiliation string
            'events': [],
            'roles': {},
        }
    if event_dir not in all_people[key]['events']:
        all_people[key]['events'].append(event_dir)
    roles = all_people[key]['roles'].get(event_dir, [])
    if role not in roles:
        roles.append(role)
    all_people[key]['roles'][event_dir] = roles
    # Store affiliation per event (if provided)
    if affiliation:
        all_people[key]['affiliations'][event_dir] = affiliation

event_map_order = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','alpha','twelve','thirteen']

for dirname in event_map:
    fpath = os.path.join(EVENTS_DIR, dirname, 'index.md')
    if not os.path.exists(fpath):
        continue
    with open(fpath) as f:
        text = f.read()

    # Participants -- handle both markdown bullets and <li> tags
    in_sec = False
    for line in text.split('\n'):
        if '## Participants' in line or '// participants' in line:
            in_sec = True
            continue
        if in_sec and re.match(r'^## ', line) and 'participant' not in line.lower():
            in_sec = False
        if not in_sec:
            continue
        raw = None
        # Markdown bullet
        if line.strip().startswith('- ') and '<' not in line:
            raw = line.strip()[2:].strip()
        # HTML <li> tag
        li_m = re.match(r'\s*<li>([^<]+)</li>', line)
        if li_m:
            raw = li_m.group(1).strip()
        if raw:
            name = re.split(r'\s*[\(\[]', raw)[0].strip()
            aff_m = re.search(r'\(([^)]+)\)', raw)
            aff = aff_m.group(1) if aff_m else ''
            add_person(name, aff, dirname, 'attendee')

    # Organisers
    in_org = False
    for line in text.split('\n'):
        if '## Organisers' in line or '// organisers' in line:
            in_org = True
            continue
        if in_org and re.match(r'^## ', line) and 'organis' not in line.lower():
            in_org = False
        if not in_org:
            continue
        raw = None
        if line.strip().startswith('- ') and '<' not in line:
            raw = line.strip()[2:].strip()
        li_m = re.match(r'\s*<li>([^<]+)</li>', line)
        if li_m:
            raw = li_m.group(1).strip()
        if raw:
            name = re.split(r'\s*[\(\[]', raw)[0].strip()
            aff_m = re.search(r'\(([^)]+)\)', raw)
            aff = aff_m.group(1) if aff_m else ''
            add_person(name, aff, dirname, 'organiser')

    # Speakers (from **Name** in talks sections)
    in_talks = False
    for line in text.split('\n'):
        if '## Talks' in line or '// talks' in line:
            in_talks = True
            continue
        if in_talks and re.match(r'^## ', line) and 'talk' not in line.lower():
            in_talks = False
        if in_talks:
            m = re.match(r'^[-*]\s+\*\*([^*]+)\*\*', line)
            if m:
                name = re.sub(r'\s*\(invited\)', '', m.group(1), flags=re.I).strip().rstrip(':,.')
                add_person(name, '', dirname, 'speaker')

# ── Bluesky lookup ──────────────────────────────────────────────────────────
bsky_cache = load_bsky_cache()
new_searches = 0

if not SKIP_BSKY:
    for key, p in all_people.items():
        # Apply known handles
        if key in KNOWN_BSKY:
            p['bluesky'] = KNOWN_BSKY[key]
            bsky_cache['found'][key] = KNOWN_BSKY[key]
            continue
        # Already found
        if key in bsky_cache.get('found', {}):
            p['bluesky'] = bsky_cache['found'][key]
            continue
        # Already searched and not found
        if key in bsky_cache.get('searched', {}):
            p['bluesky'] = ''
            continue
        # New search
        handle = search_bluesky(p['name'])
        if handle:
            p['bluesky'] = handle
            bsky_cache['found'][key] = handle
            print(f"  Found: {p['name']} -> {handle}")
        else:
            p['bluesky'] = ''
        bsky_cache['searched'][key] = True
        new_searches += 1
        time.sleep(0.4)  # rate limit
        if new_searches % 20 == 0:
            save_bsky_cache(bsky_cache)  # save progress periodically

    save_bsky_cache(bsky_cache)
    print(f"Bluesky: {new_searches} new searches, {len(bsky_cache.get('found', {}))} total found")
else:
    # Apply cache without searching
    for key, p in all_people.items():
        if key in KNOWN_BSKY:
            p['bluesky'] = KNOWN_BSKY[key]
        elif key in bsky_cache.get('found', {}):
            p['bluesky'] = bsky_cache['found'][key]
        else:
            p['bluesky'] = ''

# Build final list -- derive current affiliation from most recent event
for key, p in all_people.items():
    # Latest event with a known affiliation
    latest_aff = ''
    for ev in reversed(event_map_order):
        if ev in p.get('affiliations', {}) and p['affiliations'][ev]:
            latest_aff = p['affiliations'][ev]
            break
    p['affiliation'] = latest_aff  # keep for backwards compat

# Merge known aliases
ALIASES = {
    'rob simpson': 'robert simpson',
    'rob simpson:': 'robert simpson',
    'r. simpson': 'robert simpson',
    'dan foreman-mackey': 'daniel foreman-mackey',
    'daniel foreman-mackey': 'daniel foreman-mackey',
}

def canonical_key(key):
    return ALIASES.get(key, key)

# Merge alias entries into canonical
for alias_key, canon_key in ALIASES.items():
    if alias_key in all_people and canon_key in all_people and alias_key != canon_key:
        alias = all_people[alias_key]
        canon = all_people[canon_key]
        for ev in alias['events']:
            if ev not in canon['events']:
                canon['events'].append(ev)
            for role in alias['roles'].get(ev, []):
                if role not in canon['roles'].get(ev, []):
                    canon['roles'].setdefault(ev, []).append(role)
            if alias['affiliations'].get(ev):
                canon['affiliations'].setdefault(ev, alias['affiliations'][ev])
        del all_people[alias_key]
        print(f"  Merged '{alias_key}' into '{canon_key}'")
    elif alias_key in all_people and canon_key not in all_people and alias_key != canon_key:
        # Rename the alias to canonical
        p = all_people.pop(alias_key)
        p['name'] = ' '.join(w.capitalize() for w in canon_key.split())
        all_people[canon_key] = p

people_list = sorted(all_people.values(), key=lambda x: (-len(x['events']), x['name'].split()[-1]))

output = {
    'people': people_list,
    'events': event_map,
    'generated': __import__('datetime').datetime.utcnow().isoformat() + 'Z',
    'total': len(people_list),
    'multi_event': len([p for p in people_list if len(p['events']) > 1]),
}

with open(OUT, 'w') as f:
    json.dump(output, f)

print(f"Written {len(people_list)} people to {OUT}")
print(f"Multi-event: {output['multi_event']}")
