"""Advance dialogue to an explicitly expected choice, then select by its visible labels."""
from play import *
import re,difflib
from PIL import Image
labels=sys.argv[1].split('|');wanted=sys.argv[2];assert wanted in labels
anchors=[];seen=set();equivalent_duplicates=False
if '--source' in sys.argv:
 i=sys.argv.index('--source');mid,eid=map(int,sys.argv[i+1:i+3])
 model=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),'0','0'],stderr=subprocess.DEVNULL))
 cs=model['events'][str(eid)]['list']
 assert [c['parameters'][0]for c in cs if c['code']==102]==[labels]
 if len(labels)>1 and len(set(labels))==1:
  first=next(i for i,c in enumerate(cs) if c['code']==102);last=next(i for i in range(first+1,len(cs)) if cs[i]['code']==404)
  assert all(c['code'] in [402,0] for c in cs[first+1:last]), 'Duplicate options have different actions'
  equivalent_duplicates=True
 for idx,c in enumerate(cs):
  if c['code']not in [241,242]:continue
  block=[]
  for z in cs[idx+1:]:
   if z['code']==101:
    if block:break
    block=[str(z['parameters'][0])]
   elif z['code']==401 and block:block.append(str(z['parameters'][0]))
  if block:anchors.append((idx,' '.join(block),c['parameters'][0]['name']if c['code']==241 else '__silence__'))
blank=0
for _ in range(120):
 r=snap();t='\n'.join(x['text'] for x in r);print(t,flush=True)
 norm=lambda z:re.sub('[^a-z]','',z.lower().replace('pokemon reborn',''))
 for idx,anchor,track in anchors:
  if idx not in seen and difflib.SequenceMatcher(None,norm(t),norm(anchor)).ratio()>.7:
   with(ROOT/'recordings/music-events.jsonl').open('a')as f:f.write(json.dumps({'epoch':time.time(),'bgm':{'name':track},'source':'inspected-scripted-BGM','map':mid,'event':eid,'command_index':idx,'evidence':t})+'\n')
   seen.add(idx)
 rows=[x['text'].strip().lower() for x in r]
 def matches(label,z):
  z={'tes':'yes','ves':'yes','yee':'yes','ro':'no','mo':'no','nо':'no','p uise':'use'}.get(z,z)
  exact=z.strip(' •›>')
  compact_label=re.sub('[^a-z]','',label.lower());compact_seen=re.sub('[^a-z]','',exact)
  if len(compact_label)>2 and compact_seen==compact_label:return True
  if exact in [v.lower() for v in labels]:return exact==label.lower()
  return label.lower()==exact or difflib.SequenceMatcher(None,label.lower(),exact).ratio()>=.82
 if set(labels)=={'Yes','No'} and not all(any(matches(label,z)for z in rows)for label in labels):
  # Large pixel text can omit the short "No" beside busy scenery. Re-read
  # the actual right-side choice box in the untouched native screenshot.
  im=Image.open(NATIVE);w,h=im.size;cp=ROOT/'work/choice-region.png'
  for x0,y0,x1,y1 in [(.76,.48,.99,.76),(.02,.06,.22,.28),(.02,.06,.32,.38)]:
   im.crop((int(w*x0),int(h*y0),int(w*x1),int(h*y1))).save(cp)
   cropped=json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(cp)]))
   if all(any(matches(label,z['text'].strip().lower())for z in cropped)for label in labels):
    r=[dict(z,x=x0+z['x']*(x1-x0),y=y0+z['y']*(y1-y0))for z in cropped]
    rows=[z['text'].strip().lower()for z in r]
    print('CHOICE LABELS VERIFIED IN NATIVE CROP',rows,flush=True);break
 if not all(any(matches(label,z) for z in rows) for label in labels) and set(labels)!={'Yes','No'}:
  im=Image.open(NATIVE);w,h=im.size;cp=ROOT/'work/choice-region.png'
  x0,y0,x1,y1=((.66,.48,.99,.76) if 'Cancel' in labels and any('Repel' in z for z in labels) else ((.58,.32,.99,.82) if set(labels)=={'Ground Floor','B1F','B2F'} else (.785,.40,.99,.96)))
  im.crop((int(w*x0),int(h*y0),int(w*x1),int(h*y1))).resize((650,1400),Image.Resampling.NEAREST).save(cp)
  cropped=json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(cp)]))
  if all(any(matches(label,z['text'].strip().lower())for z in cropped)for label in labels):
   r=[dict(z,x=x0+z['x']*(x1-x0),y=y0+z['y']*(y1-y0))for z in cropped]
   rows=[z['text'].strip().lower()for z in r]
   print('CHOICE LABELS VERIFIED IN NATIVE CROP',rows,flush=True)
 if equivalent_duplicates and sum(z.strip(' •›>').lower()==wanted.lower() for z in rows)==len(labels):
  with (ROOT/'recordings/choices.jsonl').open('a') as f:f.write(json.dumps({'epoch':time.time(),'labels':labels,'answer':wanted,'evidence':t,'method':'Observed identical labels; installed branches both empty; normal confirm'})+'\n')
  act('c','wait:1');print(read(),flush=True);break
 if all(any(matches(label,z) for z in rows) for label in labels):
  if '--stop-at-choice' in sys.argv:
   print('EXPECTED CHOICE READY; no selection sent',flush=True);break
  visible=sorted([(x['y'],label) for label in labels for x in r if matches(label,x['text'].strip().lower())]); order=[label for _,label in visible]
  if len(order)!=len(labels):raise SystemExit('Ambiguous choice labels')
  with (ROOT/'recordings/choices.jsonl').open('a')as f:
   f.write(json.dumps({'epoch':time.time(),'labels':order,'answer':wanted,'evidence':t,'method':'verified visible labels; normal keyboard selection'})+'\n')
  keys=['up:0.12']*len(labels)+['down:0.12']*order.index(wanted)
  act(*[z for key in keys for z in (key,'wait:.12')],'c','wait:1');print(read(),flush=True);break
 if any(any(matches(label,z) for z in rows) for label in labels):
  raise SystemExit('Partially recognized choice; inspect labels before further input')
 if re.search(r'\bhp\b|\bpp:|\bvs\b',t.lower()) or re.search('[wmuv]ouldliketobattle',re.sub('[^a-z]','',t.lower())) or any(z in rows for z in ['yes','no','light','dark','radomus','el']):raise SystemExit('Unexpected choice or battle')
 if len(t.replace('Pokemon Reborn','').strip())<3:
  im=Image.open(STATE).convert('RGB');w,h=im.size;b=im.crop((int(w*.08),int(h*.75),int(w*.90),int(h*.87)))
  if sum(min(p)>210 for p in b.getdata())/(b.width*b.height)>.55:
   act('c','wait:0.35');continue
  blank+=1
  if blank>=5:raise SystemExit('No dialogue')
  act('wait:2');continue
 blank=0
 act('c','wait:0.35')
else:raise SystemExit('Choice not reached')
