from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('city_enter',522,530)
run('eventq',530,56,'enter')
run('eventq',56,5,'enter')
run('eventq',522,38,'enter')
q=ROOT/'work/317-eve-approach.json';q.write_text(json.dumps([[878,0,0,82,86,[]]]));run('queue_route',q)
run('checkpoint','Idyll317-EvePrepared')
