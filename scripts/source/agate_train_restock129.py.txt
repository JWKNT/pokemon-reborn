"""Execute reviewed ordinary training/restock phases sequentially; stop on any guard."""
import os, subprocess, sys, json
from pathlib import Path
os.environ['REBORN_COORD_CACHE']='1'
ROOT=Path(__file__).resolve().parents[1]
def run(name,*args):
 print('QUEUE STAGE',name,*args,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/(name+'.py')),*map(str,args)],check=True,cwd=ROOT)
def proof(label,spatk_ev):
 d=json.loads((ROOT/'notes'/(label+'-status.json')).read_text())
 c=next(m for m in d['party'] if m['species']=='COFAGRIGUS')
 assert (c.get('natureflag') or c['nature'])=='TIMID' and c['ev']==[172,4,252,spatk_ev,0,2]
 assert [m['move'] for m in c['moves']]==['TRICKROOM','HEX','WILLOWISP','DARKPULSE']
 assert c['item']=='POWERLENS'
proof('Agate-Cofa-training-ready',0)
if '--from-training' not in sys.argv:
 run('fly_to',519,'--carrier','Tranquill')
 run('checkpoint','Agate-Cofa-Opal-ready')
run('agate_prep_phase','training-pilot','--status','notes/Agate-Cofa-Opal-ready-status.json','--execute')
proof('Agate-Cofa-Lens-pilot',32)
run('agate_prep_phase','training-finish','--status','notes/Agate-Cofa-Lens-pilot-status.json','--execute')
proof('Agate-Cofa-EVs-complete',80)
run('agate_supply_queue','--status','notes/Agate-Cofa-EVs-complete-status.json','--execute')
run('agate_prep_phase','finish-lens','--status','notes/Circus-restocked129-status.json','--execute')
print('TRAINING RESTOCK NORMAL QUEUE COMPLETE',flush=True)
