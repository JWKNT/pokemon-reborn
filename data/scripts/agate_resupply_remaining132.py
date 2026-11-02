"""Explicit reviewed remainder of session132 restock; no import-time inputs.

Only --execute sends normal controls. A stopped step is never resumed here.
Root must review its actual endpoint and choose a new journal/start step.
"""
import argparse,json,subprocess
from pathlib import Path
from agate_pc_resupply import Runner,ROOT,CART,final_proof,vendor_ready_public
from agate_party_assemble import FINAL

def main():
 p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');p.add_argument('--start',type=int,required=True);p.add_argument('--journal',type=Path,required=True);p.add_argument('--reviewed-prior',type=Path,required=True)
 a=p.parse_args();a.status=Path('notes/Agate-resume132-status.json');a.navigation=Path('notes/Agate-resume132-navigation.json');a.phase='agate-assemble';a.checkpoint='Agate-restocked-south-ready132'
 steps=[('eventq',752,8,'enter'),('position',763,46,70),('fly_to',520,'--carrier','Tranquill'),('position',520),('eventq',520,101,'enter'),('position',112),('eventq',112,6,'enter'),('position',113),('eventq',113,1,'talk'),('dept_greet',),('dept_floor',8),('position',4),('eventq',4,4,'talk'),('vendor',),('mart_open',)]
 steps += [('shop_buy',name,q,price) for _,name,q,price in CART]
 steps += [('mart_exit',),('position',4),('eventq',4,6,'enter'),('position',113),('eventq',113,1,'talk'),('dept_greet',),('dept_floor',1),('position',112),('eventq',112,1,'enter'),('position',520),('fly_to',763,'--carrier','Tranquill'),('position',763,46,70),('eventq',763,79,'enter'),('position',752,10,10),('exchange',),('arrange',),('nurse',),('eventq',752,8,'enter'),('position',763,46,70),('party',),('checkpoint',a.checkpoint),('proof',)]
 assert 0<=a.start<len(steps)
 print(json.dumps({'start':a.start,'remaining_operations':[s[0] for s in steps[a.start:]],'no_replay':'Root-reviewed fresh actual endpoint required'}),flush=True)
 if not a.execute:return
 prior=json.loads(a.reviewed_prior.read_text())
 if a.start==0:
  assert prior.get('status')=='completed-carrier-ready' and prior.get('verified') is True, 'Start0 is solely AFTER the completed original PC exchange'
  receipts=[e for e in prior['events'] if e.get('kind')=='ordinary-helper-returned' and e.get('script')=='pc_exchange_named']
  assert len(receipts)==1 and receipts[0]['args']==[11,5,'Tranquill','Hexan'] and 'EXCHANGE COMPLETE Tranquill Hexan' in receipts[0]['stdout'], 'Require exact original exchange receipt; this script does not repeat that exchange'
 else:
  assert prior.get('status')=='stopped-for-actual-state-review', 'Nonzero start requires explicit review of a stopped remainder journal'
  begun=[e for e in prior['events'] if e['kind']=='remaining-step-started']
  assert begun, 'Prior remainder has no identified stopped step'
  stopped=begun[-1];pending=prior.get('pending')
  if a.start==stopped['index']+1:
   diagnostics=[e for e in prior['events'] if e['kind']=='ordinary-helper-diagnostic' and e.get('script')==stopped['operation'] and e.get('args')==stopped['args']]
   assert diagnostics and diagnostics[-1]['returncode']==0 and prior['events'][-1]['reason']=='Capture restarted; stop and review actual endpoint, never replay', 'Skip only a successful helper stopped by capture-change review'
   assert steps[a.start][0]=='position', 'The next step must independently verify the actual endpoint before inputs'
  else:assert a.start==stopped['index'] and not pending and steps[a.start][0] in {'position','proof'}, 'Cannot replay pending input or purchases'
 s=json.loads(a.status.read_text());n=json.loads(a.navigation.read_text());r=Runner(a,s,n,{'actual_resume_step':a.start,'remaining_steps':steps[a.start:]})
 names={m['species']:m['name'] for m in s['party']};r.expected=[names[k] for k in FINAL];r.expected[5]='Tranquill' if a.start<=32 else 'Hexan'
 try:
  if a.start==0:
   r.position(752,(752,14,4));r.party_check();r.position(752,(752,14,4))
  for i,(op,*args) in list(enumerate(steps))[a.start:]:
   r.record('remaining-step-started',index=i,operation=op,args=args)
   if op=='position':r.position(args[0],tuple(args) if len(args)==3 else None)
   elif op=='vendor':vendor_ready_public()
   elif op=='exchange':r.exchange_carrier('Hexan','Tranquill')
   elif op=='arrange':r.arrange()
   elif op=='nurse':r.nurse()
   elif op=='party':r.party_check();r.stage(52)
   elif op=='proof':
    sp=ROOT/'notes'/f'{a.checkpoint}-status.json';np=ROOT/'notes'/f'{a.checkpoint}-navigation.json'
    code="require_relative 'scripts/read_rgss'; h=load_rgss('/Applications/Reborn.app/Contents/Game/Data/moves.dat'); puts JSON.generate(h.transform_values{|m|m.instance_variable_get(:@maxpp)})"
    maxima=json.loads(subprocess.check_output(['ruby','-e',code],cwd=ROOT,stderr=subprocess.DEVNULL))
    final_proof(s,json.loads(sp.read_text()),json.loads(np.read_text()),maxima)
   else:r.run(op,*args)
   r.record('remaining-step-completed',index=i,operation=op)
  r.journal.update(status='completed-safe-supply-trip',verified=True);r.write();print('RESTOCKED: exact4350 cart, fullHP/PP fixedsix, stage52 safe',flush=True)
 except BaseException as e:
  r.journal.update(status='stopped-for-actual-state-review',verified=False);r.record('stop',reason=str(e));raise

if __name__=='__main__':main()
