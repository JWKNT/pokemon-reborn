"""Reviewed Starmie setup, using only screenshots and ordinary battle controls."""
from play import *
from PIL import Image
path=ROOT/'work/amaria-121-cryo-setup.json'
plan=['X Sp. Def']*2+['X Speed']*3+['X Sp. Atk']*3
state=json.loads(path.read_text())if path.exists()else{'done':0,'heals':0,'recoveries':0}
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
while state['done']<len(plan):
 run('battle_ready');r=snap();t=' '.join(v['text']for v in r);low=t.lower()
 assert 'fight'in low and any(n in low for n in ['starm','twinkle',state.get('approved_foe','starm')]) and ('hexan'in low or 'hekan'in low),t
 assert 'blub' in low or state.get('underwater_verified',False),'Confirm underwater field before setup'
 pairs=[(int(a),int(b))for a,b in re.findall(r'(\d+)\s*/\s*(\d+)',t)]
 hp=next((a for a,b in pairs if b==320 and 0<a<=b),None)
 if hp is None:
  im=Image.open(STATE).convert('RGB');w,h=im.size;fills=[]
  for y in [.575+i*.001 for i in range(35)]:
   pixels=[im.getpixel((x,int(h*y)))for x in range(int(w*.761),int(w*.929))]
   fills.append(sum((g>75 and g>r*1.3 and g>b*1.3)or(r>130 and b<70 and g<220)for r,g,b in pixels)/len(pixels))
  hp=max(0,int(max(fills)*320)-5);assert hp>0,'HP bar review: '+t
 print('AMARIA SETUP',state,'HP',hp,flush=True)
 # On the initial paid switch, unboosted Thunderbolt can leave HP below
 # the normal setup threshold. A first priority SpDef boost stops a pure
 # healing loop; inspect below150 rather than accepting a fragile action.
 if state.get('screen_remaining',99)<=1 and hp>=245:
  run('battle_move',0,'--watch');state['screen_remaining']=6
 elif state['done']==0 and 190<=hp<245:
  run('battle_item',plan[0],'Hexan','--active');state['done']+=1
 elif hp<245:
  if state['done']>=5 and hp>=160:
   assert state['recoveries']<12;run('battle_move',2,'--watch');state['recoveries']+=1
  else:
   assert state['heals']<12;run('battle_item','Ultra Potion','Hexan');state['heals']+=1
 else:run('battle_item',plan[state['done']],'Hexan','--active');state['done']+=1
 if 'screen_remaining' in state:state['screen_remaining']-=1
 path.write_text(json.dumps(state,indent=2)+'\n')
print('CRYO SETUP COMPLETE; review health/status and field before sweep',flush=True)
