"""Proposed, bounded NORMAL Agate preparation phases; dry-run by default.

Development/tests use explicit frozen JSON only. --execute imports the ordinary
UI helpers after preflight and requires a fresh overworld of the expected map.
No battle AI/RNG/log reads or game/save editing. Stops before any Agate battle.
New Heart Scale target is715E64, never the collected710E64.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASES = {"shops": 355, "build": 355, "training-pilot": 519,
          "training-finish": 519, "finish-lens": 355, "scale": 715}
BASE_EV = [252, 4, 252, 0, 0, 2]
PRE_EV = [172, 4, 252, 0, 0, 2]
FINAL_EV = [172, 4, 252, 80, 0, 2]
FINAL_MOVES = ["TRICKROOM", "HEX", "WILLOWISP", "DARKPULSE"]
TARGETS = "Rattata,Bidoof,Patrat,Zigzagoon,Meowth,Spinarak"


def need(ok, text):
    if not ok:
        raise ValueError(text)


def command(script, *args):
    return dict(script=script, args=list(args))


def effective_nature(m):
    return m.get("natureflag") or m["nature"]


def mon(status):
    matches = [m for m in status["party"] if m["species"] == "COFAGRIGUS"]
    need(len(matches) == 1 and matches[0]["name"] == "Cofagrigus"
         and matches[0]["level"] == 90, "Unique Cofagrigus90 required")
    return matches[0]


def plan(phase, status):
    need(status["map"] == PHASES[phase], "Frozen outside-battle map differs from phase")
    bag = status["bag"]["contents"]
    cmds = []
    if phase == "shops":
        berries = max(0, 4 - bag.get("POMEGBERRY", 0))
        lens = int(not bag.get("POWERLENS", 0)
                   and not any(m.get("item") == "POWERLENS" for m in status["party"]))
        need(not lens or not status.get("switches", {}).get("715"),
             "Need Lens, but Circus power vendor disappears after switch715")
        money = status["trainer"]["money"]
        need(money >= berries * 500 + lens * 15000, "Insufficient verified shopping money")
        for eid, item, count, price in [(136, "Pomeg Berry", berries, 500),
                                        (83, "Power Lens", lens, 15000)]:
            if count:
                cmds.extend([command("eventq", 355, eid, "talk"), command("mart_open"),
                             command("shop_buy", item, count, price), command("mart_exit")])
        return cmds
    if phase == "scale":
        need(bag.get("HEARTSCALE", 0) == 0, "Already have a scale; skip pickup")
        return [command("eventq", 715, 64, "item"), command("overworld")]
    cf = mon(status)
    moves = [m["move"] for m in cf["moves"]]
    if phase == "build":
        need(cf["ev"] == BASE_EV and effective_nature(cf) == "CALM", "Build phase is not resumable mid-berries/mint; review partial state")
        need(moves == ["TRICKROOM", "SHADOWBALL", "WILLOWISP", "DESTINYBOND"],
             "Reviewed Cofa replacement slots differ")
        need(cf.get("item") in (None, "SPELLTAG"), "Unexpected held item")
        for item, qty in [("TIMIDMINT", 1), ("POMEGBERRY", 4), ("TM97", 1),
                          ("HEARTSCALE", 1), ("POWERLENS", 1)]:
            need(bag.get(item, 0) >= qty, "Missing owned " + item)
        if cf.get("item"):
            cmds.append(command("party_take_named", "Cofagrigus"))
        cmds.extend([command("party_front", "Cofagrigus"),
                     dict(internal="timid-mint"),
                     command("berry_batch", "Pomeg Berry", "Cofagrigus", 4),
                     command("teach_machine", "TM97", "Cofagrigus", "Dark Pulse", 3),
                     dict(internal="hex-reminder", index=6),
                     command("give_held", "Power Lens", "Cofagrigus"),
                     command("eventq", 355, 118, "talk"), command("heal"),
                     command("checkpoint", "Agate-Cofa-training-ready")])
    elif phase in {"training-pilot", "training-finish"}:
        expected = list(PRE_EV)
        expected[3] = 0 if phase == "training-pilot" else 32
        need(cf["ev"] == expected and effective_nature(cf) == "TIMID"
             and cf.get("item") == "POWERLENS" and moves == FINAL_MOVES,
             "Training start must match exact EV/build/Lens checkpoint")
        need(cf["hp"] == cf["totalhp"] if phase == "training-pilot" else cf["hp"] > 150,
             "Heal before this training phase")
        need(cf["status"] is None and cf["moves"][3]["pp"] >= 3,
             "Status/PP training readiness failed")
        cmds.append(command("party_front", "Cofagrigus"))
        if phase == "training-pilot":
            cmds.append(command("q", "519,25,47"))
        count = 1 if phase == "training-pilot" else 2
        label = "Agate-Cofa-Lens-pilot" if count == 1 else "Agate-Cofa-EVs-complete"
        cmds.extend([command("train_wild_bulk", "Cofagrigus", 3, count,
                             "--targets", TARGETS, "--flex-targets", "--ev-ledger",
                             "--expire-repel", "--vertical", "--heal-item", "Ultra Potion"),
                     command("checkpoint", label)])
    elif phase == "finish-lens":
        need(cf["ev"] == FINAL_EV and effective_nature(cf) == "TIMID" and moves == FINAL_MOVES,
             "Finish only after exact80 SpA EV reconciliation")
        need(cf.get("item") == "POWERLENS", "Expected Lens for normal removal")
        cmds.extend([command("party_take_named", "Cofagrigus"),
                     command("eventq", 355, 118, "talk"), command("heal"),
                     command("checkpoint", "Agate-Cofa-prepared")])
    return cmds


def execute(phase, status, cmds):
    # These imports expose ordinary controls only when explicitly executing.
    from play import act, read
    from locate import locate
    text = read().lower()
    need(not re.search(r"\bfight\b|\bwild\b|\bpp:|\bhp\b", text)
         and "yes" not in text.splitlines() and "no" not in text.splitlines(),
         "Fresh overworld required")
    need(locate()[0] == PHASES[phase], "Observed map differs; no phase input sent")

    def run(script, *args):
        subprocess.run([sys.executable, str(ROOT / "scripts" / (script + ".py")),
                        *map(str, args)], check=True)

    def reminder(index):
        run("eventq", 355, 35, "talk")
        run("choose_dialog", "Teach one-by-one.|Remember all.|No", "Teach one-by-one.",
            "--source", 355, 35)
        for _ in range(5):
            t = read().lower()
            if "choose a pok" in t or "cancel" in t and t.count("hp") >= 5:
                break
            need("which pok" in t or "klhich pok" in t, "Reminder party entry requires review")
            act("c", "wait:.5")
        else:
            raise ValueError("Reminder party entry timeout")
        run("party_pick", "Cofagrigus", "--single")
        for _ in range(5):
            t = read().lower()
            if "teach which" in t:
                break
            need("what'll it be" in t or "whatll it be" in t, "Reminder list requires review")
            act("c", "wait:.5")
        else:
            raise ValueError("Reminder list timeout")
        # Installed level-up list, deduplicated and excluding known moves: Hex index6. Check both screens.
        act(*(["down"] * index), "wait:.5")
        need("hex" in read().lower(), "Hex absent from the reviewed reminder list")
        act("c", "wait:.5")
        need("teachhex" in re.sub("[^a-z]", "", read().lower()), "Selected move is not Hex")
        run("choose_dialog", "Yes|No", "Yes")
        from learning import PLANS, resolve
        PLANS["hex"] = 1
        need(resolve(read()), "Hex learning prompt requires review")
        run("relearn_finish")
        run("overworld")

    for c in cmds:
        if c.get("internal") == "timid-mint":
            run("field_medicine", "Timid Mint", "Cofagrigus")
            need("becomes timid" in read().lower(), "Timid Mint effect requires public review")
            act("c", "wait:.6")
            run("overworld")
        elif c.get("internal") == "hex-reminder":
            reminder(c["index"])
        else:
            run(c["script"], *c["args"])
    if phase not in {"shops", "scale"}:
        label = {"build": "Agate-Cofa-training-ready", "training-pilot": "Agate-Cofa-Lens-pilot",
                 "training-finish": "Agate-Cofa-EVs-complete", "finish-lens": "Agate-Cofa-prepared"}[phase]
        after = json.loads((ROOT / "notes" / (label + "-status.json")).read_text())
        cf = mon(after)
        expected = list(PRE_EV)
        expected[3] = {"build": 0, "training-pilot": 32, "training-finish": 80,
                       "finish-lens": 80}[phase]
        need(cf["ev"] == expected and effective_nature(cf) == "TIMID"
             and [m["move"] for m in cf["moves"]] == FINAL_MOVES,
             "Native EV/nature/move reconciliation failed; do not credit proposed training")
        need(cf.get("item") == (None if phase == "finish-lens" else "POWERLENS"),
             "Native held-item reconciliation failed")
        if phase in {"training-finish", "finish-lens"}:
            need([cf[k] for k in ["totalhp", "attack", "defense", "spatk", "spdef", "speed"]]
                 == [252, 93, 333, 210, 218, 68], "Native final stats differ from battle proof")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("phase", choices=PHASES)
    p.add_argument("--status", required=True, type=Path,
                   help="Explicit fresh outside-battle checkpoint JSON; never an active battle")
    p.add_argument("--execute", action="store_true")
    a = p.parse_args()
    status = json.loads(a.status.read_text())
    cmds = plan(a.phase, status)
    print(json.dumps(dict(proposal=True, phase=a.phase, expected_map=PHASES[a.phase],
                          commands=cmds), indent=2), flush=True)
    if a.execute:
        execute(a.phase, status, cmds)


if __name__ == "__main__":
    main()
