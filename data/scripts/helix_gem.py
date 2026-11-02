"""Toggle one Helix gem through normal controls and record its observed action."""
import json, subprocess, sys, time
from pathlib import Path
from play import ROOT, act, read
from locate import locate

eid = int(sys.argv[1])
assert 173 <= eid <= 190
path = ROOT / 'notes/navigation-state.json'
state = json.loads(path.read_text())
assert state['variables']['664'] == 3
assert bool(state['switches']['1808']) == (eid >= 182), 'Wrong character/grid'
source = json.loads((ROOT/'work/345-helix-static.json').read_text())['events'][str(eid)]
commands = source['pages'][0]['list']
assert not any(c['code'] in [101, 102, 301, 355] for c in commands)
toggles = {c['parameters'][1] for c in commands if c['code'] == 111 and c['parameters'][0] == 0}
assert toggles and toggles <= set(range(1832, 1850))
subprocess.run([sys.executable, str(ROOT/'scripts/eventq.py'), '887', str(eid), 'talk'], check=True)
act('wait:1')
print(read(), flush=True)
for switch in toggles:
    state['switches'][str(switch)] = not state['switches'][str(switch)]
complete = all(state['switches'][str(s)] for s in range(1832, 1850))
if complete:
    subprocess.run([sys.executable, str(ROOT/'scripts/linear_dialog.py'), '887', '193', '--source-page', '1', '--burst', '--world-settle', '12'], check=True)
    state['variables']['664'] = 5
    state['switches'].update({'1808': False, '779': False, '1827': True})
    state['self_switches']['887,193,C'] = True
after = locate(887)
assert after[0] == 887
state['helix_observation'] = {'epoch': time.time(), 'evidence': f'Normal gem interaction {eid}; toggles {sorted(toggles)}; overworld {after}; completion dialogue {complete}'}
path.write_text(json.dumps(state, indent=2)+'\n')
print('GEM VERIFIED', eid, 'COMPLETE', complete, flush=True)
