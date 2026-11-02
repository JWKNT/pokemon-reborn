"""Use an owned Fly carrier; verify the map label before committing travel."""
from play import *
from locate import locate
import difflib
import argparse
p=argparse.ArgumentParser();p.add_argument('destination',type=int);p.add_argument('--carrier',default='Tranquill');p.add_argument('--menu-open',action='store_true');p.add_argument('--origin',type=int);a=p.parse_args()
savepath=pathlib.Path.home()/'Library/Application Support/Pokemon Reborn/Game_3.rxdata'
visited=subprocess.check_output(['ruby','-e',"require_relative 'scripts/read_rgss';v=load_rgss(ARGV[0]);puts(v[:PokemonGlobal].instance_variable_get(:@visitedMaps)[ARGV[1].to_i]==true)",str(savepath),str(a.destination)],cwd=ROOT,stderr=subprocess.DEVNULL,text=True).strip()=='true'
music_events=ROOT/'recordings/music-events.jsonl'
observed=any(row.get('map')==a.destination and row.get('epoch',0)>=savepath.stat().st_mtime for row in (json.loads(l) for l in music_events.read_text().splitlines())) if music_events.exists() else False
assert visited or observed,'Destination Fly point has not been visited; walk there first'
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
if a.menu_open:
 assert a.origin is not None
 mid=a.origin
else:mid,x,y=locate(a.origin)
data=json.loads((ROOT/'work/fly-map-data.json').read_text())
source=data['maps'][str(mid)];region,cx,cy=source['MapPosition']
assert source.get('Outdoor',False),'Exit this indoor map before using Fly'
assert not source.get('MapSize'),'Large-map origin requires explicit calibration'
destinations=[v for v in data['regions'][str(region)]['points'] if v.get('flyData') and v['flyData'][0]==a.destination]
assert len(destinations)==1,'Unknown or ambiguous destination'
dest=destinations[0];tx,ty=dest['xy']
if not a.menu_open:
 run('party_open');run('party_pick',a.carrier,'--single')
rows=snap();t=' '.join(v['text']for v in rows).lower()
assert a.carrier.lower() in t and 'summary' in t and 'switch' in t,'Named carrier menu required'
from PIL import Image
im=Image.open(NATIVE);w,h=im.size;crop=ROOT/'work/fly-options.png'
im.crop((int(w*.72),int(h*.39),int(w*.99),int(h*.91))).resize((540,780),Image.Resampling.NEAREST).save(crop)
proof=json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(crop)]))
labels=[v['text'].strip().lower()for v in sorted(proof,key=lambda z:z['y'])]
labels=[{'suiteh':'switch','suitch':'switch'}.get(z,z) for z in labels]
labels=['summary' if re.fullmatch(r'[^a-z]*p?\s*summary',z) else z for z in labels]
assert any(z in ('fly','flu','fiy','flh')for z in labels),('Fly option not verified',labels)
summary=next(i for i,z in enumerate(labels)if z=='summary');fly=next(i for i,z in enumerate(labels)if z in ('fly','flu','fiy','flh'));switch=next(i for i,z in enumerate(labels)if z=='switch')
assert summary<fly<switch,'Fly menu order needs review'
# Fresh named party submenu starts on Summary. Up wraps in this menu;
# a fixed six-Up sequence selected Surf for Rayquaza's seven-option menu.
assert not a.menu_open, 'Use a freshly opened carrier submenu for verified cursor origin'
act(*[v for _ in range(fly-summary) for v in ('down:.12','wait:.12')],'wait:.25','c','wait:2')
t=read();assert 'reborn region' in t.lower(),'Fly map not displayed'
seq=['right:.08' if tx>cx else 'left:.08']*abs(tx-cx)+['down:.08' if ty>cy else 'up:.08']*abs(ty-cy)
# Map cursor animation needs a brief release gap with the fast driver.
seq=[v for key in seq for v in (key,'wait:.10')]
act(*seq,'wait:.6');t=read();print(t,flush=True)
normalize=lambda s:re.sub('[^a-z0-9]','',s.lower())
label_ok=normalize(dest['name']) in normalize(t) or any(difflib.SequenceMatcher(None,normalize(dest['name']),normalize(line)).ratio()>=.90 for line in t.splitlines())
assert label_ok,'Destination label mismatch; travel not confirmed'
if dest.get('poi'):assert normalize(dest['poi']) in normalize(t),'Destination landmark mismatch'
act('c','wait:5')
actual=locate(a.destination)
assert actual==(a.destination,*dest['flyData'][1:]),actual
print('FLY ARRIVAL VERIFIED',dest['name'],actual,flush=True)
