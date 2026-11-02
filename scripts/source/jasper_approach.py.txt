"""Reviewed Lapis-key to Jasper-double approach, using normal inputs only."""
from play import *
from locate import locate

def run(script, *args):
    subprocess.run([sys.executable, str(ROOT/'scripts'/(script+'.py')),
                    *map(str, args)], check=True)

if '--from-scene' not in sys.argv:
    run('layer_walk', 468, 10, 26, 0, 0)
    run('wtc_exit', 468, 25)
    run('layer_walk', 474, 6, 24, 0, 0)
    run('wtc_exit', 474, 27)
    run('layer_walk', 494, 26, 4, 0, 0)
    act('left:.12', 'wait:1.5')
run('linear_dialog', 494, 29, '--follow-source', 475, 37, '--burst')
actual = locate(475)
assert actual[0] == 475
p = ROOT/'notes/navigation-state.json'
s = json.loads(p.read_text())
# Installed 494/29 lowers into 475; completed 475/37 sets these two flags.
s['variables'].update({'263': 0, '276': 20})
s['switches']['547'] = True
s.get('positions', {}).pop('475', None)
p.write_text(json.dumps(s))
run('touch_heal', 475, 51)
run('party_lead', 'Hexan')
run('party_lead', 'Arcanine')
run('layer_walk', 475, 11, 11, 1, 0)
run('trainer_enter', 475, 40, 'NWCultist', 'Ichorus & Lyla')
print('JASPER DOUBLE FIRST COMMAND READY', flush=True)
