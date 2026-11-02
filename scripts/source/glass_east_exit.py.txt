from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('eventq',732,68,'enter');run('eventq',733,7,'enter');run('eventq',733,18,'enter')
print('OUTDOOR GLASS SUPPLY ORIGIN715',flush=True)
