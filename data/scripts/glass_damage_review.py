"""Read-only prebattle Glass planning, from reviewed installed static tables.

Never imports gameplay helpers, reads a live battle, or writes game/save data.
The deliberately small calculator reproduces the installed final damage
formula for explicitly supplied modifiers; it is not an AI/RNG simulator.
"""
import json
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
NATURES = {
    "ADAMANT": (1, 3), "MODEST": (3, 1), "JOLLY": (5, 3),
    "TIMID": (5, 1), "CALM": (4, 1), "BRAVE": (1, 5),
    "LONELY": (1, 2),
}


def stats(mon, species):
    forms = [f for f in species[mon["species"]].values() if f]
    base = dict(forms[0])
    if mon.get("form", 0):
        base.update(forms[mon["form"]])
    bases = base["BaseStats"]
    ev = mon.get("ev", [0] * 6)
    iv = mon.get("iv", 0)
    result = []
    for i, b in enumerate(bases):
        v = math.floor((2 * b + iv + ev[i] // 4) * mon["level"] / 100)
        if i == 0:
            result.append(v + mon["level"] + 10)
        else:
            v += 5
            up, down = NATURES.get(mon.get("nature"), (-1, -1))
            result.append(math.floor(v * (1.1 if i == up else .9 if i == down else 1)))
    return result


def damage(level, power, atk, defense, *, base_modifier=1, modifier=1):
    """Installed Battle_Move.rb final formula; positive Ruby rounding."""
    core = math.floor(math.floor((math.floor(2 * level / 5 + 2) * power *
                                  base_modifier * atk / defense)) / 50) + 2
    return [math.floor(core * modifier * roll / 100 + .5) for roll in (85, 100)]


def main():
    species = json.loads((ROOT / "work/glass-species-stats.json").read_text())
    teams = {}
    for name, wanted in (("cain", 6), ("shelly", 3), ("qmark", None)):
        rows = json.loads((ROOT / f"work/glass-{name}-teams.json").read_text())
        teams[name] = {row[0]: {m["species"]: stats(m, species) for m in row[1]}
                       for row in rows if wanted is None or row[0] == wanted}
    current = json.loads((ROOT / "notes/Glass-10AM-paused-status.json").read_text())
    us = {m["species"]: m for m in current["party"]}
    c, s, luna, serra, rad = (teams["cain"][6], teams["shelly"][3],
                             teams["qmark"][0], teams["qmark"][2], teams["qmark"][1])
    arc, kg, exc, mien = [us[x] for x in ("ARCANINE", "KLINKLANG", "EXCADRILL", "MIENSHAO")]
    reports = []

    def show(label, value, target_hp=None, notes=""):
        reports.append(dict(label=label, range=value, target_hp=target_hp, notes=notes))

    show("Marowak Fire Punch into +2Def Intimidated Klinklang",
         damage(82, 75, math.floor(c["MAROWAK"][1] * 2 / 3) * 2, kg["defense"] * 2,
                modifier=1.5 * 2), kg["totalhp"])
    show("Marowak Fire Punch crit into Klinklang, boosts bypassed",
         damage(82, 75, c["MAROWAK"][1] * 2, kg["defense"], modifier=1.5 * 2 * 1.5),
         kg["totalhp"])
    show("Marowak Shadow Bone into Intimidate Arcanine",
         damage(82, 85, math.floor(c["MAROWAK"][1] * 2 / 3) * 2, arc["defense"],
                modifier=1.5), arc["totalhp"])
    show("Ribombee Pollen Puff into Klinklang",
         damage(81, 90, s["RIBOMBEE"][3], kg["spdef"], modifier=1.5 * .5), kg["totalhp"])
    show("Ribombee Pollen Puff into Arcanine",
         damage(81, 90, s["RIBOMBEE"][3], arc["spdef"], modifier=1.5 * .5), arc["totalhp"])
    show("Arcanine Flamethrower Vivillon behind Light Screen",
         damage(90, 90, arc["spatk"], s["VIVILLON"][4], base_modifier=1.2,
                modifier=1.5 * 2 * .66), s["VIVILLON"][0],
         "Arc self-XSpeed352 outruns Vivillon222; no rain while Marowak remains.")
    show("Factory-seeded Vivillon critical Hurricane Arcanine",
         damage(80, 110, math.floor(s["VIVILLON"][3] * 1.5), arc["spdef"],
                modifier=1.5 * 1.5), arc["totalhp"],
         "GuaranteedKO if it lands: do not let slow Arc attempt an unprotected attack.")
    show("+2Atk Klinklang Gear Grind into Marowak, TWO hits",
         [2 * v for v in damage(90, 50, kg["attack"] * 2, c["MAROWAK"][2],
                               base_modifier=2, modifier=1.5 * .5)], c["MAROWAK"][0],
         "No Reflect. Two normal landed hits; separate hit rolls.")
    show("Arcanine Flamethrower Ribombee behind Light Screen",
         damage(90, 90, arc["spatk"], s["RIBOMBEE"][4], base_modifier=1.2, modifier=1.5 * 2 * .66),
         s["RIBOMBEE"][0])
    show("Arcanine Flamethrower Ribombee behind Light Screen IN RAIN",
         damage(90, 90, arc["spatk"], s["RIBOMBEE"][4], base_modifier=1.2, modifier=1.5 * 2 * .66 * .5),
         s["RIBOMBEE"][0])
    show("Weavile Night Slash crit into +Def Arcanine, boost bypassed",
         damage(83, 70, luna["WEAVILE"][1], arc["defense"], modifier=1.5 * 1.5), arc["totalhp"])
    show("Weavile Night Slash into +4Def Arcanine",
         damage(83, 70, luna["WEAVILE"][1], arc["defense"] * 3, modifier=1.5), arc["totalhp"])
    for foe, st in luna.items():
        show(f"+6SpAtk Arcanine Flamethrower {foe}",
             damage(90, 90, arc["spatk"] * 4, st[4], base_modifier=1.2,
                    modifier=1.5 * (2 if foe == "WEAVILE" else 1)), st[0],
             "Unboosted foe SpDef. Weavile Sash requires a second hit.")
    show("Round3 unboosted Arcanine Flamethrower Ninetales",
         damage(90, 90, arc["spatk"], serra["NINETALES"][4], base_modifier=1.2, modifier=1.5 * 2),
         serra["NINETALES"][0], "No Aurora Veil; Arcanine is slower without XSpeed.")
    show("Round3 unboosted Arcanine Flamethrower Ninetales WITH Veil",
         damage(90, 90, arc["spatk"], serra["NINETALES"][4], base_modifier=1.2, modifier=1.5 * 2 * .66),
         serra["NINETALES"][0])
    show("Round3 Clefable Fire Blast Klinklang",
         damage(81, 110, rad["CLEFABLE"][3], kg["spdef"], modifier=2), kg["totalhp"])
    show("Round3 Clefable Fire Blast Klinklang after SELF XSpDef",
         damage(81, 110, rad["CLEFABLE"][3], kg["spdef"] * 2, modifier=2), kg["totalhp"])
    show("Round3 Ninetales Blizzard Klinklang after SELF XSpDef",
         damage(81, 110, serra["NINETALES"][3], kg["spdef"] * 2,
                modifier=1.5 * .75 * .5), kg["totalhp"])
    show("Round3 +2Atk Factory Gear Grind Clefable TWO hits WITH Veil",
         [2 * v for v in damage(90, 50, kg["attack"] * 2, rad["CLEFABLE"][2],
                               base_modifier=2, modifier=1.5 * 2 * .66)], rad["CLEFABLE"][0])
    show("Round3 +2Atk Factory Gear Grind Ninetales TWO hits WITH Veil",
         [2 * v for v in damage(90, 50, kg["attack"] * 2, serra["NINETALES"][2],
                               base_modifier=2, modifier=1.5 * 4 * .66)], serra["NINETALES"][0])
    mega = {}
    for label, name, wanted in (("Mega Absol", "qmark", 0), ("Mega Gardevoir", "qmark", 1)):
        key = "ABSOL" if wanted == 0 else "GARDEVOIR"
        mon = next(m for row in json.loads((ROOT / f"work/glass-{name}-teams.json").read_text())
                   if row[0] == wanted for m in row[1] if m["species"] == key)
        mon = dict(mon, form=1)
        mega[label] = stats(mon, species)
    print(json.dumps({"assumptions": "Exact static stats and installed core formula; manually supplied relevant modifiers; no move choice or RNG reads.",
                      "opponent_stats_hp_atk_def_spa_spd_spe": teams,
                      "mega_stats_hp_atk_def_spa_spd_spe": mega,
                      "reports": reports}, indent=2))


if __name__ == "__main__":
    main()
