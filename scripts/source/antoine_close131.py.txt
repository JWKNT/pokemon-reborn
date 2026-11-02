"""Close observed ordinary victory and save its outside-battle evidence once."""
import subprocess,sys,json,time
from play import ROOT,read
assert 'defeated' in read().lower()
for script,args in [('victory_outro',[]),('trainer_music',['finish','--world-verified']),('checkpoint',['Agate-Antoine-won131'])]:
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{script}.py'),*args],check=True)
s=json.loads((ROOT/'notes/Agate-Antoine-won131-status.json').read_text())
n=json.loads((ROOT/'notes/Agate-Antoine-won131-navigation.json').read_text())
assert s['map']==763 and n['variables']['391']==52 and n['self_switches']['763,49,A'] is True
p=ROOT/'notes/battle-control.json';p.unlink()
print('ORDINARY ANTOINE WIN VERIFIED; NO GAUNTLET START',s['position'],flush=True)
