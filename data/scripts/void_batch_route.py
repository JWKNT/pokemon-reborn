"""Guarded normal controls: post-Glass Void story to the safe Hypno approach.

Development is source-only; importing this module sends no input. At runtime all
controls use play.act and the existing capture/session guards. Never starts a
battle. Movement stops at the first meaningful touch event; unknown events,
choices, battles, capture failures, and coordinate disagreements stop the run.

Examples (run only with the game recorded, in the observed Void overworld):
  python3 scripts/void_batch_route.py --stop-phase ame
  python3 scripts/void_batch_route.py
  python3 scripts/void_batch_route.py --from-phase florinia

Automatic map resume takes one normal checkpoint to refresh source conditions
when not at the initial754 spawn. Explicit phases have the same prerequisite.
Two normal checkpoints during a fresh run verify shard healing and the final
safe approach. Planning-note updates describe completed observed source events;
there is no direct game/save/runtime editing.
"""
import argparse
import difflib
import json
import pathlib
import re
import subprocess
import sys
import time

from PIL import Image
from play import ROOT, STATE, act, read, snap
from locate import locate, capture_ready
from void_static_paths import path


# name, map, event, player endpoint, facing, next map (if the event transfers)
PHASES = [
    ('shard', 754, 5, (16, 12), 'right', None),
    ('conductor', 754, 2, (14, 78), 'down', None),
    ('ame', 754, 3, (58, 80), None, 755),
    ('mudkip', 755, 24, (62, 64), 'down', 756),
    ('cain-first', 756, 3, (99, 69), 'right', None),
    ('julia', 756, 2, (119, 44), 'up', None),
    ('fern', 756, 4, (102, 20), 'up', 757),
    ('florinia', 757, 2, (132, 16), 'up', None),
    ('anna', 757, 14, (164, 188), 'left', None),
    ('cain-second', 757, 16, (138, 157), 'right', None),
    ('kiki', 757, 17, (132, 108), 'up', None),
    ('lin', 757, 24, (121, 81), 'down', None),
    ('radomus', 757, 26, (107, 145), 'down', None),
    ('zina', 757, 27, (120, 158), 'down', 758),
    ('hypno-approach', 758, None, (28, 106), None, None),
]
PHASE_NAMES = [p[0] for p in PHASES]
TOUCHES = {754: {6, 3}, 755: {11}, 756: set(),
           757: {3, 29, 6, 34, 54, 55, 13, 56, 57, 65, 76, 84},
           758: {17}}
STATE_FILE = ROOT/'notes/navigation-state.json'
RECEIPTS = ROOT/'work/void-batch-progress.json'
SOURCE_FILE = ROOT/'work/void-source-event-index.json'
BASE_PP = None


def run(script, *args):
    subprocess.run([sys.executable, str(ROOT/'scripts'/f'{script}.py'),
                    *map(str, args)], check=True)


def source_event(mid, eid):
    events = json.loads(SOURCE_FILE.read_text())
    return next(e for m in events if m['map'] == mid
                for e in m['events'] if e['id'] == eid)


def model(mid, xy):
    value = json.loads(subprocess.check_output(
        ['ruby', str(ROOT/'scripts/route_map.rb'), str(mid),
         str(xy[0]), str(xy[1])], stderr=subprocess.DEVNULL))
    if mid == 758:
        # Even if an alternate route is shorter, the boss tile is forbidden.
        value['events']['122'].update(x=28, y=105, character='FORBIDDEN_BOSS',
                                      through=False)
    return value


def meaningful(event):
    return any(c['code'] not in [0, 108, 408] for c in event.get('list', []))


def normalized(text):
    return re.sub('[^a-z]', '', text.lower()).replace('pokemonreborn', '')


def textbox():
    im = Image.open(STATE).convert('RGB')
    w, h = im.size
    box = im.crop((int(w*.08), int(h*.75), int(w*.90), int(h*.87)))
    white = sum(min(p)>235 and max(p)-min(p)<5 for p in box.getdata())
    white /= box.width*box.height
    def border(y):
        px = [im.getpixel((x, int(h*y)))
              for x in range(int(w*.08), int(w*.90))]
        return sum(max(p)<95 for p in px)/len(px)
    return white>.35 and max(border(y) for y in [.721,.725,.729,.733])>.8 \
        and max(border(y) for y in [.895,.900,.905,.910])>.8


