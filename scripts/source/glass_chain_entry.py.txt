"""Native pre-chain save, normal door entry, and observed first battle command."""
from play import *
from locate import locate
import argparse
p=argparse.ArgumentParser();p.add_argument('session',type=int);p.add_argument('attempt',type=int);a=p.parse_args()
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
assert locate(732)==(732,38,9),'Need the reviewed safe approach tile'
label=f'Glass-pre-gauntlet-attempt-{a.attempt}'
run('checkpoint',label)
status=ROOT/'notes'/f'{label}-status.json';v=json.loads(status.read_text())
assert [m['name']for m in v['party']]==['Arcanine','Klinklang','Swampert','Mienshao','Cofagrigus','Excadrill']
assert all(m['level']==90 and m['hp']==m['totalhp'] and not m.get('status')for m in v['party'])
expected={'Arcanine':[8,24,24,8],'Klinklang':[15,10,15,10],'Swampert':[15,10,15,20],'Mienshao':[10,10,10,15],'Cofagrigus':[5,15,15,5],'Excadrill':[10,15,10,20]}
assert all([x['pp']for x in m['moves']]==expected[m['name']]for m in v['party'])
run('eventq',732,74,'enter')
run('major_enter',ROOT/'work/major-122.json',a.session,734,12,'--status',status,'--active-dialogue')
t=read().lower();assert 'fight'in t and 'bag'in t and 'arcanine'in t,'First battle command required'
c=ROOT/'notes/current-run-control.json';control=json.loads(c.read_text())
if control.get('battle_turbo_enabled_epoch') is None:
 act('m:.12','wait:.5');control['battle_turbo_enabled_epoch']=time.time();control['battle_turbo_evidence']='First M after current app launch, at verified Glass round1 command; battle-only turbo.';c.write_text(json.dumps(control,indent=2))
print('GLASS ROUND1 READY',read(),flush=True)
