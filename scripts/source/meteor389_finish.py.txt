"""Select owned Giratina for the inspected meteor event, then save normally."""
import subprocess,sys
for cmd in [('party_pick','Giratina','--single'),('overworld',),('checkpoint','Prisma389-MeteorRemoved')]:
 print(cmd,flush=True);subprocess.run([sys.executable,'scripts/'+cmd[0]+'.py',*map(str,cmd[1:])],check=True)
