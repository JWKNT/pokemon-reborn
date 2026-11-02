"""Finish only a matching choice-free installed arrival caption, then locate."""
from play import *
from locate import locate
import difflib
mid=int(sys.argv[1]);act('wait:3');norm=lambda s:re.sub('[^a-z]','',s.lower().replace('pokemon reborn',''))
rows=snap();observed=' '.join(r['text']for r in rows);n=norm(observed)
if len(n)>10:
 source="m=load_rgss(format('/Applications/Reborn.app/Contents/Game/Data/Map%03d.rxdata',ARGV[0].to_i));puts JSON.generate(plain(m.instance_variable_get(:@events)))"
 events=json.loads(subprocess.check_output(['ruby','-r',str(ROOT/'scripts/read_rgss.rb'),'-e',source,str(mid)],stderr=subprocess.DEVNULL));matches=[]
 for eid,e in events.items():
  for page,p in enumerate(e['pages']):
   cs=p['list'];blocks=[]
   for c in cs:
    if c['code']==101:blocks.append(str(c['parameters'][0]))
    elif c['code']==401 and blocks:blocks[-1]+=' '+str(c['parameters'][0])
   score=max([difflib.SequenceMatcher(None,n,norm(b)).ratio()for b in blocks]or[0])
   if score>.65:matches.append((score,eid,page,cs))
 if matches:
  score,eid,page,cs=max(matches,key=lambda m:m[0])
  assert not any(c['code']in[102,103,104,301]or any(s in str(c['parameters'])for s in['pbTrainerBattle','pbDoubleTrainerBattle','pbWildBattle'])for c in cs),'Arrival scene needs explicit choice/battle handling'
  print('INSTALLED ARRIVAL CAPTION VERIFIED',mid,eid,page,score,observed,flush=True)
  subprocess.run([sys.executable,str(ROOT/'scripts/linear_dialog.py'),str(mid),str(eid),'--source-page',str(page),'--burst'],check=True)
actual=locate(mid);assert actual[0]==mid,actual
print('ARRIVAL VERIFIED',actual,flush=True)
