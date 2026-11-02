"""Finite normal gym exit and nurse recovery; never replay stopped steps."""
import json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 journal=ROOT/'work/PostHardy138-recovery.json';assert not journal.exists()
 steps=[('eventq',740,1,'enter'),('eventq',739,4,'enter'),('eventq',763,79,'enter'),('eventq',752,4,'talk'),('heal',),('checkpoint','PostHardy138-healed')]
 events=[]
 for i,step in enumerate(steps):
  events.append({'step':i,'helper':step[0],'args':step[1:],'started_epoch':time.time()});journal.write_text(json.dumps(events,indent=2)+'\n')
  r=subprocess.run([sys.executable,str(ROOT/'scripts'/(step[0]+'.py')),*map(str,step[1:])],cwd=ROOT)
  events[-1].update(returncode=r.returncode,ended_epoch=time.time());journal.write_text(json.dumps(events,indent=2)+'\n')
  if r.returncode:raise SystemExit('Stopped after partial step; inspect actual screen before any continuation')
 s=json.loads((ROOT/'notes/PostHardy138-healed-status.json').read_text());assert s['trainer']['badges'].count(True)==17 and all(m['hp']==m['totalhp']for m in s['party']);print('HEALED AT AGATE CENTER',s['map'],s['position'])
if __name__=='__main__':main()
