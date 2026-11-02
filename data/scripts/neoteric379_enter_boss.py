"""Register exact saved team then cross the reviewed Neoteric boss trigger."""
import json,os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ['REBORN_FAST_KEYS']='1'
def run(s,*a):subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
s=json.loads((R/'notes/Neoteric379-BossEntry-status.json').read_text());assert s['map']==895 and s['position']==[55,27]
n=json.loads((R/'notes/Neoteric379-BossEntry-navigation.json').read_text());assert n['variables']['726']==6;print('FROZEN QUEST726',n['variables']['726'],flush=True)
(R/'notes/battle-control.json').write_text(json.dumps(dict(stop=False,expected_foes=['Tyranitar','Terrakion','Kommo-o','Lunala','Groudon','Magearna','Mewtwo','Keldeo','Necrozma','Meloetta','Mew']),indent=2)+'\n')
run('major_attempt','start','work/major-219.json',379,'--status','notes/Neoteric379-BossEntry-status.json')
run('trainer_music','start','MEWTWO','Mewtwo & Mew','--map',895)
run('play','up','wait:1')
run('trainer_enter',895,125,'MEWTWO','Mewtwo & Mew','--source-page',1,'--active-dialogue','--resume-intro','--burst-dialogue')
