"""One reviewed repeatable Anthony v4 fight, reward, heal, and ordinary saved checkpoint."""
from pathlib import Path
import subprocess,sys,json,os,re
R=Path(__file__).resolve().parents[1]
label=sys.argv[1]
assert re.fullmatch(r'Postgame\d+-Anthony\d+',label), 'Explicit unique postgame training checkpoint required'
assert not (R/'notes'/f'{label}-status.json').exists(), 'Checkpoint already exists'
e=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*args):
 print('ANTHONY ROUND',s,*args,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,args)],env=e,check=True)
control_path=R/'notes/battle-control.json'
control=json.loads(control_path.read_text());control.update(stop=False,expected_foes=['Braviary','Goodra','Garchomp']);control_path.write_text(json.dumps(control,indent=2)+'\n')
run('party_lead','Zapdos')
run('eventq',38,49,'talk')
run('trainer_music','start','EXPERT_Male','Anthony','--map',38)
run('choose_dialog','Yes|No','Yes')
run('trainer_enter',38,49,'EXPERT_Male','Anthony','--expand-common','--active-dialogue','--past-choice','--resume-intro')
run('anthony_training_v4')
run('grandhall_reward')
run('overworld')
run('trainer_music','finish','--world-verified')
run('checkpoint',label)
s=json.loads((R/'notes'/f'{label}-status.json').read_text())
assert s['map']==38
assert all(m['hp']==m['totalhp'] and m['status'] is None for m in s['party'])
print('ANTHONY ROUND VERIFIED',label,'XL',s['bag']['contents'].get('EXPCANDYXL'),flush=True)
