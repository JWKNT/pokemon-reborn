"""Execute a reviewed offline WTC push plan; each group verifies actual displacement."""
import json,sys,pathlib,subprocess,itertools
ROOT=pathlib.Path(__file__).resolve().parents[1]
p=json.loads(pathlib.Path(sys.argv[1]).read_text());mid=p['map']
s=json.loads((ROOT/'notes/navigation-state.json').read_text())
if p.get('initial'):
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),'0','0'],stderr=subprocess.DEVNULL))
 assert all([v['events'][k]['x'],v['events'][k]['y']]==xy for k,xy in p['initial'].items()),'Push-plan initial position mismatch'
for (eid,key),group in itertools.groupby(p['pushes'],key=lambda a:(a['event'],a['direction'])):
 group=list(group)
 for start in range(0,len(group),6):
  actions=group[start:start+6]
  subprocess.run([sys.executable,str(ROOT/'scripts/push_trash.py'),str(mid),str(eid),key,str(len(actions))],check=True)
  s=json.loads((ROOT/'notes/navigation-state.json').read_text())
  assert s['positions'][str(mid)][str(eid)]==actions[-1]['box_to'],'Plan endpoint mismatch'
print('REVIEWED PUSH PLAN COMPLETE',mid,p['goals'],flush=True)
