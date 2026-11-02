"""Normal victory closure + one native checkpoint, then fixed-six PC assembly."""
import subprocess,sys,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
from play import read
text=read().lower();assert 'defeated' in text or 'for winning' in text, 'Actual Ricardo victory required'
commands=[('victory_outro',[]),('trainer_music',['finish','--world-verified']),('checkpoint',['Agate-Ricardo-won130']),('agate_party_assemble',['--phase','agate-assemble','--execute','--status','notes/Agate-Ricardo-won130-status.json','--navigation','notes/Agate-Ricardo-won130-navigation.json','--journal','work/agate-party-assemble-130.json'])]
for script,args in commands:
 print('RICARDO POST QUEUE',script,flush=True)
 p=subprocess.run([sys.executable,str(ROOT/'scripts'/f'{script}.py'),*args],capture_output=True,text=True)
 out=ROOT/'work'/f'ricardo-post130-{script}.txt';out.write_text(p.stdout+'\n'+p.stderr)
 print(p.stdout[-1500:],flush=True)
 if p.returncode:print(p.stderr[-2000:],flush=True);raise SystemExit(p.returncode)
