"""Execute one planned Blacksteam cage interaction via UI; shadow state is planning-only."""
import json,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent.parent
statefile=ROOT/'notes/navigation-state.json'
s=json.loads(statefile.read_text());v=s['variables'];sw=s['switches']
name=sys.argv[1].lower();mode=sys.argv[2] if len(sys.argv)>2 else 'use'
ids={'vanillite':1,'lickitung':2,'roggenrola':3,'makuhita':4,'loudred':5,'jigglypuff':6,'cyndaquil':7}
cells={108:13,109:8,110:15,111:12,112:10,113:14,114:9,115:11}
if name=='abra':eid=7;var=None
else:
 var=next(k for k in cells if v.get(str(k))==ids[name]);eid=cells[var]
if mode=='teleport' and not sw.get('165'):raise SystemExit('Planning check: Abra bond missing')
if mode=='attack' and (var!=110 or not sw.get('167')):raise SystemExit('Planning check: attack position/guard')
logs=[]
for cmd in [['eventq.py','11',str(eid),'talk'],['dialog.py','--yes']]:
 p=subprocess.Popen([sys.executable,str(ROOT/'scripts'/cmd[0]),*cmd[1:]],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 for line in p.stdout:print(line,end='',flush=True);logs.append(line)
 if p.wait():raise SystemExit('Interaction interrupted; review shadow state')
t=' '.join(logs).lower()
if mode=='teleport':
 if 'teleports' not in ''.join(t.split()):raise SystemExit('Teleport not observed')
 empty=next(k for k in cells if v.get(str(k),0)==0)
 v[str(empty)]=v[str(var)];v[str(var)]=0;sw['165']=False;sw['166']=False
elif name=='abra':
 if 'bonds with your mind' not in t:raise SystemExit('Bond not observed')
 sw['165']=True;sw['168']=False
elif name=='loudred':
 if 'screech' not in t:raise SystemExit('Screech not observed')
 sw.update({'164':True,'168':True,'167':False})
elif name=='jigglypuff':
 if 'guard falls asleep' not in t:raise SystemExit('Guard sleep not observed')
 sw.update({'164':False,'167':True,'168':False})
elif mode=='attack':
 expected={'cyndaquil':('hot',11),'vanillite':('brittle',12),'roggenrola':('shatters',13)}[name]
 if expected[0] not in t:raise SystemExit('Attack result not observed')
 v['107']=expected[1];sw['168']=False
statefile.write_text(json.dumps(s));print('CAGE STEP VERIFIED',name,mode,flush=True)
