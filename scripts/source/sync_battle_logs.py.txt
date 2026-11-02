"""Keep read-only copies of Aster's official battle logs before the game rotates them."""
import pathlib,shutil,re
root=pathlib.Path(__file__).resolve().parents[1]
src=pathlib.Path.home()/'Library/Application Support/Pokemon Reborn/Battle Logs'
out=root/'notes/battle-logs';out.mkdir(exist_ok=True)
copied=0
for p in src.glob('*.txt'):
 if not re.match(r'\d{4}-\d{2}-\d{2}_.* - Aster(?: and| vs\.)',p.name):continue
 q=out/p.name
 if not q.exists() or p.stat().st_mtime>q.stat().st_mtime:shutil.copy2(p,q);copied+=1
print('Official Aster battle logs preserved',copied)
