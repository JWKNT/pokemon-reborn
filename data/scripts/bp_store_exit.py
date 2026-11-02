from play import *
for _ in range(8):
 t=read();print(t,flush=True)
 if 'what would you like today' in t.lower():act('x','wait:.5');print(read());break
 if not any(s in t.lower()for s in ['obtained','obrtained','aster put','anything else','you have']):
  act('wait:.7');t=read()
 assert any(s in t.lower()for s in ['obtained','obrtained','aster put','anything else','you have']),t
 act('c','wait:.3')
else:raise SystemExit('Store exit review')
