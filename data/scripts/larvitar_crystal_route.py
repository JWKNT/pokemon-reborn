"""Execute an explicit static-map Larvitar solution using normal crystal buttons.
Each approach is checked against the in-game coordinate display; stop on dialogue.
"""
from play import *
from locate import locate
mid=int(sys.argv[1]);first,last=map(int,sys.argv[2:4]);assert mid in (619,620,621)
solution=json.loads((ROOT/f'work/277-rock{mid}-solution.json').read_text())
assert 0<=first<last<=len(solution)
controls={621:{'up':42,'down':45,'left':43,'right':44},620:{'up':24,'down':41,'left':42,'right':43},619:{'up':41,'down':44,'left':42,'right':43}}
assert locate(mid)[0]==mid
for n in range(first,last):
 step=solution[n];print('CRYSTAL STEP',n,step,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),str(mid),str(controls[mid][step['direction']]),'talk'],check=True)
 act('wait:3' if n+1<len(solution) else 'wait:6')
 rows=snap();text=' '.join(v['text'] for v in rows).lower()
 assert not re.search(r'\bhp\b|\bfight\b|\bwild\b|pp:',text),'Unexpected battle'
 assert not any(v['y']>.73 and len(v['text'])>18 for v in rows),'Unexpected dialogue'
 shutil.copy2(STATE,ROOT/f'work/277-crystal-{mid}-{n:02}.png')
 print('CRYSTAL ANIMATION SETTLED',n,flush=True)
print('PLANNED CRYSTAL RANGE COMPLETE; verify visible Larvitar and end state',flush=True)
