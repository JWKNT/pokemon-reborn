from play import *
def run(s,*a):
 print('RESTOCK RESUME',s,*a,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('eventq',114,6,'enter');run('eventq',113,1,'talk');run('dept_greet');run('dept_floor',1)
run('eventq',112,1,'enter');run('fly_to',519,'--carrier','Zapdos');run('eventq',519,116,'enter')
run('eventq',38,3,'talk');run('heal');run('checkpoint','Aegir369-Supplies')
