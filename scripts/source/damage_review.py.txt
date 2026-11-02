"""Explicit, offline damage sanity check; reads no live game state or RNG.

Supply every relevant field/type/item/ability multiplier yourself. This uses
the ordinary damage formula as a planning estimate, not a battle simulator.
It reports the complete multi-hit move to prevent per-hit undercounting.
"""
import argparse,json,math
p=argparse.ArgumentParser()
for k in ['level','power','attack','defense']:p.add_argument('--'+k,required=True,type=float)
p.add_argument('--stage',type=int,default=0)
p.add_argument('--hits',type=int,default=1)
p.add_argument('--stab',type=float,default=1)
p.add_argument('--effectiveness',type=float,default=1)
p.add_argument('--field',type=float,default=1)
p.add_argument('--other',type=float,default=1)
p.add_argument('--burn',action='store_true')
p.add_argument('--critical',action='store_true')
a=p.parse_args();assert -6<=a.stage<=6 and a.hits>=1 and a.defense>0
stage=(2+a.stage)/2 if a.stage>=0 else 2/(2-a.stage)
attack=math.floor(a.attack*stage)
base=math.floor(math.floor((2*a.level/5+2)*a.power*attack/a.defense)/50)+2
mod=a.stab*a.effectiveness*a.field*a.other*(.5 if a.burn else 1)*(1.5 if a.critical else 1)
rolls=[math.floor(base*mod*x/100)for x in range(85,101)]
print(json.dumps({'per_hit':[min(rolls),max(rolls)],'whole_move':[a.hits*min(rolls),a.hits*max(rolls)],'hits':a.hits,'effective_attack':attack,'assumptions':vars(a),'limitation':'Estimate only: special move formulas, spread reduction, screens, ability exceptions and Reborn field effects must be supplied explicitly.'},indent=2))
