"""Choose one reviewed move, then await the next public decision screen."""
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
args = sys.argv[1:]
assert args and args[0] in ('0', '1', '2', '3')
move = subprocess.run([sys.executable, str(root / 'battle_move.py'), *args, '--watch'])
if move.returncode:
    raise SystemExit(move.returncode)
raise SystemExit(subprocess.call([sys.executable, str(root / 'battle_ready.py')]))
