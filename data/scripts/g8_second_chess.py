from nav import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def stage(n):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['150']=n;p.write_text(json.dumps(v))
stage(31);run('q','313,9,6,up,wait:2');run('linear_dialog',316,35,'--active');stage(32)
for eid,d,n in [(39,'up',3),(39,'right',3),(38,'right',1),(38,'up',7),(38,'right',1)]:run('chess_push',316,eid,d,n)
for d,n in [('ul',2),('dl',1),('ul',1)]:run('chess_bishop',316,40,d,n)
print('SECOND BOARD POSITIONED; INSPECT BEFORE CHECK',flush=True)
