"""One source-reviewed climb avoiding all412 trainer sightlines, then resume next climb."""
import os
os.environ['REBORN_COORD_CACHE']='1'
from play import *
from locate import locate

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
assert locate(412)==(412,12,18)
run('eventq',412,1,'talk');run('dialog','--limit=10')
assert locate(710)==(710,23,49)
run('calcenon_agate_queue','--execute','--phase','approach','--climb-index',1,'--party-status',ROOT/'notes/Route4-carrier-129-status.json','--journal',ROOT/'work/calcenon-route4-climbs-129b.json')
