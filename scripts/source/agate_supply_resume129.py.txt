"""Resume ONLY the recorded department menu OCR stop; no completed route replay."""
import os,json,subprocess,sys,time,hashlib
from pathlib import Path
os.environ['REBORN_COORD_CACHE']='1'
from agate_supply_queue import ROOT,vendor_ready_public,final_proof,source_proof
old=ROOT/'work/agate-shopping-129-journal.json';out=ROOT/'work/agate-shopping-129-resume1.json'
s=json.loads(old.read_text());assert not out.exists()
assert len(s['phases'])==1 and s['phases'][0]['finished_steps']==7 and s['phases'][0]['pending_step']==7 and not s['phases'][0]['receipts']
assert s['stop_reason']=='Expected source merchant Buy/Sell/Quit greeting; no advancement'
before=json.loads(Path(s['status']).read_text());nav=json.loads(Path(s['navigation']).read_text());assert source_proof(nav)==s['proposal']['source_proof']
assert s['proposal']['commands']['dept'][7]=={'script':'vendor-ready','args':[4,4]}
from play import read
vendor_ready_public()
s.update(resumed_from=str(old.relative_to(ROOT)),resumed_from_sha256=hashlib.sha256(old.read_bytes()).hexdigest(),resume_epoch=time.time(),resume_public_reason='Reviewed Buy/Sell/Quit at department8; close crop independently verified; no purchases yet')
def write():out.write_text(json.dumps(s,indent=2)+'\n')
write()
try:
 for phase,commands in s['proposal']['commands'].items():
  if phase=='dept':entry=s['phases'][0];start=7
  else:
   entry={'phase':phase,'state':'pending','entry_epoch':time.time(),'commands':commands,'finished_steps':0,'receipts':[]};s['phases'].append(entry);start=0
  for i,c in enumerate(commands[start:],start):
   entry['pending_step']=i;write()
   if c['script']=='vendor-ready':vendor_ready_public()
   else:
    p=subprocess.run([sys.executable,str(ROOT/'scripts'/(c['script']+'.py')),*map(str,c['args'])],text=True,capture_output=True)
    entry['last_output_tail']=(p.stdout+p.stderr)[-6000:];write()
    if p.returncode:print(entry['last_output_tail'],flush=True);raise RuntimeError('Helper stopped: '+c['script'])
    if c.get('purchase'):
     r=c['purchase'];assert 'PURCHASE VERIFIED '+r['name']+' '+str(r['quantity']) in p.stdout
     entry['receipts'].append(dict(r,verified_epoch=time.time()))
    print('REMAINING QUEUE STEP VERIFIED',phase,c['script'],c['args'],flush=True)
   entry['finished_steps']=i+1;entry.pop('pending_step',None);write()
  entry.update(state='complete',complete_epoch=time.time());write()
 after=json.loads((ROOT/'notes/Circus-restocked129-status.json').read_text());final_proof(before,after,s['proposal']);s.update(verified=True,resume_complete_epoch=time.time());write()
except BaseException as e:
 s.update(resume_stopped_epoch=time.time(),resume_stop_reason=str(e));write();raise
subprocess.run([sys.executable,str(ROOT/'scripts/agate_prep_phase.py'),'finish-lens','--status','notes/Circus-restocked129-status.json','--execute'],check=True)
print('RESTOCK AND FINAL COFA HEAL VERIFIED',flush=True)
