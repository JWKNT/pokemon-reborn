"""Reviewed central car entrance and first engine, all native game controls."""
from play import *
def r(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
r('eventq',694,18,'enter');r('settle_arrival',664);r('eventq',664,11,'enter');r('settle_arrival',663)
r('ride_train',663,22,363)
print('FIRST SCRAPYARD ENGINE COMPLETE',flush=True)
