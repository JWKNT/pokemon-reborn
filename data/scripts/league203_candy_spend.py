"""Spend normally earned XL candies from a verified owned checkpoint."""
import json,pathlib,subprocess,sys,math,os
R=pathlib.Path(__file__).resolve().parents[1]
label=sys.argv[1];names=sys.argv[2:];assert names
raw=subprocess.check_output(['ruby','-e',"require_relative 'scripts/read_rgss';v=load_rgss(ARGV[0]);puts JSON.generate(plain(v[:Trainer]))",str(R/'backups'/f'Aster-{label}.rxdata')],cwd=R,stderr=subprocess.DEVNULL)
t=json.loads(raw);party=t['party'];s=json.loads((R/'notes'/f'{label}-status.json').read_text())
caps={'ARCANINE':1250000,'SWAMPERT':1059860,'MIENSHAO':1059860,'SYLVEON':1000000,'CRYOGONAL':1000000,'COFAGRIGUS':1000000,'EXCADRILL':1000000,'KRICKETUNE':1059860,'KLINKLANG':1059860,'MAWILE':800000,'SWABLU':600000,'ALTARIA':600000}
plan=[]
for name in names:
 m=next(m for m in party if m['name']==name);needed=max(0,math.ceil((caps[m['species']]-m['exp'])/30000));plan.append({'name':name,'species':m['species'],'exp':m['exp'],'xl':needed})
assert sum(p['xl']for p in plan)<=s['bag']['contents'].get('EXPCANDYXL',0),plan
(R/'work'/f'{label}-candy-spend.json').write_text(json.dumps(plan,indent=2)+'\n');print('NORMAL CANDY PLAN',plan,flush=True)
def run(script,*args):subprocess.run([sys.executable,str(R/'scripts'/f'{script}.py'),*map(str,args)],check=True,env={k:v for k,v in os.environ.items()if k!='REBORN_FAST_KEYS'})
for p in plan:
 if p['xl']:run('train_candy_one',p['name'],p['xl'],'XL')
run('checkpoint',label+'-leveled')
st=json.loads((R/'notes'/f'{label}-leveled-status.json').read_text());
for p in plan:
 expected_names={p['name']}
 if p['species']=='SWABLU' and p['name']=='Swablu':expected_names.add('Altaria')
 matches=[m for m in st['party'] if m['name'] in expected_names]
 assert len(matches)==1 and matches[0]['level']==100,(p,matches)
 if p['species']=='SWABLU':assert matches[0]['species']=='ALTARIA' and any(z['move']=='PERISHSONG' for z in matches[0]['moves']),matches[0]
print('LEVEL100 VERIFIED',names,flush=True)
