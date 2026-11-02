"""Continue reviewed Crustle5 route after its first four left pushes."""
from play import *
for direction,count in [('down',4),('left',2),('down',4),('left',1),('down',6),('right',1),('down',8)]:
 print('CRUSTLE5',direction,count,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/crustle_push.py'),'360','198',direction,str(count)],check=True)
print('CRUSTLE5 PART1 COMPLETE',flush=True)
