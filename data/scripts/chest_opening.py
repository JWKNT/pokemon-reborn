"""Reviewed opening route and three bounded wild fights using public UI only."""
from play import *
from chest_safe_pause import classify
from hashlib import sha256
session,attempt=int(sys.argv[1]),int(sys.argv[2]);label=sys.argv[3]
status=ROOT/'notes'/f'{label}-status.json';save=ROOT/'backups'/f'Aster-{label}.rxdata'
journal=ROOT/f'recordings/chest-attempts/session{session}-chain{attempt}.json'
if '--resume-bag' not in sys.argv:
 assert not journal.exists()
 journal.write_text(json.dumps({'kind':'saphira-chest-defense','attempt':attempt,'session':session,'start_epoch':time.time(),'status':str(status.relative_to(ROOT)),'status_sha256':sha256(status.read_bytes()).hexdigest(),'save_sha256':sha256(save.read_bytes()).hexdigest(),'waves':[],'result':'active','roster_changes':[],'plan':'Early22,40 Mandi interception, spaced down steps into both Ambipom paths.'},indent=2))
 p=ROOT/'notes/current-run-control.json';v=json.loads(p.read_text());v['active_gauntlet']='saphira-chest-defense';v['active_gauntlet_journal']=str(journal.relative_to(ROOT));p.write_text(json.dumps(v,indent=2))
 act('down:.05','c:.12','wait:.5')
 subprocess.run([sys.executable,str(ROOT/'scripts/chest_start.py'),'--active'],check=True)
assert classify(snap())=='bag'
act('x:.12','wait:1','x:.12')
subprocess.run([str(ROOT/'scripts/key_fast'),*[v for k in ['left','down','down','left','left','left','up','up','up','up'] for v in [k+':.12','wait:.10']]],check=True)
act('wait:5')
for wave,foe,moves in [(1,'Mandibuzz','down,down,down,down'),(2,'Ambipom','down'),(3,'Ambipom','')]:
 env=dict(os.environ,REBORN_POST_BATTLE_MOVES=moves)
 subprocess.run([sys.executable,str(ROOT/'scripts/chest_wave.py'),'Arcanine','1',foe,str(wave)],env=env,check=True)
 r=snap();t=' '.join(x['text'] for x in r).lower()
 if 'saphira' in t:raise SystemExit('DEFENSE LOSS REVIEW')
 if wave<3 and classify(r)=='bag':act('x:.12','wait:1','x:.12','wait:3')
print('OPENING FINISHED; REVIEW NEXT WAVE',flush=True)
