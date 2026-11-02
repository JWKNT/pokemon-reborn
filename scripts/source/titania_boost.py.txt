"""UI-only Titania setup on her burned lead; persist completed actions for review."""
from play import *
import difflib

path = ROOT/'work/titania-120-setup.json'
plan = [('move',2),('item','X Defend'),('item','X Defend'),
        ('item','X Sp. Def'),('item','X Speed'),('item','X Speed'),
        ('move',3),('move',3)]
state = json.loads(path.read_text()) if path.exists() else {'done':0,'heals':0}
def run(s,*args):
 subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
while state['done'] < len(plan):
 run('battle_ready')
 rows=snap();t=' '.join(v['text']for v in rows);low=t.lower()
 enemy=' '.join(v['text'].lower()for v in rows if v['y']<.37)
 foe=next((n for n in ['sandslash','excadrill']if n in enemy),None)
 assert 'fight' in low and foe,'Expected reviewed burned lead command: '+t
 own=' '.join(v['text'].lower()for v in rows if v['y']>.4)
 assert any(difflib.SequenceMatcher(None,'excadrill',w).ratio()>.75 for w in own.split()),'Expected Excadrill'
 pairs=[(int(m[0]),int(m[1]))for m in re.findall(r'(\d+)\s*/\s*(\d+)',t)]
 hp=next((h for h,total in pairs if total==358),None)
 assert hp is not None,'HP OCR review: '+t
 screens=[json.loads(line) for line in (ROOT/'recordings/screens.jsonl').read_text().splitlines()]
 attempt=json.loads((ROOT/'recordings/major-fights/session-113-attempts.json').read_text())[-1]
 assert any(s['epoch']>=attempt['battle_start_epoch'] and foe+' was burned' in ' '.join(s['text']).lower() for s in screens),'Observed burn proof required'
 print('SETUP',state,'HP',hp,flush=True)
 if hp <=245:
  assert state['heals']<6,'Heal budget review'
  run('battle_item','Ultra Potion','Excadrill');state['heals']+=1
 else:
  kind,value=plan[state['done']]
  if kind=='move':run('battle_move',value,'--watch')
  else:run('battle_item',value,'Excadrill','--active')
  state['done']+=1
 path.write_text(json.dumps(state,indent=2)+'\n')
print('TITANIA SETUP COMPLETED; review before Earthquake sweep',flush=True)
