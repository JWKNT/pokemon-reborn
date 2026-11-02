from play import *

def run(args):
 p=subprocess.Popen([sys.executable,*args],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);out=[]
 for line in p.stdout:print(line,end='',flush=True);out.append(line)
 if p.wait():raise SystemExit(2)
 return ''.join(out)
def route_steps(steps):
 p=ROOT/'notes/practice-route.json';p.write_text(json.dumps(steps));run([str(ROOT/'scripts/queue_route.py'),str(p)])
for i in range(int(sys.argv[1])):
 route_steps([[38,24,11,5,22,['up']]])
 run([str(ROOT/'scripts/heal.py')])
 route_steps([[38,5,22,24,11,['down','c','wait:1','c','wait:1','c','wait:3']]])
 out=run([str(ROOT/'scripts/train.py'),'65','Cutter','--still','--noswitch','--allowlow'])
 if 'OVERWORLD' not in out:raise SystemExit('Review training interruption')
 print('CAROL COMPLETE',i+1,flush=True)
