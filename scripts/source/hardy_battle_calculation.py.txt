"""Static Hardy19.5.43 damage review. No UI, gameplay or native-save import.

CF's Hex/EV/mint build is hypothetical, not asserted installed in the party.
Critical rows bypass positive Defense; no AI/targeting/partner prediction.
"""
import json
import math
from pathlib import Path

from agate_chain_calculation import BASE, trainer_stats
from glass_damage_review import damage

ROOT = Path(__file__).resolve().parents[1]
TYPES = {
    "COFAGRIGUS": ("GHOST",), "SWAMPERT": ("WATER", "GROUND"),
    "MIENSHAO": ("FIGHTING",), "EXCADRILL": ("GROUND", "STEEL"),
    "KLINKLANG": ("STEEL",), "LUDICOLO": ("WATER", "GRASS"),
    "ARCANINE": ("FIRE",),
}
CHART = {
    "ROCK": {"GROUND": .5, "STEEL": .5, "FIGHTING": .5, "FIRE": 2,
             "FLYING": 2, "ROCK": 1},
    "GROUND": {"GROUND": 1, "STEEL": 2, "FIRE": 2, "GRASS": .5, "FLYING": 0, "ROCK": 2},
    "FIGHTING": {"GHOST": 0, "STEEL": 2, "FLYING": .5, "ROCK": 2},
    "DARK": {"GHOST": 2, "FIGHTING": .5},
    "WATER": {"WATER": .5, "GRASS": .5, "FIRE": 2, "GROUND": 2, "ROCK": 2},
    "FLYING": {"FIGHTING": 2, "GRASS": 2, "STEEL": .5, "ROCK": .5},
    "PSYCHIC": {"FIGHTING": 2, "STEEL": .5},
    "STEEL": {"STEEL": .5, "WATER": .5, "FIRE": .5, "ROCK": 2},
    "FIRE": {"FIRE": .5, "WATER": .5, "STEEL": 2, "GRASS": 2, "ROCK": .5},
    "NORMAL": {"GHOST": 0, "STEEL": .5, "ROCK": .5},
    "GHOST": {},
}
MOVES = {
    "ROCKSLIDE": (75, "ROCK", False, True, True),
    "STOMPINGTANTRUM": (75, "GROUND", True, False, False),
    "ROCKSMASH": (40, "FIGHTING", True, False, True),
    "THROATCHOP": (80, "DARK", True, False, False),
    "AQUATAIL": (90, "WATER", True, False, False),
    "AERIALACE": (60, "FLYING", True, False, False),
    "DRILLRUN": (80, "GROUND", True, False, False),
    "BRICKBREAK": (75, "FIGHTING", True, False, False),
    "ZENHEADBUTT": (80, "PSYCHIC", True, False, True),
    "ACROBATICS": (110, "FLYING", True, False, False),
    "IRONHEAD": (80, "STEEL", True, False, True),
    "FIREPUNCH": (75, "FIRE", True, False, True),
    "ACCELEROCK": (40, "ROCK", True, False, False),
}


def type_effect(move_type, defending):
    return math.prod(CHART.get(move_type, {}).get(t, 1) for t in defending)


