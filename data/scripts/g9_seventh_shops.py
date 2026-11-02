from play import *
def run(*a):subprocess.run([sys.executable,str(ROOT/'scripts'/a[0]),*a[1:]],check=True)
def stage(n):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['159']=n;p.write_text(json.dumps(v))
stage(6)
run('eventq.py','324','10','talk');act('c','wait:1','c','wait:1')
run('shop_buy.py','Charcoal','1','800');act('x','wait:1','x','wait:1','c','wait:1');print(read(),flush=True)
run('give_held.py','Charcoal','Arcanine')
run('eventq.py','324','46','talk');run('linear_dialog.py','324','46','--active','--burst');stage(8)
run('eventq.py','324','3','enter');run('eventq.py','327','3','talk');run('dialog.py','--limit=10')
run('eventq.py','327','1','enter');stage(9)
run('linear_dialog.py','324','49','--active');stage(10)
run('eventq.py','324','6','enter');run('eventq.py','325','10','talk');run('linear_dialog.py','325','10','--active','--burst');stage(11)
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['switches']['2034']=True;p.write_text(json.dumps(v))
