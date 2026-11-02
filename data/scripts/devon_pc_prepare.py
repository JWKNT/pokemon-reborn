"""Use Devon's normal storage PC to heal and prepare the Victoria roster.
Requires the observed phase28 PC room; never changes saves or game data.
Seven named storage swaps heal the outgoing Pokemon under normal19.5 rules.
"""
from play import ROOT,read
from locate import locate
import subprocess,sys,json,re

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
v=json.loads((ROOT/'notes/navigation-state.json').read_text())
assert v['variables']['339']==28,'Devon PC-room phase required'
assert locate(628)[0]==628
chain=[(1,'Cofagrigus','Excadrill'),(0,'Excadrill','Arcanine'),(2,'Arcanine','Mienshao'),(3,'Mienshao','Klinklang'),(4,'Klinklang','Swampert'),(5,'Swampert','Ampharos'),(0,'Ampharos','Excadrill')]
for i,(slot,incoming,outgoing)in enumerate(chain):
 run('eventq.py',628,22,'talk')
 run('pc_open_reviewed.py')
 run('pc_exchange_named.py',1,slot,incoming,outgoing)
 print('DEVON STORAGE HEAL',i+1,incoming,outgoing,flush=True)
run('party_front.py','Arcanine','Cofagrigus','Mienshao','Klinklang','Swampert','Ampharos')
run('party_open.py');t=read();print(t,flush=True)
pairs=re.findall(r'(?<!\d)(\d{1,3})\s*/\s*(\d{1,3})(?!\d)',t)
assert len(pairs)==6 and all(x==y and int(x)>0 for x,y in pairs),'Full-party heal requires review'
run('overworld.py')
run('checkpoint.py','Devon-Victoria-ready')
print('DEVON VICTORIA ROSTER FULLY HEALED AND SAVED',flush=True)
