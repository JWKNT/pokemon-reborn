"""Enter final-tier hub and freeze the legitimate new cap."""
import subprocess,sys
for cmd in [('city_enter',527,826),('city_enter',826,827),('checkpoint','Nightclub389-Cap150')]:
 print(cmd,flush=True);subprocess.run([sys.executable,'scripts/'+cmd[0]+'.py',*map(str,cmd[1:])],check=True)
