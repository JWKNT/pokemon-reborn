"""Spend 28 earned XL candies, calculated from the explicit JB3 frozen EXP."""
import os,sys,subprocess,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1')
def run(s,*a):
 print('CANDY',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
for name,n in [('Zapdos',6),('Aegislash',5),('Swampert',5),('Sylveon',4),('Mawile',3),('Amoonguss',5)]:run('train_candy_one',name,n,'XL')
run('eventq',38,3,'talk');run('heal');run('checkpoint','Postgame251-Cap115Party')
s=json.loads((R/'notes/Postgame251-Cap115Party-status.json').read_text());assert all(m['level']==115 and m['hp']==m['totalhp'] for m in s['party'])
