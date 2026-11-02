"""Pure handoff prose/data helpers; safe to import without UI, save or output edits."""
from pathlib import Path
import json
import re

PREPLANS = (
    'notes/mime-completed-savequit-2026-10-04.md',
    'notes/hardy-completed-savequit-2026-10-04.md',
    'notes/hardy-piano-paused-savequit-2026-10-03.md',
    'notes/hardy-trainers-completed-savequit-2026-10-03.md',
    'notes/hardy-trainer-plan-2026-10-03.md',
    'notes/hardy-piano-queue-helper-2026-10-03.md',
    'notes/elite-four-preplan-2026-10-03.md',
    'notes/agate-street-completed-savequit-2026-10-03.md',
    'notes/agate-paired-trainer-entry-2026-10-03.md',
    'notes/agate-xitem-resupply-2026-10-03.md',
    'notes/agate-ordinary-street-policy-2026-10-03.md',
    'notes/lyla-ezra-field-review131-source-only.md',
    'notes/post-solaris-hardy-mime-route-2026-10-03.md',
    'notes/mime-fairy-roster-plan-2026-10-03.md',
    'notes/gym17-glass-plan-2026-10-03.md',
    'notes/glass-gauntlet-review-2026-10-03.md',
    'notes/void-route-plan-2026-10-03.md',
    'notes/hypno-guarded-plan-2026-10-03.md',
    'notes/post-hypno-exit-route-2026-10-03.md',
    'notes/glass-r3-completed-2026-10-03.md',
    'notes/battle-item-reconciliation-2026-10-03.md',
    'notes/post-glass-boss-preplan-2026-10-03.md',
    'notes/agate-chain-plan-2026-10-03.md',
    'notes/agate-archive-workflow-2026-10-03.md',
    'notes/agate-prep-normal-queue-2026-10-03.md',
    'notes/heartscale-normal-route-2026-10-03.md',
    'notes/hardy-battle-plan-2026-10-03.md',
    'notes/hardy-puzzle-saphira-route-2026-10-03.md',
    'notes/saphira-leg-tactical-review-2026-10-03.md',
    'notes/gauntlet-policy.md',
)


def endpoint(control, closed):
    if closed and control.get('story_complete'):
        return ('Main story and Anna-route postgame complete. Saved and actually quit. '
                + ('All recorded sessions and both victory compilations are verified; archive cleanup is complete. ' if control.get('archive_done') else 'Finish the authorized final recording reconciliation. ')
                + 'Do not replay completed final battles or resume optional content without a new user request.')
    used = control.get('usage_stop_used_percent')
    reserve = (f'Stop gameplay at {used:g}% used ({100-used:g}% remaining), '
               'with capacity reserved for verified save, actual quit and archive cleanup.') if isinstance(used, (int,float)) else 'Read the latest user instruction for the usage boundary.'
    if closed and control.get('user_requested_end_session'):
        cleanup = (' Recording edits and archive cleanup are complete.'
                   if control.get('archive_done') else ' Finish the authorized archive cleanup.')
        return ('Saved and actually quit. The user explicitly ended this gameplay session; '
                'wait for new gameplay authorization. The earlier usage endpoint does not '
                'authorize resuming this session.' + cleanup + ' Latest endpoint: '
                + control.get('milestone', 'Read the latest user instruction.'))
    if closed:
        return ('Saved and actually quit after the latest authorized play session; '
                'wait for a new gameplay endpoint. ' + reserve)
    return ('Active macOS run: ' + control.get('milestone', 'Read the latest user instruction for the authorized endpoint.') + ' ' + reserve)


def published(master, verification):
    n = int(master['published_count'])
    assert 0 <= n <= len(master['fights'])
    assert n == verification['fights'], 'Published manifest and master verification disagree'
    assert master['published_sha256'] == verification['sha256'], 'Master hashes disagree'
    rows = master['fights'][:n]
    assert len({r['id'] for r in rows}) == n, 'Duplicate published major IDs'
    return rows


def victory_summary(rows, limit=8):
    return '; '.join(f"ID{r['id']} {r.get('display_title') or r['opponent']}: {r['attempts']} attempt(s)" for r in rows[-limit:]) or 'No published victories in this manifest.'


def preplans(root):
    return [p for p in PREPLANS if (Path(root)/p).is_file()]


