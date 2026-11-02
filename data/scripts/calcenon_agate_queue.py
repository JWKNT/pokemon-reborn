"""Source-bound Calcenon briefing/PC/Route4 queue; dry-run by default.

Development and default invocation read installed event assets only. UI helpers,
current planning notes and rendered screens are accessed only under --execute.
No battle is intentionally started, no save/checkpoint is inserted, and no game
state is edited. Stop715[65,17]; the new715E64 Scale route is a separate action.
"""
from __future__ import annotations

import argparse
import difflib
import functools
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
STATE = ROOT / "notes/navigation-state.json"
PHASES = ["briefing", "carrier", "approach"]
CLIMBS = [(412, 1, (710, 23, 49)), (710, 2, (711, 20, 58)),
          (711, 3, (713, 17, 24)), (713, 5, (714, 17, 10)),
          (714, 3, (715, 65, 17))]
PAGES = [(413, 46, 0), (413, 93, 0), (413, 67, 0), (417, 29, 0),
         (417, 30, 1), (417, 6, 0), (413, 68, 0), (415, 4, 0),
         (415, 7, 0), (415, 8, 0), (413, 21, 0), (418, 2, 0)]
PAGES += [(mid, eid, 0) for mid, eid, _ in CLIMBS]
BATTLE_WORDS = ["pbTrainerBattle", "pbDoubleTrainerBattle", "pbWildBattle"]


def need(ok, message):
    if not ok:
        raise ValueError(message)


@functools.lru_cache(maxsize=None)
def event(mid, eid):
    return json.loads(subprocess.check_output(
        ["ruby", str(ROOT / "scripts/event_dump.rb"), str(mid), str(eid)],
        stderr=subprocess.DEVNULL))


def source_proof():
    """Pure installed-source validation. No native/save/planner inspection."""
    proof = []
    for mid, eid, pi in PAGES:
        e = event(mid, eid)
        page = e["pages"][pi]
        cs = page["list"]
        need(not any(c["code"] in [102, 103, 104, 301] or
                     any(k in str(c["parameters"]) for k in BATTLE_WORDS)
                     for c in cs), f"Unapproved choice/battle in{mid}E{eid}p{pi}")
        proof.append({"map": mid, "event": eid, "page": pi,
                      "sha256": hashlib.sha256(json.dumps(page, sort_keys=True).encode()).hexdigest()})
    for mid, eid, destination in CLIMBS:
        cs = event(mid, eid)["pages"][0]["list"]
        need([c["parameters"][1:4] for c in cs if c["code"] == 201] == [list(destination)],
             f"Installed climb destination differs:{mid}E{eid}")
        need(any(c["code"] == 111 and c["parameters"] == [12, "Kernel.pbRockClimb"] for c in cs),
             "Expected ordinary RockClimb source")
    for mid, eid, pi, stage in [(413, 93, 0, 50), (417, 29, 0, 51), (417, 30, 1, 51)]:
        need(any(c["code"] == 122 and c["parameters"] == [391, 391, 0, 0, stage]
                 for c in event(mid, eid)["pages"][pi]["list"]), "Missing exact story setter")
    need(event(417, 29)["pages"][0]["trigger"] == 3 and
         event(417, 30)["pages"][1]["trigger"] == 3, "House briefing must remain an autorun")
    need(event(415, 4)["pages"][0]["list"][0]["parameters"] == [1],
         "Nurse must call installed healing common event1")
    return proof


def selected_page(e, nav, mid):
    """Pure RGSS page-condition selection from an explicit snapshot."""
    sw, va, ss = [nav.get(k, {}) for k in ["switches", "variables", "self_switches"]]
    for i in range(len(e["pages"]) - 1, -1, -1):
        c = e["pages"][i]["condition"]
        if ((not c["switch1_valid"] or sw.get(str(c["switch1_id"])) is True) and
            (not c["switch2_valid"] or sw.get(str(c["switch2_id"])) is True) and
            (not c["variable_valid"] or va.get(str(c["variable_id"]), 0) >= c["variable_value"]) and
            (not c["self_switch_valid"] or ss.get(f"{mid},{e['id']},{c['self_switch_ch']}") is True)):
            return i
    return None


