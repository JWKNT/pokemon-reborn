from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('choose_dialog','Yes|No','Yes')
run('play','c','wait:.8')
run('mart_exit');run('checkpoint','Idyll317-Medicine')
run('eventq',38,6,'enter');run('fly_to',520,'--carrier','Zapdos')
run('eventq',520,67,'enter');run('eventq',369,1,'talk');run('mart_open')
run('shop_buy','Timer Ball',40,1000);run('mart_exit');run('checkpoint','Idyll317-Balls')
