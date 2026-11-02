from play import *
for direction,count in [('left', 2), ('down', 2), ('right', 1), ('down', 4), ('left', 5), ('up', 5), ('right', 1), ('up', 1)]:
 print('CRUSTLE5 FINAL',direction,count,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/crustle_push.py'),'360','198',direction,str(count)],check=True)
print('CRUSTLE5 FINAL PUSHES COMPLETE',flush=True)
