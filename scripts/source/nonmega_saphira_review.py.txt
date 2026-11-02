"""Pure future Saphira calculator; reads only named installed extracts/frozen IVs.

No gameplay helpers, live state, battle logs, controls or RNG are imported.
Separates base-power multipliers from final type-field multipliers, matching
Battle_Move.rb:1785,1947,1987,2078,2110,2212–2215. Fractions preserve Ruby's
positive rounding while defense multipliers (AV/Dragon's Den) stay fractional.
"""
import json
import math
from fractions import Fraction as F
from pathlib import Path
from saphira_damage_review import stats

ROOT = Path(__file__).resolve().parents[1]


def stage(value, stages, *, critical=False, defensive=False):
    if critical and ((defensive and stages > 0) or (not defensive and stages < 0)):
        stages = 0
    factor = F(2 + stages, 2) if stages >= 0 else F(2, 2 - stages)
    return math.floor(value * factor)


def calc(level, power, attack, defense, *, attack_stage=0, defense_stage=0,
         attack_multiplier=1, defense_multiplier=1, power_multiplier=1,
         field_multiplier=1, stab=1, effectiveness=1, critical=False,
         final_multiplier=1):
    a = stage(attack, attack_stage, critical=critical) * F(attack_multiplier)
    d = stage(defense, defense_stage, critical=critical, defensive=True) * F(defense_multiplier)
    core = math.floor(math.floor((2 * level // 5 + 2) * power * F(power_multiplier) * a / d) / 50) + 2
    modifier = F(field_multiplier) * F(stab) * F(effectiveness) * F(final_multiplier)
    if critical:
        modifier *= F(3, 2)
    return [max(1, math.floor(core * modifier * F(roll, 100) + F(1, 2)))
            for roll in (85, 100)]


def build_report(*, nature="CAREFUL", ev=None):
    species = json.loads((ROOT / "work/saphira-capture-options-source.json").read_text())["species"]
    rows = json.loads((ROOT / "work/saphira-installed-team.json").read_text())[0][1]
    old = next(m for m in json.loads((ROOT / "notes/Glass-post-gauntlet-attempt-1-status.json").read_text())["party"]
               if m["species"] == "SWAMPERT")
    build = dict(old, level=95, nature=nature,
                 ev=ev if ev is not None else [252, 0, 0, 0, 152, 104], form=0)
    swamp = stats(build, species)
    foes = {m["species"]: stats(m, species, "Mega X Form" if m["species"] == "CHARIZARD" else None)
            for m in rows}
    lead = foes["NOIVERN"]
    incoming = {}
    for name, power, stab, field, fire, effectiveness in (
            ("DRAGONPULSE", 85, F(3, 2), F(3, 2), 1, 1),
            ("BOOMBURST", 140, 1, 1, 1, 1),
            ("FLAMETHROWER", 90, 1, F(3, 2), F(3, 2), F(1, 2))):
        incoming[name] = {
            "ordinary_by_spdef_stage": {str(s): calc(95, power, lead[3], swamp[4],
                    attack_stage=1, defense_stage=s, attack_multiplier=fire,
                    defense_multiplier=F(3, 2), field_multiplier=field,
                    stab=stab, effectiveness=effectiveness) for s in (0, 2, 4, 6)},
            "critical_even_at_plus6_spdef": calc(95, power, lead[3], swamp[4],
                    attack_stage=1, defense_stage=6, attack_multiplier=fire,
                    defense_multiplier=F(3, 2), field_multiplier=field,
                    stab=stab, effectiveness=effectiveness, critical=True)}
    outgoing = {}
    physical = {}
    physical_moves = {
        "DRAGONCLAW": (80, "DRAGON", True), "EARTHQUAKE": (100, "GROUND", False),
        "FIREFANG": (65, "FIRE", True), "POISONJAB": (80, "POISON", True),
        "IRONHEAD": (80, "STEEL", True), "FLAREBLITZ": (120, "FIRE", True),
        "FIREPUNCH": (75, "FIRE", True), "EXTREMESPEED": (80, "NORMAL", True)}
    for mon in rows:
        name = mon["species"]
        st = foes[name]
        airborne = name in ("NOIVERN", "SALAMENCE", "DRAGONITE")
        outgoing[name] = dict(
            hp=st[0], move="ROCKSLIDE" if airborne else "EARTHQUAKE",
            damage=calc(95, 75 if airborne else 100, swamp[1], st[2], attack_stage=6,
                defense_multiplier=F(13, 10), stab=1 if airborne else F(3, 2),
                effectiveness=2 if airborne or name == "CHARIZARD" else 1,
                final_multiplier=F(1, 2) if name == "DRAGONITE" else 1),
            sash=mon["item"] == "FOCUSSASH")
        if name == "DRAGONITE":
            outgoing[name]["after_multiscale_broken"] = calc(95,75,swamp[1],st[2],
                    attack_stage=6,defense_multiplier=F(13,10),effectiveness=2)
        if name == "NOIVERN":
            continue
        for move in mon["moves"]:
            if move not in physical_moves:
                continue
            p, typ, contact = physical_moves[move]
            stab = F(3,2) if typ == "DRAGON" or (typ == "GROUND" and name=="GARCHOMP") or (typ == "FIRE" and name=="CHARIZARD") else 1
            field = F(3,2) if typ in ("DRAGON", "FIRE") else 1
            effect = F(1,2) if typ in ("FIRE", "STEEL", "POISON") else 1
            tough = F(13,10) if name == "CHARIZARD" and contact else 1
            physical[f"{name}:{move}"] = {
                str(s): {"ordinary_vs_plus6_def": calc(mon["level"],p,st[1],swamp[2],
                            attack_stage=s,defense_stage=6,power_multiplier=tough,
                            field_multiplier=field,stab=stab,effectiveness=effect),
                         "critical_bypasses_def": calc(mon["level"],p,st[1],swamp[2],
                            attack_stage=s,defense_stage=6,power_multiplier=tough,
                            field_multiplier=field,stab=stab,effectiveness=effect,critical=True)}
                for s in (0,2,4)}
    return dict(scope="Hypothetical trained build; no current ownership/training claim",
                stat_order=["HP","Atk","Def","SpA","SpD","Spe"], proposed_swamp=swamp,
                nature=build["nature"],level=95,ev=build["ev"],historical_iv=old["iv"],
                vest_effective_spdef=str(F(swamp[4]*3,2)), speed_plus6=swamp[5]*4,
                foes=foes,noivern_incoming=incoming,outgoing_plus6=outgoing,
                physical_incoming=physical,
                provenance=["Installed saphira source extracts; frozen Glass-post-gauntlet-attempt-1-status IV only",
                    "Battle_Move.rb damage/type-field/AV/critical and Battle_Field.rb Dragon defense factors",
                    "Does not model AI choices, future field changes, opponent Full Restore decisions or random outcomes"])


if __name__ == "__main__":
    print(json.dumps(dict(careful_special_tank=build_report(),
                         impish_balanced=build_report(nature="IMPISH",ev=[252,0,100,0,52,104])),indent=2))
