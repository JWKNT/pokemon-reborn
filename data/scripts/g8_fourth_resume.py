from nav import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
# Visual board inspection after blocked right move confirms Queen at (7,12).
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['positions']['318']['49']=[7,12];p.write_text(json.dumps(v))
for eid,d,n in [(49,'down',1),(49,'right',1),(53,'left',1),(53,'up',2),(53,'left',3),(53,'up',3),(53,'right',3),(53,'down',1)]:run('chess_push',318,eid,d,n)
run('chess_bishop',318,54,'ul',2);run('chess_push',318,57,'up',2)
print('FOURTH BOARD POSITIONED; INSPECT BEFORE CHECK',flush=True)
