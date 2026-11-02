"""Use a named bag item on an explicitly named party member, then wait for turn end."""
from play import *
item,target=sys.argv[1:3]
pocket=sys.argv[sys.argv.index('--pocket')+1] if '--pocket' in sys.argv else 'Medicine'
active_only=item in {'X Attack','X Defend','X Defense','X Sp. Atk','X Sp. Def','X Speed','X Accuracy','Dire Hit','Guard Spec.'}
normp=lambda z:re.sub('[^a-z]','',z.lower())
if '--bag-open' not in sys.argv:
 subprocess.run([sys.executable,str(ROOT/'scripts/battle_bag.py')],check=True)
for _ in range(9):
 rows=snap();t=' '.join(v['text'] for v in rows).lower()
 if (pocket=='Medicine' and any(w in t for w in ['medicine','medieine','nedicine'])) or any(normp(v['text'])==normp(pocket) for v in rows):break
 act('right','wait:0.4')
else:raise SystemExit(pocket+' pocket review')
# Use the installed seven-row viewport coverage guard for bounded strides.
# Explicit single-step remains available for an uncertain rendered viewport.
scan=[sys.executable,str(ROOT/'scripts/bag_select.py'),item]
if '--single-step' in sys.argv:scan+=['--single-step']
result=subprocess.run(scan)
if result.returncode==4:raise SystemExit('Item absent after a complete visible bag cycle; no item used')
if result.returncode:
 if '--single-step' in scan:raise SystemExit('Single-step bag selection needs review')
 print('Bounded bag scan stopped; retrying visible single-step selection before any use',flush=True)
 subprocess.run([*scan,'--single-step'],check=True)
act('c','wait:0.6','c','wait:1')
target_screen=read().lower()
if 'is selected' in target_screen and 'use' in target_screen and 'cancel' in target_screen:
 # A delayed menu can miss the second confirm; observe the pending Use
 # choice before confirming it, rather than restarting the item selection.
 act('c:0.12','wait:1')
 target_screen=read().lower()
 if 'is selected' in target_screen:raise SystemExit('Use confirmation did not advance; inspect pending item')
if ('--active' not in sys.argv and not active_only) or ('cancel' in target_screen and target_screen.count('hp')>=5):
 subprocess.run([sys.executable,str(ROOT/'scripts/party_pick.py'),target,'--single'],check=True)
last='';seen=0
for _ in range(30):
 t=read();low=t.lower()
 if any(z in low for z in ["won't have any effect","wont have any effect","no effect"]):raise SystemExit('Item has no effect; inspect pending party selection without replay')
 if re.search(r'de.?feated|for winning',low) or 'fight' in low or 'use next pok' in low or 'choose a pok' in low or ('cancel' in low and low.count('hp')>=5):break
 seen=seen+1 if t==last else 0;last=t
 if seen>=2 and 'reacting to' in low and ('mega' in low or ('foe' in low and 'ite' in low)):act('c','wait:.4')
 elif seen>=2 and any(w in low for w in ['used the','restored','recovered','healed','thawed','rose','raised','sharply']):act('c','wait:.4')
 else:act('wait:0.5')
print(t,flush=True)
