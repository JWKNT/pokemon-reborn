"""One installed Silva v4 matchup, using the public UI and normal candy reward."""
import json, os, re, subprocess, sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
label = sys.argv[1]
assert re.fullmatch(r'Postgame\d+-Silva\d+', label)
assert not (root / 'notes' / (label + '-status.json')).exists()
env = dict(os.environ, REBORN_FAST_KEYS='1', REBORN_COORD_CACHE='1', REBORN_ROUTE_CHUNK='112')

def run(script, *args):
    print('SILVA ROUND', script, *args, flush=True)
    subprocess.run([sys.executable, str(root / 'scripts' / (script + '.py')), *map(str, args)], env=env, check=True)

foes = ['Xatu', 'Natu', 'Carracosta', 'Weavile', 'Mawile']
(root / 'notes/battle-control.json').write_text(json.dumps({'expected_foes': foes, 'scope': 'Installed Silva v4, Grand Hall common79.'}, indent=2))
run('party_front', 'Zapdos')
run('overworld')
run('eventq', 38, 43, 'talk')
run('trainer_music', 'start', 'PSYCHIC_Male', 'Silva', '--map', 38)
run('choose_dialog', 'Yes|No', 'Yes')
run('trainer_enter', 38, 43, 'PSYCHIC_Male', 'Silva', '--expand-common', '--active-dialogue', '--past-choice', '--resume-intro')
if '--enable-battle-turbo' in sys.argv: run('play', 'm:.12', 'wait:.4')
run('battle_batch', 'Zapdos', 1, '--foes', ','.join(foes), '--turns', 8, '--stay', '--stay-team-reviewed', '--watch', '--min-hp', .35, '--stop-after-victory')
run('grandhall_reward')
run('overworld')
run('trainer_music', 'finish', '--world-verified')
run('checkpoint', label)
state = json.loads((root / 'notes' / (label + '-status.json')).read_text())
assert state['map'] == 38
assert all(mon['hp'] == mon['totalhp'] and mon['status'] is None for mon in state['party'])
print('SILVA REWARD VERIFIED', label, 'XL', state['bag']['contents'].get('EXPCANDYXL'), flush=True)