def frozen_party(path, phase):
    path = path.resolve()
    need(path.is_relative_to(ROOT), "Use explicit frozen workspace party evidence")
    s = json.loads(path.read_text())
    party = s.get("party", [])
    need(len(party) == 6 and party[0]["level"] == 90, "Six members and level90 lead required")
    need(party[1]["species"] == ("TRANQUILL" if phase in ["approach", "fly-circus"] else "KLINKLANG"),
         "Frozen party index1 differs; refresh evidence after any PC/party change")
    swamps = [p for p in party if p["species"] == "SWAMPERT"]
    need(len(swamps) == 1 and {"ROCKCLIMB", "SURF"} <= {m["move"] for m in swamps[0]["moves"]},
         "Owned Swampert must already know RockClimb and Surf")
    if phase in ["all", "approach"]:
        need(s.get("bag", {}).get("contents", {}).get("SUPERREPEL", 0) >= 3,
             "Require at least3 owned SuperRepels for the ordinary approach")
    if phase in ["approach", "fly-circus"]:
        need("FLY" in {m["move"] for m in party[1]["moves"]}, "Frozen Tranquill must know Fly")
        need(party[0]["hp"] == party[0]["totalhp"] and party[0]["status"] is None,
             "Heal level90 lead before standalone route")
    return s, hashlib.sha256(path.read_bytes()).hexdigest()


