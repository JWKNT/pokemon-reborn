from play import *
item,name=sys.argv[1:3]
pocket=sys.argv[sys.argv.index('--pocket')+1].lower() if '--pocket' in sys.argv else 'medicine'
if '--bag-open' not in sys.argv:
 act('x','wait:0.5','c','wait:1');t=read().lower()
 if 'pokedex' in t and ('seen' in t or 'search' in t):
  act('x','wait:1','down','down','c','wait:1');t=read().lower()
 if 'cancel' in t and t.count('hp')>=5:act('x','wait:1','down','c','wait:1');t=read().lower()
 if 'field notes' in t or 'pulse dex' in t:act('x','wait:1','up','c','wait:1');t=read().lower()
 machine_pocket=sum(bool(re.match(r't[mh][a-z0-9]',z.strip())) for z in t.splitlines())>=3
 if not ('sort' in t or 'close bag' in t or machine_pocket):raise SystemExit('Bag entry review')
for _ in range(9):
 r=snap()
 if any(v['text'].strip().lower() in ([pocket] if pocket!='medicine' else ['medicine','medieine','nedicine']) for v in r):break
 act('right','wait:0.3')
else:raise SystemExit('Medicine pocket review')
scan=[sys.executable,str(ROOT/'scripts/bag_select.py'),item]
if subprocess.run(scan).returncode:
 subprocess.run([*scan,'--single-step'],check=True)
act('c','wait:0.5');t=read();print(t,flush=True)
if not any(x['text'].strip(' •›>').lower() in ['use','ulse','uee','uze','lise','p lise','p use','llse','plse'] for x in snap()):raise SystemExit('Use menu review')
act('c','wait:1');subprocess.run([sys.executable,str(ROOT/'scripts/party_pick.py'),name,'--single'],check=True)
print(read(),flush=True)
# Stop with the result visible, before closing the party screen.
