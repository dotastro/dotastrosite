#!/usr/bin/env python3
"""
Rebuild all generated files from _data/events/*.yml (single source of truth).

Run this after any changes to _data/events/*.yml or _data/event_meta.yml.

Steps:
  1. Generate API JSON files (api/v1/*.json)
  2. Regenerate participants-data.json (assets/js/participants-data.json)
  3. Regenerate search-index.json (assets/js/search-index.json)

Usage:
  python3 scripts/rebuild-all.py            # full rebuild with Bluesky lookup
  python3 scripts/rebuild-all.py --no-bsky  # skip Bluesky API calls
"""

import os
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE, 'scripts')

# Pass through --no-bsky flag
extra_args = [a for a in sys.argv[1:] if a == '--no-bsky']


def run_script(script_path, args=None):
    cmd = [sys.executable, script_path] + (args or [])
    print(f"\n{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    print('='*60)
    result = subprocess.run(cmd, cwd=BASE)
    if result.returncode != 0:
        print(f"ERROR: {script_path} failed with exit code {result.returncode}")
        sys.exit(result.returncode)


def main():
    print("=== Rebuilding everything from _data/ ===")

    # 1. Generate API JSON files
    run_script(os.path.join(SCRIPTS_DIR, 'generate-api.py'))

    # 2. Regenerate participants-data.json
    run_script(os.path.join(SCRIPTS_DIR, 'regenerate-participants.py'), extra_args)

    # 3. Regenerate search-index.json
    run_script(os.path.join(BASE, 'generate-search-index.py'))

    print(f"\n{'='*60}")
    print("All done! Generated files are ready.")
    print('='*60)


if __name__ == '__main__':
    main()
