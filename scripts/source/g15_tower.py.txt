"""Read four native tower placards, reveal books, then climb toward Titania's scene."""
from play import *
from locate import locate
def r(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
def phase(value,evidence):
 p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s['variables']['381']=value;s.setdefault('observed_progress',[]).append({'epoch':time.time(),'variable':381,'value':value,'evidence':evidence});p.write_text(json.dumps(s))
def walk(m,x,y,tail=None):
 f=ROOT/'work/g15-tower-next.json';f.write_text(json.dumps([[m,0,0,x,y]+([tail] if tail else [])]));r('queue_route',f)
assert locate(699)==(699,6,4)
phase(3,'Observed Lin fall into tower, literal source transfer.')
for event,y,stairs,arrival,count in [(1,9,19,(2,28),4),(2,31,17,(9,49),5),(3,52,15,(2,71),6),(4,74,None,None,7)]:
 walk(699,6,y,['up:.12','c','wait:.8']);r('linear_dialog',699,event,'--source-page',0)
 phase(count,f'Read tower placard {event} via normal action, native source one-time increment.')
 if stairs:
  r('eventq',699,stairs,'enter');r('settle_arrival',699);assert locate(699)==(699,*arrival)
r('eventq',699,13,'enter');r('settle_arrival',699);assert locate(699)==(699,9,6)
phase(8,'Four placards read and native stairs set phase8, book bridge becomes visible.')
r('eventq',699,5,'enter');r('settle_arrival',699)
r('eventq',699,22,'enter');r('settle_arrival',700)
print('TOWER WINDOW COMPLETE',flush=True)
f=ROOT/'work/g15-tower-climb.json';f.write_text(json.dumps([[700,0,0,39,21]]))
rc=subprocess.call([sys.executable,str(ROOT/'scripts/queue_route.py'),str(f)]);assert rc in [0,2]
t=read().lower()
if 'taka' in t or 'up here' in t or t.strip() in ['pokemon reborn\naster!','aster!']:
 r('linear_dialog',700,45,'--source-page',1,'--burst')
 p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s['variables']['362']=20;p.write_text(json.dumps(s))
 rc=subprocess.call([sys.executable,str(ROOT/'scripts/queue_route.py'),str(f)]);assert rc in [0,2]
r('linear_dialog',700,48,'--source-page',1,'--until-choice','--log-scripted-bgm')
phase(9,'Reached Titania trust choice after native trigger700E47.')
r('choose_dialog','Yes|No','Yes','--source',700,48)
r('linear_dialog',700,48,'--source-page',1,'--past-choice','--log-scripted-bgm')
phase(10,'Trusted Titania and received Sapphire Bracelets.')
r('eventq',700,49,'enter');r('settle_arrival',701)
print('BELLY OF THE BEAST ENTRY COMPLETE',flush=True)
