from nav import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def stage(n):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['150']=n;p.write_text(json.dumps(v))
stage(34);run('q','316,9,6,up,wait:2');run('linear_dialog',317,35,'--active');stage(35)
run('chess_pawn',317,53,1)
run('chess_pawn',317,52,6,'Knight')
for eid,d,n in [(52,'down',4),(52,'left',6),(52,'up',2),(48,'up',3),(48,'left',5),(48,'up',2)]:run('chess_push',317,eid,d,n)
print('THIRD BOARD POSITIONED; INSPECT BEFORE CHECK',flush=True)
