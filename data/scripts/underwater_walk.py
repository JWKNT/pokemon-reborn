"""Use the underwater map's ordinary passability; bounded coordinate-checked route."""
from play import *
from locate import locate
m,x,y=map(int,sys.argv[1:4])
# Diving moves more slowly than running. Let each ordinary step finish
# before a direction change, avoiding dropped fast taps and repeated routes.
env=dict(os.environ,REBORN_ROUTE_STEP_PAUSE='0.10')
subprocess.run([sys.executable,str(ROOT/'scripts/q.py'),f'{m},{x},{y}'],check=True,env=env)
