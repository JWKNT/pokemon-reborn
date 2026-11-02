"""Close known harmless menus, with transition waits; leave dialogue untouched."""
from play import *
import re
for _ in range(6):
 t=read().lower().replace('res tored','restored')
 if t.count('hp')>=5 and re.search(r'\b(?:becomes|feels) (?:quiet|brave|relaxed|timid|modest|adamant|bold|calm|sassy|jolly)!',t) and 'fight' not in t:act('c','wait:.7')
 elif 'pokedex' in t and 'exit' in t and ('seen' in t or 'search' in t):act('x','wait:1.0')
 elif 'you used your last' in t or (t.count('hp')>=5 and (any(z in t for z in ['recovered','restored','became healthy','was cured','was thawed']) or ('pp' in t and 'maximized' in t)) and 'fight' not in t):
  act('c','wait:.7')
 elif sum(bool(re.match(r't[mh][a-z0-9]',z.strip())) for z in t.splitlines())>=3:
  act('x','wait:1.6')
 elif (('sort' in t and any(k in t for k in ['berries','medicine','medieine','items','key items'])) or 'sort a:' in t or ('rock smash' in t and 'struggle bug' in t and 'thief' in t) or ('close' in t and any(s in t for s in ['bag','boc','bog']))) or ('cancel' in t and (t.count('hp')>=5 or 'teach which' in t)) or any(s in t for s in ['choose a pok','do what with','dex no.','quit game','pokegear']):act('x','wait:1.6')
 elif 'deposit pok' in t and 'move pok' in t and 'seeya' in t:
  act('x','wait:1.2')
 elif len(t.splitlines())<4 or (all(len(s)<20 for s in t.splitlines()) and not any(s in t for s in ['hp','fight','pp:','yes','no'])):act('wait:0.8');break
 else:raise SystemExit('Unrecognized screen: '+t)
print(read())
