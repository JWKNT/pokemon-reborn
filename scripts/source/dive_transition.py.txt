"""Activate reviewed Dive/Surfacing from a verified DeepWater coordinate."""
from play import *
from locate import locate
m,x,y,dest=map(int,sys.argv[1:5]);assert locate(m)==(m,x,y)
# Only the dark DeepWater terrain supports the action-button transition.
from surface_readonly import tag
metadata=json.loads((ROOT/'work/fly-map-data.json').read_text())['maps']
surface=m if metadata[str(m)].get('DiveMap')==dest else dest
assert metadata[str(surface)].get('DiveMap')==(dest if surface==m else m), 'Reviewed paired Dive maps required'
source=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(surface),str(x),str(y)],stderr=subprocess.DEVNULL))
assert tag(source,(x,y))==5, 'DeepWater tile required before Dive input'
act('c','wait:.6')
prompt=read().lower()
assert any(re.sub('[^a-z]','',line) in ['yes','tes','ves'] for line in prompt.splitlines()) and 'no' in prompt, ('Dive confirmation not visible',prompt)
run=[sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'];subprocess.run(run,check=True)
# Clear the ordinary used-Dive message, then permit the transfer animation.
t=read().lower()
if 'used dive' in t:act('c','wait:3')
else:act('wait:3')
actual=locate(dest)
if actual!=(dest,x,y):raise SystemExit('Dive transfer mismatch '+str(actual))
print('DIVE TRANSFER VERIFIED',actual,flush=True)
