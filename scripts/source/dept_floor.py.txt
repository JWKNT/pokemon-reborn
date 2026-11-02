"""Select a department-store floor from its visible numbered menu."""
from play import *
from PIL import Image
from statistics import median
floor=int(sys.argv[1]);assert 1<=floor<=11
def selected(rows):
 im=Image.open(NATIVE).convert('RGB');w,h=im.size;options=[]
 candidates=[r for r in rows if re.search(r'([0-9I]+)F\s*[-–]',r['text'].strip()) and r['y']<.72]
 assert candidates,'No floor rows recognized'
 label_x=median(r['x'] for r in candidates)
 for r in rows:
  match=re.search(r'([0-9I]+)F\s*[-–]',r['text'].strip())
  if not match or r['y']>.72:continue
  number=int(match[1].replace('I','1'));x=label_x;cy=r['y']+r['h']/2
  box=im.crop((int((x-.036)*w),int((cy-r['h']*.48)*h),int((x-.004)*w),int((cy+r['h']*.48)*h)))
  score=sum(max(p)<150 for p in box.getdata())/(box.width*box.height)
  options.append((score,number))
 assert options,('No numbered floor options',rows)
 score,number=max(options)
 assert score>.12 and score-sorted(options)[-2][0]>.08,('Floor arrow not located',options)
 print('FLOOR ARROW VERIFIED',number,options,flush=True);return number
rows=snap();text=' '.join(r['text'] for r in rows)
assert 'which floor' in text.lower(),'Floor choice must already be open'
current=selected(rows)
if current!=floor:act(*(['down:.08' if floor>current else 'up:.08']*abs(floor-current)),'wait:.5')
assert selected(snap())==floor,'Requested floor not selected; no confirmation sent'
act('c','wait:1');print(read(),flush=True)
path=ROOT/'notes/navigation-state.json';state=json.loads(path.read_text());state.setdefault('variables',{})['68']=floor;path.write_text(json.dumps(state)+'\n')
subprocess.run([sys.executable,str(ROOT/'scripts/dialog.py')],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),'113','2','enter'],check=True)
from locate import locate
expected={1:112,2:114,3:141,4:183,5:1,6:2,7:3,8:4,9:5,10:7,11:6}[floor]
actual=locate(expected);assert actual[0]==expected,actual
print('FLOOR ARRIVAL VERIFIED',floor,actual,flush=True)
