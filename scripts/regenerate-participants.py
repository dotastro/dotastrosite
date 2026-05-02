#!/usr/bin/env python3
"""Regenerate participants-data.json from _data/events/*.yml (single source of truth).

Also runs incremental Bluesky lookup for new participants.

Usage:
  python3 scripts/regenerate-participants.py           # rebuild + Bluesky lookup
  python3 scripts/regenerate-participants.py --no-bsky # rebuild only, skip Bluesky
"""

import os, re, json, sys, time, yaml

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_EVENTS_DIR = os.path.join(BASE, '_data', 'events')
EVENT_META_PATH = os.path.join(BASE, '_data', 'event_meta.yml')
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

ALIASES = {
    'rob simpson': 'robert simpson',
    'rob simpson:': 'robert simpson',
    'r. simpson': 'robert simpson',
    'dan foreman-mackey': 'daniel foreman-mackey',
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
            bio = (actor.get('description') or '').lower()
            display_parts = set(display.split())
            if not name_parts.issubset(display_parts) and not display_parts.issubset(name_parts):
                name_words = name_lower.split()
                if len(name_words) >= 2:
                    if not (name_words[0] in display and name_words[-1] in display):
                        continue
            if not any(kw in bio for kw in ASTRO_KEYWORDS):
                continue
            return actor.get('handle')
    except Exception:
        pass
    return None


def load_events():
    """Load event metadata and all event YAML files."""
    with open(EVENT_META_PATH) as f:
        meta = yaml.safe_load(f)

    event_order = [e['slug'] for e in meta['events']]
    events = {}
    for slug in event_order:
        path = os.path.join(DATA_EVENTS_DIR, f'{slug}.yml')
        if os.path.exists(path):
            with open(path) as f:
                events[slug] = yaml.safe_load(f)
    return event_order, events


def main():
    event_order, events = load_events()
    print(f"Loaded {len(events)} events from _data/events/")

    all_people = {}

    def add_person(name, affiliation, event_slug, role):
        if not name or len(name) < 3 or name.startswith('http'):
            return
        key = name.lower().strip()
        key = ALIASES.get(key, key)
        canonical_name = name
        if key in ALIASES.values() and key not in all_people:
            canonical_name = ' '.join(w.capitalize() for w in key.split())

        if key not in all_people:
            all_people[key] = {
                'name': canonical_name,
                'affiliations': {},
                'events': [],
                'roles': {},
            }
        if event_slug not in all_people[key]['events']:
            all_people[key]['events'].append(event_slug)
        roles = all_people[key]['roles'].get(event_slug, [])
        if role not in roles:
            roles.append(role)
        all_people[key]['roles'][event_slug] = roles
        if affiliation:
            all_people[key]['affiliations'][event_slug] = affiliation

    # Process each event
    for slug in event_order:
        event = events.get(slug)
        if not event:
            continue

        # Participants
        for p in event.get('participants', []):
            add_person(p['name'], p.get('affiliation', ''), slug, 'attendee')

        # Organisers
        for org in event.get('organisers', []):
            add_person(org['name'], org.get('affiliation', ''), slug, 'organiser')

        # Speakers
        for talk in event.get('talks', []):
            speaker = talk.get('speaker', '')
            if speaker:
                add_person(speaker, talk.get('affiliation', ''), slug, 'speaker')

    # Bluesky lookup
    bsky_cache = load_bsky_cache()
    new_searches = 0

    if not SKIP_BSKY:
        for key, p in all_people.items():
            if key in KNOWN_BSKY:
                p['bluesky'] = KNOWN_BSKY[key]
                bsky_cache['found'][key] = KNOWN_BSKY[key]
                continue
            if key in bsky_cache.get('found', {}):
                p['bluesky'] = bsky_cache['found'][key]
                continue
            if key in bsky_cache.get('searched', {}):
                p['bluesky'] = ''
                continue
            handle = search_bluesky(p['name'])
            if handle:
                p['bluesky'] = handle
                bsky_cache['found'][key] = handle
                print(f"  Found: {p['name']} -> {handle}")
            else:
                p['bluesky'] = ''
            bsky_cache['searched'][key] = True
            new_searches += 1
            time.sleep(0.4)
            if new_searches % 20 == 0:
                save_bsky_cache(bsky_cache)

        save_bsky_cache(bsky_cache)
        print(f"Bluesky: {new_searches} new searches, {len(bsky_cache.get('found', {}))} total found")
    else:
        for key, p in all_people.items():
            if key in KNOWN_BSKY:
                p['bluesky'] = KNOWN_BSKY[key]
            elif key in bsky_cache.get('found', {}):
                p['bluesky'] = bsky_cache['found'][key]
            else:
                p['bluesky'] = ''

    # Derive current affiliation from most recent event
    for key, p in all_people.items():
        latest_aff = ''
        for ev in reversed(event_order):
            if ev in p.get('affiliations', {}) and p['affiliations'][ev]:
                latest_aff = p['affiliations'][ev]
                break
        p['affiliation'] = latest_aff

    # Build event map for output
    event_map = {}
    for slug in event_order:
        event = events.get(slug, {})
        event_map[slug] = {
            'num': event.get('number', ''),
            'name': event.get('name', ''),
            'year': event.get('year', 0),
            'city': event.get('city', ''),
        }

    people_list = sorted(all_people.values(), key=lambda x: (-len(x['events']), x['name'].split()[-1]))

    output = {
        'people': people_list,
        'events': event_map,
        'generated': __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
        'total': len(people_list),
        'multi_event': len([p for p in people_list if len(p['events']) > 1]),
    }

    with open(OUT, 'w') as f:
        json.dump(output, f)

    print(f"Written {len(people_list)} people to {OUT}")
    print(f"Multi-event: {output['multi_event']}")


if __name__ == '__main__':
    main()
