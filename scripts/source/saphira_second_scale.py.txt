"""Normal verified route to Route 1 hidden Heart Scale."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ['REBORN_COORD_CACHE']='1'
def run(s,*a):
 print('STAGE',s,*a,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/(s+'.py')),*map(str,a)],check=True,cwd=R)
run('q','292,33,7','292,33,0,up,wait:2','291,0,30,left,wait:2')
run('eventq',287,49,'item')
run('checkpoint','Saphira-HeartScale-two')
