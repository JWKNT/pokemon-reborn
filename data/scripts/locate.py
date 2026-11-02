from play import *
import re
def capture_ready():
 for _ in range(30):
  try:
   h=json.loads((ROOT/'recordings/capture-health.json').read_text())
   if h.get('active') and time.time()-h.get('epoch',0)<2:return
  except (OSError,ValueError):pass
  time.sleep(.5)
 raise SystemExit('Capture did not recover; coordinate input stopped')
def open_coordinates():
 for attempt in range(3):
  try:
   act('d:1.0','wait:.3');return
  except subprocess.CalledProcessError as error:
   if error.returncode!=2:raise
   capture_ready();t=read().lower()
   # The completed hold may already have opened the coordinate display.
   if re.search(r'[,.;]\s*map\s*[0-9oq]+',t):return
   if 'would you like to save' in t:act('x','wait:.7')
 raise SystemExit('Repeated capture interruption opening coordinates')
def last_action_end():
 try:
  with (ROOT/'recordings/actions.jsonl').open('rb') as f:
   f.seek(max(0,f.seek(0,2)-4096));lines=f.read().splitlines()
  return json.loads(lines[-1])['end']
 except (OSError,ValueError,KeyError,IndexError):return None
def locate(expected=None):
 cachefile=ROOT/'work/last-native-position.json'
 if os.environ.get('REBORN_COORD_CACHE')=='1' and cachefile.exists():
  cache=json.loads(cachefile.read_text());position=tuple(cache['position'])
  if time.time()-cache['epoch']<25 and cache['action_end']==last_action_end() and (expected is None or expected==position[0]):
   rows=snap();text=' '.join(v['text']for v in rows).lower()
   if not re.search(r'\bhp\b|\bfight\b|\bwild\b|pp:',text) and not any(v['y']>.73 and len(v['text'])>18 for v in rows):
    print('RECENT UNMOVED COORDINATE',position,flush=True);return position
 open_coordinates();t=read().translate(str.maketrans({'У':'Y','у':'y','Х':'X','х':'x'}))
 if 'would you like to save' in t.lower():
  # A capture interruption can shorten the previous D hold. Cancel its
  # harmless quicksave prompt before reopening the coordinate display.
  act('x','wait:.7');open_coordinates();t=read().translate(str.maketrans({'У':'Y','у':'y','Х':'X','х':'x'}))
 for retry in range(2):
  if 'map' in t.lower() or len(t.splitlines())>3:break
  act('wait:1');open_coordinates();t=read().translate(str.maketrans({'У':'Y','у':'y','Х':'X','х':'x'}))
 m=re.search(r'[XKNM]\s*([0-9OQ]+)\s*[,.;]?\s*Y[^0-9O\n]*([0-9OQ]+)\s*[,.;]?\s*map\s*([0-9OQ]+)',t,re.I)
 if not m:
  # A malformed full-screen glyph (for example 83 -> 8G) must be checked
  # from pixels, never replaced by a guessed numeric coordinate.
  from PIL import Image
  from collections import Counter
  im=Image.open(NATIVE if NATIVE.exists() else STATE);w,h=im.size;box=im.crop((int(w*.09),int(h*.75),int(w*.91),int(h*.86)))
  candidates=[];cp=ROOT/'work/coords-ocr.png'
  for scale in [2,3,4]:
   box.resize((box.width*scale,box.height*scale),Image.Resampling.NEAREST).save(cp)
   ct=' '.join(z['text'] for z in json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(cp)])))
   cm=re.search(r'[XKNM]\s*([0-9OQ]+)\s*[,.;]?\s*Y[^0-9O\n]*([0-9OQ]+)\s*[,.;]?\s*map\s*([0-9OQ]+)',ct,re.I)
   if cm:
    value=tuple(int(g.upper().replace('O','0').replace('Q','0')) for g in cm.groups())
    if expected is None or value[2]==expected:candidates.append(value)
  ranked=Counter(candidates).most_common()
  if ranked and ranked[0][1]>=2:
   xx,yy,mi=ranked[0][0];t=f'X{xx}, Y{yy}, map{mi}'
   m=re.search(r'X(\d+), Y(\d+), map(\d+)',t)
  else:print('COORDINATE REVIEW',t,flush=True);raise SystemExit(2)
 x,y,mid=[int(g.upper().replace('O','0').replace('Q','0')) for g in m.groups()]
 if (expected is not None and (678<=expected<=683 or 732<=expected<=738))or 678<=mid<=683 or 732<=mid<=738:
  from coordinate_digits import fix_coordinates
  fixed=fix_coordinates(NATIVE,(x,y,mid))
  if fixed!=(x,y,mid):print('NATIVE DIGIT TEMPLATE CORRECTION',(x,y,mid),'->',fixed,flush=True)
  x,y,mid=fixed
 if 'belrose manse' in t.lower():mid=233
 if expected==335 and mid==395 and 'iolia' in t.lower():mid=335 # Verified X47,Y14,map335 coordinate image.
 if expected==333 and mid==303 and 'iolia' in t.lower():mid=333 # Verified coordinate image X10,Y40,map333.
 if expected==336 and mid==306 and 'iolia' in t.lower():mid=336 # Verified coordinate image: X11,Y31,map336.
 if expected==330 and mid==300 and 'subseven' in t.lower():mid=330 # Visually verified stealth map.
 if expected==332 and mid==392 and 'subseven' in t.lower():mid=332 # Visually verified 332 OCR confusion in the library.
 if expected==288 and mid==208 and 'north a' in t.lower():mid=288 # Visually verified font/OCR confusion on North Aventurine Woods.
 # Crop the coordinate line to prevent 6/5 errors caused by surrounding sprites.
 # Fiore's purple backdrop makes enlarged coordinate crops read repeated
 # 3s as8s (observed Y33->Y38). Preserve the valid native full-size reading
 # on these maps; still use crop recovery when the map number is unclear.
 if expected is not None and not ((678<=expected<=683 or expected in [364,375,376,389,393,402,403,856,857,886]) and mid==expected):
  from PIL import Image
  im=Image.open(NATIVE if NATIVE.exists() else STATE);w,h=im.size;b=im.crop((int(w*.09),int(h*.75),int(w*.91),int(h*.86)));cp=ROOT/'work/coords-ocr.png';b.resize((b.width*3,b.height*3),Image.Resampling.NEAREST).save(cp)
  rt=' '.join(z['text'] for z in json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(cp)])))
  cm=re.search(r'[XKNM]\s*([0-9OQ]+)\s*[,.;]?\s*Y[^0-9O\n]*([0-9OQ]+)\s*[,.;]?\s*map\s*([0-9OQ]+)',rt,re.I)
  if cm:
   xx,yy,mi=[int(g.upper().replace('O','0').replace('Q','0')) for g in cm.groups()]
   if mi==expected:
    if (xx,yy,mi)!=(x,y,mid):
     b.resize((b.width*2,b.height*2),Image.Resampling.NEAREST).save(cp)
     rt2=' '.join(z['text'] for z in json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(cp)])))
     cm2=re.search(r'[XKNM]\s*([0-9OQ]+)\s*[,.;]?\s*Y[^0-9O\n]*([0-9OQ]+)\s*[,.;]?\s*map\s*([0-9OQ]+)',rt2,re.I)
     second=tuple(int(g.upper().replace('O','0').replace('Q','0')) for g in cm2.groups()) if cm2 else None
     if second==(xx,yy,mi):x,y,mid=xx,yy,mi
     elif second!=(x,y,mid):
      from collections import Counter
      candidates=[(xx,yy,mi)]+([second] if second and second[2]==expected else [])
      for scale in [4,5]:
       b.resize((b.width*scale,b.height*scale),Image.Resampling.NEAREST).save(cp)
       ct=' '.join(z['text'] for z in json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(cp)])))
       cmx=re.search(r'[XKNM]\s*([0-9OQ]+)\s*[,.;]?\s*Y[^0-9O\n]*([0-9OQ]+)\s*[,.;]?\s*map\s*([0-9OQ]+)',ct,re.I)
       if cmx:
        candidate=tuple(int(g.upper().replace('O','0').replace('Q','0')) for g in cmx.groups())
        if candidate[2]==expected:candidates.append(candidate)
      winners=[c for c,n in Counter(candidates).items() if n>=2]
      if len(winners)!=1:raise SystemExit('Coordinate OCR disagreement: '+str(((x,y,mid),candidates)))
      x,y,mid=winners[0]
    else:x,y,mid=xx,yy,mi
 # Enlarged OCR can turn repeated 3s into 5s. The native-pixel exact
 # templates must have final authority after the crop recovery above.
 if (expected is not None and (678<=expected<=683 or 732<=expected<=738 or 776<=expected<=778 or expected in [333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,364,375,376,389,393,402,403,787,790,812,856,857])) or 678<=mid<=683 or 732<=mid<=738 or 776<=mid<=778 or mid in [333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,364,375,376,389,393,402,403,787,790,812,856,857]:
  from coordinate_digits import fix_coordinates
  fixed=fix_coordinates(NATIVE,(x,y,mid))
  if fixed!=(x,y,mid):print('FINAL NATIVE DIGIT CORRECTION',(x,y,mid),'->',fixed,flush=True)
  x,y,mid=fixed
 if expected is not None and mid!=expected:
  for _ in range(3):
   act('wait:0.4');tt=read().translate(str.maketrans({'У':'Y','у':'y','Х':'X','х':'x'}));mm=re.search(r'[XKNM]\s*([0-9OQ]+)\s*[,.;]?\s*Y[^0-9O\n]*([0-9OQ]+)\s*[,.;]?\s*map\s*([0-9OQ]+)',tt,re.I)
   if mm:
    xx,yy,mi=[int(g.upper().replace('O','0').replace('Q','0')) for g in mm.groups()]
    if mi==expected:x,y,mid=xx,yy,mi;break
 try:act('c:0.20','wait:0.5')
 except subprocess.CalledProcessError as error:
  if error.returncode!=2:raise
  capture_ready()
  # Close only a coordinate popup that is still visibly open.
  if re.search(r'[,.;]\s*map\s*[0-9oq]+',read().lower()):act('c:0.20','wait:.5')
 if 732<=mid<=738:
  # A newly launched window can miss the first dismissing press. Never send
  # walking keys while a positively identified coordinate textbox is open.
  for _ in range(2):
   closed_text=read().lower()
   if not re.search(r'[,.;]\s*map\s*[0-9oq]+',closed_text):break
   act('c:.25','wait:.7')
  else:raise SystemExit('Coordinate popup remained open; movement stopped')
 # Log observed map changes for the final normal-speed BGM reconstruction.
 cuefile=ROOT/'recordings/music-events.jsonl'
 lastfile=ROOT/'work/last-music-map.txt'
 if not lastfile.exists() or lastfile.read_text()!=str(mid):
  music=json.loads((ROOT/'work/bgm/game-music.json').read_text())['maps'].get(str(mid),{})
  with cuefile.open('a') as f:f.write(json.dumps({'epoch':time.time(),'map':mid,'map_name':music.get('name'),'bgm':music.get('bgm'),'source':'observed coordinates; approximate transition'})+'\n')
  lastfile.write_text(str(mid))
 cachefile.write_text(json.dumps({'position':[mid,x,y],'epoch':time.time(),'action_end':last_action_end()}))
 return mid,x,y
if __name__=='__main__':print(locate())
