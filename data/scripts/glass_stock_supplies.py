"""Normal department/Grand Hall shopping from a reviewed outdoor Fly origin."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
if '--from-shop' not in sys.argv:
 if '--from-clerk' not in sys.argv:
  run('fly_to',520)
  run('eventq',520,101,'enter');run('eventq',112,6,'enter')
  run('eventq',113,1,'talk')
 run('dept_greet');run('dept_floor',8)
 run('eventq',4,4,'talk');run('mart_open')
for name,count,price in [('X Sp. Def',6,350),('X Defend',5,550),('X Sp. Atk',6,350),('X Speed',4,350),('X Accuracy',2,950)]:run('shop_buy',name,count,price)
run('mart_exit');run('eventq',4,6,'enter')
run('eventq',113,1,'talk');run('dept_greet');run('dept_floor',1)
run('eventq',112,1,'enter');run('fly_to',519)
run('eventq',519,116,'enter');run('eventq',38,5,'talk');run('mart_open')
run('shop_buy','Ultra Potion',15,1200)
run('shop_buy','Super Repel',10,700)
run('mart_exit');run('eventq',38,6,'enter')
run('fly_to',413)
print('SUPPLIES BOUGHT; CALCENON FLY POINT',flush=True)
