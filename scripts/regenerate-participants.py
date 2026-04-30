#!/usr/bin/env python3
"""Regenerate /tmp/dotastro_people.json from current event pages.
Run this whenever event pages are updated to keep the participants
directory in sync. The community/participants.md page reads from this data
at build time via the JS embedded in the page.

Usage: python3 scripts/regenerate-participants.py
"""

import os, re, json, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_DIR = os.path.join(BASE, 'events')
OUT = os.path.join(BASE, 'assets/js/participants-data.json')

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
            'affiliation': affiliation,
            'events': [],
            'roles': {},
        }
    if event_dir not in all_people[key]['events']:
        all_people[key]['events'].append(event_dir)
    roles = all_people[key]['roles'].get(event_dir, [])
    if role not in roles:
        roles.append(role)
    all_people[key]['roles'][event_dir] = roles
    if affiliation and not all_people[key]['affiliation']:
        all_people[key]['affiliation'] = affiliation

for dirname in event_map:
    fpath = os.path.join(EVENTS_DIR, dirname, 'index.md')
    if not os.path.exists(fpath):
        continue
    with open(fpath) as f:
        text = f.read()

    # Participants
    in_sec = False
    for line in text.split('\n'):
        if '## Participants' in line or '// participants' in line:
            in_sec = True
            continue
        if in_sec and re.match(r'^## ', line) and 'participant' not in line.lower():
            in_sec = False
        if in_sec and line.strip().startswith('- ') and '<' not in line:
            raw = line.strip()[2:].strip()
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
        if in_org and line.strip().startswith('- ') and '<' not in line:
            raw = line.strip()[2:].strip()
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
                name = re.sub(r'\s*\(invited\)', '', m.group(1), flags=re.I).strip()
                add_person(name, '', dirname, 'speaker')

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
