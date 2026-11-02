"""Reach Aegir via Charous and the normal descending waterfall; no battle trigger."""
from play import *
def run(s,*a):
 print('AEGIR TRAVEL',s,*a,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('eventq',849,54,'talk')
run('choose_dialog','Yes|No','Yes','--source',849,54)
run('play','c','wait:3')
from locate import locate
assert locate(850)[0]==850
run('teach_machine','TM80','Rayquaza','Rock Slide',1)
run('teach_machine','TM17','Rayquaza','Protect',3)
run('checkpoint','Aegir370-Arrived')
