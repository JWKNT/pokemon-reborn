"""Unlock the inspected Beryl door and finish Titania's initial trap scene."""
from play import *
from locate import locate

def run(script, *args):
    subprocess.run([sys.executable, str(ROOT/'scripts'/(script+'.py')),
                    *map(str, args)], check=True)

p = ROOT/'notes/navigation-state.json'
s = json.loads(p.read_text())
assert s['variables'].get('276') == 21, 'Complete the Jasper victory scene first'
if '--in-beryl' not in sys.argv:
    actual = locate(475)
    assert actual[0] == 475
    run('layer_walk', 475, 9, 4, int(s['switches'].get('410', False)), 0)
    began = time.time()
    run('eventq', 475, 21, 'talk')
    run('linear_dialog', 475, 21, '--active', '--burst')
    screens = [json.loads(z) for z in (ROOT/'recordings/screens.jsonl').read_text().splitlines()]
    assert any(z['epoch'] >= began and 'usedtheberylgridkey' in
               re.sub('[^a-z]', '', ' '.join(z['text']).lower()) for z in screens), \
               'Beryl key use needs review'
    s = json.loads(p.read_text()); s['switches']['547'] = False
    p.write_text(json.dumps(s))
    run('wtc_exit', 475, 21)
run('layer_walk', 496, 31, 23, 0, 0)
act('up:.12', 'wait:1.5')
run('linear_dialog', 496, 57, '--burst')
assert locate(476) == (476, 29, 19)
run('checkpoint', 'WTC-Beryl-low')
print('BERYL INITIAL LOW WATER AND SAVE VERIFIED', flush=True)