def world_guard(rows=None, fade_retries=2):
    rows = snap() if rows is None else rows
    text = '\n'.join(r['text'] for r in rows).lower()
    compact = re.sub('[^a-z]', '', text)
    if 'repel' in compact and 'woreoff' in compact:
        # Void maps have no wild encounters; decline normal renewal instead
        # of spending another Repel. Reinspect before sending any movement.
        run('renew_repel', '--cancel')
        rows = snap()
        text = '\n'.join(r['text'] for r in rows).lower()
    choices = {r['text'].strip().lower() for r in rows}
    if re.search(r'\bhp\b|\bfight\b|\bwild\b|\bpp:', text) \
            or choices & {'yes', 'no'} or textbox():
        raise SystemExit('Void overworld required; resolve/review screen: '+text)
    if re.search(r'[,.;]\s*map\s*[0-9oq]+', text):
        raise SystemExit('Coordinate popup remained open; movement stopped')
    im = Image.open(STATE).convert('RGB')
    w, h = im.size
    px = list(im.crop((int(w*.06), int(h*.08), int(w*.94), int(h*.88))).getdata())
    # The animated Void floor is mostly black even after its arrival has
    # completed. Its bright speckles vary from gray to blue with the animation.
    # Require missing terrain texture as well before
    # treating the frame as a black transition; coordinates remain guarded.
    void_texture = sum(max(p)>70 for p in px)/len(px)
    if sum(max(p)<25 for p in px)/len(px)>.997 and void_texture<.0005:
        if fade_retries:
            act('wait:.6')
            return world_guard(snap(), fade_retries-1)
        raise SystemExit('Void fade/animation still active; no movement sent')


def record(kind, **data):
    value = json.loads(RECEIPTS.read_text()) if RECEIPTS.exists() else {'events': []}
    value['events'].append({'epoch': time.time(), 'kind': kind, **data})
    RECEIPTS.write_text(json.dumps(value, indent=2)+'\n')


def mirror_completed(mid, eid):
    """Only unconditional effects after the observed scene has finished."""
    event = source_event(mid, eid)
    state = json.loads(STATE_FILE.read_text())
    for page in event['pages']:
        for c in page['list']:
            if c['indent'] != 0:
                continue
            a = c['parameters']
            if c['code'] == 123:
                state.setdefault('self_switches', {})[f'{mid},{eid},{a[0]}'] = a[1] == 0
            elif c['code'] == 121 and a[0] == a[1]:
                state.setdefault('switches', {})[str(a[0])] = a[2] == 0
            elif c['code'] == 122 and a[0] == a[1] and a[2:4] == [0, 0]:
                # Progress setters in approved story events; never source reads
                # of player coordinates or the conditional Mudkip choice body.
                state.setdefault('variables', {})[str(a[0])] = a[4]
    STATE_FILE.write_text(json.dumps(state)+'\n')
    if (mid, eid) == (757, 24):
        # Lin's runtime move route removes her; the installed single page keeps
        # a sprite. Self-A is written only at the scene's end. Planner-only.
        p = ROOT/'notes/navigation-overrides.json'
        v = json.loads(p.read_text()) if p.exists() else {}
        if 24 not in v.setdefault('757', []):
            v['757'].append(24)
        p.write_text(json.dumps(v)+'\n')


def settle(mid, eid):
    event = source_event(mid, eid)
    cs = [c for p in event['pages'] for c in p['list']]
    if any(c['code'] in [102,103,104,301] or any(
            k in str(c['parameters']) for k in
            ['pbTrainerBattle','pbDoubleTrainerBattle','pbWildBattle']) for c in cs):
        raise SystemExit(f'Unapproved choice/battle source {mid}E{eid}')
    text = read()
    if textbox():
        blocks = []
        for c in cs:
            if c['code'] == 101:
                blocks.append(str(c['parameters'][0]))
            elif c['code'] == 401 and blocks:
                blocks[-1] += ' '+str(c['parameters'][0])
        n = normalized(text)
        matches = [difflib.SequenceMatcher(None, n, normalized(b)).ratio()
                   for b in blocks]
        if len(n)>4 and (not matches or max(matches)<.52):
            raise SystemExit(f'Visible dialogue does not match {mid}E{eid}: '+text)
    long = (mid,eid) in {(754,3),(757,6),(757,34),(757,54),(757,55),
                        (757,57),(757,26)}
    args = ['--burst','--world-settle',30 if long else 12]
    if any(c['code'] in [241,242] for c in cs):
        args.append('--log-scripted-bgm')
    run('linear_dialog', mid, eid, *args)
    world_guard()
    mirror_completed(mid, eid)
    record('scene-completed', map=mid, event=eid)


