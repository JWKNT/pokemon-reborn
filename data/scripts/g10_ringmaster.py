from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('mark_event',355,47)
run('eventq',355,76,'talk');run('linear_dialog',355,76,'--active','--burst')
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v.setdefault('self_switches',{})['355,76,A']=True;p.write_text(json.dumps(v))
run('eventq',355,79,'talk');run('linear_dialog',355,79,'--active','--burst')
v=json.loads(p.read_text());v['variables']['173']=4;p.write_text(json.dumps(v))
print('SAMSON INTRO COMPLETE',flush=True)
