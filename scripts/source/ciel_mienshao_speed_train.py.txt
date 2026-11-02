"""Two reviewed speed KOs with a Ghost pivot; normal game menus only."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('party_take_named','Hexan')
run('give_held','Power Anklet','Mienshao');run('party_lead','Mienshao')
run('train_wild_bulk','Cofagrigus',1,2,'--hunter','Mienshao','--targets','Meditite,Mienfoo','--flex-targets','--grass-pair','--expire-repel','--ev-ledger')
run('party_take_named','Mienshao');run('party_lead','Cofagrigus')
print('TRAINING FINISHED — FREE NURSE HEAL AND SAVED STAT RECONCILIATION STILL REQUIRED',flush=True)
