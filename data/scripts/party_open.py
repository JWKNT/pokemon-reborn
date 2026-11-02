"""Swap party lead with an explicitly chosen slot; requires Pokemon remembered in main menu."""
from play import *
import re
act('x','wait:0.5','c','wait:1.6');t=read().lower()
if 'field notes' in t and 'region map' in t and 'pulse dex' in t:
 # Pokégear was the remembered main-menu command after a roamer map check.
 act('x','wait:1.5','up','wait:.2','up','wait:.2','c','wait:1.6');t=read().lower()
if 'would you like to save' in t:
 act('x','wait:2','x','wait:2','x','wait:2',*(['up:0.22']*4),'c','wait:2');t=read().lower()
if 'pokedex' in t and ('seen' in t or 'search' in t):
 act('x','wait:1.5','down','c','wait:1.6');t=read().lower()
if sum(bool(re.match(r't[mh][a-z0-9]',z.strip())) for z in t.splitlines())>=3 or ('sort' in t and any(k in t for k in ['medicine','medieine','items','berries'])) or 'sort a:' in t or ('close bag' in t) or ('rock smash' in t and any(w in t for w in ['charge beam','safeguard','nature power'])):
 act('x','wait:1.5','up','c','wait:1.6');t=read().lower()
# A moving hazard can swallow the menu key. Retry only a verified empty
# overworld frame; never press through dialogue, choices or another menu.
for retry in range(3):
 if 'cancel' in t and (t.count('hp')>=5 or ('choose a pok' in t and t.count('hp')>=1)):break
 if re.sub(r'[^a-z]', '', t) not in ['', 'pokemonreborn']:break
 act('x','wait:.8','c','wait:1.6');t=read().lower()
if not ('cancel' in t and (t.count('hp')>=5 or ('choose a pok' in t and t.count('hp')>=1))):raise SystemExit('Party entry review: '+t)
print(read(),flush=True)
