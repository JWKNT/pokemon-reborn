"""Heal, restock, verify EVs, and swap training items through native controls."""
from play import ROOT
import subprocess,sys,json

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
run('fly_to.py',519)
run('eventq.py',519,116,'enter')
run('eventq.py',38,3,'talk');run('heal.py')
run('eventq.py',38,5,'talk');run('mart_open.py')
run('shop_buy.py','Ultra Potion',12,1200)
run('shop_buy.py','Full Heal',5,600)
run('mart_exit.py')
run('party_take_named.py','Klinklang');run('party_take_named.py','Excadrill')
run('give_held.py','Power Bracer','Klinklang');run('give_held.py','Power Weight','Excadrill')
run('checkpoint.py','Adrienn-Steel-EV-first-complete')
s=json.loads((ROOT/'notes/Adrienn-Steel-EV-first-complete-status.json').read_text());p={m['species']:m for m in s['party']}
assert p['KLINKLANG']['ev']==[252,23,3,0,0,0],p['KLINKLANG']['ev']
assert p['EXCADRILL']['ev']==[2,252,0,0,0,11],p['EXCADRILL']['ev']
assert all(m['hp']==m['totalhp'] for m in s['party'])
assert s['bag']['contents']['ULTRAPOTION']==12
if '--prepare-only' in sys.argv:
 print('FIRST EV PHASE VERIFIED; READY FOR RECORDING ROTATION',flush=True);raise SystemExit(0)
run('eventq.py',38,6,'enter')
run('party_front.py','Klinklang')
run('q.py','519,35,47','519,25,47')
run('train_wild_bulk.py','Excadrill',0,8,'--hunter','Klinklang','--targets','Rattata,Bidoof,Patrat,Meowth,Spinarak,Stunky','--flex-targets','--ev-ledger','--relead-hunter','--vertical')
print('STEEL EV SECOND BLOCK DONE; HEAL AND VERIFY NEXT',flush=True)
