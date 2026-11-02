"""Resume after confirmed53E10 dialogue; do not duplicate shopping or recruitment."""
from play import *
def r(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
r('recruit_volunteer.py',53,10,'--active-dialogue');r('city_enter.py',53,530)
r('city_enter.py',530,531);r('recruit_volunteer.py',531,3);r('city_enter.py',531,530)
r('city_enter.py',530,522);r('city_enter.py',522,594);r('recruit_volunteer.py',594,5);r('city_enter.py',594,522)
r('checkpoint.py','Adrienn-recruitment-eleven')
assert json.loads((ROOT/'notes/Adrienn-recruitment-eleven-navigation.json').read_text())['variables']['339']==61
for block in [4,5]:r('adrienn_volunteer_circuit.py',block)
