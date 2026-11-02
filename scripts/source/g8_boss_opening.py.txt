from nav import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('q','318,9,6,up,wait:2','315,9,19,up,wait:2')
run('choose_dialog','Yes|No','Yes')
run('battle_batch','Drapion',0,'--foes','reuniclus,malamar','--watch','--turns',0)
print('BOSS INTRO READY; INSPECT TARGETS BEFORE OPENING',flush=True)
