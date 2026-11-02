"""One reviewed repeatable JB v4 fight, reward, heal, and ordinary saved checkpoint."""
from pathlib import Path
import subprocess,sys,json,os,re
R=Path(__file__).resolve().parents[1]
label=sys.argv[1]
assert re.fullmatch(r'Postgame\d+-JB\d+',label), 'Explicit unique postgame training checkpoint required'
assert not (R/'notes'/f'{label}-status.json').exists(), 'Checkpoint already exists'
# This originally planned fourth Walrein round can be skipped once the
# previous ordinary checkpoint proves enough owned candy, conservatively
# using the minimum EXP at the saved level (no native battle/runtime read).
if label=='Postgame244-JB8':
 assert not (R/'work/active-trainer-music.json').exists()
 prior=json.loads((R/'notes/Postgame244-JB7-status.json').read_text())
 wal=next(m for m in prior['party'] if m['species']=='WALREIN')
 def medium_slow(n):return (6*n*n*n)//5-15*n*n+100*n-140
 import math
 needed=math.ceil((medium_slow(110)-medium_slow(wal['level']))/30000)
 owned=prior['bag']['contents'].get('EXPCANDYXL',0)
 if owned>=needed:
  print('SKIPPED SURPLUS TRAINING: Walrein',wal['level'],'ownedXL',owned,'maximumNeededXL',needed,flush=True)
  raise SystemExit(0)
e=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*args):
 print('JB ROUND',s,*args,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,args)],env=e,check=True)
control_path=R/'notes/battle-control.json'
control=json.loads(control_path.read_text());control.update(stop=False,expected_foes=['Greninja','Delphox','Chesnaught','Goodra']);control_path.write_text(json.dumps(control,indent=2)+'\n')
run('party_lead','Zapdos')
run('eventq',38,44,'talk')
run('trainer_music','start','EXPERT_Male','JB','--map',38)
run('choose_dialog','Yes|No','Yes')
run('trainer_enter',38,44,'EXPERT_Male','JB','--expand-common','--active-dialogue','--past-choice','--resume-intro')
run('jb_training_v4')
run('grandhall_reward')
run('overworld')
run('trainer_music','finish','--world-verified')
run('checkpoint',label)
s=json.loads((R/'notes'/f'{label}-status.json').read_text())
assert s['map']==38
assert all(m['hp']==m['totalhp'] and m['status'] is None for m in s['party'])
print('JB ROUND VERIFIED',label,'XL',s['bag']['contents'].get('EXPCANDYXL'),flush=True)
