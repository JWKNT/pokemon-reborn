from play import *
def run(*args):subprocess.run([sys.executable,str(ROOT/'scripts'/args[0]),*args[1:]],check=True)
run('q.py','291,48,49,down:0.22,wait:1','292,43,8,right:0.22,wait:2')
run('g9_iolia_first.py')
