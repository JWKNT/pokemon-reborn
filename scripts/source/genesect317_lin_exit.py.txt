from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
q=ROOT/'work/317-lin-route.json';q.write_text(json.dumps([[596,0,0,74,7,[]]]));run('queue_route',q)
run('play','right:.12','wait:.5');run('linear_dialog',596,22,'--source-page',1,'--burst');run('checkpoint','Genesect317-LinPortal')
run('eventq',596,23,'enter');run('linear_dialog',877,202,'--source-page',1,'--burst');run('checkpoint','Genesect317-QuestComplete')
