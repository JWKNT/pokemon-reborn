"""Advance the inspected Circus PC menus into Box1; never touch passwords."""
from play import *
import unicodedata
for _ in range(10):
 t=unicodedata.normalize('NFKD',read().lower()).encode('ascii','ignore').decode();print(t,flush=True)
 if re.search(r'\bbox\s+\d+\b',t) and ('rattata' in t or 'lu.' in t or 'party' in t):break
 if 'deposit pok' in t and any(s in t for s in ['move pok','hove pok','organize']):act('c:.12','wait:1');break
 if re.search(r'boo?r?ted up the pc',t) or 'storagesystem' in t.replace(' ','') or (any(z in t.replace(' ','') for z in ['logoff','loguff','log0ff']) and any(z in t for z in ['add password','add paseword'])):
  act('c:.12','wait:.7');continue
 raise SystemExit('PC entry review: '+t)
else:raise SystemExit('PC menu limit')
print(read(),flush=True)
