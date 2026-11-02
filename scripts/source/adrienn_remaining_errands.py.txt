"""Sequential reviewed errand blocks, stop on any unrecognized input state."""
from play import *
for block in [3,4,5]:
 subprocess.run([sys.executable,str(ROOT/'scripts/adrienn_volunteer_circuit.py'),str(block)],check=True)
 print('NATIVE MILESTONE COMPLETE BLOCK',block,flush=True)
