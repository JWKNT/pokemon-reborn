"""Pure installed-source Mime/Fairy planning; no controls or live data imports.

Reads named static species/trainer extracts plus frozen historical IVs only.
Reports supplied field/stage modifiers, never predicts AI or random outcomes.
"""
import json
from fractions import Fraction as F
from pathlib import Path

from nonmega_saphira_review import calc
from saphira_damage_review import stats

ROOT = Path(__file__).resolve().parents[1]


def moonblast(spa, mime_spdef, *, boost=2, drop=-3, gem=True):
    return calc(95, 95, spa, mime_spdef, attack_stage=boost,
                defense_stage=drop, power_multiplier=F(3, 2) * (F(13, 10) if gem else 1),
                stab=F(3, 2), effectiveness=2)


def aroma_incoming(spd, *, stage=0):
    # Aromatisse93 source Modest/31IV/252SpA =303, not314.
    moves = (("DAZZLINGGLEAM", 80, F(3, 2), 1, F(3, 4), F(3, 2)),
             ("PSYCHIC", 90, 1, 1, 1, 1),
             ("FLASHCANNON", 80, 1, 2, 1, 1),
             ("THUNDER", 120, 1, 1, 1, 1))
    return {name: {
        "ordinary": calc(93, power, 303, spd, defense_stage=stage,
                         defense_multiplier=F(3, 2), power_multiplier=power_mult,
                         stab=stab, effectiveness=effect, final_multiplier=spread),
        "critical": calc(93, power, 303, spd, defense_stage=stage,
                         defense_multiplier=F(3, 2), power_multiplier=power_mult,
                         stab=stab, effectiveness=effect, final_multiplier=spread,
                         critical=True)}
        for name, power, stab, effect, spread, power_mult in moves}


def build_report():
    installed = json.loads((ROOT / "work/pulse-mime-installed-team-static.json").read_text())
    species = installed["species"]
    species.update(json.loads((ROOT / "work/saphira-capture-options-source.json").read_text())["species"])
    teams = {t["teamid"][1]: t["mons"] for t in installed["teams"] if t["teamid"][1] in ("FRIEND", "MIME")}
    foes = {m["species"]: stats(m, species) for mons in teams.values() for m in mons}
    foes["MEGAALAKAZAM"] = stats(next(m for m in teams["FRIEND"] if m["species"] == "ALAKAZAM"), species, "Mega Form")
    # HP/SpD EV training is504 total; no unowned SpeedWing is required.
    neutral = stats(dict(species="SYLVEON", level=95, nature="HARDY", iv=0,
                         ev=[252, 0, 0, 0, 252, 0]), species)
    calm = stats(dict(species="SYLVEON", level=95, nature="CALM", iv=0,
                      ev=[252, 0, 0, 0, 252, 0]), species)
    # Independent all-nature stat minima are deliberately conservative.
    minimum = [neutral[0], neutral[1] * 9 // 10, neutral[2] * 9 // 10,
               neutral[3] * 9 // 10, neutral[4] * 9 // 10, neutral[5] * 9 // 10]
    out = []
    for spa in (193, 195, 214):
        for drop in (0, -2, -3, -5):
            for boost in (0, 2, 4, 6):
                for gem in (False, True):
                    out.append(dict(spa=spa, mime_spdef_stage=drop, own_spatk_stage=boost,
                                    gem=gem, damage=moonblast(spa, foes["MRMIME"][4], boost=boost, drop=drop, gem=gem)))
    incoming = {str(spd): {str(stage): aroma_incoming(spd, stage=stage)
                           for stage in (-2, -1, 0, 2)} for spd in (279, 290, 311, 342)}
    middrop = {str(spd): aroma_incoming(spd)["FLASHCANNON"]["critical"][1]
                + aroma_incoming(spd, stage=-1)["FLASHCANNON"]["critical"][1]
               for spd in (279, 290, 311, 342)}
    frozen = json.loads((ROOT / "notes/Agate-Ricardo-won130-status.json").read_text())
    sw = dict(next(m for m in frozen["party"] if m["species"] == "SWAMPERT"), level=95)
    swamp = stats(sw, species)
    ev_counter = {"hypothetical_unchanged_swamp95": swamp,
                  "electivire_critical_crosschop": calc(95,100,328,swamp[2],power_multiplier=F(13,10),critical=True),
                  "electivire_critical_spread_earthquake": calc(95,100,328,swamp[2],power_multiplier=F(13,10),final_multiplier=F(3,4),critical=True),
                  "electivire_critical_icepunch": calc(95,75,328,swamp[2],power_multiplier=F(13,10),critical=True),
                  "plus2_wave_waterfall_vs_electivire": calc(95,80,swamp[1],foes["ELECTIVIRE"][2],attack_stage=2,power_multiplier=F(6,5),stab=F(3,2))}
    return dict(scope="Hypothetical95 gift build, not current ownership/training", stat_order=["HP", "Atk", "Def", "SpA", "SpD", "Spe"],
                sylveon_minimum_iv_neutral=neutral, sylveon_minimum_iv_calm=calm,
                independent_all_nature_minima=minimum, trainer_stats=foes,
                misty_moonblast=out, misty_aromatisse_incoming=incoming,
                two_critical_flashcannons_first_causes_one_spdef_drop=middrop,
                electivire_swamp_counter=ev_counter,
                hazards=["NightShade adds100 when Mime chooses it instead of Instruct.",
                         "Instruct plus Aroma's own move permits two attacks; do not add NightShade too.",
                         "FlashCannon can lowerSpDef between those attacks; observed negative stages matter.",
                         "PositiveXSpDef is ignored by crits; Misty's Fairy defense remains.",
                         "MetalSound is-3 onShortcircuit, -2 afterMisty;85accuracy,93.5withWideLens.",
                         "No AI/move/target/crit prediction; field/HP/status/stages determine action eligibility."])


if __name__ == "__main__":
    print(json.dumps(build_report(), indent=2))
