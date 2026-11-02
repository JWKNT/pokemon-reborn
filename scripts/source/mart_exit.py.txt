"""Close a reviewed vendor's menus and exit dialogue, inspecting each transition."""
from play import *
from PIL import Image
for _ in range(12):
 t=read();low=t.lower();print(t,flush=True)
 if 'here you are' in low and ('thank you' in low or 'thankyou' in low):
  act('c:.12','wait:.8');continue
 if 'sort' in low and ('close bag' in low or 'items' in low):
  act('x:0.12','wait:1');continue
 if ('quit' in low or 'buit' in low) and ('sell' in low or '\nell\n' in '\n'+low+'\n'):
  act('x:0.12','wait:1');continue
 if ('$' in low and any(z in low for z in ['money:','honey:','cancel','chancel','chncel'])) or (len(re.findall(r'\$\s*\d',t))>=4 and not any(z in low for z in ['how many','yes','no\n'])):
  act('x:0.12','wait:1');continue
 if any(z in low for z in ['fight','do what with','would you like to save','pokedex','yes','no\n']):raise SystemExit('Vendor exit review')
 im=Image.open(STATE).convert('RGB');w,h=im.size;b=im.crop((int(w*.08),int(h*.75),int(w*.90),int(h*.87)))
 box=sum(min(px)>235 and max(px)-min(px)<5 for px in b.getdata())/(b.width*b.height)>.55
 if box:act('c:0.12','wait:1');continue
 if len(low.splitlines())<5:print('VENDOR CLOSED',flush=True);break
 raise SystemExit('Unexpected vendor screen')
else:raise SystemExit('Vendor exit limit')
