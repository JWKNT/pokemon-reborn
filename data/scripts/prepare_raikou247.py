"""Assemble owned Raikou preparation party via verified PC exchanges."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1')
def run(s,*args):subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,args)],env=env,check=True)
for boxslot,slot,incoming,outgoing in [(16,1,'Sylveon','Cresselia'),(17,3,'Amoonguss','Hexan')]:
 run('q','38,9,20,up:.12,c,wait:1');run('pc_open_reviewed');run('pc_exchange_named',boxslot,slot,incoming,outgoing)
run('checkpoint','Postgame247-PrepParty')
