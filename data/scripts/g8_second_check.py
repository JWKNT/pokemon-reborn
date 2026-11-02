from nav import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('eventq',316,49,'talk');run('choose_dialog','Yes|No','Yes');run('linear_dialog',316,49,'--active','--past-choice')
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['150']=33;p.write_text(json.dumps(v))
run('eventq',316,43,'talk');run('battle_batch','Drapion',0,'--foes','meowstic,meougtic','--watch','--turns',8,'--stay','--min-hp',.2)
