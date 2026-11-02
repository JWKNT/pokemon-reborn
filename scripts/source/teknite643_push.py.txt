"""One reviewed ridge push; verify actual boulder position from a normal save."""
from play import *
from locate import locate
plan=json.loads((ROOT/'work/223-teknite643-boulder-plan.json').read_text());i=int(sys.argv[1]);assert 0<=i<3
step=plan['pushes'][i];eid=str(step['event'])
n=json.loads((ROOT/'notes/navigation-state.json').read_text());assert n['positions']['643'][eid]==step['box_from'], 'Boulder initial position differs'
subprocess.run([sys.executable,str(ROOT/'scripts/teknite_point.py'),'643,'+','.join(map(str,step['from']))],check=True)
act(step['direction']+':.12','wait:2');print(read(),flush=True)
label=(sys.argv[sys.argv.index('--label-prefix')+1] if '--label-prefix' in sys.argv else 'League223-RidgePush')+str(i+1)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),label],check=True)
n=json.loads((ROOT/'notes/navigation-state.json').read_text());actual=n['positions']['643'][eid]
expected=step['box_to'] if not step['erased_drop'] else [21,22]
assert actual==expected,('Observed ridge boulder differs',actual,expected)
print('RIDGE PUSH VERIFIED',eid,actual,flush=True)
