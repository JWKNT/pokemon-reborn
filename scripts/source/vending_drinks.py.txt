"""Buy a bounded number of drinks from an already open, source-reviewed vending menu."""
from play import *
from PIL import Image

name = sys.argv[1]
count = int(sys.argv[2])
assert name in ('Fresh Water', 'Soda Pop', 'Lemonade') and 1 <= count <= 20
labels = ['Fresh Water - $200', 'Soda Pop - $300', 'Lemonade - $350', 'Cancel']
def is_menu(t):
    compact = ''.join(t.split())
    return all(word in compact for word in ['freshwater', 'sodapop', 'lemonade', 'cancel'])
def dropped(t):
    return 'dropped down' in t.replace('doun', 'down')
def cursor():
    rows = snap()
    words = sorted([r for r in rows if r['x'] > .45 and any(''.join(s.lower().split()) in ''.join(r['text'].lower().split()) for s in ['Fresh Water', 'Soda Pop', 'Lemonade', 'Cancel'])], key=lambda r:r['y'])
    assert len(words) == 4, 'Four drink labels required'
    im = Image.open(STATE).convert('RGB');w,h=im.size
    scores=[]
    for r in words:
        x0=int(w*(r['x']-.029));x1=int(w*(r['x']-.008))
        y0=int(h*(r['y']+.002));y1=int(h*(r['y']+r['h']-.002))
        pixels=list(im.crop((x0,y0,x1,y1)).getdata())
        scores.append(sum(max(p)<150 for p in pixels)/len(pixels))
    cur=max(range(4),key=lambda i:scores[i])
    assert scores[cur]>.15 and scores[cur]-sorted(scores)[-2]>.10, ('Vending arrow review',scores)
    return cur
def select(index):
    cur=cursor()
    for _ in range(4):
        if cur==index:break
        act('down:.12' if index>cur else 'up:.12', 'wait:.15')
        cur=cursor()
    assert cur==index, 'Selected drink cursor must match before payment'
    act('c', 'wait:.9')
for bought in range(count):
    t = read().lower()
    for _ in range(8):
        if is_menu(t):
            break
        if dropped(t):
            act('c', 'wait:.3')
        else:
            raise SystemExit('Vending menu review: ' + t)
        t = read().lower()
    else:
        raise SystemExit('Vending return timeout')
    select(['Fresh Water', 'Soda Pop', 'Lemonade'].index(name))
    t = read().lower()
    if name.lower() not in t or not dropped(t):
        raise SystemExit('Purchase result review: ' + t)
    print('PURCHASE VERIFIED', bought + 1, name, flush=True)
    act('c', 'wait:.8')
for _ in range(8):
    t = read().lower()
    if is_menu(t):
        select(3)
        break
    if not dropped(t):
        raise SystemExit('Final vending menu review: ' + t)
    act('c', 'wait:.3')
else:
    raise SystemExit('Final vending timeout')
print('VENDING PURCHASES COMPLETE', count, name, flush=True)
