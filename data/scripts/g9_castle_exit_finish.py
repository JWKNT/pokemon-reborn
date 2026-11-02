from nav import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def navset(stage):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['159']=stage;p.write_text(json.dumps(v))
navset(1)
run('q','293,9,38,down,wait:2')
navset(2)
run('linear_dialog',293,31)
navset(3)
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['switches']['423']=True
for sw in [295,299,303,301,304,306,308,311,313,315,317,318,319,320,321,322,323]:v['switches'][str(sw)]=False
p.write_text(json.dumps(v))
run('eventq',292,22,'talk')
run('dialog','--limit=5')
print('OUTSIDE CASTLE AND HEALED — INSPECT BEFORE MAZE',flush=True)