def walk(mid, goal, chunk_limit, transfer=None):
    seen = []
    for _ in range(120):
        world_guard()
        actual, x, y = locate(mid)
        if actual != mid:
            raise SystemExit(f'Unexpected map before movement: {actual}, wanted{mid}')
        world_guard()
        if (x,y) == goal:
            return actual, x, y
        seen.append((x,y))
        if len(seen)>=3 and len(set(seen[-3:]))==1:
            raise SystemExit('Repeated Void coordinate; obstacle/timing review')
        v = model(mid, (x,y))
        keys, nodes = path(v, (x,y), goal)
        keys, nodes = keys[:chunk_limit], nodes[:chunk_limit+1]
        stop = None
        for i, xy in enumerate(nodes[1:], 1):
            at = [(int(eid), e) for eid,e in v['events'].items()
                  if e['trigger'] in [1,2] and (e['x'],e['y']) == xy
                  and meaningful(e)]
            if not at:
                continue
            if len(at)!=1:
                raise SystemExit(f'Ambiguous Void touch at {mid}{xy}: {at}')
            eid, event = at[0]
            if eid not in TOUCHES.get(mid,set()):
                raise SystemExit(f'Unplanned touch {mid}E{eid}{xy}; no batch sent')
            if (mid,eid)==(754,3) and transfer!=755:
                raise SystemExit('Ame transfer reached outside its approved phase')
            keys, nodes, stop = keys[:i], nodes[:i+1], eid
            break
        if not keys:
            raise SystemExit('Empty Void path away from target')
        seq = []
        for key in keys:
            if key.startswith('jump:'):
                seq.extend([key[5:]+':.12','wait:.9'])
            else:
                seq.append(key+':.12')
        print('VOID SEGMENT',mid,(x,y),'->',nodes[-1],len(keys),'touch',stop,flush=True)
        # Never replay after a capture failure. Existing guards release keys;
        # explicit/map resume will inspect actual state rather than guessing.
        try:
            act(*seq)
        except subprocess.CalledProcessError as error:
            if error.returncode != 2:
                raise
            capture_ready()
            world_guard()
            record('capture-recovered-replan', map=mid)
            print('CAPTURE RECOVERED; replanning from observed coordinates', flush=True)
            continue
        if stop is not None:
            settle(mid, stop)
            actual, x, y = locate(transfer if (mid,stop)==(754,3) else mid)
            if (mid,stop)==(754,3):
                if actual!=transfer:
                    raise SystemExit('Ame scene did not reach its expected map')
                return actual,x,y
            if actual != mid:
                raise SystemExit('Unexpected story transfer after touch')
        else:
            world_guard()
    raise SystemExit('Void route segment limit')


def native():
    value = json.loads(subprocess.check_output(
        ['ruby',str(ROOT/'scripts/map_state.rb')],stderr=subprocess.DEVNULL))
    # map_state.rb's selected party fields retain Ruby instance-variable names;
    # nested PBMove fields pass through plain(), which already strips the prefix.
    value['party'] = [{key.removeprefix('@'): field for key,field in member.items()}
                      for member in value['party']]
    return value


def full_pp(member):
    """Installed compiled move data plus PBMove.rb's PP-Up calculation."""
    global BASE_PP
    if BASE_PP is None:
        code = ("require_relative 'scripts/read_rgss'; "
                "h=load_rgss('/Applications/Reborn.app/Contents/Game/Data/moves.dat'); "
                "puts JSON.generate(h.transform_values{|m|m.instance_variable_get(:@maxpp)})")
        BASE_PP = json.loads(subprocess.check_output(
            ['ruby','-e',code],cwd=ROOT,stderr=subprocess.DEVNULL))
    for move in member['moves']:
        base = BASE_PP.get(move['move'])
        ups = move.get('ppup',0)
        if not isinstance(base,int) or not 0<=ups<=3 \
                or move['pp'] != base*(5+ups)//5:
            return False
    return True


