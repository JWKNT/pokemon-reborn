"""Reviewed ice crossings and Bruno's story encounter, through normal input."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def mirror(n,value):
 p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s['variables'][str(n)]=value;p.write_text(json.dumps(s))
for x,y,e,var in [(28,36,88,398),(16,33,90,399),(8,36,92,400)]:
 run('layer_walk',732,x,y,0,0)
 run('eventq',732,e,'talk');run('linear_dialog',732,e,'--active');mirror(var,90)
run('layer_walk',732,10,24,0,0)
run('party_front','Swampert')
rc=subprocess.call([sys.executable,str(ROOT/'scripts/eventq.py'),'732','93','talk']);assert rc in[0,2]
run('choose_dialog','Yes|No','Yes','--source',732,93)
run('trainer_enter',732,93,'MeteorAceM','Bruno','--active-dialogue','--past-choice')
run('trainer_plan',ROOT/'work/glass-bruno-plan.json',ROOT/'work/glass-bruno-live.log','--stop-after-battle')
run('linear_dialog',732,93,'--source-page',0,'--past-battle','--after-last-battle','--burst','--world-settle',15)
run('trainer_music','finish','--world-verified');mirror(391,21)
print('BRUNO DEFEATED; NEXT ESPEON ROOM GLASS55',flush=True)
