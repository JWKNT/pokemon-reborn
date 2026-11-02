"""Talk to an adjacent follower using a fresh native checkpoint, never changing it."""
from play import *
from locate import locate
name=sys.argv[1];savepath=pathlib.Path.home()/'Library/Application Support/Pokemon Reborn/Game_3.rxdata'
assert time.time()-savepath.stat().st_mtime<120,'Fresh checkpoint required for follower coordinates'
src='v=load_rgss(ARGV[0]);puts JSON.generate({position:v[:position],map:v[:map_id],followers:plain(v[:PokemonGlobal].instance_variable_get(:@dependentEvents))})'
s=json.loads(subprocess.check_output(['ruby','-r',str(ROOT/'scripts/read_rgss.rb'),'-e',src,str(savepath)],stderr=subprocess.DEVNULL))
x,y=s['position'][:2];assert locate(s['map'])==(s['map'],x,y)
f=[f for f in s['followers']if f[8]==name];assert len(f)==1,f
f=f[0];assert f[2]==s['map'];dx,dy=f[3]-x,f[4]-y
key={(0,1):'down',(0,-1):'up',(-1,0):'left',(1,0):'right'}[(dx,dy)]
act(key+':.03','wait:.3','c','wait:.7');print(read(),flush=True)
