"""Finish observed victory, one native checkpoint, actualnormalquit, closecapture."""
import subprocess,sys,json,time
from play import ROOT,read
assert 'defeated'in read().lower()
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('victory_outro')
run('trainer_music','finish','--world-verified')
label='Agate-street-won131'
run('checkpoint',label)
s=json.loads((ROOT/'notes'/f'{label}-status.json').read_text());n=json.loads((ROOT/'notes'/f'{label}-navigation.json').read_text())
assert s['map']==763 and n['variables']['391']==52
assert all(n['self_switches'].get(f'763,{i},A') is True for i in [45,46,49])
subprocess.run([str(ROOT/'scripts/native_quit')],check=True)
stop_epoch=time.time();(ROOT/'recordings/session-131.stop').touch()
for _ in range(100):
 processes=subprocess.check_output(['ps','-axo','command='],text=True).splitlines()
 if not any(x.strip().startswith('/Applications/Reborn.app/')for x in processes):break
 time.sleep(.2)
else:raise RuntimeError('Normalquit did notclosegame;save/capture retained')
run('quit_saved_game',label)
log=ROOT/'recordings/session-131-game-capture.log'
for _ in range(100):
 t=log.read_text()
 if 'DONE'in t:break
 time.sleep(.2)
else:raise RuntimeError('Capture closure did notfinish;raw retained')
assert 'status=2'in t
p=ROOT/'recordings/session-131.json';d=json.loads(p.read_text());dur=float(subprocess.check_output(['/opt/homebrew/bin/ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(ROOT/d['raw'])]));d.update(stop_epoch=stop_epoch,raw_duration=dur,wall_duration=stop_epoch-d['start_epoch']);p.write_text(json.dumps(d,indent=2))
c=ROOT/'notes/current-run-control.json';v=json.loads(c.read_text());v.update(game_saved_quit=True,native_checkpoint=label,recording_paused=True,recording_closed_session=131,game_quit_epoch=stop_epoch);c.write_text(json.dumps(v,indent=2))
print('SAVEDQUIT + CLOSED131',s['position'],dur,flush=True)
