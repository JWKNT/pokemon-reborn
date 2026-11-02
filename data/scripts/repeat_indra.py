"""Repeat inspected Indra practice via UI; stop on any unreviewed matchup or result."""
from play import *
from locate import locate
rounds=int(sys.argv[1]);assert 1<=rounds<=8
if locate(355)!=(355,40,16):raise SystemExit('Start next to Indra at35540,16')
def run(script,*args,expected=None):
 p=subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],capture_output=True,text=True)
 print(p.stdout[-1600:],flush=True)
 if expected and expected in (p.stdout+p.stderr):return p.stdout
 if p.returncode:raise SystemExit(p.stderr or 'Helper stopped for review')
 return p.stdout
for i in range(rounds):
 start=time.time();print('INDRA ROUND START',i+1,start,flush=True)
 act('up','c','wait:.5')
 run('dialog.py','--yes','--limit=25',expected='BATTLE/LEARNING REVIEW')
 run('battle_batch.py','Swoobat',3,'--foes','scizor,empoleon,ribombee,hawlucha,toucannon,ursaring,tsareena,carbink,castform,musharna','--turns',0)
 t=read().lower()
 if 'fight' not in t:raise SystemExit('Battle command menu review')
 out=run('indra_battle.py')
 if 'INDRA VICTORY' not in out:raise SystemExit('Training battle needs review')
 run('dialog.py','--limit=20')
 t=read().lower()
 if len(t.splitlines())>3:raise SystemExit('Post-prize state review: '+t)
 with (ROOT/'recordings/training-events.jsonl').open('a') as f:f.write(json.dumps({'start':start,'end':time.time(),'trainer':'Indra','victory':True,'round_in_batch':i+1})+'\n')
 print('INDRA ROUND COMPLETE',i+1,flush=True)
