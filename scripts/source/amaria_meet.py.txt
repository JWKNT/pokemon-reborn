"""Complete one reviewed choice-free maze conversation, then update route notes only."""
from play import *
from locate import locate
m,e,before,after=map(int,sys.argv[1:5]);p=ROOT/'notes/navigation-state.json'
state=json.loads(p.read_text());assert state['variables']['381']==before
model=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),'0','0'],stderr=subprocess.DEVNULL))
cs=model['events'][str(e)]['list']
assert any(c['code']==122 and c['parameters']==[381,381,0,0,after]for c in cs)
assert not any(c['code']in[102,103,104,301]or 'Battle('in str(c['parameters'])for c in cs)
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('eventq',m,e,'talk')
assert 'amaria'in read().lower(),'No visible Amaria dialogue; route notes unchanged'
run('linear_dialog',m,e,'--active','--burst')
observed=locate(m);assert observed[0]==m
state=json.loads(p.read_text());state['variables']['381']=after
state.setdefault('observed_progress',[]).append({'epoch':time.time(),'variable':381,'value':after,'evidence':f'Completed visible choice-free scene {m}/{e}, installed quest assignment, returned to observed overworld {observed}; route notes only.'})
p.write_text(json.dumps(state,indent=2)+'\n');print('OBSERVED MAZE PHASE',after,flush=True)
