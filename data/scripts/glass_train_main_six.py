"""Build the owned Glass roster to Lv90 using normal PC and candy menus.
Requires Circus overworld, reviewed Box1 slots and completed Indra training.
Leaves Fly carrier in party; trained Klinklang is stored in Box1 slot12.
"""
from play import *
import math

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def exchange(boxslot,partyslot,incoming,outgoing):
 run('eventq',355,5,'talk');run('pc_open_reviewed');run('pc_exchange_named',boxslot,partyslot,incoming,outgoing)
exchange(6,1,'Klinklang','Hexan')
run('train_candy_one','Klinklang',5,'XL')
exchange(12,1,'Excadrill','Klinklang')
exchange(5,4,'Cofagrigus','Ludicolo')
run('checkpoint','Glass-training-roster')
raw=subprocess.check_output(['ruby','-e',"require_relative 'scripts/read_rgss';v=load_rgss(ARGV[0]);puts JSON.generate(v[:Trainer].instance_variable_get(:@party).map{|p|plain(p).slice('species','name','level','exp')})",str(pathlib.Path.home()/'Library/Application Support/Pokemon Reborn/Game_3.rxdata')],cwd=ROOT,stderr=subprocess.DEVNULL)
party=json.loads(raw);expected=['ARCANINE','EXCADRILL','SWAMPERT','MIENSHAO','COFAGRIGUS','TRANQUILL']
assert [p['species']for p in party]==expected,party
exp90={'ARCANINE':90**3*5//4,'EXCADRILL':90**3,'SWAMPERT':6*90**3//5-15*90**2+100*90-140,'MIENSHAO':6*90**3//5-15*90**2+100*90-140,'COFAGRIGUS':90**3}
for p in party[:5]:
 assert p['level']<=90 and isinstance(p['exp'],int),p
 count=max(0,math.ceil((exp90[p['species']]-p['exp'])/30000))
 assert 0<=count<=5,(p,count)
 print('VERIFIED NATIVE CANDY PLAN',p,'XL',count,flush=True)
 if count:run('train_candy_one',p['name'],count,'XL')
run('give_held','Protective Pads','Mienshao')
run('give_held','Spell Tag','Cofagrigus')
run('checkpoint','Glass-main-six-trained')
print('MAIN FIVE Lv90 NATIVE CHECKPOINT; KLINKLANG Lv90 BOX1 SLOT12',flush=True)