class Runner:
    def __init__(self, args, party, binding):
        self.args, self.party = args, party
        self.path = args.journal.resolve()
        need(self.path.is_relative_to(ROOT), "Journal must be in the workspace")
        need(not self.path.exists(), "Existing journal: inspect partial inputs; use a NEW journal only after actual-state review")
        self.journal = {"frozen_party_sha256": binding, "source_proof": source_proof(),
                        "phase": args.phase, "events": [], "pending": None}
        self.write()

    def write(self):
        self.path.write_text(json.dumps(self.journal, indent=2) + "\n")

    def record(self, kind, **data):
        self.journal["events"].append({"epoch": time.time(), "kind": kind, **data})
        self.write()

    def run(self, script, *args):
        self.journal["pending"] = {"script": script, "args": list(args), "epoch": time.time()}
        self.write()
        subprocess.run([sys.executable, str(ROOT / "scripts" / (script + ".py")),
                        *map(str, args)], check=True)
        self.record("ordinary-helper-returned", script=script, args=list(args))
        self.journal["pending"] = None
        self.write()

    def nav(self):
        return json.loads(STATE.read_text())

    def stage(self, expected):
        need(self.nav().get("variables", {}).get("391") == expected,
             f"Observed completed planning stage must be391={expected}")

    def world(self):
        from play import snap, STATE as IMAGE
        from PIL import Image
        rows = snap()
        text = "\n".join(r["text"] for r in rows).lower()
        compact = re.sub("[^a-z]", "", text)
        if "repel" in compact and ("woreoff" in compact or "uoreoff" in compact):
            self.run("renew_repel")
            return self.world()
        need(not re.search(r"\bhp\b|\bfight\b|\bwild\b|\bpp:|\bvs\b", text),
             "Battle/party screen interrupted queue; no further action")
        need(not {r["text"].strip().lower() for r in rows} & {"yes", "no", "ves", "tes", "mo", "ro"},
             "Choice interrupted queue; no further action")
        im = Image.open(IMAGE).convert("RGB"); w, h = im.size
        box = im.crop((int(w*.08), int(h*.75), int(w*.90), int(h*.87)))
        white = sum(min(p)>235 and max(p)-min(p)<5 for p in box.getdata())/(box.width*box.height)
        def border(y):
            px = [im.getpixel((x, int(h*y))) for x in range(int(w*.08), int(w*.90))]
            return sum(max(p)<95 for p in px)/len(px)
        need(not (white>.35 and max(border(y) for y in [.721,.725,.729,.733])>.8 and
                  max(border(y) for y in [.895,.900,.905,.910])>.8), "Unresolved dialogue; no further action")
        need(not ("bag" in text and any(n in text for n in ["options","uptions","controls"])), "Main menu remained open")
        need(not re.search(r"[,.;]\s*map\s*[0-9oq]+", text), "Coordinate popup remained open")
        return rows

    def position(self, expected_map, exact=None):
        from locate import locate
        self.world()
        actual = locate(expected_map)
        need(actual[0] == expected_map and (exact is None or actual == tuple(exact)),
             f"Observed arrival{actual} differs from expected{exact or expected_map}")
        self.world()
        self.record("position-verified", position=list(actual))
        return actual

    def active_source(self, mid, eid, pi):
        need(selected_page(event(mid, eid), self.nav(), mid) == pi,
             f"{mid}E{eid} does not have approved page{pi}; no event interaction")

    def no_auto_battle(self, mid):
        # Reject a still-active auto-trigger trainer anywhere on this small map.
        # Conservative by design: do not accidentally turn prep into a new fight.
        value = json.loads(subprocess.check_output(
            ["ruby", str(ROOT / "scripts/route_map.rb"), str(mid), "0", "0"],
            stderr=subprocess.DEVNULL))
        hits = [eid for eid, e in value["events"].items() if e["trigger"] in [1, 2, 3] and
                any(k in str(e.get("list", [])) for k in BATTLE_WORDS)]
        if not hits:
            return
        need(getattr(self.args, "allow_source_avoided_trainers", False) and
             mid in {m for m, _, _ in CLIMBS},
             f"Active automatic trainer/boss events on{mid}:{hits}; inspect a safe route separately")
        # These reviewed Route4 trainers stand still. Exclude their complete
        # source sightlines as HARD planner obstacles, rather than treating a
        # trainer anywhere on this large map as an unavoidable encounter.
        hazards = set()
        for eid in hits:
            e = value["events"][eid]
            match = re.fullmatch(r"Trainer\((\d+)\)", e["name"])
            need(e["trigger"] == 2 and e["move_type"] == 0 and match and
                 e["direction"] in [2, 4, 6, 8],
                 f"Unreviewed automatic battle geometry on{mid}E{eid}; stop")
            dx, dy = {2:(0,1), 4:(-1,0), 6:(1,0), 8:(0,-1)}[e["direction"]]
            hazards.update((e["x"] + n*dx, e["y"] + n*dy)
                           for n in range(int(match[1]) + 1))
        state = self.nav()
        old = set(map(tuple, state.get("avoid", {}).get(str(mid), [])))
        state.setdefault("avoid", {})[str(mid)] = [list(p) for p in sorted(old | hazards)]
        STATE.write_text(json.dumps(state) + "\n")
        self.record("stationary-source-trainers-hard-excluded", map=mid,
                    events=hits, tiles=[list(p) for p in sorted(hazards)])
        # eventq's fresh path search reads these exclusions before any walking
        # input and refuses if no accessible climb face remains.

    def mirror(self, mid, eid, pi):
        from post_hypno_exit import mirror_page
        mirror_page(mid, eid, event(mid, eid)["pages"][pi])
        self.record("completed-source-effects-mirrored-to-planner", map=mid, event=eid, page=pi)

    def transfer(self, mid, eid, destination):
        self.position(mid)
        self.no_auto_battle(mid)
        self.active_source(mid, eid, 0)
        self.run("eventq", mid, eid, "enter")
        self.position(destination[0], destination)
        self.mirror(mid, eid, 0)

    def linear(self, mid, eid, pi, *, started=False):
        if not started:
            from play import act, read
            self.position(mid)
            self.active_source(mid, eid, pi)
            self.run("eventq", mid, eid, "talk")
            blocks = [str(c["parameters"][0]) for c in event(mid, eid)["pages"][pi]["list"]
                      if c["code"] == 101]
            norm = lambda s: re.sub("[^a-z]", "", s.lower().replace("pokemon reborn", ""))
            for _ in range(5):
                visible = read()
                need(not re.search(r"\bhp\b|\bfight\b|\bpp:", visible.lower()), "Battle interrupted story interaction")
                if any(difflib.SequenceMatcher(None, norm(visible), norm(b)).ratio() >= .50
                       for b in blocks):
                    break
                act("wait:.6")
            else:
                raise ValueError(f"No installed dialogue observed for{mid}E{eid}p{pi}; no source effects credited")
        self.run("linear_dialog", mid, eid, "--source-page", pi, "--burst", "--world-settle", 12)
        self.position(mid)
        self.mirror(mid, eid, pi)

    def briefing(self):
        from play import act, read
        stage = self.nav().get("variables", {}).get("391")
        need(stage in [49, 50, 51], "Briefing accepts only post-recovery39149..51")
        actual = self.position(413)
        if stage == 49:
            if not self.args.skip_shelly and not self.nav().get("switches", {}).get("1023"):
                self.linear(413, 46, 0)
            self.linear(413, 93, 0)
            # This is the one inspected conditional source effect on Eve's
            # first page; her next page is a PULSE choice and is NOT replayed.
            state = self.nav()
            if not state.get("switches", {}).get("573"):
                state.setdefault("switches", {})["990"] = True
                STATE.write_text(json.dumps(state) + "\n")
            self.stage(50)
        if self.nav().get("variables", {}).get("391") == 50:
            self.active_source(413, 67, 0)
            eid, pi = (30, 1) if self.nav().get("switches", {}).get("878") else (29, 0)
            # The house entrance starts this autorun. Do not open coordinate
            # UI or send any movement between the transfer and its dialogue.
            self.run("eventq", 413, 67, "enter")
            # A returned movement helper is not itself transfer proof. Observe
            # an installed house line before reflecting its entrance effects.
            blocks = [str(c["parameters"][0]) for c in event(417, eid)["pages"][pi]["list"]
                      if c["code"] == 101]
            norm = lambda s: re.sub("[^a-z]", "", s.lower().replace("pokemon reborn", ""))
            for _ in range(6):
                visible = read()
                need(not re.search(r"\bhp\b|\bfight\b|\bpp:", visible.lower()), "Unexpected battle during house transfer")
                if any(difflib.SequenceMatcher(None, norm(visible), norm(b)).ratio() >= .50
                       for b in blocks):
                    break
                act("wait:1")
            else:
                raise ValueError("House autorun line not observed; no dialogue tap or source mirror sent")
            self.mirror(413, 67, 0)
            self.active_source(417, eid, pi)
            self.linear(417, eid, pi, started=True)
            self.stage(51)
            self.transfer(417, 6, (413, 28, 32))
        self.stage(51)
        self.record("phase-completed", phase="briefing")

    def carrier(self):
        from play import act, read, snap
        self.stage(51)
        actual = self.position(self.nav_start_map())
        if actual[0] == 413:
            self.transfer(413, 68, (415, 10, 10))
        self.active_source(415, 4, 0)
        self.run("eventq", 415, 4, "talk")
        welcome = read().lower()
        need("welcome" in welcome or "rest" in welcome, "Expected nurse welcome")
        self.run("choose_dialog", "Yes|No", "Yes")
        self.run("heal")
        self.position(415)
        self.run("eventq", 415, 7, "talk")
        self.run("pc_open_reviewed")
        need(re.search(r"\bbox\s*1\b", read().lower()), "Fresh Box1 required; no cursor move sent")
        # Storage.rb pbStartBox resets selection0; this was just opened, never
        # resumed from an old box cursor. The existing helper verifies both names.
        self.run("pc_exchange_named", 12, 1, "Tranquill", "Klinklang")
        self.position(415)
        self.run("party_open")
        rows = snap()
        expected = [p["name"] for p in self.party]
        expected[1] = "Tranquill"
        for slot, name in enumerate(expected):
            matches = []
            for r in rows:
                word = re.sub("[^a-z]", "", r["text"].lower())
                score = difflib.SequenceMatcher(None, name.lower(), word).ratio()
                if score >= .78 and .1 < r["y"] < .7:
                    col = int(r["x"] > .5)
                    row = round((r["y"] - (.15 if not col else .195))/.21)
                    if row in [0, 1, 2]:
                        matches.append(row*2+col)
            need(matches == [slot], f"Party card{name} is not uniquely in expected slot{slot}")
        self.run("party_pick", "Tranquill", "--single")
        text = read().lower()
        need("summary" in text and "switch" in text and
             any(s.strip().lower() in ["fly", "flu", "fiy", "flh"] for s in text.splitlines()),
             "Owned Tranquill Fly option not visible; stop before route")
        act("x", "wait:.5", "x", "wait:.6")
        # Party cancellation returns to PauseMenu unless a hidden move was
        # actually used (PauseMenu.rb199..212). Close that known menu once.
        labels = {s.strip().lower() for s in read().splitlines()}
        need({"bag", "options"} <= labels, "Expected main menu after inspecting Fly; no extra X sent")
        act("x", "wait:.6")
        self.run("overworld")
        self.transfer(415, 8, (413, 45, 28))
        self.record("phase-completed", phase="carrier", swap={"box": 1, "slot": 12, "party_index": 1},
                    fly_verified=True, nurse_yes=True)

    def nav_start_map(self):
        from locate import locate
        self.world()
        mid = locate()[0]
        need(mid in [413, 415], "Carrier phase must start in Calcenon or its center")
        return mid

    def approach(self):
        self.stage(51)
        if self.args.climb_index is None:
            self.transfer(413, 21, (418, 17, 7))
            self.transfer(418, 2, (412, 12, 18))
            self.run("use_field_item", "Super Repel")
            self.position(412)
            first = 0
        else:
            first = self.args.climb_index
            self.position(CLIMBS[first][0])
        for mid, eid, destination in CLIMBS[first:]:
            self.position(mid)
            self.no_auto_battle(mid)
            self.active_source(mid, eid, 0)
            if mid == 713:
                state = self.nav()
                need(isinstance(state.get("switches", {}).get("410"), bool), "Observed410 layer proof required")
                self.run("layer_walk", 713, 48, 36, int(state["switches"]["410"]))
                self.position(713, (713, 48, 36))
            self.run("eventq", mid, eid, "talk")
            self.run("dialog", "--limit=10")
            self.position(destination[0], destination)
            self.record("ordinary-climb-verified", map=mid, event=eid, destination=list(destination))
        self.record("phase-completed", phase="approach", stop=[715, 65, 17],
                    scale_collected=False, collected710_scale_not_replayed=True)
        print("SAFE715[65,17]. Continue the reviewed715E64 dry-layer/Surf pickup separately; no Fly sent.", flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--execute", action="store_true")
    p.add_argument("--phase", choices=["all", *PHASES, "fly-circus"], default="all")
    p.add_argument("--stop-phase", choices=PHASES, default="approach")
    p.add_argument("--skip-shelly", action="store_true")
    p.add_argument("--allow-source-avoided-trainers", action="store_true")
    p.add_argument("--climb-index", type=int, choices=range(5))
    p.add_argument("--party-status", type=pathlib.Path)
    p.add_argument("--journal", type=pathlib.Path, default=ROOT / "work/calcenon-agate-queue-progress.json")
    args = p.parse_args()
    need(args.climb_index is None or args.phase == "approach", "Climb resume is only a standalone approach phase")
    print(json.dumps({"proposal": True, "source_proof": source_proof(),
                      "phases": PHASES, "optional_shelly": True, "stop": [715, 65, 17],
                      "new_scale": [715, 64], "replay710_scale": False,
                      "climbs": CLIMBS, "no_automatic_save": True}, indent=2), flush=True)
    if not args.execute:
        return
    need(args.party_status is not None, "--execute requires explicit frozen --party-status")
    status, binding = frozen_party(args.party_status, args.phase)
    runner = Runner(args, status["party"], binding)
    try:
        if args.phase == "fly-circus":
            # Root owns the Scale pickup. This separate phase requires an
            # actual refreshed party+bag checkpoint after that normal pickup.
            need(status.get("bag", {}).get("contents", {}).get("HEARTSCALE", 0) >= 1,
                 "Frozen new HeartScale required before the optional Circus leg")
            need(status.get("map") == 715, "Fly phase expects actual715 outdoors")
            need(status.get("position") == [57, 21], "Fly phase requires the reviewed dry715[57,21] Scale endpoint")
            runner.stage(51)
            runner.position(715, (715, *status["position"]))
            runner.run("fly_to", 355, "--carrier", "Tranquill")
            runner.position(355)
            runner.record("phase-completed", phase="fly-circus")
        else:
            phases = PHASES if args.phase == "all" else [args.phase]
            for phase in phases:
                getattr(runner, phase)()
                if phase == args.stop_phase:
                    break
        runner.journal["status"] = "completed-approved-stop"
        runner.write()
    except BaseException as error:
        runner.journal["status"] = "stopped-for-actual-state-review"
        runner.record("stop", error=type(error).__name__, reason=str(error))
        raise


if __name__ == "__main__":
    main()
