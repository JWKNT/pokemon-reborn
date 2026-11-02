"""Use purchased berries/Power Items and Fly, all through native verified menus."""
from play import ROOT,act
import subprocess,sys,json,time

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
for item,mon,n in [('Hondew Berry','Klinklang',2),('Grepa Berry','Klinklang',1),('Tamato Berry','Klinklang',1),('Qualot Berry','Excadrill',1),('Hondew Berry','Excadrill',1),('Grepa Berry','Excadrill',1)]:
 run('berry_batch.py',item,mon,n)
run('party_take_named.py','Klinklang')
run('give_held.py','Power Weight','Klinklang')
run('give_held.py','Power Bracer','Excadrill')
run('fly_to.py',519)
run('party_front.py','Klinklang')
run('checkpoint.py','Adrienn-Steel-EV-entry')
s=json.loads((ROOT/'notes/Adrienn-Steel-EV-entry-status.json').read_text());p={m['species']:m for m in s['party']}
assert p['KLINKLANG']['ev']==[5,23,3,0,0,0],p['KLINKLANG']['ev']
assert p['EXCADRILL']['ev']==[2,0,0,0,0,11],p['EXCADRILL']['ev']
assert p['KLINKLANG']['item']=='POWERWEIGHT' and p['EXCADRILL']['item']=='POWERBRACER'
run('q.py','519,35,51','519,28,51,up:.12,wait:1')
run('train_wild_bulk.py','Excadrill',0,8,'--hunter','Klinklang','--targets','Rattata,Bidoof,Patrat,Zigzagoon,Meowth,Spinarak,Stunky','--flex-targets','--ev-ledger','--relead-hunter')
print('STEEL EV FIRST BLOCK DONE; HEAL AND VERIFY STATS NEXT',flush=True)
