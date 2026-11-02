"""Pure, hypothetical Sylveon/Noivern source review; never imports controls.

Inputs are two named installed-source extracts. No runtime save, UI, AI,
battle log, future RNG, active recording, or native inspection is used.
"""
import json
from fractions import Fraction as F
from pathlib import Path

from nonmega_saphira_review import calc
from saphira_damage_review import stats

ROOT = Path(__file__).resolve().parents[1]
EVS = [252, 0, 0, 0, 252, 4]


def backed_up_field_after_defog(layers):
    """Model only the installed breakField pop, not Defog's availability."""
    remaining = list(layers)[:-1]
    return remaining[-1] if remaining else "INDOOR"


def incoming(noivern_stats, sylveon_stats, field, *, spdef_stage=0,
             enemy_spatk_stage=1):
    fairy_defense = F(3, 2) if field == "MISTY" else 1
    result = {"DRAGONPULSE": {"ordinary": [0, 0], "critical": [0, 0]}}
    for move, power, flash_fire in (("FLAMETHROWER", 90, F(3, 2)),
                                    ("BOOMBURST", 140, 1)):
        options = dict(attack_stage=enemy_spatk_stage,
                       defense_stage=spdef_stage,
                       attack_multiplier=flash_fire,
                       defense_multiplier=fairy_defense,
                       field_multiplier=F(3, 2) if field == "DRAGONSDEN" and move == "FLAMETHROWER" else 1)
        result[move] = {
            "ordinary": calc(95, power, noivern_stats[3], sylveon_stats[4], **options),
            "critical": calc(95, power, noivern_stats[3], sylveon_stats[4], critical=True, **options),
        }
    return result


def moonblast(noivern_stats, sylveon_stats, field, *, spatk_stage=0):
    return calc(95, 95, sylveon_stats[3], noivern_stats[4],
                attack_stage=spatk_stage,
                defense_multiplier=F(13, 10) if field == "DRAGONSDEN" else 1,
                power_multiplier=F(3, 2) if field == "MISTY" else 1,
                stab=F(3, 2), effectiveness=2)


def build_report():
    species = json.loads((ROOT / "work/saphira-capture-options-source.json").read_text())["species"]
    rows = json.loads((ROOT / "work/saphira-installed-team.json").read_text())[0][1]
    noivern = next(m for m in rows if m["species"] == "NOIVERN")
    ns = stats(noivern, species)
    builds = []
    for iv in (0, 15, 31):
        proposed = dict(species="SYLVEON", level=95, nature="CALM",
                        iv=[iv] * 6, ev=EVS)
        s = stats(proposed, species)
        fields = {}
        for field in ("DRAGONSDEN", "MISTY", "INDOOR"):
            fields[field] = {
                "incoming": incoming(ns, s, field),
                "incoming_after_one_x_spdef": incoming(ns, s, field, spdef_stage=2),
                "moonblast": moonblast(ns, s, field),
                "moonblast_after_one_x_spatk": moonblast(ns, s, field, spatk_stage=2),
            }
        builds.append(dict(proposed_iv=proposed["iv"], stats=s,
                           burn_tick=s[0] // 16, fields=fields))
    minimum_spdef = {}
    for hp in (345, 359, 374):
        for defense in range(1, 1000):
            test = [hp, 0, 0, 214, defense, 0]
            ceiling = max(v["critical"][1] for v in incoming(ns, test, "DRAGONSDEN").values())
            if hp > ceiling + hp // 16 + 2:
                minimum_spdef[str(hp)] = dict(spdef=defense, critical_ceiling=ceiling,
                                               burn_tick=hp // 16, rounding_margin=2)
                break
    return dict(scope="Source-only future proposal, not an acquired/trained party claim",
                stat_order=["HP", "Atk", "Def", "SpA", "SpD", "Spe"],
                recommended_level=95, recommended_nature="CALM", recommended_ev=EVS,
                noivern=ns, noivern_moves=noivern["moves"], noivern_has_roost="ROOST" in noivern["moves"],
                builds=builds, minimum_first_misty_spdef=minimum_spdef,
                caveats=["Uses seed +1 SpA, persistent Flash Fire and all relevant field multipliers.",
                         "Critical ignores positive SpDef stages, but retains Misty's Fairy defense multiplier.",
                         "Public field, HP, status, elapsed turns and observed SpA drops must govern each action.",
                         "Defog/expiry restores actual backup; no AI, damage-roll or opponent-healing prediction.",
                         "Add two HP rounding margin and residual-status damage to displayed attack ceilings."])


if __name__ == "__main__":
    print(json.dumps(build_report(), indent=2))
