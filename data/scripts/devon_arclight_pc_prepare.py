"""Heal after Victoria and restore Excadrill by seven normal named PC swaps."""
from play import ROOT,read
from locate import locate
import subprocess,sys,json,re

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
assert json.loads((ROOT/'notes/navigation-state.json').read_text())['variables']['339']==33
assert locate(628)[0]==628
run('eventq.py',628,18,'enter')
chain=[(2,'Excadrill','Mienshao'),(0,'Mienshao','Arcanine'),(1,'Arcanine','Cofagrigus'),(3,'Cofagrigus','Klinklang'),(4,'Klinklang','Swampert'),(5,'Swampert','Ampharos'),(0,'Ampharos','Mienshao')]
for i,(slot,incoming,outgoing) in enumerate(chain):
 run('eventq.py',628,22,'talk');run('pc_open_reviewed.py');run('pc_exchange_named.py',1,slot,incoming,outgoing)
 print('DEVON ARCLIGHT STORAGE HEAL',i+1,incoming,outgoing,flush=True)
run('party_front.py','Swampert','Arcanine','Cofagrigus','Excadrill','Klinklang','Ampharos')
run('party_open.py');t=read();print(t,flush=True)
pairs=re.findall(r'(?<!\d)(\d{1,3})\s*/\s*(\d{1,3})(?!\d)',t)
assert len(pairs)==6 and all(x==y and int(x)>0 for x,y in pairs)
run('overworld.py');run('checkpoint.py','Devon-Arclight-ready')
print('DEVON ARCLIGHT ROSTER HEALED AND SAVED',flush=True)
