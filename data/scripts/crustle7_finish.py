from play import *
for direction,count in [('left',2),('down',5),('right',1),('down',6)]:
 print('CRUSTLE7',direction,count,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/crustle_push.py'),'360','137',direction,str(count)],check=True)
print('CRUSTLE7 PUSHES COMPLETE',flush=True)
