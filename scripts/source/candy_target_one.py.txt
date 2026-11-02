"""Spend normal candies for one Pokemon using an explicit fresh owned checkpoint."""
import json,subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
label,name,target=sys.argv[1],sys.argv[2],int(sys.argv[3])
s=json.loads((R/'notes'/f'{label}-status.json').read_text());nav=json.loads((R/'notes'/f'{label}-navigation.json').read_text())
assert 1<=target<=min(150,100+nav['variables']['595'])
ruby="""require_relative 'scripts/read_rgss';MAXIMUMLEVEL=200
load '/Applications/Reborn.app/Contents/Game/Scripts/PBExperience.rb'
load '/Applications/Reborn.app/Contents/Game/Scripts/Reborn/montext.rb'
p=plain(load_rgss(ARGV[0])[:Trainer])['party'].find{|m|m['name']==ARGV[1]};raise 'Missing Pokemon' unless p
puts JSON.generate({level:p['level'],exp:p['exp'],target:PBExp.pbGetExpInternal(ARGV[2].to_i,MONHASH[p['species'].to_sym].values.first[:GrowthRate])})"""
a=json.loads(subprocess.check_output(['ruby','-e',ruby,str(R/'backups'/f'Aster-{label}.rxdata'),name,str(target)],cwd=R,stderr=subprocess.DEVNULL));count=max(0,(a['target']-a['exp']+29999)//30000)
assert count<=s['bag']['contents'].get('EXPCANDYXL',0),'Insufficient owned XL candy'
print('CANDY TARGET',name,target,count,flush=True)
while count:
 n=min(35,count);subprocess.run([sys.executable,str(R/'scripts/train_candy_one.py'),name,str(n),'XL'],check=True);count-=n
