from nav import *
def run(s,*a):
 if s=='q':
  f=ROOT/'work/g8-logic-route.json';f.write_text(json.dumps([['q',*a]]));s='safe_steps';a=(f,)
 subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def stage(n):
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['variables']['150']=n;p.write_text(json.dumps(v))
run('choose_dialog','Yes|No','Yes');run('linear_dialog',309,3,'--active','--past-choice');stage(19)
run('eventq',309,9,'talk');run('linear_dialog',309,9,'--active');stage(20)
run('q','309,15,3,up,wait:2','310,7,77,up,wait:2')
for eid,answer,sw in [(39,'Light',397),(40,'Dark',398),(41,'Dark',400),(42,'Light',399)]:
 run('eventq',310,eid,'talk');run('choose_dialog','Light|Dark',answer);run('dialog','--limit=5')
 p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v['switches'][str(sw)]=True;p.write_text(json.dumps(v))
stage(21)
run('q','310,7,40,up,wait:2')
run('eventq',310,43,'talk');run('dialog','--limit=5')
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v.setdefault('self_switches',{})['310,43,A']=True;p.write_text(json.dumps(v))
run('q','310,7,62,down,wait:2')
f=ROOT/'work/g8-to-el.json';f.write_text(json.dumps([['q','306,33,28']]))
run('safe_steps',f)
run('party_swap',0,4)
save();raw=subprocess.check_output(['ruby',str(ROOT/'scripts/status.rb')],stderr=subprocess.DEVNULL);(ROOT/'notes/g8-before-el.json').write_bytes(raw);v=json.loads(raw);assert v['party'][0]['species']=='COFAGRIGUS' and v['party'][0]['hp']==v['party'][0]['totalhp']
print('EL READY AND SAVED',flush=True)
