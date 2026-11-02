"""Reviewed cave route after healing, with explicit story transitions and battle stop."""
from play import *
from locate import locate
def run(name,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/f'{name}.py'),*map(str,args)],check=True)
def flag(n):
 p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s.setdefault('switches',{})[str(n)]=True;p.write_text(json.dumps(s))
run('eventq',257,3,'enter')
run('q','258,12,25')
act('up','wait:1');print(read(),flush=True)
run('linear_dialog',258,16)
if locate(258)[0]!=258:raise SystemExit('Wrong cave map')
flag(278)
run('q','258,12,7,up')
run('story_transition',264,13,263,11)
run('story_transition',263,17,262,12)
run('story_transition',262,27,247,13)
run('q','247,74,66')
print('STEELIX APPROACH: REVIEW BEFORE BATTLE ACTIONS',flush=True)
