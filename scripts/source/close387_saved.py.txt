"""Quit normally after a fresh named overworld save; close and freeze recording."""
import subprocess,sys,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
label=sys.argv[1]
s=json.loads((R/'notes'/f'{label}-status.json').read_text())
assert not (R/'work/active-trainer-music.json').exists()
assert time.time()-(R/'notes'/f'{label}-status.json').stat().st_mtime<180
assert (R/'backups'/f'Aster-{label}.rxdata').read_bytes()==(Path.home()/'Library/Application Support/Pokemon Reborn/Game_3.rxdata').read_bytes()
subprocess.run([str(R/'scripts/native_quit')],check=True)
time.sleep(2)
for script,args in [('quit_saved_game',[label]),('record_session',['stop','387','--close-only']),('freeze_closed_public_logs',['387','work/session387-closed-public'])]:
 subprocess.run([sys.executable,str(R/'scripts'/f'{script}.py'),*args],check=True)
