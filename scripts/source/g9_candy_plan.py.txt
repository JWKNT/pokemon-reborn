"""Read-only calculation of candies needed to reach level65 from the latest save."""
import json,subprocess,re,math,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
ruby="require_relative 'scripts/read_rgss'; v=load_rgss('/Users/jw/Library/Application Support/Pokemon Reborn/Game_3.rxdata'); puts JSON.generate(v[:Trainer].instance_variable_get(:@party).map{|p|plain(p).slice('species','name','level','exp')})"
party=json.loads(subprocess.check_output(['ruby','-e',ruby],cwd=root,stderr=subprocess.DEVNULL))
s=pathlib.Path('/Applications/Reborn.app/Contents/Game/Scripts/Reborn/montext.rb').read_text();out=[]
for p in party:
 block=re.search(r'^  :'+p['species']+r' => \{[\s\S]*?(?=^  :|\Z)',s,re.M)[0]
 rate=re.search(r':GrowthRate => :(\w+)',block)[1];n=65
 goal={'MediumFast':n**3,'Slow':5*n**3//4,'MediumSlow':6*n**3//5-15*n*n+100*n-140}[rate]
 out.append({'name':p['name'],'level':p['level'],'exp':p['exp'],'target_exp':goal,'candies':max(0,math.ceil((goal-p['exp'])/10000))})
print(json.dumps(out,indent=2));print('Total',sum(p['candies'] for p in out))
(root/'work/g9-candy-plan.json').write_text(json.dumps(out,indent=2))
