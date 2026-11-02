"""Pure proposal for PULSE Hypno, from an explicitly supplied visible-turn ledger.

No gameplay imports, native saves, battle logs, AI/RNG, UI, or subprocesses.
The output is ONE ordinary-control action proposal, never an executed queue.
Every completed turn (including items/failed actions) must be entered first.
See notes/hypno-guarded-plan-2026-10-03.md for the input contract and limitations.
"""
import argparse
import json
import math
from pathlib import Path

from glass_damage_review import damage

BUILD = dict(species="ARCANINE", level=90, totalhp=294, attack=228,
             spdef=171, speed=176, item="CHARCOAL", ability="INTIMIDATE")
MOVES = {"SAFEGUARD", "FLAMETHROWER", "CRUNCH", "MORNINGSUN"}
ITEMS = {"XSPEED": "X Speed", "XATTACK": "X Attack",
         "XSPDEF": "X Sp. Def", "FULLHEAL": "Full Heal",
         "ULTRAPOTION": "Ultra Potion", "FULLRESTORE": "Full Restore"}
ENEMY_MOVES = {"HYPNOSIS", "DREAMEATER", "DARKPULSE", "CALMMIND"}
RESULTS = {"success", "failed", "asleep", "flinched"}


def require(test, message):
    if not test:
        raise ValueError(message)


def boosted(stat, stage):
    return math.floor(stat * (2 + stage) / 2)


def pulse_ranges(enemy_spa, own_spdef):
    """Starlight Dark+Fairy vs Fire: STAB1.5, field1.5, effectiveness0.5."""
    atk = boosted(287, enemy_spa)
    normal = damage(100, 80, atk, boosted(171, own_spdef),
                    modifier=1.5 * 1.5 * .5)
    critical = damage(100, 80, atk, 171, modifier=1.5 * 1.5 * .5 * 1.5)
    return normal, critical


def crunch_range(own_attack):
    # Ignore possible defense drops/crits: this is a conservative HP upper bound.
    return damage(90, 80, boosted(228, own_attack), 479, modifier=1.5 * 2)


def ledger(state):
    o = state["observation"]
    require(o.get("confirmed") is True and o.get("command_menu") is True,
            "Fresh visible command-menu confirmation is required")
    require(o.get("actor") == "Arcanine" and o.get("foe") == "Hypno",
            "This proposal handles only the unchanged Arcanine/Hypno singles")
    require(o.get("field") == "STARLIGHT" and o.get("weather") == "NONE",
            "Starlight with no weather must be confirmed")
    require(state.get("ledger_complete") is True, "Missed messages/turns require review")
    require(all(state["build"].get(k) == v for k, v in BUILD.items()),
            "Frozen outside-battle Arcanine build differs from reviewed stats")
    require(set(state["build"]["moves"]) == MOVES, "Reviewed four moves are required")
    turns = state.get("turns", [])
    require(isinstance(o.get("turn"), int) and o["turn"] == len(turns) + 1,
            "Command turn must follow every contiguous completed turn")
    require(isinstance(o.get("hp"), int) and 0 < o["hp"] <= 294,
            "Fresh visible numeric Arcanine HP is required")
    require(o.get("status") in (None, "SLEEP"), "Unexpected status requires review")
    stock = {k: int(state["stock"].get(k, 0)) for k in ITEMS}
    require(all(v >= 0 for v in stock.values()), "Invalid frozen stock")
    attack = speed = spdef = enemy_spa = safeguard = 0
    foe_hp_bound = 381
    last_pulse_damage = None
    for n, row in enumerate(turns, 1):
        require(row.get("turn") == n and row.get("completed") is True
                and row.get("confirmed") is True,
                "Each turn must have a confirmed completion, not a button receipt")
        p, e = row["player"], row["enemy"]
        action, result = p["action"], p["result"]
        require(action in ITEMS or action in MOVES, "Unknown player action requires review")
        require(result in RESULTS and e["move"] in ENEMY_MOVES
                and e["result"] in {"success", "failed"}, "Unknown outcome requires review")
        if action in ITEMS:
            require(isinstance(p.get("consumed"), bool), "Confirm consumed/refunded item")
            require(p["consumed"] == (result == "success"),
                    "Item consumption/outcome disagreement requires reconciliation")
            if p["consumed"]:
                stock[action] -= 1
                require(stock[action] >= 0, "Consumed quantity exceeds frozen stock")
        if result == "success":
            if action in {"XSPEED", "XATTACK", "XSPDEF"}:
                old = {"XSPEED": speed, "XATTACK": attack, "XSPDEF": spdef}[action]
                require(old < 6, "A capped X item cannot count as a successful boost")
                if action == "XSPEED":
                    speed = min(6, speed + 2)
                elif action == "XATTACK":
                    attack = min(6, attack + 2)
                else:
                    spdef = min(6, spdef + 2)
            elif action == "SAFEGUARD":
                require(safeguard == 0, "Safeguard fails while already active")
                safeguard = 5
            elif action == "CRUNCH":
                foe_hp_bound = max(0, foe_hp_bound - crunch_range(attack)[0])
        if e["move"] == "CALMMIND" and e["result"] == "success":
            require(enemy_spa < 6, "A capped Calm Mind cannot count as a successful boost")
            enemy_spa += 1
        if e["move"] == "HYPNOSIS" and e["result"] == "success":
            require(safeguard == 0, "No Guard does not bypass active Safeguard")
        if e["move"] == "DREAMEATER" and e["result"] == "success":
            # Never guess the Big Root healing quantity from an obscured HP bar.
            foe_hp_bound = 381
        if e["move"] == "DARKPULSE" and e["result"] == "success":
            last_pulse_damage = row.get("observed_hp_damage")
            require(last_pulse_damage is None or isinstance(last_pulse_damage, int)
                    and last_pulse_damage >= 0, "Invalid visible HP delta")
        expired = safeguard == 1
        safeguard = max(0, safeguard - 1)
        require(row.get("safeguard_expired") is expired,
                "Safeguard expiry line disagrees with completed-turn count")
    require(foe_hp_bound > 0, "A conservative winning hit is already recorded; verify victory")
    return dict(attack=attack, speed=speed, spdef=spdef, enemy_spa=enemy_spa,
                safeguard=safeguard, foe_hp_bound=foe_hp_bound, stock=stock,
                last_pulse_damage=last_pulse_damage)


