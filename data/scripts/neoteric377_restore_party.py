"""Withdraw the four saved core members and assemble owned Kyogre/Zapdos via normal PC controls."""
from play import *
import difflib

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
def nameok(name,t):
 return re.sub('[^a-z]','',name.lower()) in re.sub('[^a-z]','',t.lower()) or any(difflib.SequenceMatcher(None,name.lower(),w.lower()).ratio()>=.8 for w in t.split())
def withdraw(slot,name):
 keys=['right:.12']*(slot%6)+['down:.12']*(slot//6)
 act(*[v for k in keys for v in (k,'wait:.18')],'wait:.5')
 t=read();print('WITHDRAW TARGET',name,t,flush=True);assert nameok(name,t),t
 act('c','wait:.8');run('choose_dialog','Move|Summary|Multi-Move|Withdraw|Item|Mark|Release|Cancel','Withdraw')
 act('wait:1');t=read();assert 'full'not in t.lower(),t
 keys=['up:.12']*(slot//6)+['left:.12']*(slot%6)
 act(*[v for k in keys for v in (k,'wait:.18')],'wait:.5')
run('pc_open_reviewed');run('pc_select_box',4)
for slot,name in [(4,'Rayquaza'),(0,'Amoonguss'),(1,'Cresselia'),(2,'Magearna')]:withdraw(slot,name)
run('pc_select_box',3)
run('pc_exchange_named',17,0,'Kyogre','Latios','--box',3,'--stay-open')
withdraw(15,'Zapdos')
act('x','wait:.5');run('choose_dialog','Yes|No','No');act('x','wait:.5','x','wait:.5');run('overworld')
run('checkpoint','Neoteric377-Training-team')
s=json.loads((ROOT/'notes/Neoteric377-Training-team-status.json').read_text())
assert [p['species']for p in s['party']]==['KYOGRE','RAYQUAZA','AMOONGUSS','CRESSELIA','MAGEARNA','ZAPDOS'],s['party']
print('OWNED TRAINING PARTY VERIFIED',flush=True)
