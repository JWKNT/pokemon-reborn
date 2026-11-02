from play import *
def r(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
r('connected_walk.py',544,525,21,23);r('connected_walk.py',525,551,15,12);r('recruit_volunteer.py',551,18)
r('checkpoint.py','Adrienn-all-volunteers')
assert json.loads((ROOT/'notes/Adrienn-all-volunteers-navigation.json').read_text())['variables']['339']==65
act('x','wait:.5');print(read(),flush=True)
