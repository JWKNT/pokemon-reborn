"""Record exact full-health team then cross the reviewed Anna-route anomaly trigger."""
import json,os,sys,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];os.environ['REBORN_FAST_KEYS']='1'
def run(s,*a):subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
s=json.loads((R/'notes/Zygarde383-BossEntry-status.json').read_text());n=json.loads((R/'notes/Zygarde383-BossEntry-navigation.json').read_text())
assert s['map']==846 and s['position']==[51,14] and n['variables']['699']==6 and n['switches']['735']
(R/'notes/battle-control.json').write_text(json.dumps(dict(stop=False,expected_foes=['Kyurem','Deoxys','Gyarados','Chansey','Toxapex','Zygarde']),indent=2))
run('major_attempt','start','work/major-220.json',383,'--status','notes/Zygarde383-BossEntry-status.json')
run('trainer_music','start','ZYGARDE','Zygarde','--map',846)
run('play','up','wait:.8')
run('trainer_enter',846,98,'ZYGARDE','Zygarde','--source-page',2,'--active-dialogue','--resume-intro','--post-battle-choices','--burst-dialogue','--log-scripted-bgm')
