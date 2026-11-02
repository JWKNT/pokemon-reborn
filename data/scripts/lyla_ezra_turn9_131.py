"""Root-reviewed single remaining active Mantine; finite2normalactions."""
import subprocess,sys
from play import ROOT,read
from hypno_turn import name_matches
t=read();assert name_matches(t,'Hexan') and name_matches(t,'Mantine') and 'fight'in t.lower()
def run(*a):subprocess.run([sys.executable,str(ROOT/'scripts/battle_move.py'),*map(str,a)],check=True)
run(3,3,'--foe-names','Haxorus,Mantine','--watch')
t=read();assert name_matches(t,'Excadrill') and 'fight'in t.lower()
run(2,'--watch')
