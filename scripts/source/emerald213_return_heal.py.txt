"""Return through the earned Emerald shortcut and use the unused Light Shard."""
from play import *
def run(script,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],check=True)
run('victory_wild_safe_event.py',809,53,'enter')
run('victory_gem_cliff_event.py',791,50,'talk')
run('checkpoint.py','Emerald213-Healed')
s=json.loads((ROOT/'notes/Emerald213-Healed-status.json').read_text());assert all(p['hp']==p['totalhp'] for p in s['party'])
print('ALL SIX HEALED FROM NORMAL LIGHT SHARD',flush=True)
