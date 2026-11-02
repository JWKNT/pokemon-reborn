"""Source-only future preparation estimates; never imports a control helper.

Reads installed-source extracts and one named, frozen historical snapshot.
No live save, battle log, AI, RNG, memory, UI, or game data mutation.
Explicit modifiers reproduce ordinary damage to within rounding boundaries.
They are planning estimates, not a simulator or proof of a future outcome.
"""
import json
import math
from pathlib import Path
from glass_damage_review import damage

ROOT = Path(__file__).resolve().parents[1]
NATURES = {"ADAMANT": (1, 3), "JOLLY": (5, 3), "TIMID": (5, 1),
           "CAREFUL": (4, 3), "CALM": (4, 1), "IMPISH": (2, 3),
           "MODEST": (3, 1), "BOLD": (2, 1)}


def stats(mon, species, form=None):
    forms = [v for k, v in species[mon["species"]].items()
             if k != "OnCreation" and v]
    base = dict(forms[0])
    if form is not None:
        base.update(species[mon["species"]][form])
    elif mon.get("form", 0):
        base.update(forms[mon["form"]])
    lv = mon["level"]
    ivs = mon.get("iv", 10)
    if isinstance(ivs, int):
        ivs = [31] * 5 + [0] if ivs == 32 else [ivs] * 6
    evs = mon.get("ev", [min(85, lv * 3 // 2)] * 6)
    vals = []
    up, down = NATURES.get(mon.get("nature"), (-1, -1))
    for i, b in enumerate(base["BaseStats"]):
        v = (2 * b + ivs[i] + evs[i] // 4) * lv // 100
        v += lv + 10 if i == 0 else 5
        if i:
            v = v * (110 if i == up else 90 if i == down else 100) // 100
        vals.append(v)
    return vals


def main():
    species = json.loads((ROOT / "work/saphira-capture-options-source.json").read_text())["species"]
    rows = json.loads((ROOT / "work/saphira-installed-team.json").read_text())[0][1]
    foes = {m["species"]: stats(m, species,
            "Mega X Form" if m["species"] == "CHARIZARD" else None) for m in rows}
    steelix_mon = json.loads((ROOT / "work/saphira-steelix-installed-team.json").read_text())[0][1][0]
    steelix = stats(steelix_mon, species)
    historical = json.loads((ROOT / "notes/Glass-post-gauntlet-attempt-1-status.json").read_text())
    old_swamp = next(m for m in historical["party"] if m["species"] == "SWAMPERT")
    planned = dict(old_swamp, level=95, nature="CAREFUL", ev=[252, 4, 0, 0, 212, 40])
    swamp = stats(planned, species, "Mega Form")
    n = foes["NOIVERN"]
    reports = []

    def report(label, values, hp=None, note=""):
        reports.append(dict(label=label, damage_range=values, target_hp=hp, note=note))

    for name, power, stab, fire, field in (("Boomburst", 140, 1, 1, 1),
            ("Dragon Pulse", 85, 1.5, 1, 1.5),
            ("Flamethrower", 90, 1, 1.5, 1.5)):
        type_eff = .5 if name == "Flamethrower" else 1
        report(f"Noivern seeded {name} into proposed Mega Swampert",
               damage(95, power, math.floor(n[3] * 1.5 * fire), swamp[4],
                      base_modifier=field, modifier=stab * type_eff), swamp[0])
        report(f"Noivern seeded CRITICAL {name} into proposed Mega Swampert",
               damage(95, power, math.floor(n[3] * 1.5 * fire), swamp[4],
                      base_modifier=field, modifier=stab * type_eff * 1.5), swamp[0],
               "Crit bypasses positive X SpDef stages.")
    for name, power, stab, fire in (("Boomburst", 140, 1, 1),
                                  ("Flamethrower", 90, 1, 1.5)):
        report(f"After 10 PUBLIC Dragon Pulse uses: {name} into +6 SpDef Mega",
               damage(95, power, math.floor(n[3] * 1.5 * fire), swamp[4] * 4,
                      base_modifier=1.5 if fire > 1 else 1,
                      modifier=stab * (.5 if fire > 1 else 1)), swamp[0])
    for name, st in foes.items():
        if name in ("NOIVERN", "SALAMENCE", "DRAGONITE"):
            p, stab, eff = 75, 1, 2
            multiscale = .5 if name == "DRAGONITE" else 1
            move = "Rock Slide"
        else:
            p, stab, eff = 100, 1.5, 2 if name == "CHARIZARD" else 1
            multiscale, move = 1, "Earthquake"
        report(f"+6 Atk Mega {move} into {name}, Dragon's Den",
               damage(95, p, swamp[1] * 4, st[2] * 1.3,
                      modifier=stab * eff * multiscale), st[0],
               "Sash leaves1HP. Use Curse on final Dragonite; this is not an ES/Dragon Dance safety proof.")
    for name, p, mod in (("Earthquake", 100, 1.5),
                          ("Dragon Tail", 60, 1.5),
                          ("Fire Fang", 65, 1.5 * 1.3),
                          ("Heavy Slam", 120, 1.5)):
        report(f"Steelix {name} into hypothetical252HP/333Def Cofa",
               damage(100, p, steelix[1], 333, modifier=mod), 252)
        report(f"Steelix critical {name} into Cofa",
               damage(100, p, steelix[1], 333, modifier=mod * 1.5), 252)
    result = dict(scope="future proposal; not executed", stat_order=["HP","Atk","Def","SpA","SpD","Spe"],
                  proposed_mega_swamp=swamp, proposed_ev=planned["ev"], owned_iv=old_swamp["iv"],
                  nature="CAREFUL", level=95, foes=foes, gargantuan=steelix,
                  curse_tick=steelix[0]//4, speed_at_plus6=swamp[5]*4,
                  reports=reports,
                  caveats=["Explicit modifiers only; small intermediate rounding uncertainty.",
                           "Noivern Dragon Pulse PP must be counted from visible uses, never read from runtime.",
                           "Hot-switch Sash is not free entry: inspect HP before claiming next-turn survival."])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
