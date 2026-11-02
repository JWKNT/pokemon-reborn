"""Use one Rare Candy, resolving inspected natural moves through ordinary UI."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('field_medicine','Rare Candy',sys.argv[1]);run('candy_progress');run('overworld')
