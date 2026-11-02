from play import *
from learning import resolve
evolving=False
for i in range(100):
 t=read();l=' '.join(t.lower().split());print(i,l,flush=True)
 # Once the last candy is consumed, selection returns to the bag. Item
 # descriptions containing "attack" are not a level-up confirmation.
 if 'sort' in l and any(z in l for z in ['medicine','medieine','nedicine','close bag','close boc','close aoc','cloce boc','cloce aog']):break
 if 'how many do you want to use?' in l:
  if not any(z in l for z in [':001',': 001']):raise SystemExit('Candy quantity needs review')
  act('c','wait:.7');continue
 if 'evol' in l:evolving=True
 if evolving and (len(l)<25 or 'what?'==l):act('wait:1');continue
 if 'trying to' in l:
  if not resolve(t):raise SystemExit('Unknown move')
  continue
 if 'you used your last' in l:
  act('c','wait:0.6');continue
 if i<2 and 'do what with' in l:
  act('wait:1');continue
 if any(w in l for w in ['close bag','close boc','close aoc','choose a pok','do what with','on which']) and not any(w in l for w in ['gained','level','max. hp','max.hp','defense','sp. htk','sp. atk','learned','forgot','poof']):break
 if any(w in l for w in ['gained','level','grew to','max. hp','max.hp','attack','evol','learned','did not learn','poof','forgot','and..']):act('c','wait:0.6');continue
 if i>1:print('CANDY REVIEW');break
 act('wait:1')
