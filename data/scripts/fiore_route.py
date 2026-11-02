"""Execute one explicit, source-reviewed Fiore route; stop on any mismatch."""
from play import *
from locate import locate
plan=json.loads(pathlib.Path(sys.argv[1]).read_text())
begin=int(sys.argv[sys.argv.index('--from')+1])if '--from'in sys.argv else 0
if begin==0:assert locate(plan['start'][0])==tuple(plan['start'])
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
for i,s in enumerate(plan['segments'][begin:],begin):
 print('FIORE SEGMENT',i,s,flush=True)
 if s['kind']=='walk':
  if s['map']in[678,679]:run('surface_walk',s['map'],*s['target'],'--hold-straights')
  else:
   try:run('q',','.join(map(str,[s['map'],*s['target']])))
   except subprocess.CalledProcessError:
    actual=locate(s['map']);assert actual==(s['map'],*s['target']),actual
    print('WALK ENDPOINT VERIFIED AFTER OCR INTERRUPTION',actual,flush=True)
 elif s['kind']=='portal':
  run('surface_event'if s['map']in[678,679]else'eventq',s['map'],s['event'],'enter')
  run('settle_arrival',s['arrival'][0]);assert locate(s['arrival'][0])==tuple(s['arrival'])
 elif s['kind']=='dive':run('dive_transition',*s['from'],s['arrival'][0])
 elif s['kind']=='waterfall':run('waterfall_step',s['map'],*s['from'],s['direction'],*s['arrival'])
 else:raise SystemExit('Unreviewed Fiore segment')
assert locate(plan['goal'][0])==tuple(plan['goal']);print('FIORE ROUTE COMPLETE',flush=True)
