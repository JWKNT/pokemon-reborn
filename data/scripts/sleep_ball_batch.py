"""Throw up to six Timer Balls at a reviewed sleeping genie; stop on waking/low HP."""
from play import *
from public_owned_hp import read as owned_hp
foe=sys.argv[1];limit=int(sys.argv[2]);assert foe in ['Landorus','Thundurus','Tornadus','Meloetta'] and 1<=limit<=6
for _ in range(limit):
 rows=snap();t=' '.join(r['text'] for r in rows);low=t.lower();print(t,flush=True)
 if any(s in low for s in ['gotcha','was caught','nickname','pokedex','party is full']):break
 assert 'fight' in low and re.search(r'\b(?:bag|bae)\b',low),'Public command required'
 prompt=' '.join(r['text'] for r in rows if r['y']>.72 and r['x']<.5)
 assert 'amoonguss' in re.sub('[^a-z]','',prompt.lower()),prompt
 enemy=' '.join(r['text'] for r in rows if r['y']<.37).lower()
 assert foe.lower() in enemy,enemy
 if not re.search(r'\bsl(?:p|f)[a-z]*/?\s*(?:hp)?',enemy):print('AWAKE: root review',flush=True);break
 hp=owned_hp(rows,487 if foe=='Meloetta' else 467)
 if hp<(350 if foe=='Meloetta' else 250):print('LOW HP: root review',hp,flush=True);break
 subprocess.run([sys.executable,str(ROOT/'scripts/throw_ball.py'),'Timer Ball'],check=True)
 rows=snap();low=' '.join(r['text'] for r in rows).lower()
 if any(s in low for s in ['gotcha','was caught','nickname','pokedex','party is full']):break
 subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
