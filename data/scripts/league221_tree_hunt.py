"""Bounded visible Headbutt hunting; retain desired birds, flee other inspected tree species."""
from play import *
for attempt in range(8):
 began=time.time();print('TREE ATTEMPT',attempt+1,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/league221_headbutt.py')],check=True)
 t=read().lower();print(t,flush=True)
 if any(z in t for z in ['swablu','altaria']):
  (ROOT/'work/221-target-encounter.json').write_text(json.dumps({'began':began,'public_text':t}));print('TARGET READY',flush=True);break
 if any(z in t for z in ['pineco','forretress','aipom','ambipom']):
  subprocess.run([sys.executable,str(ROOT/'scripts/flee.py'),'--since',str(began)],check=True);continue
 if len(re.sub('[^a-z]','',t).replace('pokemonreborn',''))<3:continue
 raise SystemExit('Unrecognized tree result')
else:raise SystemExit('Hunt bound; inspect before another batch')
