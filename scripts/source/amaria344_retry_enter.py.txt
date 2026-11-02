"""Capture the fresh Amaria retry roster, then enter its reviewed normal fight."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1')
def run(s,*a):
 subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('major_attempt','start',R/'work/major-207.json',344,'--status',R/'notes/Amaria343-Retry-status.json')
run('trainer_enter',850,125,'UMBAMARIA','Amaria')
run('major_battle_intro',R/'work/major-207.json',344)
