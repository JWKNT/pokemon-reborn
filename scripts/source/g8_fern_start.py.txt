from nav import *
from locate import locate
assert locate(285)[0]==285
save()
raw=subprocess.check_output(['ruby',str(ROOT/'scripts/status.rb')],stderr=subprocess.DEVNULL);(ROOT/'notes/g8-before-fern.json').write_bytes(raw)
s=json.loads(raw);assert s['map']==285 and all(p['level']==60 for p in s['party'])
print('SAVED LEVEL60 PARTY',flush=True)
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),'285,5,37,up,wait:2'],check=True)
p=ROOT/'notes/navigation-state.json';n=json.loads(p.read_text());n['variables']['150']=3;p.write_text(json.dumps(n))
subprocess.run([sys.executable,str(ROOT/'scripts/battle_batch.py'),'Klinklang','3','--foes','haxorus','--turns','1','--watch'],check=True)
