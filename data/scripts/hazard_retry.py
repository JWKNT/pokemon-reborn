"""Retry only an unchanged, normally saved hazard attempt from verified Party.
No hidden runtime reads. A changed result or an unverified screen stops the queue.
"""
import json,os,sys,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
helper,*args=sys.argv[1:]
assert helper in ['victory_hazard_boulder_fast.py','victory_hazard_interact_fast.py']
eid=args[0];label=args[2]if 'boulder'in helper else args[1]
initial=json.loads((R/'notes/navigation-state.json').read_text())
source=json.loads(subprocess.check_output(['ruby',str(R/'scripts/route_map.rb'),'784','0','0'],stderr=subprocess.DEVNULL))
tracked={i for i,e in source['events'].items()if e['name']=='Boulder'}|{'128','132','133','140','141'}
for attempt in range(4):
 began=time.time()
 rc=subprocess.call([sys.executable,str(R/'scripts'/helper),*args],env=dict(os.environ,REBORN_FAST_KEYS='1'))
 if rc==0:raise SystemExit(0)
 checkpoint=R/'notes'/f'{label}-navigation.json'
 if not checkpoint.exists()or checkpoint.stat().st_mtime<began:raise SystemExit('Retry refused: no fresh normal checkpoint')
 now=json.loads(checkpoint.read_text())
 if any(now['positions']['784'].get(i)!=initial['positions']['784'].get(i)for i in tracked):raise SystemExit('Retry refused: an event moved; inspect result before replanning')
 if any(now['variables'].get(str(i))!=initial['variables'].get(str(i))for i in [475,*range(490,501)]) or any(now['switches'].get(str(i))!=initial['switches'].get(str(i))for i in range(1100,1161)):raise SystemExit('Retry refused: puzzle state changed')
 out=subprocess.check_output([sys.executable,str(R/'scripts/play.py')],text=True).lower()
 if not('cancel'in out and out.count('hp')>=5):raise SystemExit('Retry refused: Party not visible')
 print('UNCHANGED NORMAL-SAVE ATTEMPT; RETRY',attempt+2,flush=True)
raise SystemExit('Four unchanged attempts: manual route review needed')
