"""Register the fresh reviewed anomaly attempt, then enter through normal controls."""
import subprocess,sys,json,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
label,session=sys.argv[1],int(sys.argv[2]);cfg='work/major-154.json'
E=dict(os.environ,REBORN_FAST_KEYS='1')
def run(s,*a):subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],env=E,check=True)
s=json.loads((R/'notes'/f'{label}-status.json').read_text());assert s['map']==545 and s['position']==[30,19]
p=R/'notes/battle-control.json';c=json.loads(p.read_text());c.update(stop=False,expected_foes=['Dragonite','Tornadus','Volcanion','Silvally','Hydreigon','Naganadel']);p.write_text(json.dumps(c,indent=2)+'\n')
run('major_attempt','start',cfg,session,'--status',f'notes/{label}-status.json')
run('trainer_music','start','VOLCANION','Volcanion','--map',545)
run('play','up:.12','wait:1')
run('trainer_enter',545,31,'VOLCANION','Volcanion','--source-page',0,'--active-dialogue','--resume-intro')
run('major_battle_intro',cfg,session)
