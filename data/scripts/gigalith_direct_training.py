"""Complete verified partial EVs using normal Strength attacks on weak bats."""
import json,math,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(n,*a):
 print('STAGE',n,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
def mon(label):
 return next(m for m in json.loads((R/'notes'/f'{label}-status.json').read_text())['party']if m['species']=='GIGALITH')
x=mon('Saphira177-Gigalith-partial-HP');assert x['item']=='POWERWEIGHT' and x['ability']=='STURDY' and x['level']==95
assert x['ev'][1:]==[0,0,0,0,0]
remaining=math.ceil((252-x['ev'][0])/32);assert 1<=remaining<=7
print('NATIVE HP EV',x['ev'][0],'remaining knockouts',remaining,flush=True)
run('teach_machine','TMX4','Gigalith','Strength',1,'--single-step',*(['--bag-open'] if '--bag-open' in sys.argv else []))
run('party_front','Gigalith')
def batch(count):run('train_wild_bulk','Gigalith',1,count,'--targets','Noibat,Woobat','--flex-targets','--ev-ledger','--expire-repel','--dense-horizontal')
batch(remaining);run('checkpoint','Saphira-Gigalith-hp-rest');assert mon('Saphira-Gigalith-hp-rest')['ev']==[252,0,0,0,0,0]
run('give_held','Power Bracer','Gigalith');batch(8)
run('teach_machine','TM78','Gigalith','Bulldoze',1,'--single-step')
run('checkpoint','Saphira-Gigalith-attack');assert mon('Saphira-Gigalith-attack')['ev']==[252,252,0,0,0,0]
print('HP AND ATTACK COMPLETE; BULLDOZE RESTORED',flush=True)
