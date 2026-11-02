"""Heal minor training damage, route to Fiore, verify the fixed gauntlet build."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
if '--verify-only' not in sys.argv:
 run('field_medicine','Hyper Potion','Cofagrigus');run('overworld')
 run('use_field_item','Super Repel');run('circus_to_fiore',1)
 run('q','359,50,55')
 run('checkpoint','Fiore-speed-ready')
s=json.loads((ROOT/'notes/Fiore-speed-ready-status.json').read_text());ms={m['name']:m for m in s['party']}
assert s['map']==359 and s['position']==[50,55]
assert s['trainer']['badges'].count(True)==12 and s['party'][0]['name']=='Cofagrigus'
assert all(m['level']==75 and m['hp']==m['totalhp'] for m in s['party'])
assert ms['Hexan']['speed']==172 and ms['Hexan']['ev']==[252,0,75,41,0,142],ms['Hexan']
assert ms['Mienshao']['speed']==181 and ms['Mienshao']['ev'][5]==97,ms['Mienshao']
assert ms['Hexan']['item'] is None and ms['Mienshao']['item'] is None
assert ms['Arcanine']['ability']=='INTIMIDATE'
print('FIORE FULL RUN BUILD VERIFIED — CRYO172 / MIENSHAO181 / INTIMIDATE / ALLHPFULL',flush=True)
