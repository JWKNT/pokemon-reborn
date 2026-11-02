from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
for mid,eid in [(877,1),(596,1),(595,20),(594,26)]:run('eventq',mid,eid,'enter')
run('fly_to',519,'--carrier','Zapdos')
run('eventq',519,116,'enter')
run('eventq',38,3,'talk')
run('dialog','--limit','20')
run('checkpoint','Genesect316-Healed')
