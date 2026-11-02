"""Sell one explicitly named inspected item in the ordinary mart bag screen."""
from play import *
import re
name,expected=sys.argv[1],int(sys.argv[2])
t=read().lower()
if not any(z in t for z in ['sort','close bag','how many','sell']) and sum(bool(re.match(r't[mh][a-z0-9]',z.strip())) for z in t.splitlines())<3:raise SystemExit('Mart selling bag expected')
for _ in range(9):
 if any(v['text'].strip().lower()=='items' for v in snap()):break
 act('left','wait:.3')
else:raise SystemExit('Items pocket expected')
subprocess.run([sys.executable,str(ROOT/'scripts/bag_select.py'),name],check=True)
act('c','wait:.7');t=read();print(t,flush=True)
if 'how many' in t.lower():
 act('c','wait:.6');t=read();print(t,flush=True)
if 'yes' not in t.lower() or 'canpay' not in re.sub(r'\s+','',t.lower()) or str(expected) not in re.sub('[^0-9]','',t):raise SystemExit('Sale price confirmation requires review')
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
t=read();print(t,flush=True)
if not any(z in t.lower() for z in ['thank','turned over','sold']):raise SystemExit('Sale result requires review')
act('c','wait:.5');print(read(),flush=True);print('SALE VERIFIED',name,expected,flush=True)
