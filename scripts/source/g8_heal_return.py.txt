from nav import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('q','318,9,19,down,wait:2','317,9,19,down,wait:2','316,9,19,down,wait:2','313,9,19,down,wait:2','293,9,38,down,wait:2')
run('eventq',293,7,'talk');run('dialog','--yes','--limit=8')
run('q','293,9,4,up,wait:2','293,9,30,up,wait:2','313,9,6,up,wait:2','316,9,6,up,wait:2','317,9,6,up,wait:2')
print('HEALED AND RETURNED TO FOURTH ROOM',flush=True)