def hypno_prepared_pp(member):
    """Final Hypno readiness only; preserve the strict shard/full-PP test.

    Normal TM teaching caps new current PP at the replaced move's current PP
    (Items.rb pbLearnMove, bymachine=True). The healed ExtremeSpeed slot had8;
    its newly taught Safeguard is therefore8/25, PP-Up0, not full. This exact
    recorded Arcanine90 slot is enough for the reviewed short Hypno plan.
    Every other move/member must still have its actual installed maximum PP.
    """
    if full_pp(member):
        return True
    moves = member.get('moves', [])
    if member.get('species') != 'ARCANINE' or member.get('level') != 90 \
            or len(moves) != 4 or [m['move'] for m in moves] != [
                'SAFEGUARD', 'FLAMETHROWER', 'CRUNCH', 'MORNINGSUN'] \
            or moves[0].get('ppup') != 0 or moves[0].get('pp') != 8:
        return False
    source = pathlib.Path('/Applications/Reborn.app/Contents/Game/Scripts/Items.rb').read_text()
    if BASE_PP.get('SAFEGUARD') != 25 or BASE_PP.get('EXTREMESPEED') != 5 \
            or 'oldmovepp = pokemon.moves[forgetmove].pp' not in source \
            or 'pokemon.moves[forgetmove].pp = [oldmovepp, pokemon.moves[forgetmove].totalpp].min if bymachine' not in source:
        return False
    # Arithmetic validation of a COPY; this neither heals nor edits game/native
    # evidence. Only the exact known TM carryover is exempted from full_pp().
    checked = dict(member, moves=[dict(m) for m in moves])
    checked['moves'][0]['pp'] = 25
    return full_pp(checked)


def prepare_safeguard(saved):
    arc = next((p for p in saved['party'] if p['species']=='ARCANINE'),None)
    if arc is None or len(saved['party'])!=6:
        raise SystemExit('Fixed six/Arcanine native build review')
    moves = [m['move'] for m in arc['moves']]
    if 'SAFEGUARD' in moves:
        return
    if moves[0]!='EXTREMESPEED' or not {'CRUNCH','MORNINGSUN','FLAMETHROWER'} <= set(moves):
        raise SystemExit('Arcanine replacement slot changed; no TM input sent')
    if saved['bag'].get('TM20',0)<1:
        raise SystemExit('Owned TM20 missing; Safeguard preparation stopped')
    run('teach_machine','TM20','Arcanine','Safeguard',0)
    world_guard()


def sync_lin_override():
    """Freshly synchronized self-A supersedes an old planner removal."""
    state = json.loads(STATE_FILE.read_text())
    if state.get('self_switches',{}).get('757,24,A'):
        mirror_completed(757,24)
        return
    p = ROOT/'notes/navigation-overrides.json'
    if p.exists():
        value = json.loads(p.read_text())
        if 24 in value.get('757',[]):
            value['757'].remove(24)
            p.write_text(json.dumps(value)+'\n')


