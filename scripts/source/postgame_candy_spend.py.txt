"""Calculate candy from an explicit owned save and installed growth curves; use normal UI."""
import json,pathlib,subprocess,sys,os
R=pathlib.Path(__file__).resolve().parents[1]
label,target=sys.argv[1],int(sys.argv[2]);assert 105<=target<=150 and target%5==0
s=json.loads((R/'notes'/f'{label}-status.json').read_text())
nav=json.loads((R/'notes'/f'{label}-navigation.json').read_text());assert nav['variables']['595']+100==target
ruby="""require_relative 'scripts/read_rgss';MAXIMUMLEVEL=200
load '/Applications/Reborn.app/Contents/Game/Scripts/PBExperience.rb'
load '/Applications/Reborn.app/Contents/Game/Scripts/Reborn/montext.rb'
p=plain(load_rgss(ARGV[0])[:Trainer])['party']; puts JSON.generate(p.map{|m|g=MONHASH[m['species'].to_sym].values.first[:GrowthRate];goal=PBExp.pbGetExpInternal(ARGV[1].to_i,g);{name:m['name'],exp:m['exp'],target_exp:goal,xl:[0,((goal-m['exp'])/30000.0).ceil].max}})"""
plan=json.loads(subprocess.check_output(['ruby','-e',ruby,str(R/'backups'/f'Aster-{label}.rxdata'),str(target)],cwd=R,stderr=subprocess.DEVNULL))
need=sum(x['xl'] for x in plan);stock=s['bag']['contents'].get('EXPCANDYXL',0)
(R/'work'/f'{label}-candy-plan.json').write_text(json.dumps(dict(target=target,need=need,stock=stock,party=plan),indent=2)+'\n')
print('CANDY PLAN',plan,'need',need,'stock',stock,flush=True);assert need<=stock,'Earn more candy before spending'
if '--plan-only' in sys.argv:raise SystemExit(0)
env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1')
def run(name,*args):subprocess.run([sys.executable,str(R/'scripts'/f'{name}.py'),*map(str,args)],env=env,check=True)
for m in plan:
 remaining=m['xl']
 while remaining:
  count=min(35,remaining)
  run('train_candy_one',m['name'],count,'XL')
  remaining-=count
run('eventq',38,3,'talk');run('heal');run('checkpoint',label+'-Cap'+str(target))
post=json.loads((R/'notes'/f'{label}-Cap{target}-status.json').read_text());assert all(m['level']==target and m['hp']==m['totalhp'] for m in post['party'])
print('FULL PARTY CAP VERIFIED',target,flush=True)
