from play import *
for direction,count in [('left',5),('down',1),('left',4),('down',2),('right',2),('down',1)]:
 print('CRUSTLE6',direction,count,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/crustle_push.py'),'360','123',direction,str(count)],check=True)
print('CRUSTLE6 PUSHES COMPLETE',flush=True)
