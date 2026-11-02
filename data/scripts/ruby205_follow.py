"""Follow the offline Ruby proposal with normal controls and explicit guards."""
import json,subprocess,sys,os,time
from pathlib import Path
R=Path(__file__).resolve().parents[1];start=int(sys.argv[1]);end=int(sys.argv[2]);proposal=json.loads((R/'work/205-ruby-solution.json').read_text());journal=R/'work/ruby205-progress.jsonl'
def run(script,*a):
 env=dict(os.environ,REBORN_COORD_CACHE='1');env.pop('REBORN_FAST_KEYS',None)
 result=subprocess.run([sys.executable,str(R/'scripts'/f'{script}.py'),*map(str,a)],check=True,env=env,capture_output=script=='victory_gem_cliff_event',text=True)
 if result.stdout:print(result.stdout,flush=True)
 return result.stdout or ''
for i in range(start,min(end,len(proposal['steps']))):
 a=proposal['steps'][i];print('RUBY STEP',i,a,flush=True)
 if a['kind']=='crystal':
  nav=json.loads((R/'notes/navigation-state.json').read_text());assert bool(nav['switches'].get(str(a['switch']),False))!=a['value'],('Unexpected crystal state',a)
  observed=run('victory_gem_cliff_event',803,a['eid'],'talk',*a['stand']);assert 'reacted to the crystal' in observed.lower(), observed[-500:]
  run('dialog','--limit=12')
  nav=json.loads((R/'notes/navigation-state.json').read_text());nav['switches'][str(a['switch'])]=a['value'];nav.setdefault('observed_ruby_toggles',[]).append(dict(epoch=time.time(),event=a['eid'],switch=a['switch'],value=a['value'],evidence='Normal key interaction displayed Key reacted to Crystal then overworld; installed source toggles this switch'))
  (R/'notes/navigation-state.json').write_text(json.dumps(nav))
  nav=json.loads((R/'notes/navigation-state.json').read_text());assert nav['switches'][str(a['switch'])]==a['value']
 else:
  run('victory_gem_cliff_event',803,a['eid'],'approach',*a['stand']);run('ruby204_boulder',a['eid'],a['direction'],a['count'],f'Ruby205-Push-{i}')
 with journal.open('a')as f:f.write(json.dumps(dict(step=i,action=a,epoch=time.time(),status='public action completed'))+'\n')
 if (i+1)%5==0:run('checkpoint',f'Ruby205-Step-{i+1}')
run('checkpoint',f'Ruby205-Queue-{end}')
