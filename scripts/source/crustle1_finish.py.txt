from play import *
for direction,count in [('up',1),('right',4),('up',2),('right',3),('up',1),('right',5),('down',2),('right',3)]:
 print('CRUSTLE1',direction,count,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/crustle_push.py'),'358','301',direction,str(count)],check=True)
print('CRUSTLE1 PUSHES COMPLETE',flush=True)
