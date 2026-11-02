"""Advance Anna's reviewed fake ending with normal UI reloads and saved evidence.

Run while the first reloaded 'gold and ivory keys' message is visible.
Stops on the third reload's message, before the final reveal.
"""
from play import *
import shutil, hashlib

native = pathlib.Path.home()/'Library/Application Support/Pokemon Reborn/Game_3.rxdata'
journal_path = ROOT/'notes/giratina361-normal-reloads.json'
journal = json.loads(journal_path.read_text()) if journal_path.exists() else []
stages = [3] if '--last-only' in sys.argv else [2, 3]
for stage in stages:
    text = read().lower()
    assert all(s in text for s in ['anna', 'gold and ivory keys']), text
    before = native.stat().st_mtime
    act('c', 'wait:2')
    text = read().lower()
    assert 'bad' in text and 'end' in text and 'anna' not in text, text
    assert native.stat().st_mtime > before, 'Scripted autosave did not advance'
    backup = ROOT/'backups'/f'Aster-Giratina361-BadEnd{stage}.rxdata'
    shutil.copy2(native, backup)
    journal.append(dict(stage=stage, epoch=time.time(), save_mtime=native.stat().st_mtime,
                        backup=str(backup.relative_to(ROOT)), sha256=hashlib.sha256(backup.read_bytes()).hexdigest()))
    journal_path.write_text(json.dumps(journal, indent=2))
    act('f12', 'wait:4')
    text = read().lower()
    # ENTER blinks; the rendered title still contains two REBORN labels.
    assert text.count('reborn') == 2 and 'continue' not in text and 'bad' not in text, text
    act('c', 'wait:2')
    text = read().lower()
    assert all(s in text.replace('distor ted', 'distorted') for s in ['continue', 'aster', 'distorted space']), text
    act('c', 'wait:7')
    text = read().lower()
    assert 'anna' in text and 'gold and ivory keys' in text, text
    print('NORMAL RELOAD VERIFIED', stage+1, text, flush=True)
print('Third reload reached; final story message remains for reviewed dialogue.', flush=True)
