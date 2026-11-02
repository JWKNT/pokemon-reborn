"""Resume an ordinary route after explicitly identified wild encounters only."""
from play import *
mid,eid,kind=sys.argv[1:4]
assert int(mid) in [809]
assert int(eid) in [24,25,26,47,48,53]
for attempt in range(8):
 r=subprocess.run([sys.executable,str(ROOT/'scripts/victory_gem_cliff_event.py'),mid,eid,kind],capture_output=True,text=True)
 print(r.stdout,flush=True);print(r.stderr,flush=True)
 if r.returncode==0:break
 if 'wild' not in r.stdout.lower():raise SystemExit('Non-wild route interruption; review')
 subprocess.run([sys.executable,str(ROOT/'scripts/flee.py'),'--since','1791315272.411097'],check=True)
else:raise SystemExit('Eight route interruptions; stop for review')
