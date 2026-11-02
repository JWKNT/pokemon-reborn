from nav import *
from locate import locate
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def stage(n):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['150']=n;p.write_text(json.dumps(v))
run('linear_dialog',296,6,'--active');stage(12)
run('eventq',296,11,'talk');run('linear_dialog',296,11,'--active')
assert locate(302)[0]==302
run('party_swap',0,3)
run('eventq',302,2,'talk');run('linear_dialog',302,2,'--active');stage(13)
run('q','302,10,41,down,wait:2')
