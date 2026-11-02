"""Execute exactly two root-reviewed doubles selections from public command screens.
No opponent inspection, native-state reads, or adaptive choices. Stop at any mismatch.
"""
from play import *
import difflib
plan=json.loads(pathlib.Path(sys.argv[1]).read_text());assert isinstance(plan,list) and len(plan)==2
def norm(s):
 # Repeatedly observed public OCR spellings; retain exact actor checking.
 s=re.sub('[^a-z]','',s.lower())
 for old,new in [('valcanion','volcanion'),('mamile','mawile'),('mauile','mawile'),('malrein','walrein'),('sylweon','sylveon'),('amoonguse','amoonguss'),('sulveon','sylveon'),('suampert','swampert')]:s=s.replace(old,new)
 return s
for step in plan:
 assert set(step)<= {'actor','foes','slot','target','mega'}
 rows=snap();t=' '.join(v['text'] for v in rows)
 assert 'fight' in t.lower() and re.search(r'\b(?:bag|bae)\b',t.lower()),t
 prompt=' '.join(v['text']for v in rows if v['y']>.72 and v['x']<.50)
 assert norm(step['actor']) in norm(prompt),('Actor mismatch',prompt)
 for name in step['foes']:
  enemy=' '.join(v['text']for v in rows if v['y']<.37)
  assert norm(name) in norm(enemy) or any(difflib.SequenceMatcher(None,name.lower(),w.lower()).ratio()>=.8 for w in enemy.split()),('Foe mismatch',name,enemy)
 assert 0<=step['slot']<=3
 args=[str(step['slot'])]
 if step.get('target') is not None:args += [str(step['target'])]
 if step.get('mega'):
  assert step['mega'] is True
  args += ['--mega']
 print('REVIEWED SELECTION',step,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/battle_move.py'),*args,'--watch'],check=True)
 subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
print('TWO SELECTIONS RETURNED; REVIEW NEXT PUBLIC COMMAND',flush=True)
