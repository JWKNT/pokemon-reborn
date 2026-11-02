"""Use a bounded vitamin quantity through the public bag and party menus."""
from play import *
from PIL import Image

item, name, count = sys.argv[1:4]
count = int(count)
assert item in ['HP Up', 'Protein', 'Iron', 'Calcium', 'Zinc', 'Carbos']
assert 1 <= count <= 8
subprocess.run([sys.executable, str(ROOT/'scripts/field_medicine.py'), item, name,
                *(['--bag-open'] if '--bag-open' in sys.argv else [])], check=True)
t = read()
assert 'how many' in t.lower(), ('Vitamin quantity prompt required', t)
act(*[key for _ in range(count-1) for key in ('up:.12', 'wait:.12')], 'wait:.3')
snap()
im = Image.open(STATE)
w, h = im.size
p = ROOT/'work/vitamin-quantity.png'
im.crop((int(w*.82), int(h*.82), int(w*.94), int(h*.92))).resize((600,400)).save(p)
qty = ' '.join(v['text'] for v in json.loads(subprocess.check_output([str(ROOT/'scripts/observe'), str(p)])))
print('VITAMIN QUANTITY', qty, flush=True)
assert re.search(r'(?<!\d)0*'+str(count)+r'(?!\d)', qty), 'Quantity verification failed; no use confirmed'
act('c', 'wait:.7')
t = read()
print(t, flush=True)
assert 'increased' in t.lower(), 'Vitamin result needs review'
act('c', 'wait:.5')
t = read()
if 'used your last' in t.lower():
    act('c', 'wait:.5')
subprocess.run([sys.executable, str(ROOT/'scripts/overworld.py')], check=True)
print('VITAMIN USE COMPLETE; verify EVs at next ordinary checkpoint', flush=True)
