"""Take an inspected held item from a named party member, ordinary menus."""
from play import *
name=sys.argv[1]
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('party_open');run('party_pick',name,'--single')
run('choose_dialog','Summary|Switch|Item|Rename|Cancel','Item')
run('choose_dialog','Give|Take|Cancel','Take')
t=read();print(t,flush=True)
if not any(w in t.lower()for w in ['received','took','taken']):raise SystemExit('Held item take result review')
act('c:.12','wait:.5');run('overworld')
