from nav import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('q','315,9,33,down,wait:2','318,9,19,down,wait:2','317,9,19,down,wait:2','316,9,19,down,wait:2','313,9,19,down,wait:2')
print('CASTLE EXIT — REVIEW ELIAS SCENE',flush=True)
