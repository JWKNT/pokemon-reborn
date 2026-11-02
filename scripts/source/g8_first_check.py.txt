from nav import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('eventq',313,43,'talk');run('choose_dialog','Yes|No','Yes');run('linear_dialog',313,43,'--active','--past-choice')
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['150']=30;p.write_text(json.dumps(v))
run('eventq',313,10,'talk');run('battle_batch','Drapion',0,'--foes','sigilyph','--watch','--turns',5,'--min-hp',.2)
