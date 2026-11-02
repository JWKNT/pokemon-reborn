"""Read-only final shutdown evidence for the completed Hardy session."""
from pathlib import Path
import datetime,hashlib,json,subprocess
root=Path(__file__).resolve().parents[1]
meta=json.loads((root/'recordings/session-137.json').read_text())
rows=subprocess.check_output(['ps','-axo','pid=,comm=,args='],text=True).splitlines()
processes={int(row.split(None,1)[0]):row.split(None,1)[1]for row in rows if row.strip()}
assert not any(v.startswith('/Applications/Reborn.app/')for v in processes.values())
assert meta['pid']not in processes and meta['caffeinate_pid']not in processes
assert not any(v.startswith(str(root/'scripts/window_record'))for v in processes.values())
paths=[Path.home()/'Library/Application Support/Pokemon Reborn/Game_3.rxdata',root/'backups/Aster-Hardy137-won-paused.rxdata',root/'backups/Aster-Hardy137-won-paused-quit.rxdata']
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}
assert set(hashes.values())=={'9d9e9e7aa1fa444b34da3e127c287be647c2e015f7830299c925f274b184075b'}
s=json.loads((root/'notes/Hardy137-won-paused-status.json').read_text())
report={'status':'verified_saved_and_actually_quit','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'save_mtime':s['save_mtime'],'map':s['map'],'position':s['position'],'badges':s['trainer']['badges'].count(True),'hashes':hashes,'game_running':False,'recorder_running':False,'caffeinate_running':False,'recording_finalized':bool(meta['stop_epoch']),'latest_user_endpoint':'Finish this attempt, edit recording, stop for permission changes'}
(root/'notes/session137-savequit-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],report['badges'],'badges')
