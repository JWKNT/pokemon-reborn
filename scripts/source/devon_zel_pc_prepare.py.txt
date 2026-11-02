"""After Arclight, return normally to the PC and prepare/heal the ZEL six."""
from play import ROOT,read,act
from locate import locate
import json,sys,subprocess,re

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
def set_switch(value):
 p=ROOT/'notes/navigation-state.json';d=json.loads(p.read_text());d['switches']['749']=value;p.write_text(json.dumps(d))
state=json.loads((ROOT/'notes/Devon-Arclight-defeated-status.json').read_text())
assert state['story_variables']['339']==36 if '339' in state['story_variables'] else json.loads((ROOT/'notes/navigation-state.json').read_text())['variables']['339']==36
party=[m['name'] for m in state['party']]
assert set(party)=={'Swampert','Arcanine','Cofagrigus','Excadrill','Hexan','Ampharos'},party
run('eventq.py',628,13,'enter');run('eventq.py',628,15,'enter')
run('devon_walk.py',630,27,14,'--go','--conveyors')
assert locate(630)==(630,27,14)
act('up:.12','c:.12','wait:.6');print(read(),flush=True);set_switch(False)
run('devon_walk.py',630,27,26,'--go','--conveyors');run('eventq.py',630,1,'enter');run('eventq.py',628,18,'enter')
for boxslot,incoming,outgoing in [(1,'Mienshao','Swampert'),(6,'Klinklang','Hexan'),(1,'Swampert','Arcanine'),(1,'Arcanine','Cofagrigus'),(1,'Cofagrigus','Excadrill'),(1,'Excadrill','Ampharos'),(1,'Ampharos','Swampert')]:
 slot=party.index(outgoing)
 run('eventq.py',628,22,'talk');run('pc_open_reviewed.py');run('pc_exchange_named.py',boxslot,slot,incoming,outgoing)
 party[slot]=incoming
 print('ZEL NORMAL PC EXCHANGE',incoming,outgoing,flush=True)
run('party_front.py','Klinklang','Arcanine','Excadrill','Mienshao','Ampharos','Cofagrigus')
run('party_open.py');t=read();print(t,flush=True)
pairs=re.findall(r'(?<!\d)(\d{1,3})\s*/\s*(\d{1,3})(?!\d)',t)
assert len(pairs)==6 and all(x==y and int(x)>0 for x,y in pairs),t
run('overworld.py');run('checkpoint.py','Devon-ZEL-roster-ready')
print('ZEL SIX FULLY HEALED VIA PC AND VERIFIED',flush=True)
