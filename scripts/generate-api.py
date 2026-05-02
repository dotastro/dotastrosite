#!/usr/bin/env python3
"""
Generate static JSON API files for the .Astronomy conference archive.
Reads from _data/events/*.yml (single source of truth) and participants-data.json.
Writes API files to api/v1/.
"""

import json
import os
import re
import yaml
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_EVENTS_DIR = os.path.join(REPO_ROOT, '_data', 'events')
EVENT_META_PATH = os.path.join(REPO_ROOT, '_data', 'event_meta.yml')
API_DIR = os.path.join(REPO_ROOT, 'api', 'v1')
EVENTS_API_DIR = os.path.join(API_DIR, 'events')
PARTICIPANTS_JSON = os.path.join(REPO_ROOT, 'assets', 'js', 'participants-data.json')
BSKY_CACHE = os.path.join(REPO_ROOT, 'assets', 'js', 'bluesky-cache.json')
BASE_URL = 'https://dotastro.github.io/dotastrosite'
API_BASE = f'{BASE_URL}/api/v1'

NOW = datetime.now(timezone.utc).isoformat()


def read_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Wrote {path}")


def load_bsky_cache():
    if os.path.exists(BSKY_CACHE):
        with open(BSKY_CACHE) as f:
            data = json.load(f)
        return data.get('found', {})
    return {}


def get_bsky(name, bsky_cache):
    return bsky_cache.get(name.lower().strip(), None)


def load_events():
    """Load all event YAML files."""
    meta = read_yaml(EVENT_META_PATH)
    events = []
    for entry in meta['events']:
        slug = entry['slug']
        path = os.path.join(DATA_EVENTS_DIR, f'{slug}.yml')
        if os.path.exists(path):
            data = read_yaml(path)
            events.append(data)
        else:
            print(f"  WARNING: {path} not found")
    return events


def build_talks_list(events):
    """Flatten all talks across events."""
    talks = []
    for event in events:
        for talk in event.get('talks', []):
            t = {
                'event': event['slug'],
                'year': event['year'],
                'speaker': talk.get('speaker', ''),
                'affiliation': talk.get('affiliation'),
                'title': talk.get('title'),
                'type': talk.get('type', 'talk'),
                'notes': talk.get('notes'),
                'slides_url': talk.get('slides_url'),
                'video_url': talk.get('video_url'),
            }
            talks.append(t)
    return talks


def build_hacks_list(events):
    """Flatten all hacks across events."""
    hacks = []
    for event in events:
        for hack in event.get('hacks', []):
            h = {
                'title': hack['title'],
                'event': event['slug'],
                'year': event['year'],
                'creators': hack.get('creators', []),
                'description': hack.get('description', ''),
                'source_url': hack.get('source_url'),
                'live_url': hack.get('live_url'),
                'doi': hack.get('doi'),
            }
            hacks.append(h)
    return hacks


def build_people_endpoint(events, bsky_cache):
    """Build people endpoint from participants-data.json if it exists, else from event data."""
    if os.path.exists(PARTICIPANTS_JSON):
        with open(PARTICIPANTS_JSON) as f:
            pdata = json.load(f)

        people = []
        for person in pdata.get('people', []):
            name = person['name']
            bsky = person.get('bluesky', '') or get_bsky(name, bsky_cache) or None
            p = {
                'name': name,
                'events': person.get('events', []),
                'event_count': len(person.get('events', [])),
            }
            roles = person.get('roles', {})
            clean_roles = {}
            for evt, role_list in roles.items():
                notable = [r for r in role_list if r in ('organiser', 'speaker')]
                if notable:
                    clean_roles[evt] = notable
            if clean_roles:
                p['roles'] = clean_roles
            if bsky:
                p['bluesky'] = bsky
            aff = person.get('affiliation', '')
            if aff:
                aff = re.sub(r',?\s*@\w+', '', aff).strip().rstrip(',')
                p['current_affiliation'] = aff
            people.append(p)

        people.sort(key=lambda x: (-x['event_count'], x['name']))
        return {'people': people, 'total': len(people), 'generated_at': NOW}

    # Fallback: build from event data
    person_map = {}
    for event in events:
        slug = event['slug']
        for p in event.get('participants', []):
            name = p['name']
            key = name.lower()
            if key not in person_map:
                person_map[key] = {'name': name, 'events': [], 'affiliation': p.get('affiliation', '')}
            person_map[key]['events'].append(slug)
            if p.get('affiliation') and not person_map[key]['affiliation']:
                person_map[key]['affiliation'] = p['affiliation']

    people = []
    for key, info in person_map.items():
        p = {'name': info['name'], 'events': info['events'], 'event_count': len(info['events'])}
        bsky = get_bsky(info['name'], bsky_cache)
        if bsky:
            p['bluesky'] = bsky
        if info.get('affiliation'):
            p['current_affiliation'] = info['affiliation']
        people.append(p)

    people.sort(key=lambda x: (-x['event_count'], x['name']))
    return {'people': people, 'total': len(people), 'generated_at': NOW}


