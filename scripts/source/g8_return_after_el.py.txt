from nav import *
from locate import locate
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def stage(n):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['150']=n;p.write_text(json.dumps(v))
assert locate(312)[0]==312
stage(23)
run('q','312,16,8,right,wait:2');run('linear_dialog',295,14,'--active');stage(24)
run('q','295,11,12,down,wait:2');run('choose_dialog','Yes|No','Yes');run('linear_dialog',79,104,'--active','--past-choice');stage(25)
assert locate(97)[0]==97
run('eventq',97,50,'talk');run('choose_dialog','Yes|No','Yes');run('linear_dialog',97,50,'--active','--past-choice');stage(26)
assert locate(292)[0]==292
run('q','292,16,16,up,wait:2');run('linear_dialog',293,10,'--active')
stage(27)
run('eventq',293,7,'talk');run('dialog','--yes','--limit=8')
save();raw=subprocess.check_output(['ruby',str(ROOT/'scripts/status.rb')],stderr=subprocess.DEVNULL);(ROOT/'notes/g8-after-el.json').write_bytes(raw);v=json.loads(raw);assert all(p['hp']==p['totalhp'] for p in v['party'])
flag=subprocess.check_output(['ruby','-I',str(ROOT/'scripts'),'-r','read_rgss','-e',"v=load_rgss('/Users/jw/Library/Application Support/Pokemon Reborn/Game_3.rxdata');puts v[:switches].instance_variable_get(:@data)[250]"],stderr=subprocess.DEVNULL).decode().strip();assert flag=='true',flag
for a,b in [(0,4),(1,4),(2,3),(3,4)]:run('party_swap',a,b)
print('HEALED, SAVED EL ROUTE FLAG, CHESS PARTY ORDER READY',flush=True)
