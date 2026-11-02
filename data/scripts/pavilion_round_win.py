"""Close a publicly won Pavilion round and stop at the next-round prompt."""
from play import *
name=sys.argv[1];n=int(sys.argv[2]);roundno=int(sys.argv[3])
t=read();assert re.search(r'de.?feated',t,re.I) and name.lower() in t.lower(),t
act('c','wait:.6');t=read();print(t,flush=True)
assert 'fight' not in t.lower() and 'what will' not in t.lower(),t
act('c','wait:1');t=read();print(t,flush=True)
for _ in range(6):
 if 'thanks for playing' in t.lower() and 'heal' in t.lower():break
 assert re.sub('[^a-z]','',t.lower()) in ['', 'pokemonreborn'],t
 act('wait:.7');t=read();print(t,flush=True)
else:raise AssertionError('Healing boundary not observed: '+t)
subprocess.run([sys.executable,str(ROOT/'scripts/trainer_music.py'),'finish','--world-verified'],check=True)
p=ROOT/'notes'/f'pavilion{n}-progress.json';v=json.loads(p.read_text());v['completed_rounds'].append(dict(round=roundno,trainer=name,result='victory',items=[]));v['current_round']=roundno+1;p.write_text(json.dumps(v,indent=2))
act('c','wait:.7');print(read(),flush=True)
print('STOPPED before next-round confirmation',flush=True)