def main():
    print("=== .Astronomy API Generator (from _data/) ===\n")

    events = load_events()
    bsky_cache = load_bsky_cache()
    print(f"Loaded {len(events)} events from _data/events/\n")

    all_talks = build_talks_list(events)
    all_hacks = build_hacks_list(events)

    os.makedirs(EVENTS_API_DIR, exist_ok=True)

    # 1. index.json
    write_json(os.path.join(API_DIR, 'index.json'), {
        'name': '.Astronomy Conference Archive API',
        'version': '1.0',
        'description': 'A read-only JSON API for the .Astronomy conference series archive. Free to use, no auth required.',
        'base_url': API_BASE,
        'endpoints': {
            'events': '/events.json',
            'event': '/events/{slug}.json',
            'people': '/people.json',
            'hacks': '/hacks.json',
            'talks': '/talks.json',
        },
        'generated_at': NOW,
        'source': 'https://github.com/dotastro/dotastrosite',
        'licence': 'CC BY 4.0'
    })

    # 2. events.json
    events_list = []
    for event in events:
        events_list.append({
            'slug': event['slug'],
            'number': event['number'],
            'name': event['name'],
            'year': event['year'],
            'city': event['city'],
            'country': event['country'],
            'venue': event.get('venue', ''),
            'dates': event.get('dates', ''),
            'url': f'{BASE_URL}/events/{event["slug"]}/',
            'participant_count': len(event.get('participants', [])),
            'hack_count': len(event.get('hacks', [])),
            'talk_count': len(event.get('talks', [])),
        })
    write_json(os.path.join(API_DIR, 'events.json'), {
        'events': events_list,
        'total': len(events_list),
        'generated_at': NOW
    })

    # 3. Individual event files
    for event in events:
        event_out = dict(event)
        event_out['url'] = f'{BASE_URL}/events/{event["slug"]}/'
        event_out['participant_count'] = len(event.get('participants', []))
        event_out['hack_count'] = len(event.get('hacks', []))
        event_out['talk_count'] = len(event.get('talks', []))
        write_json(os.path.join(EVENTS_API_DIR, f'{event["slug"]}.json'), event_out)

    # 4. people.json
    people_data = build_people_endpoint(events, bsky_cache)
    write_json(os.path.join(API_DIR, 'people.json'), people_data)

    # 5. hacks.json
    write_json(os.path.join(API_DIR, 'hacks.json'), {
        'hacks': all_hacks,
        'total': len(all_hacks),
        'generated_at': NOW
    })

    # 6. talks.json
    write_json(os.path.join(API_DIR, 'talks.json'), {
        'talks': all_talks,
        'total': len(all_talks),
        'generated_at': NOW
    })

    print(f"\n=== API Generation Complete ===")
    print(f"Events:  {len(events)}")
    print(f"People:  {people_data['total']}")
    print(f"Hacks:   {len(all_hacks)}")
    print(f"Talks:   {len(all_talks)}")


if __name__ == '__main__':
    main()
