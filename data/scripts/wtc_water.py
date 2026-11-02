"""Route to a reviewed WTC water button on the upper plane, press and verify transfer."""
from play import *
from locate import locate
from wtc_model import predict
old,eid,new=map(int,sys.argv[1:4]);actual=locate(old);assert actual[0]==old
s=json.loads((ROOT/'notes/navigation-state.json').read_text())
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(old),str(actual[1]),str(actual[2])],stderr=subprocess.DEVNULL));e=v['events'][str(eid)]
assert any(c['code']==122 and c['parameters'][0]in range(256,265)for c in e['list']), 'Not a water-control event'
assert any(c['code']==201 for c in e['list']), 'No control transfer'
assert predict(s,old,eid)[1]==new,'Inspected control destination mismatch; no input sent'
subprocess.run([sys.executable,str(ROOT/'scripts/layer_walk.py'),str(old),str(e['x']),str(e['y']+1),str(int(s['switches'].get('410',False))),'0'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),str(old),str(eid),'talk'],check=True)
if '--scene' in sys.argv:
 i=sys.argv.index('--scene');sm,se=sys.argv[i+1:i+3]
 assert int(sm)==new
 subprocess.run([sys.executable,str(ROOT/'scripts/linear_dialog.py'),sm,se,'--active','--burst'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/wtc_control_notes.py'),str(old),str(eid),str(new)],check=True)
