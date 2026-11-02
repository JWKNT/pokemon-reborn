"""Select a numbered storage box through its header, preserving visible checks."""
from play import *
from PIL import Image
target=int(sys.argv[1]);assert 1<=target<=50
rows=snap();text=' '.join(r['text'] for r in rows)
match=re.search(r'\bB(?:l)?ox\s+(\d+)\b',text,re.I)
if not match:
 p=ROOT/'work/pc-select-header.png'
 Image.open(ROOT/'recordings/capture-preview.png').crop((517,48,635,90)).resize((708,252)).save(p)
 text=' '.join(r['text']for r in json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(p)])))
 match=re.search(r'\bB(?:l)?ox\s+(\d+)\b',text,re.I)
assert match,'Storage box header needs review: '+text
current=int(match[1]);assert abs(current-target)<=5,'Only nearby observed box change allowed'
if current!=target:
 # Caller must have just opened Organize with cursor at slot0.
 act('up:.12','wait:.3')
 for _ in range(abs(current-target)):act(('left' if target<current else 'right')+':.12','wait:.9')
 act('down:.12','wait:.2','left:.12','wait:.2','left:.12','wait:.3')
print(read(),flush=True)
