"""Bounded Genesect throws; fresh public HUDs, healing checks, stop on capture."""
from play import *
from public_owned_hp import parse as parse_hp
from PIL import Image
def owned_hp(rows,total):
 hp=parse_hp(rows,total)
 if hp is not None:return hp
 im=Image.open(STATE);w,h=im.size
 crop=ROOT/"work/317-public-hp-crop.png"
 im.crop((int(w*.54),int(h*.46),int(w*.97),int(h*.69))).resize((1200,600)).save(crop)
 observed=json.loads(subprocess.check_output([str(ROOT/"scripts/observe"),str(crop)]))
 text=" ".join(r["text"]for r in observed)
 with (ROOT/"recordings/public-hp-crops.jsonl").open("a")as f:f.write(json.dumps(dict(epoch=time.time(),text=text))+"\n")
 assert "Zeraora" in text,text
 values=[int(a)for a,b in re.findall(r"(\d+)\s*/\s*(\d+)",text)if int(b)==total and 0<=int(a)<=total]
 assert len(values)==1,text
 return values[0]
limit=int(sys.argv[1]);assert 1<=limit<=4
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
for _ in range(limit):
 rows=snap();low=' '.join(r['text']for r in rows).lower()
 if any(k in low for k in ['gotcha','was caught','nickname','pokedex','party is full']):break
 assert 'genesect' in low and 'zeraora' in low and 'fight' in low and 'par' in low,'Capture state review'
 hp=owned_hp(rows,371);print('Observed HP before throw',hp,flush=True)
 if hp<180:
  run('battle_item','Ultra Potion','Zeraora');run('battle_ready');rows=snap()
  assert owned_hp(rows,371)>=180,'Review healing turn'
 run('throw_ball','Timer Ball')
 rows=snap();low=' '.join(r['text']for r in rows).lower()
 if any(k in low for k in ['gotcha','was caught','nickname','pokedex','party is full']):break
 run('battle_ready')
