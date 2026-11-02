"""Take a named party member's verified held item through normal overworld UI."""
from play import *
import difflib
name,expected=sys.argv[1:3]
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
if '--menu-open'not in sys.argv:run('party_open');run('party_pick',name,'--single')
r=snap()
for v in r:
 v['text']=v['text'].strip(' •›>')
 if v['text'].lower()=='p summary':v['text']='Summary'
 if v['text'].lower()=='water fall':v['text']='Waterfall'
labels=[v for v in r if v['x']>.62 and .35<v['y']<.92 and v['text'].strip().lower()in['summary','relearn','switch','item','rename','cancel','cut','fly','surf','strength','flash','rock smash','waterfall','dive','rock climb','teleport','dig','sweet scent','headbutt']]
labels=sorted(labels,key=lambda x:x['y'])
words=[x['text'].strip().lower()for x in labels]
assert 'summary'in words and 'item'in words and 'cancel'in words,('Party action review',words)
# Caller opens a fresh action menu with installed Summary index0.
assert words[0]=='summary', 'Fresh default Summary menu required'
act(*[k for _ in range(words.index('item'))for k in ('down:.12','wait:.16')],'c','wait:.6')
rows=snap();menu=[v['text'].strip().lower()for v in rows if v['x']>.74 and v['y']>.45]
assert all(x in menu for x in ['give','take','cancel']),('Held item submenu review',menu)
# The freshly opened installed party submenu starts at Use. Its arrow makes
# that one word unreliable in OCR; the other three labels verify this menu.
act('down:.12','wait:.16','down:.12','wait:.16','c','wait:.7')
t=read();print(t,flush=True)
norm=lambda x:re.sub('[^a-z]','',x.lower())
receipt=next((line for line in t.splitlines()if 'from'in line.lower()and any(x in line.lower()for x in ['received','receiued'])), '')
itemtext=re.sub(r'^.*?the\s+|\s+from.*$','',receipt,flags=re.I)
assert receipt and (norm(expected)in norm(itemtext)or difflib.SequenceMatcher(None,norm(expected),norm(itemtext)).ratio()>=.78),'Held item take result review'
act('c','wait:.5');run('overworld')
