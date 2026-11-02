"""One inspected Circus challenge, with capture/BGM, roster guards, and reward handling."""
from play import *
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
run('eventq',355,126,'talk')
run('choose_dialog','Yes|No','Yes')
run('trainer_music','start','INDRA','Indra')
run('battle_batch','Arcanine',0,'--foes','Scizor,Empoleon,Ribombee,Hawlucha,Toucannon,Ursaring,Tsareena,Carbink,Castform,Musharna','--turns',0)
run('indra_battle')
run('trainer_music','finish')
run('linear_dialog',355,126,'--active','--past-battle','--past-choice','--burst')
print('INDRA ROUND COMPLETE',flush=True)
