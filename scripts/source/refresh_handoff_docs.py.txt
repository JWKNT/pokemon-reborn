"""Refresh handoff prose from explicit verified metadata; no game input.

Safe to import. Writes Desktop package documents only from the explicit CLI.
"""
from pathlib import Path
import argparse
import json

from handoff_context import journey_verification, refreshed_documents

ROOT = Path(__file__).resolve().parents[1]
DEST = Path('/Users/jw/Desktop/bin/reborn')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('label')
    parser.add_argument('session', type=int)
    parser.add_argument('--quit', action='store_true')
    args = parser.parse_args()
    save = json.loads((ROOT/'notes'/f'{args.label}-status.json').read_text())
    verification = json.loads((ROOT/'recordings/major-fights/verification.json').read_text())
    master = json.loads((ROOT/'recordings/major-fights/manifest.json').read_text())
    meta = json.loads((ROOT/f'recordings/session-{args.session:03}.json').read_text())
    if args.quit:
        assert 'stop_epoch' in meta, 'Finalize the supplied recording before claiming save+quit'
        assert (ROOT/'notes'/f'{args.label}-quit-status.json').is_file(), 'Missing actual-quit evidence'
    _, _, journey = journey_verification(ROOT, meta)
    catalog = json.loads((DEST/'handoff/media-catalog.json').read_text())
    control = json.loads((ROOT/'notes/current-run-control.json').read_text())
    names = ('README.md', 'docs/DOT_HANDOFF.md', 'docs/LINUX_SETUP.md', 'AGENTS.md')
    texts = {name:(DEST/name).read_text() for name in names}
    updated = refreshed_documents(texts, root=ROOT, label=args.label, save=save,
                                  session=args.session, metadata=meta, journey=journey,
                                  master=master, verification=verification, catalog=catalog,
                                  control=control, closed=args.quit)
    for name, value in updated.items():
        (DEST/name).write_text(value)
    print('CURRENT HANDOFF PROSE REFRESHED', args.label, save['trainer']['badges'].count(True),
          'badges', len(catalog['files']), 'exports', verification['fights'], 'major victories')


if __name__ == '__main__':
    main()
