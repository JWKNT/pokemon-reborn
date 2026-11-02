"""Collect remaining Emerald Stars normally, stopping on unreviewed interruptions."""
from play import *
def run(script,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],check=True)
run('victory_wild_safe_event.py',809,26,'item')
run('checkpoint.py','Emerald213-Star2')
run('victory_wild_safe_event.py',809,47,'talk')
run('dialog.py','--limit=8')
run('checkpoint.py','Emerald213-Crystal47')
run('victory_wild_safe_event.py',809,48,'smash')
run('victory_wild_safe_event.py',809,25,'item')
run('checkpoint.py','Emerald213-AllStars')
