"""Ride one reviewed functional train; verify its Yes/No prompt and world exit."""
from play import *
from locate import locate
m,e,var=map(int,sys.argv[1:4]);statepath=ROOT/'notes/navigation-state.json'
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),'0','0'],stderr=subprocess.DEVNULL));cs=v['events'][str(e)]['list']or[]
assert [c['parameters'][0]for c in cs if c['code']==102]==[['Yes','No']]
assert any(c['code']==122 and c['parameters'][0]==var for c in cs), 'Train has no reviewed advance on this page'
assert 'Full steam ahead?' in str(cs)
subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),str(m),str(e),'talk'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/linear_dialog.py'),str(m),str(e),'--source-page','0','--past-choice','--world-settle','12'],check=True)
actual=locate();assert actual[0]==m,actual
state=json.loads(statepath.read_text());value=2 if var==369 and state['variables'].get('363',0)>=1 else 1
state['variables'][str(var)]=value
if var==367:state['variables']['371']=1
statepath.write_text(json.dumps(state))
print('TRAIN RIDE OBSERVED',m,e,var,actual,flush=True)
