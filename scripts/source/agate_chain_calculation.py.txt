"""Read-only installed-stat Agate planning; no game/UI/save imports.

Explicit move modifiers only. Does not predict AI, rolls, targeting, order of
replacement Pokemon, partner damage, Mummy procs, drops, or weather persistence.
Run from any directory; stdout is JSON for reviewer inspection.
"""
import json
import math
from pathlib import Path

from glass_damage_review import damage

ROOT = Path(__file__).resolve().parents[1]
NATURES = {"ADAMANT": (1, 3), "JOLLY": (5, 3), "CALM": (4, 1),
           "TIMID": (5, 1), "BRAVE": (1, 5)}
BASE = json.loads((ROOT / "work/installed-base-stats.json").read_text())
LABELS = ("hp", "atk", "def", "spa", "spd", "spe")


def trainer_stats(mon, form=None):
    forms = BASE[mon["species"]]
    selected = mon.get("form", 0) if form is None else form
    bases = forms[selected].get("BaseStats", forms[0]["BaseStats"])
    level = mon["level"]
    iv = mon.get("iv", 10)
    ivs = [31] * 5 + [0] if iv == 32 else [iv] * 6
    ev = list(mon.get("ev", [min(85, level * 3 // 2)] * 6))
    if iv == 32:
        ev[5] = 0
    values = [math.floor((2 * b + ivs[i] + ev[i] // 4) * level / 100)
              + (level + 10 if i == 0 else 5) for i, b in enumerate(bases)]
    if mon.get("nature") in NATURES:
        up, down = NATURES[mon["nature"]]
        values[up] = math.floor(values[up] * 1.1)
        values[down] = math.floor(values[down] * .9)
    return dict(zip(LABELS, values))


def main():
    teams = {}
    for name in ("solaris", "howaya", "christina", "hardy-partner"):
        mons = json.loads((ROOT / f"work/postglass-{name}-installed.json").read_text())[0][1]
        teams[name] = [dict(mon, stats=trainer_stats(mon)) for mon in mons]
    garchomp = teams["solaris"][-1]
    teams["solaris"].append(dict(garchomp, species="MEGAGARCHOMP", form=1,
                                 stats=trainer_stats(garchomp, 1)))
    foes = {m["species"]: m for m in teams["solaris"]}
    warmup = {m["species"]: m for name in ("howaya", "christina") for m in teams[name]}
    snapshot = json.loads((ROOT / "notes/Glass-restocked-fixed-six-status.json").read_text())
    own = {m["species"]: dict(zip(LABELS, [m["totalhp"], m["attack"], m["defense"],
                                          m["spatk"], m["spdef"], m["speed"]]))
           for m in snapshot["party"]}
    cf = dict(own["COFAGRIGUS"], spd=218, spe=68)  # Normal owned Timid Mint.
    preferred_cf = dict(cf, hp=252, spa=210)  # 4 Pomeg, PowerLens 3 normal KOs.
    cryo = dict(zip(LABELS, (320, 114, 132, 205, 260, 207)))
    rows = []

    def show(label, level, power, attack, defense, modifier=1, base_modifier=1, hp=None):
        rows.append(dict(label=label, range=damage(level, power, attack, defense,
                                                  base_modifier=base_modifier,
                                                  modifier=modifier), target_hp=hp))

    ludi, beheeyem = [warmup[n] for n in ("LUDICOLO", "BEHEEYEM")]
    for stage, multiplier in ((2, 2), (4, 3)):
        show(f"warmup Ludicolo rainy Surf Timid CF +{stage}SpD", 87, 90,
             ludi["stats"]["spa"], cf["spd"] * multiplier, .75 * 1.5 * 1.5, hp=cf["hp"])
        show(f"warmup Ludicolo Giga Drain Timid CF +{stage}SpD", 87, 75,
             ludi["stats"]["spa"], cf["spd"] * multiplier, 1.5, hp=cf["hp"])
        show(f"warmup Beheeyem DarkPulse/ShadowBall Timid CF +{stage}SpD", 87, 80,
             beheeyem["stats"]["spa"], cf["spd"] * multiplier, 2, hp=cf["hp"])
    show("warmup Beheeyem DarkPulse critical CF, positive SpD bypassed", 87, 80,
         beheeyem["stats"]["spa"], cf["spd"], 2 * 1.5, hp=cf["hp"])
    show("stock Cryo FreezeDry warmup Ludicolo", 90, 70, cryo["spa"],
         ludi["stats"]["spd"], 1.5 * 4, hp=ludi["stats"]["hp"])
    for name, mon in warmup.items():
        for multiplier in (2, 3):
            show(f"warmup CF SpA x{multiplier} ShadowBall {name}", 90, 80,
                 cf["spa"] * multiplier, mon["stats"]["spd"],
                 0 if name == "PORYGONZ" else 1.5, hp=mon["stats"]["hp"])
        if name == "PORYGONZ":
            show("warmup CF +4SpA DarkPulse PorygonZ", 90, 80, cf["spa"] * 3,
                 mon["stats"]["spd"], hp=mon["stats"]["hp"])

    star, scizor = [foes[n] for n in ("STARAPTOR", "SCIZOR")]
    for name, st in (("CF", cf), ("Arc", own["ARCANINE"]), ("Cryo", cryo)):
        show(f"Staraptor BraveBird {name} critical, no Intimidate", 89, 120,
             star["stats"]["atk"], st["def"], 1.5 * 1.5, hp=st["hp"])
    show("Staraptor BraveBird +2Def CF ordinary", 89, 120, star["stats"]["atk"],
         cf["def"] * 2, 1.5, hp=cf["hp"])
    show("Staraptor burned BraveBird CF critical", 89, 120, star["stats"]["atk"],
         cf["def"], 1.5 * 1.5 * .5, hp=cf["hp"])
    for item_power, label in ((1, "no item"), (1.5, "held item")):
        show(f"Scizor KnockOff CF critical {label}", 88, 65, scizor["stats"]["atk"],
             cf["def"], 2 * 1.3 * 1.5, item_power, hp=cf["hp"])
    show("Scizor Technician LifeOrb BulletPunch CF critical unburned", 88, 40,
         scizor["stats"]["atk"], cf["def"], 1.5 * 1.3 * 1.5, 1.5, hp=cf["hp"])
    for name, move, power, stab, base in (("TYRANITAR", "Crunch", 80, 1.5 * 2, 1),
                                        ("EXCADRILL", "Earthquake", 100, 1.5, 1),
                                        ("GYARADOS", "Waterfall", 80, 1.5, 1),
                                        ("MEGAGARCHOMP", "Earthquake in sand", 100, 1.5, 1.3)):
        mon = foes[name]
        for attack_stage, multiplier in ((0, 1), (2, 2), (4, 3), (6, 4)):
            if name == "TYRANITAR" and attack_stage:
                continue
            show(f"{name} +{attack_stage}Atk burned {move} CF critical", mon["level"],
                 power, mon["stats"]["atk"] * multiplier, cf["def"],
                 stab * 1.5 * .5, base, hp=cf["hp"])
        show(f"{name} unboosted {move} CF critical unburned", mon["level"], power,
             mon["stats"]["atk"], cf["def"], stab * 1.5, base, hp=cf["hp"])
    for name, mon in foes.items():
        if name == "GARCHOMP":
            continue
        defense = mon["stats"]["spd"]
        if name == "TYRANITAR":
            defense = math.floor(defense * 1.5 + .5)
        show(f"Solaris CF +6SpA ShadowBall {name}", 90, 80, cf["spa"] * 4,
             defense, 0 if name == "STARAPTOR" else 1.5 * (.5 if name == "TYRANITAR" else 1),
             hp=mon["stats"]["hp"])
        if name == "STARAPTOR":
            show("Solaris CF +6SpA DarkPulse Staraptor", 90, 80, cf["spa"] * 4,
                 defense, hp=mon["stats"]["hp"])
            show("preferred CF SpA210 +6 DarkPulse Staraptor", 90, 80,
                 preferred_cf["spa"] * 4, defense, hp=mon["stats"]["hp"])
        for status, power in (("unstatus", 65), ("burned", 130)):
            show(f"preferred CF SpA210 +6 Hex {name} {status}", 90, power,
                 preferred_cf["spa"] * 4, defense,
                 0 if name == "STARAPTOR" else 1.5 * (.5 if name == "TYRANITAR" else 1),
                 hp=mon["stats"]["hp"])
    for multiplier in (1, 2):
        for name, move, power in (("MEGAGARCHOMP", "IceBeam", 90), ("GYARADOS", "FreezeDry", 70)):
            mon = foes[name]
            show(f"Cryo SpA x{multiplier} {move} {name}, no damage item", 90, power,
                 cryo["spa"] * multiplier, mon["stats"]["spd"], 1.5 * 4, hp=mon["stats"]["hp"])
    ttar = foes["TYRANITAR"]["stats"]
    show("Swamp +2Atk WaveIncense Waterfall Tyranitar", 90, 80, own["SWAMPERT"]["atk"] * 2,
         ttar["def"], 1.5 * 2, 1.2, hp=ttar["hp"])
    show("Mien Reckless HighJumpKick Tyranitar", 90, 130, own["MIENSHAO"]["atk"],
         ttar["def"], 1.5 * 4, 1.2, hp=ttar["hp"])
    print(json.dumps({"assumptions": "NoField. Static supplied weather; no AI/target/partner/drop prediction. Critical rows bypass positive defense stages and retain burn. Held consumables are not restored by partner HP/PP heal.",
                      "trainer_stats": teams, "cf_after_owned_timid_mint": cf,
                      "cf_preferred_hex_after_legal_ev_training": preferred_cf,
                      "speeds": {"CF_Timid_plus6": cf["spe"] * 4,
                                 "SandRush_Excadrill": foes["EXCADRILL"]["stats"]["spe"] * 2,
                                 "Gyarados_plus1": math.floor(foes["GYARADOS"]["stats"]["spe"] * 1.5),
                                 "Gyarados_plus2": foes["GYARADOS"]["stats"]["spe"] * 2},
                      "reports": rows}, indent=2))


if __name__ == "__main__":
    main()
