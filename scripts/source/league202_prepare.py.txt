"""Normal berry controls, with frozen-save EV checks after each bounded phase."""
import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(s,*args):
 print('STAGE',s,*args,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,args)],check=True)
def verify(label,species,expected):
 run('checkpoint',label)
 st=json.loads((R/'notes'/f'{label}-status.json').read_text())
 m=next(m for m in st['party'] if m['species']==species)
 assert m['ev']==expected,(species,m['ev'],expected)
 print('SAVED EV VERIFIED',species,expected,flush=True)
phase=sys.argv[1]
if phase=='mienshao':
 for item,n in [('Pomeg Berry',3),('Qualot Berry',3),('Hondew Berry',2),('Grepa Berry',2)]:run('berry_batch',item,'Mienshao',n)
 verify('Prep202-Mienshao-reset','MIENSHAO',[0,79,0,0,0,108])
elif phase=='hexan':
 for item,n in [('Pomeg Berry',9),('Pomeg Berry',4),('Qualot Berry',4)]:run('berry_batch',item,'Hexan',n)
 verify('Prep202-Hexan-reset','CRYOGONAL',[0,0,0,41,0,142])
else:raise SystemExit('Unknown phase')
