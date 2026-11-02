"""Execute a bounded surface path through normal game controls, verifying progress."""
from surface_plan import *
from locate import locate
mid,tx,ty=map(int,sys.argv[1:4]);stalls=0;previous=None
def handle_common_wild(t):
 approved=['spheal','delibird','beartic','dew gong','dewgong','cryogonal','jynx','sneasel','piloswine','swinub','cubchoo','bergmite','seel','wailmer','lumineon','wishiwashi','golduck']
 if mid==375 and 'delibird' in t and (' hp' in ' '.join(t.split()) or 'fight' in t):
  # Normal return encounter visually observed in session292.
  subprocess.run([sys.executable,str(ROOT/'scripts/flee.py'),'--since',str(action_started)],check=True)
  return True
 if mid==232:
  # Reviewed installed Tanzan Cove water encounters, below Arcanine79.
  approved=['ducklett','lumineon','seaking','swanna']
  if (' hp' in ' '.join(t.split()) or 'fight' in t) and any(z in t for z in approved):
   subprocess.run([sys.executable,str(ROOT/'scripts/flee.py'),'--since',str(action_started)],check=True)
   return True
 if mid==467 or mid in range(497,506):
  # Installed WTC Surf encounter pool: Gulpin, Grimer, Muk, Swalot.
  approved=['gulp','grimer','muk','sualot','swalot']
  if (' hp' in ' '.join(t.split()) or 'fight' in t) and any(z in t for z in approved):
   subprocess.run([sys.executable,str(ROOT/'scripts/flee.py'),'--since',str(action_started)],check=True)
   return True
 if mid in [359,380,430,390,364,366,373] and (' hp' in ' '.join(t.split()) or 'fight' in t) and any(z in t for z in approved):
  subprocess.run([sys.executable,str(ROOT/'scripts/flee.py')],check=True)
  return True
 return False
action_started=time.time()
for iteration in range(100):
 if handle_common_wild(read().lower()):continue
 try:m,x,y=locate(mid)
 except SystemExit as error:
  if error.code==2 and handle_common_wild(read().lower()):continue
  raise
 except subprocess.CalledProcessError as error:
  if error.returncode!=2:raise
  recovered=False
  for _ in range(30):
   h=json.loads((ROOT/'recordings/capture-health.json').read_text())
   recovered=h.get('active') and time.time()-h.get('epoch',0)<2
   if recovered:break
   time.sleep(.5)
  if not recovered:raise
  print('CAPTURE RECOVERED during coordinate check',flush=True)
  continue
 stalls=stalls+1 if previous==(m,x,y) else 0
 previous=(m,x,y)
 if stalls>=3:raise SystemExit('Surface route stalled; inspect the obstruction')
 if m!=mid:raise SystemExit('Surface map transition review')
 if (x,y)==(tx,ty):print('SURFACE ROUTE COMPLETE',mid,x,y,flush=True);break
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(x),str(y)],stderr=subprocess.DEVNULL))
 steps=surface_plan(v,(tx,ty));first=steps[0];chunk=[]
 for s in steps:
  # Fiore and Ametrine Core have source-reviewed automatic dry touch jumps.
  # Queue a bounded dry section, then verify the actual landing coordinate.
  if mid in [679,870,872] and not first['from'][2] and not s['to'][2] and (':'not in s['key'] or s['key'].startswith('jump:') or (mid in [870,872] and s['key'].startswith('slide:'))):
   chunk.append(s)
   if len(chunk)>=(12 if any(':' in step['key'] for step in chunk) else 24):break
   continue
  if ':' in s['key']:
   if not chunk:chunk.append(s)
   elif mid in [374,439] and first['key'].startswith('jump:') and s['key']==first['key'] and len(chunk)<8:
    chunk.append(s);continue
   else:break
   if mid in [374,439] and first['key'].startswith('jump:'):continue
   break
  if first['key'].startswith('jump:'):break
  chunk.append(s)
  if len(chunk)>=24:break
 print('SURFACE',first['from'],'→',chunk[-1]['to'],len(chunk),'edges',flush=True)
 action_started=time.time()
 if first['key'].startswith('surf:'):
  direction=first['key'].split(':')[1]
  act(direction+':.12','c','wait:.8');t=read().lower();print(t,flush=True)
  compact_prompt=re.sub('[^a-z]','',t)
  if 'surf' in compact_prompt and ('youliketosurf' in compact_prompt or 'wouldyouliketo' in compact_prompt.replace('hould','would')):
   subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
   t=read().lower()
  if 'used surf' in t or 'surf!' in t:act('c','wait:2')
  elif len(t.splitlines())<=3:act('wait:2')
  else:raise SystemExit('Surf boarding review: '+t)
 else:
  seq=[]
  for key,g in groupby(chunk,key=lambda z:z['key']):
   n=len(list(g))
   if ':' in key:seq.extend([key.split(':')[1]+':.12','wait:2.5']*n)
   elif '--hold-straights' in sys.argv and n>1:seq.append(key+':'+str(round(n*.1+.02,3)))
   else:seq.extend([key+':.12']*n)
  try:act(*seq)
  except subprocess.CalledProcessError as error:
   if error.returncode!=2:raise
   recovered=False
   for _ in range(30):
    h=json.loads((ROOT/'recordings/capture-health.json').read_text())
    recovered=h.get('active') and time.time()-h.get('epoch',0)<2
    if recovered:break
    time.sleep(.5)
   if not recovered:raise
   print('CAPTURE RECOVERED; replan from actual position',flush=True)
   continue
 r=snap();t=' '.join(z['text'] for z in r).lower()
 if handle_common_wild(t):continue
 compact=''.join(t.split())
 if 'repel' in compact and ('woreoff' in compact or 'uoreoff' in compact):
  subprocess.run([sys.executable,str(ROOT/'scripts/renew_repel.py')],check=True)
  continue
 if any(w in t for w in ['repel','fight',' hp','yes']) or any(z['text'].strip().lower()=='no' for z in r) or any(z['y']>.73 and len(z['text'])>22 for z in r):raise SystemExit('Surface dialogue/battle review: '+t)
 # The next iteration observes the real endpoint before planning further inputs.
else:raise SystemExit('Surface iteration limit')
