"""Press one planned library monitor, then update the route notes only on success."""
import subprocess,sys,pathlib,json
root=pathlib.Path(__file__).resolve().parent.parent
n=int(sys.argv[1]);targets={18:(16,24,'up'),17:(2,24,'up'),62:(8,6,'up'),87:(4,4,'up'),55:(12,7,'up'),69:(16,7,'up'),91:(2,15,'up')}
x,y,k=targets[n]
r=subprocess.call([sys.executable,str(root/'scripts/q.py'),f'182,{x},{y},{k},c,wait:2,down,wait:.3'])
if r:raise SystemExit(r)
subprocess.run([sys.executable,str(root/'scripts/puzzle_note.py'),str(n)],check=True)
