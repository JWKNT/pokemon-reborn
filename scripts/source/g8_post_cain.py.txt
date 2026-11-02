from nav import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def stage(n):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['150']=n;p.write_text(json.dumps(v))
stage(8)
run('eventq',293,12,'talk');run('linear_dialog',293,12,'--active')
run('q','293,10,38,down,wait:2')
run('eventq',293,7,'talk');run('dialog','--limit=8','--yes')
save();raw=subprocess.check_output(['ruby',str(ROOT/'scripts/status.rb')],stderr=subprocess.DEVNULL);(ROOT/'notes/g8-after-cain.json').write_bytes(raw);v=json.loads(raw);assert all(p['hp']==p['totalhp'] for p in v['party'])
run('eventq',293,18,'talk');run('linear_dialog',293,18,'--active');stage(9)
run('q','293,10,11,down,wait:2')
