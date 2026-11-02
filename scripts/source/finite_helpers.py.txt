"""Execute an explicit finite list of reviewed normal-control helpers.

No automatic replay or resume. A new plan/journal is required after inspecting a
stopped step. Existing helper guards remain active; capture restart stops the list.
"""
import argparse,json,re,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def health():
 h=json.loads((ROOT/'recordings/capture-health.json').read_text());assert h.get('active')and time.time()-h['epoch']<8,'Fresh recording required';return h
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('journal',type=Path);p.add_argument('--execute',action='store_true');a=p.parse_args()
 steps=json.loads(a.plan.read_text());assert 1<=len(steps)<=80
 for step in steps:
  assert re.fullmatch('[a-z][a-z0-9_]*',step[0])and(ROOT/'scripts'/(step[0]+'.py')).is_file();assert all(type(x)in[str,int,float]for x in step[1:])
 if not a.execute:print(json.dumps(steps,indent=2));return
 from input_owner import acquire
 acquire()
 assert not a.journal.exists();initial=health();data={'plan':str(a.plan.resolve()),'status':'running','events':[]};log=a.journal.with_suffix('.log')
 with log.open('x')as out:
  for i,step in enumerate(steps):
   before=health();assert before['pid']==initial['pid']and before['restart_count']==initial['restart_count'],'Capture changed; review before next input'
   event={'index':i,'helper':step[0],'args':step[1:],'started_epoch':time.time()};data['events'].append(event);a.journal.write_text(json.dumps(data,indent=2)+'\n')
   out.write('START '+repr(step)+'\n');out.flush();r=subprocess.run([sys.executable,str(ROOT/'scripts'/(step[0]+'.py')),*map(str,step[1:])],cwd=ROOT,stdout=out,stderr=subprocess.STDOUT)
   event.update(returncode=r.returncode,ended_epoch=time.time());a.journal.write_text(json.dumps(data,indent=2)+'\n');print('HELPER RETURN',i,step[0],r.returncode,flush=True)
   if r.returncode:break
   after=health()
   if after['restart_count']!=initial['restart_count']:event['capture_restart_review']=True;break
  else:data['status']='completed';a.journal.write_text(json.dumps(data,indent=2)+'\n');print('FINITE LIST COMPLETE',len(steps));return
 data['status']='stopped_for_actual_state_review';a.journal.write_text(json.dumps(data,indent=2)+'\n');raise SystemExit('Inspect log and actual screen; never replay the list')
if __name__=='__main__':main()
