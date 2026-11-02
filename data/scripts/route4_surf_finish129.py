"""Finish from root's recorded visual Surf/50,24 review; fresh guards, no replay."""
import os
os.environ['REBORN_COORD_CACHE']='1'
from play import *
from locate import locate
from void_batch_route import world_guard
from post_hypno_exit import mirror_page,source_event

def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
world_guard();assert locate(715)==(715,50,24)
world_guard();act('down:.12','wait:.5');world_guard();assert locate(715)==(715,50,25)
mirror_page(715,97,source_event(715,97)['pages'][0])
assert json.loads((ROOT/'notes/navigation-state.json').read_text())['switches']['410'] is True
run('surface_walk',715,57,21)
world_guard();assert locate(715)==(715,57,21)
run('eventq',715,64,'item')
world_guard();run('checkpoint','Route4-Scale-129')
s=json.loads((ROOT/'notes/Route4-Scale-129-status.json').read_text());n=json.loads((ROOT/'notes/Route4-Scale-129-navigation.json').read_text())
assert s['bag']['contents']['HEARTSCALE']==1 and n['self_switches']['715,64,A'] is True
run('calcenon_agate_queue','--execute','--phase','fly-circus','--party-status',ROOT/'notes/Route4-Scale-129-status.json','--journal',ROOT/'work/route4-circus-fly-129.json')
run('checkpoint','Circus-Cofa-before-shopping-129')
run('agate_prep_phase','shops','--status',ROOT/'notes/Circus-Cofa-before-shopping-129-status.json','--execute')
run('checkpoint','Circus-Cofa-after-shopping-129')
run('agate_prep_phase','build','--status',ROOT/'notes/Circus-Cofa-after-shopping-129-status.json','--execute')
