"""Pure installed-source ordinary Agate damage review; no runtime/game reads.

Trainer IV/EV/nature defaults are those of the installed trainer loader. Player
stats below are the parent's reviewed/frozen level90 build, not live evidence.
No AI choice or random future outcome is assumed.
"""
from fractions import Fraction as F
import json
from pathlib import Path
from nonmega_saphira_review import calc
from saphira_damage_review import stats

ROOT=Path(__file__).resolve().parents[1]
CF=[252,93,333,210,218,68]
CRYO=[320,114,132,205,260,207]
MIEN=[228,251,130,195,145,217]


def report():
    species=json.loads((ROOT/'work/agate-street-species-static.json').read_text())
    teams={name:json.loads((ROOT/f'work/agate-{name}1-static-roster.json').read_text())[0][1]
           for name in ['antoine','lyla','ezra']}
    foes={m['species']:stats(m,species) for team in teams.values() for m in team}
    mamo=foes['MAMOSWINE']
    incoming={}
    for move,power,stab in [('EARTHQUAKE',100,F(3,2)),('ICICLECRASH',85,F(3,2)),
                             ('ICESHARD',40,F(3,2)),('ROCKSLIDE',75,1)]:
        incoming[move]={
            'ordinary':calc(86,power,mamo[1],CF[2],stab=stab),
            'critical':calc(86,power,mamo[1],CF[2],stab=stab,critical=True),
            'ordinary_at_plus2_def':calc(86,power,mamo[1],CF[2],stab=stab,defense_stage=2),
            'burned_critical':calc(86,power,mamo[1],CF[2],stab=stab,critical=True,final_multiplier=F(1,2))}
    ant_out={}
    for m in teams['antoine']:
        name=m['species'];st=foes[name]
        ant_out[name]={
            'hp':st[0],
            'plus6_unstatused_hex':calc(90,65,CF[3],st[4],attack_stage=6,stab=F(3,2),
                effectiveness=F(1,2) if name in {'LIEPARD','MIGHTYENA','TYRANITAR'} else 1,
                defense_multiplier=F(3,2) if name=='TYRANITAR' else 1),
            'plus6_status_hex':calc(90,130,CF[3],st[4],attack_stage=6,stab=F(3,2),
                effectiveness=F(1,2) if name in {'LIEPARD','MIGHTYENA','TYRANITAR'} else 1,
                defense_multiplier=F(3,2) if name=='TYRANITAR' else 1)}
    ice={}
    for m in teams['lyla']+teams['ezra']:
        name=m['species'];st=foes[name]
        if name=='DITTO':continue
        eff=4 if name=='NOIVERN' else (2 if name in {'WHIMSICOTT','HAXORUS','BELLOSSOM','KOMMOO'} else 1)
        ice[name]={'hp':st[0],'speed':st[5],
                   'icebeam0':calc(90,90,CRYO[3],st[4],stab=F(3,2),effectiveness=eff),
                   'icebeam_plus2':calc(90,90,CRYO[3],st[4],stab=F(3,2),effectiveness=eff,attack_stage=2),
                   'icebeam_plus2_lightscreen':calc(90,90,CRYO[3],st[4],stab=F(3,2),
                         effectiveness=eff,attack_stage=2,final_multiplier=F(2,3))}
    return {'scope':'Read-only static source planning; not actual battle outcomes',
        'stat_order':['HP','Atk','Def','SpA','SpD','Spe'],
        'players':{'CF':CF,'Cryo':CRYO,'Mien':MIEN},'foes':foes,
        'mamo_into_cf':incoming,'cf_hail_chip':15,'mamo_safe_min_hp_preburn':144,
        'mamo_safe_min_hp_burned':80,'antoine_outgoing':ant_out,
        'liepard_foul_play_crit_by_cf_attack_stage':{
            str(s):calc(87,95,CF[1],CF[2],attack_stage=s,defense_stage=2,
                        stab=F(3,2),effectiveness=2,critical=True) for s in [0,2,4,6]},
        'cryo_icebeam':ice,
        'noivern_hurricane_crit_cf':calc(87,110,200,CF[4],stab=F(3,2),critical=True),
        'copied_cf_ditto_hex_crit_cf':calc(87,65,CF[3],CF[4],stab=F(3,2),effectiveness=2,critical=True),
        'noivern_hurricane_crit_cryo':calc(87,110,200,CRYO[4],stab=F(3,2),critical=True),
        'noivern_heatwave_crit_cryo':calc(87,95,200,CRYO[4],effectiveness=2,
                                             critical=True,final_multiplier=F(3,4)),
        'mien_brickbreak_copied_cryo_ditto':calc(90,75,MIEN[1],CRYO[2],stab=F(3,2),effectiveness=2),
        'whimsicott_dazzle_crit_mien':calc(87,80,165,MIEN[4],stab=F(3,2),effectiveness=2,
                                               critical=True,final_multiplier=F(3,4)),
        'cryo_plus2_freezedry_mantine':calc(90,70,CRYO[3],275,stab=F(3,2),effectiveness=4,attack_stage=2)}


if __name__=='__main__':print(json.dumps(report(),indent=2))
