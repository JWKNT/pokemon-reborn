"""Render installed map tiles for offline route review, with observed event labels."""
import sys,json,subprocess,pathlib,ast
from PIL import Image,ImageDraw,ImageFont
ROOT=pathlib.Path(__file__).resolve().parents[1];GAME=pathlib.Path('/Applications/Reborn.app/Contents/Game');mid=int(sys.argv[1])
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),'0','0',json.dumps({'switches':{'410':False}})],stderr=subprocess.DEVNULL))
code="require_relative 'scripts/read_rgss';m=load_rgss('/Applications/Reborn.app/Contents/Game/Data/Map%03d.rxdata'%ARGV[0].to_i);ts=load_rgss('/Applications/Reborn.app/Contents/Game/Data/Tilesets.rxdata')[m.instance_variable_get(:@tileset_id)];puts JSON.generate([ts.instance_variable_get(:@tileset_name),ts.instance_variable_get(:@autotile_names)])"
name,autos=json.loads(subprocess.check_output(['ruby','-e',code,str(mid)],cwd=ROOT,stderr=subprocess.DEVNULL))
ts=Image.open(GAME/'Graphics/Tilesets'/f'{name}.png').convert('RGBA');aut=[]
for n in autos:aut.append(Image.open(GAME/'Graphics/Autotiles'/f'{n}.png').convert('RGBA')if n else None)
s=(GAME/'Scripts/TileDrawingHelper.rb').read_text();table=ast.literal_eval(s.split('Autotiles =',1)[1].split('# converts',1)[0].strip())
cache={}
def tile(n):
 if n in cache:return cache[n]
 t=Image.new('RGBA',(32,32))
 if n>=384:
  x=(n-384)%8*32;y=(n-384)//8*32;t=ts.crop((x,y,x+32,y+32))
 elif n>=48:
  a=aut[n//48-1]
  if a is None:return t
  if a.height==32:t=a.crop((0,0,32,32))
  else:
   for i,p in enumerate(table[(n%48)//8][n%8]):
    p-=1;x=p%6*16;y=p//6*16;t.alpha_composite(a.crop((x,y,x+16,y+16)),(i%2*16,i//2*16))
 cache[n]=t;return t
w,h=v['width'],v['height'];im=Image.new('RGBA',(w*32,h*32),(0,0,0,255))
for z in range(3):
 for y in range(h):
  for x in range(w):im.alpha_composite(tile(v['data']['data'][x+w*y+w*h*z]),(x*32,y*32))

tile(958).convert("RGB").save(ROOT/"work/amethyst-floor958.png")

for eid,x,y in [(59,35,32),(61,55,37),(62,26,47),(63,17,62),(64,50,61)]:
 t=im.crop((x*32,y*32,(x+1)*32,(y+1)*32));t.alpha_composite(tile(958));t.convert("RGB").save(ROOT/"work"/f"amethyst-broken-{eid}.png")

for stage,x,y in [(3,39,33),(4,61,38),(5,27,49),(6,21,62),(7,53,60)]:
 im.crop((x*32,y*32,(x+1)*32,(y+1)*32)).convert("RGB").save(ROOT/"work"/f"amethyst-open-{stage}.png")
