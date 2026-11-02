"""Finish already-planned normal-UI EV phases, verifying actual saved stats."""
from play import *
def run(s,*args):
 subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
def verify(label,ce,xe):
 run('checkpoint',label)
 j=json.loads((ROOT/'notes'/f'{label}-status.json').read_text());p={x['species']:x for x in j['party']}
 assert p['COFAGRIGUS']['ev'][0]==ce[0] and p['COFAGRIGUS']['ev'][2]==ce[2],p['COFAGRIGUS']
 assert p['CRYOGONAL']['ev']==xe,p['CRYOGONAL']
 print('EV PHASE VERIFIED',label,ce,xe,flush=True)
def train(n):
 run('train_wild_bulk','Cofagrigus',1,n,'--hunter','Hexan','--targets','Meditite,Donphan,Rhydon,Rhyhorn,Boldore,Rockruff','--flex-targets','--grass-pair','--ev-ledger')
train(3)
verify('EV-training-complete',[252,0,252,0,0,0],[252,27,135,41,13,42])
run('party_take_named','Hexan')
run('grass_to_circus_heal')
run('eventq',355,90,'talk');run('mart_open');run('shop_buy','Hyper Potion',6,1000);run('mart_exit')
run('circus_to_blake')
print('DEFENSIVE PREPARATION COMPLETE',flush=True)
