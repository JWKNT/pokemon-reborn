"""One installed Jace v4 matchup, using the public UI and normal candy reward."""
import json, os, re, subprocess, sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
label = sys.argv[1]
assert re.fullmatch(r'Postgame\d+-Jace\d+', label)
assert not (root / 'notes' / (label + '-status.json')).exists()
env = dict(os.environ, REBORN_FAST_KEYS='1', REBORN_COORD_CACHE='1', REBORN_ROUTE_CHUNK='112')

def run(script, *args):
    print('JACE ROUND', script, *args, flush=True)
    subprocess.run([sys.executable, str(root / 'scripts' / (script + '.py')), *map(str, args)], env=env, check=True)

foes = ['Drifblim', 'Watchog', 'Cherrim', 'Comfey', 'Bisharp']
(root / 'notes/battle-control.json').write_text(json.dumps({'expected_foes': foes, 'scope': 'Installed Jace v4, Grand Hall common79.'}, indent=2))
run('party_front', 'Magearna')
run('overworld')
run('eventq', 38, 42, 'talk')
run('trainer_music', 'start', 'COOLTRAINER_Male', 'Jace', '--map', 38)
run('choose_dialog', 'Yes|No', 'Yes')
run('trainer_enter', 38, 42, 'COOLTRAINER_Male', 'Jace', '--expand-common', '--active-dialogue', '--past-choice', '--resume-intro')
run('battle_batch', 'Magearna', 0, '--foes', ','.join(foes), '--turns', 8, '--stay', '--stay-team-reviewed', '--watch', '--min-hp', .35, '--stop-after-victory')
run('grandhall_reward')
run('overworld')
run('trainer_music', 'finish', '--world-verified')
run('checkpoint', label)
state = json.loads((root / 'notes' / (label + '-status.json')).read_text())
assert state['map'] == 38
assert all(mon['hp'] == mon['totalhp'] and mon['status'] is None for mon in state['party'])
print('JACE REWARD VERIFIED', label, 'XL', state['bag']['contents'].get('EXPCANDYXL'), flush=True)
