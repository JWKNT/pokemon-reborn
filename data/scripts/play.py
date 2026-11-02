import subprocess,json,time,pathlib,sys,re,shutil,os
from input_owner import acquire
acquire()
ROOT=pathlib.Path(__file__).resolve().parent.parent
KEY=str(ROOT/'scripts'/('key_fast' if os.environ.get('REBORN_FAST_KEYS')=='1' else 'key')); STATE=ROOT/'state.png'
NATIVE=ROOT/'work/state-native.png'
def verify_capture_frame():
 framing=ROOT/'recordings/capture-frame.json'
 if not framing.exists():return
 expected=json.loads(framing.read_text())
 health=json.loads((ROOT/'recordings/capture-health.json').read_text())
 if health.get('pid')!=expected['pid']:raise RuntimeError('Capture framing receipt belongs to another recorder; verify framing before input')
 info=subprocess.check_output([str(ROOT/'scripts/observe')],text=True)
 block=next((b for b in info.split(']\n') if 'Pokemon Reborn' in b),'')
 bounds={k:float(re.search(r'\b'+k+r' = ([\d.-]+);',block)[1]) for k in ['X','Y','Width','Height']}
 if bounds!=expected['bounds']:raise RuntimeError('Game window moved outside verified capture framing; input blocked: '+str(bounds))
def act(*keys):
 league_path=ROOT/'notes/active-league-chain.json'
 if league_path.exists() and any(k.split(':')[0]=='d' and k!='d:1.0' for k in keys):
  if json.loads(league_path.read_text()).get('status') in ['active','failed']:
   raise RuntimeError('Hard League no-save guard: quicksave input prohibited during the chain')
 verify_capture_frame()
 control=ROOT/'notes/current-run-control.json'
 if control.exists():
  settings=json.loads(control.read_text())
  if not settings.get('cleanup_mode',False):
   if time.time()>=settings.get('deadline_epoch',float('inf')) or settings.get('last_usage_used_percent',0)>=settings.get('usage_stop_used_percent',95):
    raise RuntimeError('Session limit reached: stop gameplay and enter save/quit cleanup mode')
 hold=float(os.environ.get('REBORN_CONFIRM_HOLD','0.12'));assert .04<=hold<=.3
 keys=tuple(k+':'+str(hold) if k in ('c','x') else k for k in keys)
 subprocess.run([KEY,*keys],check=True)
def snap():
 capture_epoch=time.time()
 match=None
 for attempt in range(4):
  info=subprocess.check_output([str(ROOT/'scripts/observe')],text=True)
  gameinfo=next((block for block in info.split(']\n') if 'Pokemon Reborn' in block),'')
  match=re.search(r'kCGWindowNumber[^0-9]+(\d+)',gameinfo)
  if match:break
  time.sleep(.25)
 if not match:raise RuntimeError('No visible Reborn window')
 health_path=ROOT/'recordings/capture-health.json'
 health=json.loads(health_path.read_text()) if health_path.exists() else {}
 if 'preview_epoch' in health:
  # Observe a newly recorded frame rather than starting a competing capture.
  for _ in range(40):
   health=json.loads(health_path.read_text())
   if health.get('active') and health.get('preview_epoch',0)>=capture_epoch and time.time()-health['epoch']<2:break
   time.sleep(.1)
  else:raise RuntimeError('Fresh recorded observation unavailable; inputs remain blocked')
  from PIL import Image
  frame=Image.open(ROOT/'recordings/capture-preview.png').convert('RGB')
  assert frame.size==(852,640)
  canvas=Image.open(ROOT/'work/capture-preview-frame-template.png').convert('RGB')
  assert canvas.size==(2272,1816), 'Preview framing requires revalidation'
  canvas.paste(frame.resize((2048,1536)),(112,134));canvas.save(STATE)
 else:
  subprocess.run(['/usr/sbin/screencapture','-x','-l',match[1],str(STATE)],check=True)
 result=json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(STATE)]))
 with (ROOT/'recordings/screens.jsonl').open('a') as f:f.write(json.dumps({'epoch':capture_epoch,'ocr_complete_epoch':time.time(),'text':[v['text'] for v in result]})+'\n')
 shutil.copyfile(STATE,NATIVE)
 subprocess.run(['/usr/bin/sips','-Z','1100',str(STATE)],stdout=subprocess.DEVNULL)
 return result
def read():
 r=snap(); return '\n'.join(v['text'] for v in r)
if __name__=='__main__':
 if len(sys.argv)>1: act(*sys.argv[1:])
 print(read())