def phase_done(phase, value):
    name, mid, eid, goal, facing, transfer = phase
    if eid is None or transfer is not None:
        return False
    state = json.loads(STATE_FILE.read_text())
    if name=='lin':
        if state.get('self_switches',{}).get('757,24,A'):
            mirror_completed(757,24)
            return True
        return False
    e = value['events'].get(str(eid))
    return e is None or not meaningful(e)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--from-phase',choices=PHASE_NAMES)
    p.add_argument('--stop-phase',choices=PHASE_NAMES,default='hypno-approach')
    p.add_argument('--chunk',type=int,default=56)
    p.add_argument('--list-phases',action='store_true')
    a = p.parse_args()
    if a.list_phases:
        print('\n'.join(PHASE_NAMES));return
    if not 1<=a.chunk<=84:
        raise SystemExit('Void chunk must be1..84')
    # Only if this source-specific optional prompt is already on screen. It can
    # be unlocked by another file; never activate it or skip the recorded story.
    initial = read()
    if 'skipcutscenesonthisfile' in normalized(initial):
        skip = source_event(754,14)['pages'][1]['list']
        if [c['parameters'][0] for c in skip if c['code']==102] != [['Yes','No']]:
            raise SystemExit('Void skip prompt source changed; no choice sent')
        run('choose_dialog','Yes|No','No')
        run('linear_dialog',754,14,'--source-page',1,'--past-choice')
    world_guard()
    mid,x,y = locate()
    if mid not in range(754,759):
        raise SystemExit('Observed game is not in the pre-Hypno Void maps')
    world_guard()
    # On resume, refresh actual page conditions and runtime actor state once.
    # A new run at754spawn instead verifies its save after the normal shard heal.
    if (mid,x,y)!=(754,31,12):
        run('checkpoint','Void-route-resume')
        sync_lin_override()
        if mid==758 and json.loads(STATE_FILE.read_text()).get('switches',{}).get('1874'):
            raise SystemExit('Hypno already defeated; this helper is only pre-boss')
    start = PHASE_NAMES.index(a.from_phase) if a.from_phase else next(
        i for i,phase in enumerate(PHASES) if phase[1]==mid)
    stop = PHASE_NAMES.index(a.stop_phase)
    if start>stop or PHASES[start][1]!=mid:
        raise SystemExit('Requested phase does not match observed map/stop boundary')
    # Map entrance autoruns may already be complete; no dialogues or choices.
    if mid==754:
        settle(754,8)
    elif mid==755:
        settle(755,5)
    for phase in PHASES[start:stop+1]:
        name, expected, eid, goal, facing, transfer = phase
        world_guard()
        actual,x,y = locate(expected)
        if actual!=expected:
            raise SystemExit(f'Phase{name} expected{expected}, observed{actual}')
        if name!='shard' and not json.loads(STATE_FILE.read_text()).get(
                'self_switches',{}).get('754,5,A'):
            raise SystemExit('Mandatory Light Shard not consumed; resume at shard')
        v = model(expected,(x,y))
        if phase_done(phase,v):
            print('VOID SOURCE-CONFIRMED DONE',name,flush=True)
            continue
        print('VOID PHASE',name,flush=True)
        actual,x,y = walk(expected,goal,a.chunk,transfer)
        if facing is not None:
            world_guard()
            e = v['events'].get(str(eid))
            if e is None:
                raise SystemExit('Target event missing before interaction')
            # .12 matches the existing calibrated route tap. No walking after C.
            if name=='shard':
                act(facing+':.12','wait:1')
                settle(expected,eid)
            elif name=='mudkip':
                fresh = model(expected,(x,y))['events'][str(eid)]['list']
                if [c['parameters'][0] for c in fresh if c['code']==102] != [['Yes','No']]:
                    raise SystemExit('Mudkip starter choice source is not active')
                act(facing+':.12','c','wait:1')
                run('choose_dialog','Yes|No','Yes','--source',expected,eid)
                run('linear_dialog',expected,eid,'--source-page',1,'--past-choice')
            else:
                act(facing+':.12','c','wait:1')
                settle(expected,eid)
            actual,x,y = locate(transfer or expected)
        if actual != (transfer or expected):
            raise SystemExit('Phase transfer mismatch after source dialogue')
        if transfer==755:
            settle(755,5)
        record('phase-completed',phase=name,position=[actual,x,y])
        if name=='shard':
            run('checkpoint','Void-shard-healed')
            sync_lin_override()
            saved = native()
            if saved['map']!=754 or len(saved['party'])!=6 or any(
                    member['hp']!=member['totalhp'] or member['status'] is not None
                    or not full_pp(member) for member in saved['party']):
                raise SystemExit('Native Light Shard healing verification failed')
            prepare_safeguard(saved)
        if name=='hypno-approach':
            if (actual,x,y)!=(758,28,106):
                raise SystemExit('Hypno safe endpoint mismatch')
            run('checkpoint','Void-Hypno-ready')
            saved = native()
            if saved['map']!=758 or saved['position']!=[28,106]:
                raise SystemExit('Native Hypno safe position mismatch')
            prepare_safeguard(saved)
            # If teaching was needed on a resume, save that normal move change.
            if not any(m['move']=='SAFEGUARD' for member in saved['party']
                       if member['species']=='ARCANINE' for m in member['moves']):
                run('checkpoint','Void-Hypno-ready')
            ready = native()
            arc = next((member for member in ready['party']
                        if member['species']=='ARCANINE'),None)
            if ready['position']!=[28,106] or len(ready['party'])!=6 or arc is None \
                    or not {'SAFEGUARD','CRUNCH','MORNINGSUN'} <= {
                        m['move'] for m in arc['moves']} or any(
                        member['hp']!=member['totalhp'] or member['status'] is not None
                        or not hypno_prepared_pp(member) for member in ready['party']):
                raise SystemExit('Final native Hypno preparation verification failed')
            if not full_pp(arc):
                record('hypno-ready-normal-TM-PP-carryover', species='ARCANINE', slot=0,
                       move='SAFEGUARD', current_pp=8, maximum_pp=25, ppup=0,
                       full_pp=False, evidence='Installed Items.rb pbLearnMove bymachine preserves min(old currentPP,new totalPP)')
                print('HYPNO READY: Safeguard8/25 (normal TM carryover); all other moves full PP',flush=True)
            print('SAFE HYPNO APPROACH758[28,106]; BOSS NOT STARTED',flush=True)
    print('VOID BATCH STOPPED AT REQUESTED PHASE',a.stop_phase,flush=True)


if __name__=='__main__':
    main()
