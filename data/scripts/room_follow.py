"""Follow a reviewed literal room-transfer plan through normal controls."""
from play import *
from locate import locate
plan=json.loads(pathlib.Path(sys.argv[1]).read_text())
assert locate(plan['start'][0])==tuple(plan['start']),'Reviewed route start mismatch'
for step in plan['transfers']:
 assert step['kind']=='enter'
 subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),str(step['map']),str(step['event']),'enter'],check=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/settle_arrival.py'),str(step['arrival'][0])],check=True)
 actual=locate(step['arrival'][0]);assert actual==tuple(step['arrival']),('Room arrival differs',actual,step)
print('REVIEWED ROOM TRANSFERS COMPLETE',flush=True)
