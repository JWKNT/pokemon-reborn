"""Touch an inspected Light Shard through ordinary controls; verify every HP card."""
from layer_route import *
from locate import locate
from surface_plan import surface_plan

mid, eid = map(int, sys.argv[1:3])
actual = locate(mid)
assert actual[0] == mid
state_path = ROOT / 'notes/navigation-state.json'
state = json.loads(state_path.read_text())
ground = bool(state['switches'].get('410', False))
surface='--surface' in sys.argv
model = json.loads(subprocess.check_output(
    ['ruby', str(ROOT/'scripts/route_map.rb'), str(mid), *map(str, actual[1:])],
    stderr=subprocess.DEVNULL))
event = model['events'][str(eid)]
commands = event['list'] or []
assert event['name'] == 'Light Shard' and event['trigger'] == 1
assert any(c['code'] == 314 and c['parameters'] == [0] for c in commands)
assert all(c['code'] in [0, 106, 121, 123, 224, 250, 314] for c in commands)
assert all(c['parameters'][0]==c['parameters'][1] and c['parameters'][2]==0
           for c in commands if c['code']==121), 'Unexpected shard switch operation'
options = []
for key, (dx, dy, _) in DIR.items():
    x, y = event['x']-dx, event['y']-dy
    for target_ground in [False, True]:
        try:
            steps = surface_plan(model,(x,y)) if surface else plan(mid, actual[1], actual[2], ground, x, y, target_ground)
            options.append((len(steps), x, y, target_ground, key))
        except ValueError:
            pass
assert options, 'No reviewed approach to the shard'
_, x, y, target_ground, key = min(options)
if surface:
    subprocess.run([sys.executable,str(ROOT/'scripts/surface_walk.py'),str(mid),str(x),str(y)],check=True)
else:
    subprocess.run([sys.executable, str(ROOT/'scripts/layer_walk.py'), str(mid),
                    str(x), str(y), str(int(ground)), str(int(target_ground))], check=True)
act(key+':.12', 'wait:3')
subprocess.run([sys.executable, str(ROOT/'scripts/party_open.py')], check=True)
text = read()
ratios = re.findall(r'(?<!\d)(\d{1,3})\s*/\s*(\d{1,3})(?!\d)', text)
assert len(ratios) == 6 and all(a == b and int(a) > 0 for a, b in ratios), (
    'Full-party heal needs visual review', text)
subprocess.run([sys.executable, str(ROOT/'scripts/overworld.py')], check=True)
state = json.loads(state_path.read_text())
state.setdefault('self_switches', {})[f'{mid},{eid},A'] = True
for c in commands:
    if c['code']==121:state.setdefault('switches',{})[str(c['parameters'][0])]=True
state_path.write_text(json.dumps(state))
print('LIGHT SHARD FULL PARTY VERIFIED', mid, eid, ratios, flush=True)