def journey_verification(root, metadata):
    """Select the recording's own journey; never fall back to an unrelated gym."""
    gym = int(metadata['journey_gym'])
    match = re.search(r'session-(\d+)-game-raw', metadata.get('raw', ''))
    if match:
        registry = Path(root)/'recordings'/f'session-{int(match[1]):03}-journey-segments.json'
        if registry.is_file():
            gym = int(json.loads(registry.read_text())['segments'][-1]['gym'])
    candidates = [Path(root)/'notes'/f'gym{gym}-{tail}.json'
                  for tail in ('progress-verification', 'verification')]
    existing = [p for p in candidates if p.is_file()]
    if not existing:
        raise FileNotFoundError(f'No verified journey metadata for recording gym{gym}')
    path = max(existing, key=lambda p:p.stat().st_mtime)
    result = json.loads(path.read_text())
    assert 'decode' in result['verified'], f'Journey not decode-verified: {path}'
    assert re.match(rf'gym-{gym:02}-(?:progress-)?game-4x-bgm\.mp4$', Path(result['desktop']).name), result['desktop']
    return gym, path, result


def catalog_summary(catalog):
    complete, partial = [], []
    for row in catalog['files']:
        name = row['filename']
        if re.fullmatch(r'gym-\d+-game-4x-bgm\.mp4', name):
            complete.append(name)
        elif re.fullmatch(r'gym-\d+-progress-game-4x-bgm\.mp4', name):
            partial.append(name)
    return len(catalog['files']), sorted(complete), sorted(partial)


def resume_text(*, root, name, save, navigation, sha, capture, metadata,
                journey, master, verification, control, closed, now):
    rows = published(master, verification)
    badges = save['trainer']['badges'].count(True)
    party = '\n'.join(f"- {m['name']} Lv{m['level']}; HP{m['hp']}/{m['totalhp']}; {m['ability']}; {m['item'] or 'no item'}; " + ', '.join(z['move'] for z in m['moves']) for m in save['party'])
    notes = ', '.join(f'`{p}`' for p in preplans(root))
    recorder = ('is finalized; discover any newer capture from metadata' if 'stop_epoch' in metadata else 'is the current local capture; verify fresh frames before input')
    variables = navigation.get('variables', {})
    story = ', '.join(f'{k}={variables[k]}' for k in ('391','475','339','342') if k in variables) or 'consult the exact navigation snapshot'
    if closed and control.get('story_complete') and control.get('archive_done'):
        return f"""# Completed Reborn playthrough — {now[:10]}

{endpoint(control, closed)}

Final native checkpoint: **{name}**, Aster, {badges} badges, map{save['map']}{save['position']} (Nightclub). Saved {save['save_mtime']}. Canonical `saves/current/Game_3.rxdata`, SHA256 `{sha}`; matching backup and post-quit snapshot retained.

Shade225, Anna226 and PULSE Arceus227 were defeated in one uninterrupted first attempt. Arceus was then caught. Anna's ending, credits, Agate farewell and final group photo are complete; see `notes/final394-completion-flags.json` and `notes/active-league-chain.json`.

Video30 is complete in `{Path(journey['desktop']).name}`: {journey['frames']} frames, {journey['duration']:.6f}s, SHA256 `{journey['sha256']}`. The established filename retains “progress”; its verification marks the completed milestone. Recorder{capture} is closed. All consumed sources are reconciled; protected raw079/080 review holds remain untouched.

The original major-fights compilation contains {verification['fights']} victories. The separately verified postgame compilation includes the final gauntlet. All exports remain local; no Drive upload was performed.

Final party:

{party}

Optional collecting and side activities were not required for completion. No further gameplay is pending. Any newly requested gameplay must use normal controls and a fresh verified recording.
"""
    return f'''# Current Reborn state — {now[:10]}

{endpoint(control, closed)}

Latest verified native checkpoint: **{name}**; Aster, {badges} badges, Reborn19.5.43, HARDCAP only. Saved{save['save_mtime']}, map{save['map']}{save['position']}; story variables {story}. Canonical `saves/current/Game_3.rxdata`, SHA256 `{sha}`; matching `backups/Aster-{name}.rxdata` and `handoff/save-state.json`. Native checkpoint is authoritative; later live navigation notes can be ahead.

{party}

Latest published major victories: {victory_summary(rows)}. The published manifest proves archived victories, not the absence of later gameplay. **Do not replay a completed fight because its archive has not yet been appended.** Determine the next story gate from the verified save and latest progress notes. Relevant current/future preparation: {notes}. Glass is a consecutive fixed-six chain; an already completed victory must not be replayed. Its normal Void follow-up uses the LightShard and Safeguard preparation before Hypno. Agate's partner warmup and Solaris are also one fixed-six chain with an automatic full heal between. Hardy/Saphira notes distinguish actual checkpoint opportunities from immediate battle commitments; read those before entering a later chain. These are plans, not claims that unrecorded battles were won.

Recorder{capture} {recorder}. Reconcile editing at natural activity pauses; no mandatory hourly game restart; start a verified recording before any gameplay input. Do not reuse a session number. The current journey is `{Path(journey['desktop']).name}` ({'completed leg' if journey['milestone_complete'] else 'partial leg'}), {journey['frames']}frames/{journey['duration']:.6f}s, SHA256 `{journey['sha256']}`. Major master has {verification['fights']} selected victories, SHA256 `{verification['sha256']}`. Full journeys keep all attempts; the major compilation keeps victories only with honest attempt counts and exact player item totals. Verify both required archives before source cleanup; raw079/080 review holds remain untouched.

Continue through normal controls; never edit game/save/memory to win. Only read completed battle logs. Actual doubles columns follow allied left/right and opposing left/right, with sprites/types/builds. Use normal saves/reloads liberally wherever permitted in game. Only game-enforced no-save sequences such as Fiore/Glass restart in full on loss. No Drive upload requested. Linux drivers remain unvalidated; this is still the Mac run.
'''


