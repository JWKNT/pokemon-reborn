"""Verified normal pushes across the lower Emerald floor."""
from play import *
for key,count,label in [('up',1,'U1'),('right',7,'R7'),('up',1,'U2'),('right',6,'R6East'),('up',8,'U8')]:
 subprocess.run([sys.executable,str(ROOT/'scripts/emerald212_boulder_fast.py'),'43',key,str(count),'Emerald212-B43-'+label],check=True)
