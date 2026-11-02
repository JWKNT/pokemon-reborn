"""Train an owned reserve and teach the inspected Dive machine through normal menus."""
import json,os,pathlib,subprocess,sys
R=pathlib.Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
label='Diancie268-Party';s=json.loads((R/'notes'/f'{label}-status.json').read_text())
assert [m['species'] for m in s['party']]==['MAWILE','CRESSELIA','MIENSHAO','ALTARIA','AMOONGUSS','SWAMPERT']
ruby="""require_relative 'scripts/read_rgss';MAXIMUMLEVEL=200
load '/Applications/Reborn.app/Contents/Game/Scripts/PBExperience.rb'
load '/Applications/Reborn.app/Contents/Game/Scripts/Reborn/montext.rb'
p=plain(load_rgss(ARGV[0])[:Trainer])['party'];m=p.find{|a|a['species']==:ALTARIA};g=MONHASH[m['species']].values.first[:GrowthRate];goal=PBExp.pbGetExpInternal(116,g);puts JSON.generate({exp:m['exp'],goal:goal,xl:[0,((goal-m['exp'])/30000.0).ceil].max})"""
plan=json.loads(subprocess.check_output(['ruby','-e',ruby,str(R/'backups'/f'Aster-{label}.rxdata')],cwd=R,stderr=subprocess.DEVNULL))
assert plan['xl']<=s['bag']['contents']['EXPCANDYXL'];print('ALTARIA CANDY',plan,flush=True)
(R/'work/Diancie268-altaria-candy.json').write_text(json.dumps(plan,indent=2)+'\n')
def run(n,*a):subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
if plan['xl']:run('train_candy_one','Altaria',plan['xl'],'XL')
run('teach_machine','TMX6 Dive','Swampert','Dive',0)
run('eventq',38,3,'talk');run('heal');run('checkpoint','Diancie268-Trained')
