from nav import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def stage(n):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['150']=n;p.write_text(json.dumps(v))
stage(37);run('q','317,9,6,up,wait:2');run('linear_dialog',318,35,'--active');stage(38)
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['154']=0;p.write_text(json.dumps(v))
run('chess_pawn',318,49,5,'Queen')
for eid,d,n in [(49,'down',5),(49,'right',1),(53,'left',1),(53,'up',2),(53,'left',3),(53,'up',3),(53,'right',3),(53,'down',1)]:run('chess_push',318,eid,d,n)
run('chess_bishop',318,54,'ul',2);run('chess_push',318,57,'up',2)
print('FOURTH BOARD POSITIONED; INSPECT BEFORE CHECK',flush=True)