def main():
    mons = json.loads((ROOT / "work/postglass-hardy-installed.json").read_text())[0][1]
    foes = []
    for mon in mons:
        form = 1 if mon["species"] == "AERODACTYL" else mon.get("form", 0)
        data = dict(BASE[mon["species"]][0]); data.update(BASE[mon["species"]][form])
        types = tuple(data[k] for k in ("Type1", "Type2") if k in data)
        foes.append(dict(mon, form=form, label=("MEGAAERODACTYL" if mon["species"] == "AERODACTYL"
                                               else f"LYCANROC_FORM{form}" if mon["species"] == "LYCANROC"
                                               else mon["species"]),
                         ability="TOUGHCLAWS" if mon["species"] == "AERODACTYL" else mon["ability"],
                         stats=trainer_stats(mon, form), types=types))
    saved = json.loads((ROOT / "notes/Glass-restocked-fixed-six-status.json").read_text())
    own = {m["species"]: dict(hp=m["totalhp"], atk=m["attack"], de=m["defense"],
                              spa=m["spatk"], spd=m["spdef"], spe=m["speed"], item=m["item"])
           for m in saved["party"]}
    own["COFAGRIGUS"] = dict(hp=252, atk=93, de=333, spa=210, spd=218, spe=68, item=None)
    own["LUDICOLO"] = dict(hp=285, atk=140, de=153, spa=194, spd=208, spe=142, item="WISEGLASSES")
    incoming, outgoing = [], []
    for mon in foes:
        for move in mon["moves"]:
            if move == "ENDEAVOR":
                continue
            power, typ, contact, spread, secondary = MOVES[move]
            base = (2 if move == "ROCKSMASH" else 1.5 if move == "ACCELEROCK" else 1)
            if mon["ability"] == "TOUGHCLAWS" and contact:
                base *= 1.3
            if mon["ability"] == "SHEERFORCE" and secondary:
                base *= 1.3
            if move == "ACROBATICS":
                base *= 1.3  # First FlyingGem attack: installed base doubles with gem.
            atk = mon["stats"]["atk"] * (1.5 if mon.get("item") == "CHOICEBAND" else 1)
            generic = (1.5 if typ in mon["types"] else 1) * (1.5 if typ == "ROCK" else 1)
            generic *= .75 if spread else 1
            for who, ours in own.items():
                eff = type_effect(typ, TYPES[who])
                for stage, defense_mul in ((0, 1), (1, 1.5), (2, 2)):
                    for critical in (False, True):
                        defender = ours["de"] if critical else math.floor(ours["de"] * defense_mul)
                        values = ([0, 0] if not eff else damage(mon["level"], power, atk, defender,
                                  base_modifier=base,
                                  modifier=generic * eff * (1.5 if critical else 1)))
                        incoming.append(dict(enemy=mon["label"], move=move, target=who,
                                             def_stage=stage, critical=critical, range=values,
                                             target_hp=ours["hp"], note="First Acrobatics includes gem; later unboosted is /1.3" if move=="ACROBATICS" else ""))
        defense = mon["stats"]["def"]
        if mon["species"] == "LYCANROC" and mon.get("form") == 2:
            defense = math.floor(defense * 1.5)  # TelluricSeed.
        spdef_sand = math.floor(mon["stats"]["spd"] * 1.5 + .5)
        for multiplier in (1, 2, 3):
            outgoing.append(dict(move=f"Swamp Waterfall Atk x{multiplier}", target=mon["label"],
                                 range=damage(90,80,own["SWAMPERT"]["atk"]*multiplier,defense,
                                              base_modifier=1.2,modifier=1.5*2), hp=mon["stats"]["hp"]))
            outgoing.append(dict(move=f"Ludi WiseGlasses Scald SpA x{multiplier}, sand", target=mon["label"],
                                 range=damage(90,80,194*multiplier,spdef_sand,
                                              base_modifier=1.1,modifier=1.5*2), hp=mon["stats"]["hp"]))
            outgoing.append(dict(move=f"KG GearGrind Atk x{multiplier}, two hits", target=mon["label"],
                                 range=[2*v for v in damage(90,50,own["KLINKLANG"]["atk"]*multiplier,defense,modifier=1.5*2)],
                                 hp=mon["stats"]["hp"]))
        outgoing.append(dict(move="CF unboosted Hex into burn, sand", target=mon["label"],
                             range=damage(90,130,210,spdef_sand,modifier=1.5), hp=mon["stats"]["hp"]))
        outgoing.append(dict(move="Mien Reckless HighJumpKick", target=mon["label"],
                             range=damage(90,130,own["MIENSHAO"]["atk"],defense,
                                          base_modifier=1.2,modifier=1.5*type_effect("FIGHTING",mon["types"])),hp=mon["stats"]["hp"]))
        # Rocky Earthquake adds Rock effectiveness but keeps Ground STAB/type.
        eff = type_effect("GROUND", mon["types"]) * type_effect("ROCK", mon["types"])
        outgoing.append(dict(move="Exc Earthquake Rocky, spread", target=mon["label"],
                             range=[0,0] if not eff else damage(90,100,own["EXCADRILL"]["atk"],defense,
                                          base_modifier=1.5,modifier=1.5*.75*eff),hp=mon["stats"]["hp"]))
    print(json.dumps(dict(assumptions="Hypothetical CF252/210/68 after legal Agate prep; other six stats from archived restock checkpoint/owned Ludi. Rocky, first Mega stats, active sand; no target choices or Mummy/Defeatist procs assumed. Enemy moves into DEF+2 use no preceding RockSmash drop; see DEF+1/0 rows after drops. Crits bypass boost. Initial StompingTantrum75; double listed result approximately if later Tantrum flag. RockSlide .75 assumes >1 target.",
                          own=own, opponents=foes, incoming=incoming, outgoing=outgoing),indent=2))


if __name__ == "__main__":
    main()