def refreshed_documents(texts, *, root, label, save, session, metadata,
                        journey, master, verification, catalog, control, closed):
    """Return updated documents without writing or reading game/native state."""
    rows = published(master, verification)
    badges = save['trainer']['badges'].count(True)
    state = f'Aster, {badges} badges, map{save["map"]}{save["position"]}'
    status = endpoint(control, closed)
    exports, complete, partial = catalog_summary(catalog)
    count = verification['fights']
    extra = (' The current partial journey is ' + ', '.join(f'`{n}`' for n in partial) + '.') if partial else ''
    inventory = (f'There are {exports} verified local exports: {len(complete)} completed gym journeys and '
                 f'the {count}-victory major compilation.{extra} See [the media catalog](handoff/media-catalog.json).')
    if control.get('story_complete') and control.get('archive_done'):
        inventory = f'There are {exports} verified local exports: 30 journey videos and two major-fight compilations. Established postgame filenames retain “progress” despite completed story milestones. See [the media catalog](handoff/media-catalog.json).'
    note_list = ', '.join(f'`{p}`' for p in preplans(root))
    next_session = max(session + 1, 1)
    out = dict(texts)

    t = out['README.md']
    t = re.sub(r'\*\*\d+ badges[;.].*?\*\*', f'**{badges} badges. {status} Latest verified save is in RESUME.md.**', t, count=1)
    t = re.sub(r'(Start with \[the Dot handoff\][^\n]*?\)\.).*?\n\n## Resources', r'\1 ' + status + ' Linux installation and driver adaptation remain necessary only if a VM transfer is requested.\n\n## Resources', t, count=1, flags=re.S)
    t = re.sub(r'There are\s*\d+ (?:completed|verified) local exports:.*?See \[the media catalog\]\(handoff/media-catalog.json\)\.', inventory, t, count=1, flags=re.S)
    t = t.replace('plus two calibration images', 'and calibration templates')
    out['README.md'] = t

    t = out['docs/DOT_HANDOFF.md']
    t = re.sub(r'The \d+ current (?:finished videos|verified local exports)', f'The {exports} current verified local exports', t, count=1)
    t = re.sub(r'The current Mac run.*?(?=\n## Read in this order)',
               f'The current Mac run is summarized in RESUME.md. Latest native checkpoint is {label}, {state}. {status} A later Linux transfer still requires recorded compatibility/input/capture validation.\n', t, count=1, flags=re.S)
    t = re.sub(r'4\. `recordings/major-fights/manifest.json`.*?\n5\..*?\n6\.',
               '4. `recordings/major-fights/manifest.json`, `recordings/major-fights/verification.json`, and the current journey verification named in RESUME.md.\n5. The latest relevant preparation notes: ' + note_list + '; newest explicit corrections supersede earlier proposals.\n6.', t, count=1, flags=re.S)
    t = re.sub(r'Confirm Aster, \d+ badges, map\d+\[[^\]]+\], and the exact current party', f'Confirm {state}, and the exact current party', t, count=1)
    t = re.sub(r'fetch at least the completed Gym\d+ journey and\s*\d+-fight master', 'fetch the latest verified journey (including any partial leg) and the ' + str(count) + '-fight master', t, count=1)
    t = re.sub(r'The next unused session (?:after the handoff is expected to be|is at least) \*\*\d+\*\*;', f'The next unused session is at least **{next_session:03}**;', t, count=1)
    t = re.sub(r'`record_session.py start N --gym \d+`', '`record_session.py start N --gym G`', t, count=1)
    t = re.sub(r'Gym\d+ is complete in `gym-\d+-game-4x-bgm.mp4`\.', f'The current leg has a verified {"completed" if journey["milestone_complete"] else "partial"} journey in `{Path(journey["desktop"]).name}`; the media catalog lists all completed legs.', t, count=1)
    heading = '## Current finished video baselines\n\n'
    a = t.index(heading) + len(heading)
    b = t.index('## Important-battles selection and presentation', a)
    old = t[a:b]
    history = old[old.index('- Historical chapters'):] if '- Historical chapters' in old else ''
    baseline = (f'The source machine has {exports} verified local exports: {len(complete)} completed gym journeys, the {count}-victory major compilation, and {len(partial)} partial leg(s). Videos are excluded from Git; the user handles uploads. Verify against the media catalog.\n\n'
                f'- Current journey `{Path(journey["desktop"]).name}`: {journey["frames"]} frames, {journey["duration"]:.6f}s, SHA256 `{journey["sha256"]}`.\n'
                f'- Major master: {count} victories/chapters, {verification["frames"]} frames, {verification["duration"]:.6f}s, SHA256 `{verification["sha256"]}`.\n')
    if control.get('story_complete') and control.get('archive_done'):
        baseline = inventory + '\n\n' + baseline[baseline.index('- Current journey'):]
    t = t[:a] + baseline + history.rstrip() + '\n\n' + t[b:]
    t = re.sub(r'Approved through now: all\d+ badge battles;', f'Approved through now: all{badges} badge battles;', t)
    t = re.sub(r'Future non-gym additions should.*?(?=\n\nBefore a major attempt)',
               'Future non-gym additions should meet the same climax/PULSE/exceptional-boss standard. Latest published victories: ' + victory_summary(rows) + '. Consult the actual manifest for all IDs. A missing later publication is not evidence that its battle must be replayed.', t, count=1, flags=re.S)
    t = re.sub(r'The normal append path uses.*?(?=\n\nThe old master)',
               'The normal append path uses `prepare_major_append.py`, `export_major_types.rb`, `render_major_fights.py`, and `finish_major_fights.py`, with exact opponent data from `export_major_opponents.rb`. Read the workflow and current scripts first. Published IDs: ' + ', '.join(str(r['id']) for r in rows) + '. Also inspect pending attempt records/configs before allocating a new ID. Avoid ID collisions.', t, count=1, flags=re.S)
    t = re.sub(r'1\. Read current RESUME, exact save, recording policy and gauntlet policy\..*?\n2\.',
               '1. Read current RESUME, exact save, recording policy and gauntlet policy. ' + status + '\n2.', t, count=1, flags=re.S)
    t = re.sub(r'Next unused capture is (?:at least )?\d+;.*?(?=\n3\.)', f'Next unused capture is at least {next_session:03}; discover it from metadata.\n', t, count=1, flags=re.S)
    t = re.sub(r'4\. Plan the next authorized segment.*?(?=\n5\.)',
               '4. Plan the next authorized segment from the verified native story gate and actual installed trainers/build. Relevant preparation: ' + note_list + '. Do not replay completed Glass or other fights because an older paragraph lists them as upcoming. HARDCAP alone leaves normal Fly carrier requirements in place.', t, count=1, flags=re.S)
    out['docs/DOT_HANDOFF.md'] = t

    t = out['docs/LINUX_SETUP.md']
    t = re.sub(r'Current major master has\s*\d+\s*fights;', f'Current major master has {count} fights;', t)
    recorder = 'is finalized' if 'stop_epoch' in metadata else 'may still be active; verify actual recorder health'
    t = re.sub(r'Session\d+ (?:is the current local recording number|is finalized); the next unused number is at least \d+;.*?(?=\n)', f'Session{session} {recorder}; the next unused number is at least {next_session}; discover newer metadata before using it.', t)
    t = t.replace('heal at the circus', 'heal the saved party if needed')
    t = re.sub(r'Preserve the completed Gym\d+ journey and the\s*\d+-fight major prefix\.', f'Preserve every completed journey, the current `{Path(journey["desktop"]).name}` and the {count}-fight major prefix.', t)
    t = t.replace('`notes/ciel-continuation-plan.md`', note_list)
    t = t.replace('The current instruction is a handoff, not automatic permission to resume playing.', 'Read RESUME.md and the latest user message for gameplay authorization; a transfer alone is not an instruction to play.')
    out['docs/LINUX_SETUP.md'] = t

    t = out['AGENTS.md']
    a = t.index('Read README.md')
    b = t.index('\n\nDo not start a new game', a)
    t = t[:a] + ('Read README.md, RESUME.md, docs/DOT_HANDOFF.md and docs/LINUX_SETUP.md first. These current entrypoints and verified manifests supersede old goals in historical notes. User instructions take precedence. ' + status + ' See RESUME.md for current checkpoints. Do not replay a completed battle due to stale upcoming lists. No Linux gameplay driver has been validated; the Linux kit is for a possible later transfer.') + t[b:]
    out['AGENTS.md'] = t
    return out
