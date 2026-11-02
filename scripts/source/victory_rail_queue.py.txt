"""Run an explicit reviewed map786 rail plan, checking each normal save.

Plans contain cart ids and expected switch/variable/position results derived
from installed event scripts. No game data, saves or memory are modified.
"""
from play import *
import runpy

plan=json.loads(pathlib.Path(sys.argv[1]).read_text())
prefix=sys.argv[2];assert re.fullmatch(r'[A-Za-z0-9-]+',prefix)
def run(name,*args):
 subprocess.run([sys.executable,str(ROOT/'scripts'/(name+'.py')),*map(str,args)],check=True)
run('overworld')
for i,step in enumerate(plan,1):
 state=json.loads((ROOT/'notes/navigation-state.json').read_text())
 assert state['variables'][str(step['var'])]==step['before'],('Unexpected cart state',i)
 if 'lever' in step:
  assert state['switches'][str(step['switch'])]!=step['value'],('Lever already toggled',i)
  run('eventq',786,step['lever'],'talk')
 run('eventq',786,step['cart'],'talk')
 act('wait:10');t=read().lower()
 if any(w in t for w in ['fight','yes','no','used ','would like','repel']):
  raise SystemExit('Rail interruption; inspect public screen: '+t)
 label=f'{prefix}-{i}'
 run('checkpoint',label)
 state=json.loads((ROOT/'notes/navigation-state.json').read_text())
 assert state['variables'][str(step['var'])]==step['after'],('Cart outcome differs',i)
 assert state['positions']['786'][str(step['cart'])]==step['position'],('Cart position differs',i)
 if 'lever' in step:assert state['switches'][str(step['switch'])]==step['value']
 receipt={'epoch':time.time(),'label':label,'step':step,'result':'normal save confirms expected puzzle state'}
 with (ROOT/'notes/victory-rail-actions.jsonl').open('a') as f:f.write(json.dumps(receipt)+'\n')
 print('RAIL STEP VERIFIED',i,step,flush=True)
run('party_open')
