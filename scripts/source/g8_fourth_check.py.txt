from nav import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('eventq',318,51,'talk');run('choose_dialog','Yes|No','Yes');run('linear_dialog',318,51,'--active','--past-choice')
print('FOURTH CHECK FINISHED; VERIFY ACCEPTANCE BEFORE TRAINER',flush=True)
