from nav import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def stage(n):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['150']=n;p.write_text(json.dumps(v))
run('q','293,10,4,up,wait:2','293,10,30,up,wait:2')
run('linear_dialog',313,1,'--active');stage(28)
run('chess_push',313,9,'up',7)
run('chess_push',313,42,'up',5)
run('chess_push',313,42,'right',2)
print('FIRST BOARD POSITIONED; INSPECT BEFORE CHECK',flush=True)
