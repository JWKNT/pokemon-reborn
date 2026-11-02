from play import *
def heal():
 t=read().lower()
 if 'fight' not in t:raise SystemExit('Heal needs command menu')
 # Call only with Fight selected (the training driver restores it each turn).
 act('right','c','wait:0.8')
 if 'items' in read().lower():act('right','wait:0.5')
 for i in range(14):
  t=read().lower();flat=''.join(t.split())
  if 'medicine' not in t and 'medieine' not in t and 'nedicine' not in t:
   raise SystemExit('Heal pocket review')
  if '60hp' in flat:break
  act('down','wait:0.2')
 else:raise SystemExit('Super Potion selection review')
 act('c','c','wait:0.8','c','wait:0.6','c','wait:3')
 
 for _ in range(20):
  t=read()
  if 'fight' in t.lower() or ('cancel' in t.lower() and t.lower().count('hp')>=5):break
  act('wait:0.5')
 print('HEALED',t,flush=True)
if __name__=='__main__':heal()
