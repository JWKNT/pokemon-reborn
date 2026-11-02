"""Normal UI boosts against reviewed Klefki; stop on any unexpected matchup."""
from play import *
path=ROOT/'work/titania-120-attempt2-klefki-setup.json'
plan=[('item','X Sp. Def'),('item','X Sp. Def'),('item','X Defend'),
      ('item','X Defend'),('item','X Speed'),('move',3),('move',3)]
state=json.loads(path.read_text()) if path.exists() else {'done':0,'heals':0}
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
while state['done']<len(plan):
 run('battle_ready');rows=snap();t=' '.join(v['text']for v in rows);low=t.lower()
 assert 'fight' in low and 'klef' in low and 'excadr' in low,t
 pairs=[(int(a),int(b))for a,b in re.findall(r'(\d+)\s*/\s*(\d+)',t)]
 hp=next((a for a,b in pairs if b==358 and 0<a<=b),None)
 if hp is None:
  from PIL import Image
  im=Image.open(STATE).convert('RGB');w,h=im.size
  fills=[]
  for y in [.575+i*.001 for i in range(35)]:
   pixels=[im.getpixel((x,int(h*y)))for x in range(int(w*.761),int(w*.929))]
   fills.append(sum((g>75 and g>r*1.3 and g>b*1.3)or(r>130 and b<70 and g<220)for r,g,b in pixels)/len(pixels))
  hp=max(0,int(max(fills)*358)-5)
  assert hp>0,'HP bar review: '+t
  print('Conservative visible HP-bar estimate',hp,flush=True)
 print('KLEFKI SETUP',state,'HP',hp,flush=True)
 if hp<230:
  assert state['heals']<4,'Heal budget review'
  run('battle_item','Ultra Potion','Excadrill');state['heals']+=1
 else:
  kind,value=plan[state['done']]
  if kind=='item':run('battle_item',value,'Excadrill','--active')
  else:run('battle_move',value,'--watch')
  state['done']+=1
 path.write_text(json.dumps(state,indent=2)+'\n')
print('KLEFKI SETUP DONE; inspect health and battle before sweep',flush=True)
