"""Continue the verified room-two exit to both reviewed Distorted Space orbs."""
import os,subprocess,sys
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_STEP_PAUSE='.10',REBORN_ROUTE_CHUNK='56')
def run(s,*a):
 print(s,a,flush=True);subprocess.run([sys.executable,'scripts/'+s+'.py',*map(str,a)],check=True)
run('eventq',891,8,'enter')
run('linear_dialog',891,144,'--source-page',7,'--burst')
run('checkpoint','Giratina360-RoomThree')
run('distorted_space_execute','work/360-room3-left-plan.json')
run('eventq',890,207,'talk')
run('checkpoint','Giratina360-LeftOrb')
run('distorted_space_execute','work/360-room3-right-plan.json')
run('eventq',891,208,'talk')
run('checkpoint','Giratina360-Orbs')
