"""Store four verified party members in empty Box4; begins at Cresselia Store menu."""
from play import *
for name in ['Magearna','Darkrai','Rayquaza']:
 t=read();assert name.lower() in t.lower(),t
 if not ('--resume-box-choice' in sys.argv and name=='Cresselia'):
  assert 'store' in t.lower() and 'selected' in t.lower(),t
  act('c','wait:1.2');t=read()
 assert 'deposit in which' in t.lower() and re.search(r'[•›>]\s*Box\W*2',t,re.I),t
 act('down:.12','wait:.2','down:.12','wait:.3');t=read();assert re.search(r'[•›>]\s*Box\W*4',t,re.I),t
 act('c','wait:1.5');t=read();print('STORED',name,t,flush=True)
 if name!='Rayquaza':act('c','wait:1')
assert 'latios' in t.lower(),t
act('x','wait:.5')
subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','No'],check=True)
act('x','wait:.5','x','wait:.5')
subprocess.run([sys.executable,str(ROOT/'scripts/overworld.py')],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),'Neoteric377-Solo-Latios'],check=True)