def propose(state):
    """Return review or one proposal. Caller must observe again before any next action."""
    try:
        d = ledger(state)
        o = state["observation"]
        normal, critical = pulse_ranges(d["enemy_spa"], d["spdef"])
        cr = crunch_range(d["attack"])
        report = dict(turn=o["turn"], derived=d, dark_pulse_normal=normal,
                      dark_pulse_critical=critical, crunch=cr,
                      critical_can_ohko_full_hp=critical[1] >= 294,
                      warning="Positive Sp. Def does not protect from critical hits.")

        def choose(action, reason):
            if action in ITEMS:
                require(d["stock"][action] > 0, f"No verified stock for {action}")
                argv = ["python3", "scripts/battle_item.py", ITEMS[action], "Arcanine"]
                if action in {"XSPEED", "XATTACK", "XSPDEF"}:
                    argv.append("--active")
            else:
                require(isinstance(o["pp"].get(action), int) and o["pp"][action] > 0,
                        f"Fresh visible PP confirmation required for {action}")
                argv = ["python3", "scripts/battle_named_move.py", "Arcanine", action]
            return dict(status="proposal", action=action, reason=reason,
                        ordinary_helper_argv=argv, **report)

        # Priority items occur before Hypno's attack; Dream Eater fails after cure.
        if o["status"] == "SLEEP":
            if o["hp"] <= normal[1] and d["stock"]["FULLRESTORE"]:
                return choose("FULLRESTORE", "Cure sleep and restore HP before any enemy action")
            require(o["hp"] > normal[1],
                    "Sleep plus potentially lethal Dark Pulse: separate HP/status item dilemma")
            return choose("FULLHEAL", "Cure sleep first; confirm enemy action and new HP afterward")

        faster = boosted(176, d["speed"]) > 196
        if faster and cr[0] >= d["foe_hp_bound"]:
            return choose("CRUNCH", "Conservative faster finishing hit; no exposed enemy turn")

        # Respect the current critical margin. +2 enemy SpA cannot be fixed by HP/SpDef.
        accept = state.get("accept_critical_risk") is True
        if o["hp"] <= critical[1] and not accept:
            if critical[1] < 294 and min(294, o["hp"] + 200) > critical[1]:
                return choose("ULTRAPOTION", "Restore HP above the current critical maximum")
            raise ValueError("Critical maximum reaches current/full HP; explicit tactical review required")
        if o["hp"] <= normal[1]:
            require(min(294, o["hp"] + 200) > normal[1],
                    "Ultra Potion cannot reach ordinary survival margin")
            return choose("ULTRAPOTION", "Heal before the currently lethal ordinary Dark Pulse")

        if not faster:
            return choose("XSPEED", "One +2 Speed item makes Arcanine352 faster than Hypno196")
        if d["safeguard"] == 0:
            return choose("SAFEGUARD", "Awake faster cast after expiry, before Hypnosis can act")
        # One defensive item only when actual ordinary damage/boost warrants it.
        if d["spdef"] == 0 and (normal[1] >= 160 or
                d["last_pulse_damage"] is not None and d["last_pulse_damage"] >= 100):
            return choose("XSPDEF", "One defensive boost responds to observed/boosted ordinary damage")
        if d["attack"] < 4:
            return choose("XATTACK", "Reach +4 Attack with two items; two ordinary Crunch hits suffice")
        return choose("CRUNCH", "Attack promptly rather than adding unnecessary setup turns")
    except (KeyError, TypeError, ValueError) as exc:
        return dict(status="review", reason=str(exc), ordinary_helper_argv=None)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger_json", type=Path)
    args = parser.parse_args()
    value = propose(json.loads(args.ledger_json.read_text()))
    print(json.dumps(value, indent=2))
    return 0 if value["status"] == "proposal" else 2


if __name__ == "__main__":
    raise SystemExit(main())
