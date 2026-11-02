"""Reviewed Amaria setup through screenshots and ordinary battle controls only.
Bounded item plan; stop on unapproved foes, status, uncertain HP or dangerous
physical matchup. Progress file is archive/control metadata, never game data.
"""
from play import *
from PIL import Image
import difflib
state_path=ROOT/'work/amaria-121-ludicolo-setup.json'
plan=['X Sp. Def','X Sp. Def','X Defend','X Speed','X Sp. Atk','X Sp. Atk','X Sp. Atk']
state=json.loads(state_path.read_text())if state_path.exists()else{'done':0,'heals':0}
assert len(sys.argv)>1,'Give exact native totalHP'
total=int(sys.argv[1]);assert 280<=total<=320
names=['twinkle','starmie','wishbuckler','wishiwashi','indiana','ludicolo','kipkip','swampert','atlantica','kingdra']
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
while state['done']<len(plan):
 run('battle_ready');r=snap();t=' '.join(v['text']for v in r);low=t.lower()
 assert 'fight'in low and 'ludicolo'in low,t
 foe=' '.join(v['text'].lower()for v in r if v['y']<.37)
 assert any(any(difflib.SequenceMatcher(None,n,w.strip('.,')).ratio()>=.78 for w in foe.split())for n in names),('Unapproved setup foe',foe)
 pairs=[(int(a),int(b))for a,b in re.findall(r'(\d+)\s*/\s*(\d+)',t)]
 hp=next((a for a,b in pairs if b==total and 0<a<=b),None)
 if hp is None:
  im=Image.open(STATE).convert('RGB');w,h=im.size;fractions=[]
  for by in [.575+i*.001 for i in range(35)]:
   pixels=[im.getpixel((x,int(h*by)))for x in range(int(w*.761),int(w*.929))]
   fractions.append(sum((g>75 and g>r*1.3 and g>b*1.3)or(r>130 and b<70 and g<220)for r,g,b in pixels)/len(pixels))
  hp=max(0,int(max(fractions)*total)-5);assert hp>0,'HP observation review'
 if any(s in low for s in ['parf','parh','slpf','slph','psnf','psnh','frzf','frzh']):raise SystemExit('Status treatment review')
 physical=any(n in foe for n in ['kipkip','swampert'])
 assert not physical or hp>=281,'Mega Swampert critical-hit safety review'
 floor=281 if physical else (190 if state['done']==0 else 235)
 print('LUDI SETUP',state,'HP',hp,'FOE',foe,flush=True)
 if hp<floor:
  assert state['heals']<12
  run('battle_item','Ultra Potion','Ludicolo');state['heals']+=1
 else:
  run('battle_item',plan[state['done']],'Ludicolo','--active');state['done']+=1
 state_path.write_text(json.dumps(state,indent=2)+'\n')
print('LUDICOLO SETUP COMPLETE; verify HP/field before MegaDrain sweep',flush=True)
