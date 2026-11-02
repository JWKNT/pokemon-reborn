"""Travel from Sweet Kiss to the Spyce drink counter using reviewed transfers."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('q','256,10,13,down,wait:2')
run('eventq',36,89,'enter')
run('q','29,35,9,up,wait:2')
run('eventq',79,22,'enter')
run('q','517,7,5,up,c,wait:1')
