"""Throw one named ball through the ordinary bag; stop for capture/party decisions."""
from play import *
item=' '.join(sys.argv[1:]) or 'Poke Ball'
subprocess.run([sys.executable,str(ROOT/'scripts/battle_bag.py')],check=True)
for _ in range(9):
 t=read().lower()
 if ('balls' in t or 'balla' in t) and ('sort' in t or 'close bag' in t):break
 act('right:0.22','wait:0.5')
else:raise SystemExit('Ball pocket review')
subprocess.run([sys.executable,str(ROOT/'scripts/bag_select.py'),item],check=True)
act('c','wait:0.6');t=read();print(t,flush=True)
if not any(z.strip(' •›>').lower() in ['use','lse','uee','uise'] for z in t.splitlines()):raise SystemExit('Ball Use menu review')
act('c','wait:1')
missed=False;empty_after_miss=0
for _ in range(40):
 t=read();print(t,flush=True);low=t.lower()
 missed=missed or any(s in low for s in ['broke free','so close','appeared to be caught','almost had it'])
 empty_after_miss=empty_after_miss+1 if missed and re.sub('[^a-z]','',low) in ['', 'pokemonreborn'] else 0
 if empty_after_miss>=3:
  print('Post-throw overworld boundary verified after failed ball; encounter ended',flush=True);break
 if "hp was restored" in low:raise SystemExit('Enemy restored HP: review weakening before another throw')
 if any(s in low for s in ['gotcha','caught','nickname','pokedex','party is full','add to your','fight','fled!']):break
 if 'fainted' in low or 'choose a pok' in low or 'use next pok' in low:raise SystemExit('Battle ended during capture')
 act('wait:0.5')
else:raise SystemExit('Capture animation timeout')
