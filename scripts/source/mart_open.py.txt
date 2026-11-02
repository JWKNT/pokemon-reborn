"""Advance an inspected vendor greeting, stopping at its purchase list."""
from play import *
for _ in range(20):
 t=read();low=t.lower();print(t,flush=True)
 if 'how many' in low or 'yes' in low.splitlines() or 'no' in low.splitlines():raise SystemExit('Unexpected purchase prompt')
 if len(re.findall(r'\$\s*\d',t))>=4:
  print('PRICE LIST READY',flush=True);break
 if 'buy' in low and 'sell' in low and any(z in low for z in ['quit','money:','honey:']):
  act('c:0.12','wait:1');print(read(),flush=True);break
 if '$' in low and any(z in low for z in ['cancel','chancel','chncel']):break
 if any(z in low for z in ['fight','how many','yes','no\n','choose a pok','pp:']):raise SystemExit('Vendor greeting review')
 if len(low.splitlines())<2:raise SystemExit('Vendor dialogue missing')
 act('c:0.12','wait:.8')
else:raise SystemExit('Vendor greeting limit')
