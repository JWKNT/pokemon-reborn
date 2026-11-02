from play import *
for i in range(int(sys.argv[1])):
 t=read().lower()
 if 'choose a pok' not in t:raise SystemExit('Party review')
 act('s','wait:0.6','c','wait:1.5')
 t=read().lower()
 if 'candy' not in t or 'moderate' not in t:raise SystemExit('Candy selection review')
 act('c','wait:1.5')
 subprocess.run([sys.executable,str(ROOT/'scripts/candy_progress.py')],check=True)
 print('CANDY DONE',i+1,flush=True)
