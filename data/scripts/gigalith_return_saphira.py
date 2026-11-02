"""Leave the verified Railnet training strip, buy supplies, restore battle six."""
import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(n,*args):
 print('STAGE',n,*args,flush=True)
 e=dict(os.environ,REBORN_COORD_CACHE='1');e.pop('REBORN_FAST_KEYS',None)
 if n in ['q','eventq']:e['REBORN_FAST_KEYS']='1'
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,args)],check=True,env=e)
if '--repel-bag-open' not in sys.argv:run('take_held','Gigalith','Power Bracer')
run('field_repel','Super Repel',*(['--bag-open'] if '--repel-bag-open' in sys.argv else []))
run('eventq',633,3,'enter')
run('fly_to',519,'--carrier','Tranquill')
run('eventq',519,116,'enter');run('eventq',38,5,'talk');run('mart_open')
run('shop_buy','Max Potion',5,2500);run('mart_exit');run('eventq',38,6,'enter')
run('fly_to',414,'--carrier','Tranquill')
run('eventq',414,22,'enter');run('eventq',772,7,'talk');run('pc_open_reviewed')
run('pc_exchange_named',12,5,'Excadrill','Tranquill')
run('give_held','Fairy Gem','Sylveon')
run('party_front','Sylveon','Arcanine','Cofagrigus','Swampert','Gigalith','Excadrill')
run('saphira_return_trained')
s=json.loads((R/'notes/Saphira-return-trained-ready-status.json').read_text())
assert [m['species']for m in s['party']]==['SYLVEON','ARCANINE','COFAGRIGUS','SWAMPERT','GIGALITH','EXCADRILL']
assert all(m['hp']==m['totalhp'] and m['level']==95 for m in s['party'])
g=next(m for m in s['party']if m['species']=='GIGALITH');assert g['ev']==[252,252,0,0,0,0] and g['ability']=='STURDY' and g['item'] is None
assert s['bag']['contents']['MAXPOTION']>=5
print('BATTLE PARTY READY; NO BATTLE STARTED',flush=True)
